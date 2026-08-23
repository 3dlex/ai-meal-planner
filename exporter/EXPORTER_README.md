# Deterministic Meal Plan Exporter

`meal_plan_exporter.py` turns the AI Meal Planner's structured ingredient JSON
into deterministic shopping-list files.

## What version 1 does

- accepts one recipe, selected recipes, or the full week
- filters `pantry: true` ingredients
- excludes optional ingredients by default
- combines equivalent ingredient names
- adds compatible quantities
- converts compatible volume units (`tsp`, `tbsp`, `cup`)
- converts compatible weight units (`oz`, `lb`)
- preserves ingredients whose quantity is `null` instead of inventing a number
- creates:
  - `shopping-list.md`
  - `shopping-list.txt`
  - `structured-ingredients.json`
  - `export-manifest.json`
- optionally creates a ZIP bundle

## Important design choice

Version 1 does **not** guess store package sizes.

For example, it can deterministically calculate:

```text
12 clove garlic
1.5 cup quinoa
2 lb ground turkey
```

It does not silently convert those into:

```text
2 heads garlic
1 lb bag quinoa
2 lb package turkey
```

Package-size conversion requires an explicit rule table and will be a separate
layer. This prevents the exporter from repeating the same guessing errors we
were trying to remove from the language model.

## Expected input

Array form is recommended:

```json
[
  {
    "day": "Monday",
    "recipe": "Shrimp & Zucchini Stir-Fry with Brown Rice",
    "ingredients": [
      {
        "name": "garlic",
        "quantity": 3,
        "unit": "clove",
        "size": "",
        "preparation": "minced",
        "optional": false,
        "pantry": false,
        "alternative": null
      }
    ]
  }
]
```

The program also accepts a single recipe object or:

```json
{
  "recipes": [
    ...
  ]
}
```

## Examples

Whole week:

```bash
python3 meal_plan_exporter.py structured-ingredients.json
```

Selected days:

```bash
python3 meal_plan_exporter.py structured-ingredients.json \
  --select Monday Wednesday Friday
```

One recipe:

```bash
python3 meal_plan_exporter.py structured-ingredients.json \
  --select Sunday
```

Include optional ingredients:

```bash
python3 meal_plan_exporter.py structured-ingredients.json \
  --include-optional
```

Create ZIP:

```bash
python3 meal_plan_exporter.py structured-ingredients.json \
  --zip
```

Choose output directory:

```bash
python3 meal_plan_exporter.py structured-ingredients.json \
  --output-dir meal-plan
```

## Output

```text
meal-plan-export/
├── shopping-list.md
├── shopping-list.txt
├── structured-ingredients.json
└── export-manifest.json
```

With `--zip`:

```text
meal-plan-export.zip
```

## Next layer

The next deterministic layer should be a configurable purchase-rule file, for
example:

```json
{
  "garlic": {
    "purchase_unit": "head",
    "approx_cloves_per_unit": 10
  },
  "quinoa": {
    "purchase_unit": "bag",
    "package_oz": 16
  }
}
```

That layer should be explicit and editable rather than inferred by the model.
