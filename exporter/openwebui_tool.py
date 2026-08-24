#!/usr/bin/env python3
"""
title: AI Meal Planner Exporter
author: OpenAI / project contributor
version: 0.1.0
description: Deterministically converts structured AI meal-plan ingredient data into a consolidated Markdown shopping list.

This Open WebUI Tool is intentionally narrow:
- accepts structured recipe records
- excludes pantry items
- excludes optional ingredients by default
- consolidates compatible quantities deterministically
- returns a Markdown shopping list
- does not guess package sizes
- does not access arbitrary files
- does not execute shell commands
"""


from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable


PANTRY_DEFAULTS = {
    "salt",
    "black pepper",
    "pepper",
    "olive oil",
    "vegetable oil",
    "canola oil",
    "avocado oil",
    "cooking oil",
    "water",
    "garlic powder",
    "onion powder",
    "dried oregano",
    "dried basil",
    "dried thyme",
    "dried rosemary",
    "ground cumin",
    "cumin",
    "smoked paprika",
    "paprika",
    "chili powder",
    "cayenne",
    "cayenne pepper",
    "red pepper flakes",
}

SECTION_ORDER = [
    "Produce",
    "Meat and Seafood",
    "Dairy and Eggs",
    "Bread and Grains",
    "Canned and Jarred Goods",
    "Frozen Foods",
    "Spices and Condiments",
    "Other",
]

# Explicit, conservative category mapping.
PRODUCE_WORDS = {
    "apple","apricot","arugula","asparagus","avocado","basil","bean sprouts",
    "bell pepper","blackberry","blueberry","broccoli","cabbage","carrot","cauliflower",
    "celery","cherry tomatoes","cilantro","corn","cucumber","dill","eggplant",
    "garlic","ginger","grape","green beans","green onions","jalapeño","jalapeno",
    "lemon","lettuce","lime","mushroom","onion","orange","parsley","peach","pear",
    "pepper","potato","red onion","scallion","spinach","squash","sweet potato",
    "thyme","tomato","tomatoes","zucchini",
}
MEAT_WORDS = {
    "beef","chicken","chicken breast","chicken breasts","chicken thigh","chicken thighs",
    "flank steak","ground beef","ground chicken","ground turkey","pork","pork chop",
    "pork chops","pork tenderloin","salmon","shrimp","steak","turkey",
}
DAIRY_WORDS = {
    "butter","cheddar","cheese","egg","eggs","feta","greek yogurt","milk",
    "mozzarella","parmesan","parmesan cheese","sour cream","yogurt",
}
GRAIN_WORDS = {
    "bread","brown rice","corn tortilla","corn tortillas","couscous","flour tortilla",
    "flour tortillas","orzo","panko breadcrumbs","pasta","quinoa","rice","spaghetti",
    "tortilla","tortillas","whole-wheat spaghetti",
}
CANNED_WORDS = {
    "black beans","chickpeas","crushed tomatoes","enchilada sauce","marinara",
    "marinara sauce","tomato paste","white beans",
}
CONDIMENT_WORDS = {
    "balsamic vinegar","capers","cornstarch","dijon mustard","honey","hot sauce",
    "maple syrup","red wine vinegar","rice vinegar","sesame seeds","soy sauce","tamari",
    "za'atar","zaatar",
}


ALIASES = {
    # Ingredient identity aliases only. Do not merge different foods.
    "scallions": "green onions",
    "scallion": "green onions",
    "green onion": "green onions",
    "cherry tomato": "cherry tomatoes",
    "bell peppers": "bell pepper",
    "red bell peppers": "red bell pepper",
    "yellow bell peppers": "yellow bell pepper",
    "orange bell peppers": "orange bell pepper",
    "sweet potatoes": "sweet potato",
    "pork chops": "pork chop",
    "chicken breasts": "chicken breast",
    "chicken thighs": "chicken thigh",
}

UNIT_ALIASES = {
    "": "",
    "piece": "piece",
    "pieces": "piece",
    "clove": "clove",
    "cloves": "clove",
    "cup": "cup",
    "cups": "cup",
    "tbsp": "tbsp",
    "tablespoon": "tbsp",
    "tablespoons": "tbsp",
    "tsp": "tsp",
    "teaspoon": "tsp",
    "teaspoons": "tsp",
    "oz": "oz",
    "ounce": "oz",
    "ounces": "oz",
    "lb": "lb",
    "lbs": "lb",
    "pound": "lb",
    "pounds": "lb",
    "can": "can",
    "cans": "can",
    "bunch": "bunch",
    "bunches": "bunch",
    "fillet": "fillet",
    "fillets": "fillet",
    "stalk": "stalk",
    "stalks": "stalk",
    "ear": "ear",
    "ears": "ear",
    "loaf": "loaf",
    "jar": "jar",
    "head": "head",
    "pint": "pint",
    "quart": "quart",
}

# Conversion bases:
# volume -> tsp
# weight -> oz
VOLUME_TO_TSP = {
    "tsp": 1.0,
    "tbsp": 3.0,
    "cup": 48.0,
    "pint": 96.0,
    "quart": 192.0,
}
WEIGHT_TO_OZ = {"oz": 1.0, "lb": 16.0}


def norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def normalize_name(name: str) -> str:
    s = norm_space(name).lower()
    s = s.replace("’", "'")
    return ALIASES.get(s, s)


def normalize_unit(unit: Any) -> str:
    if unit is None:
        return ""
    s = norm_space(str(unit)).lower()
    return UNIT_ALIASES.get(s, s)


def format_number(value: float) -> str:
    if math.isclose(value, round(value), abs_tol=1e-9):
        return str(int(round(value)))
    # Common kitchen-friendly decimals
    common = {
        0.125: "1/8",
        0.25: "1/4",
        0.333333: "1/3",
        0.375: "3/8",
        0.5: "1/2",
        0.625: "5/8",
        0.666667: "2/3",
        0.75: "3/4",
        0.875: "7/8",
    }
    frac = value - math.floor(value)
    for k, label in common.items():
        if abs(frac - k) < 0.015:
            whole = math.floor(value)
            return f"{whole} {label}" if whole else label
    return f"{value:.2f}".rstrip("0").rstrip(".")


@dataclass
class Ingredient:
    name: str
    quantity: float | None
    unit: str
    size: str
    preparation: str
    optional: bool
    pantry: bool
    alternative: str | None
    source_day: str
    source_recipe: str

    @classmethod
    def from_obj(cls, obj: dict[str, Any], day: str, recipe: str) -> "Ingredient":
        q = obj.get("quantity")
        if q is not None:
            if isinstance(q, bool) or not isinstance(q, (int, float)):
                raise ValueError(
                    f"{day} / {recipe}: quantity for {obj.get('name')!r} must be numeric or null"
                )
            q = float(q)
        name = normalize_name(str(obj.get("name", "")))
        if not name:
            raise ValueError(f"{day} / {recipe}: ingredient name is empty")
        return cls(
            name=name,
            quantity=q,
            unit=normalize_unit(obj.get("unit", "")),
            size=norm_space(str(obj.get("size", ""))),
            preparation=norm_space(str(obj.get("preparation", ""))),
            optional=bool(obj.get("optional", False)),
            pantry=bool(obj.get("pantry", False)) or name in PANTRY_DEFAULTS,
            alternative=(
                norm_space(str(obj["alternative"]))
                if obj.get("alternative") not in (None, "")
                else None
            ),
            source_day=day,
            source_recipe=recipe,
        )


def normalize_recipe_input(data: Any) -> list[dict[str, Any]]:
    """
    Accept:
      1) one recipe object
      2) an array of recipe objects
      3) an object containing a "recipes" array
    """
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError as exc:
            raise ValueError(f"recipes must be valid JSON when passed as a string: {exc}") from exc

    if isinstance(data, dict) and "recipes" in data:
        data = data["recipes"]
    elif isinstance(data, dict) and {"day", "recipe", "ingredients"} <= set(data):
        data = [data]

    if not isinstance(data, list):
        raise ValueError(
            "Input must be a recipe object, recipe array, or {'recipes': [...]} object"
        )

    recipes: list[dict[str, Any]] = []
    for i, rec in enumerate(data, start=1):
        if not isinstance(rec, dict):
            raise ValueError(f"Recipe #{i} is not an object")
        for key in ("day", "recipe", "ingredients"):
            if key not in rec:
                raise ValueError(f"Recipe #{i} is missing required key {key!r}")
        if not isinstance(rec["ingredients"], list):
            raise ValueError(f"Recipe #{i}: 'ingredients' must be an array")
        recipes.append(rec)

    return recipes


def select_recipes(recipes: list[dict[str, Any]], selectors: list[str] | None) -> list[dict[str, Any]]:
    if not selectors:
        return recipes

    wanted = {s.strip().lower() for s in selectors if s.strip()}
    selected = []
    for rec in recipes:
        day = str(rec["day"]).strip().lower()
        name = str(rec["recipe"]).strip().lower()
        if day in wanted or name in wanted:
            selected.append(rec)

    missing = wanted - {
        str(rec["day"]).strip().lower() for rec in selected
    } - {
        str(rec["recipe"]).strip().lower() for rec in selected
    }
    if missing:
        raise ValueError("No recipe matched selector(s): " + ", ".join(sorted(missing)))
    return selected


def ingredient_category(name: str) -> str:
    n = normalize_name(name)

    def matches(words: set[str]) -> bool:
        return n in words or any(n.endswith(" " + w) or n.startswith(w + " ") for w in words)

    if matches(MEAT_WORDS):
        return "Meat and Seafood"
    if matches(DAIRY_WORDS):
        return "Dairy and Eggs"
    if matches(GRAIN_WORDS):
        return "Bread and Grains"
    if matches(CANNED_WORDS):
        return "Canned and Jarred Goods"
    if matches(PRODUCE_WORDS):
        return "Produce"
    if matches(CONDIMENT_WORDS):
        return "Spices and Condiments"
    return "Other"


def consolidate(ingredients: Iterable[Ingredient]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """
    Returns (quantified_items, unquantified_items).

    Quantities are only combined when compatible. We intentionally do not
    invent a quantity for null values.
    """
    groups: dict[str, list[Ingredient]] = defaultdict(list)
    for ing in ingredients:
        groups[ing.name].append(ing)

    quantified: list[dict[str, Any]] = []
    unquantified: list[dict[str, Any]] = []

    for name, items in sorted(groups.items()):
        with_q = [x for x in items if x.quantity is not None]
        without_q = [x for x in items if x.quantity is None]

        # Separate by unit family.
        vol = [x for x in with_q if x.unit in VOLUME_TO_TSP]
        weight = [x for x in with_q if x.unit in WEIGHT_TO_OZ]
        other: dict[str, list[Ingredient]] = defaultdict(list)
        for x in with_q:
            if x in vol or x in weight:
                continue
            other[x.unit].append(x)

        if vol:
            total_tsp = sum(x.quantity * VOLUME_TO_TSP[x.unit] for x in vol)

            input_units = {x.unit for x in vol}

            if "quart" in input_units:
                qty, unit = total_tsp / 192, "quart"
            elif "pint" in input_units:
                qty, unit = total_tsp / 96, "pint"
            elif "cup" in input_units:
                qty, unit = total_tsp / 48, "cup"
            elif "tbsp" in input_units:
                qty, unit = total_tsp / 3, "tbsp"
            else:
                qty, unit = total_tsp, "tsp"
            quantified.append(make_item(name, qty, unit, vol))

        if weight:
            total_oz = sum(x.quantity * WEIGHT_TO_OZ[x.unit] for x in weight)  # type: ignore[operator]
            input_units = {x.unit for x in weight}

            if "lb" in input_units:
                qty, unit = total_oz / 16, "lb"
            else:
                qty, unit = total_oz, "oz"

            quantified.append(make_item(name, qty, unit, weight))

        for unit, unit_items in other.items():
            qty = sum(x.quantity for x in unit_items if x.quantity is not None)
            quantified.append(make_item(name, qty, unit, unit_items))

        if without_q:
            unquantified.append(
                {
                    "name": name,
                    "category": ingredient_category(name),
                    "sources": sorted(
                        {f"{x.source_day}: {x.source_recipe}" for x in without_q}
                    ),
                    "optional": all(x.optional for x in without_q),
                    "alternatives": sorted(
                        {x.alternative for x in without_q if x.alternative}
                    ),
                }
            )

    return quantified, unquantified


def make_item(name: str, qty: float, unit: str, items: list[Ingredient]) -> dict[str, Any]:
    return {
        "name": name,
        "quantity": qty,
        "unit": unit,
        "category": ingredient_category(name),
        "sources": sorted({f"{x.source_day}: {x.source_recipe}" for x in items}),
        "optional": all(x.optional for x in items),
        "alternatives": sorted({x.alternative for x in items if x.alternative}),
    }


COUNT_NAME_PLURALS = {
    "avocado": "avocados",
    "chicken breast": "chicken breasts",
    "chicken thigh": "chicken thighs",
    "corn tortilla": "corn tortillas",
    "egg": "eggs",
    "eggplant": "eggplants",
    "flour tortilla": "flour tortillas",
    "green onion": "green onions",
    "green onions": "green onions",
    "lemon": "lemons",
    "lime": "limes",
    "orange bell pepper": "orange bell peppers",
    "pork chop": "pork chops",
    "red bell pepper": "red bell peppers",
    "red onion": "red onions",
    "salmon fillet": "salmon fillets",
    "yellow bell pepper": "yellow bell peppers",
    "yellow onion": "yellow onions",
    "zucchini": "zucchini",
}


def pluralize_count_name(name: str) -> str:
    if name in COUNT_NAME_PLURALS:
        return COUNT_NAME_PLURALS[name]

    if name.endswith(("s", "x", "z", "ch", "sh")):
        return name + "es"
    if len(name) > 1 and name.endswith("y") and name[-2] not in "aeiou":
        return name[:-1] + "ies"
    return name + "s"


def display_name(name: str) -> str:
    return name


def render_line(item: dict[str, Any]) -> str:
    quantity = float(item["quantity"])
    qty = format_number(quantity)
    unit = item["unit"]
    name = display_name(item["name"])

    if unit == "piece":
        display_item_name = name if quantity <= 1.0 else pluralize_count_name(name)
        text = f"{qty} {display_item_name}"
    elif unit:
        display_unit = unit

        if quantity > 1.0:
            plurals = {
                "clove": "cloves",
                "cup": "cups",
                "tbsp": "tbsp",
                "tsp": "tsp",
                "oz": "oz",
                "lb": "lb",
                "can": "cans",
                "bunch": "bunches",
                "fillet": "fillets",
                "stalk": "stalks",
                "ear": "ears",
                "loaf": "loaves",
                "jar": "jars",
                "head": "heads",
                "pint": "pints",
                "quart": "quarts",
            }
            display_unit = plurals.get(unit, unit)

        text = f"{qty} {display_unit} {name}"
    else:
        text = f"{qty} {name}"

    if item.get("alternatives"):
        text += " (alternative: " + " / ".join(item["alternatives"]) + ")"
    return text


def render_unquantified(item: dict[str, Any]) -> str:
    text = display_name(item["name"])
    if item.get("alternatives"):
        text += " (alternative: " + " / ".join(item["alternatives"]) + ")"
    text += " — quantity not specified"
    return text


def gather_ingredients(
    recipes: list[dict[str, Any]],
    include_optional: bool,
) -> list[Ingredient]:
    out: list[Ingredient] = []
    for rec in recipes:
        day = str(rec["day"])
        recipe = str(rec["recipe"])
        for obj in rec["ingredients"]:
            if not isinstance(obj, dict):
                raise ValueError(f"{day} / {recipe}: ingredient record is not an object")
            ing = Ingredient.from_obj(obj, day, recipe)
            if ing.pantry:
                continue
            if ing.optional and not include_optional:
                continue
            out.append(ing)
    return out

def build_markdown_shopping_list(
    selected: list[dict[str, Any]],
    quantified: list[dict[str, Any]],
    unquantified: list[dict[str, Any]],
    include_optional: bool,
) -> str:
    by_section: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_section_unq: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in quantified:
        by_section[item["category"]].append(item)
    for item in unquantified:
        by_section_unq[item["category"]].append(item)

    lines = ["# Shopping List", ""]
    lines.append("Recipes included: " + ", ".join(str(r["day"]) for r in selected))
    lines.append("")

    if not include_optional:
        lines.append("_Optional ingredients are excluded by default._")
        lines.append("")

    for section in SECTION_ORDER:
        items = by_section.get(section, [])
        unq = by_section_unq.get(section, [])

        if not items and not unq:
            continue

        lines += [f"## {section}", ""]

        for item in sorted(items, key=lambda x: x["name"]):
            lines.append(f"- [ ] {render_line(item)}")

        for item in sorted(unq, key=lambda x: x["name"]):
            lines.append(f"- [ ] {render_unquantified(item)}")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


class Tools:
    def __init__(self):
        pass

    def export_meal_plan(
        self,
        recipes: list[dict[str, Any]] | dict[str, Any] | str,
        include_optional: bool = False,
        select: list[str] | None = None,
    ) -> str:
        """
        Generate a deterministic Markdown shopping list from structured meal-plan data.

        :param recipes: Structured recipe data. Accepts a recipe array, one recipe
                       object, an object containing {"recipes": [...]}, or a JSON string.
        :param include_optional: Include ingredients explicitly marked optional.
                                Defaults to False.
        :param select: Optional list of exact day names or exact recipe names to export.
                       Omit or pass null to export all recipes.
        :return: Consolidated Markdown shopping list.
        """
        normalized = normalize_recipe_input(recipes)
        selected = select_recipes(normalized, select)

        if not selected:
            raise ValueError("No recipes selected")

        ingredients = gather_ingredients(selected, include_optional)
        quantified, unquantified = consolidate(ingredients)

        return build_markdown_shopping_list(
            selected,
            quantified,
            unquantified,
            include_optional,
        )
