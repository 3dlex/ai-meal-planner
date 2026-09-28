# Mealie Recipe Export

Use this Skill only when the user explicitly asks to export, convert, or format one or more existing recipes for Mealie.

Do not automatically export recipes after meal planning.

Do not create Mealie JSON unless the user requests it.

## Purpose

Convert selected recipes already present in the conversation into Mealie-compatible schema.org `Recipe` JSON-LD.

This Skill is for recipe conversion, not recipe creation.

## Source Recipe

Use the recipe already established in the current conversation.

Preserve the original recipe as closely as possible.

Do not redesign, improve, simplify, substitute, or otherwise alter the recipe unless the user explicitly asks for a change.

Preserve:

- recipe name
- description, if available
- serving count
- ingredients
- ingredient quantities
- preparation time
- cooking time
- total time
- cuisine or style
- estimated calories
- cooking instructions

If the user refers to a recipe by day, name, ingredient, or other clear description, identify that recipe from the conversation.

Examples:

- "Export Sunday's chicken recipe for Mealie."
- "Give me the lamb recipe in Mealie format."
- "Export Tuesday and Thursday."
- "Convert the salmon recipe to Mealie JSON."

If the requested recipe cannot be identified reliably from the conversation, ask which recipe the user means.

## Output Format

Convert each selected recipe to schema.org `Recipe` JSON-LD.

Use:

- `"@context": "https://schema.org"`
- `"@type": "Recipe"`

Include when available:

- `name`
- `description`
- `recipeYield`
- `prepTime`
- `cookTime`
- `totalTime`
- `recipeCategory`
- `recipeCuisine`
- `nutrition`
- `recipeIngredient`
- `recipeInstructions`

## Time Format

Use ISO 8601 duration values.

Examples:

- 10 minutes → `PT10M`
- 25 minutes → `PT25M`
- 45 minutes → `PT45M`
- 1 hour → `PT1H`
- 1 hour 15 minutes → `PT1H15M`

Do not use plain-language duration strings in the JSON time fields.

## Servings

Set `recipeYield` from the source recipe.

Example:

```json
"recipeYield": "2 servings"
```

Do not change the serving count unless the user requests scaling.

## Ingredients

`recipeIngredient` must be an array of complete human-readable strings.

Each ingredient string should preserve the original quantity, unit, preparation, and optional status when applicable.

Example:

```json
"recipeIngredient": [
  "12 oz boneless skinless chicken breast",
  "1 medium zucchini, sliced",
  "2 cloves garlic, minced",
  "1 tbsp olive oil"
]
```

Do not generate:

- Mealie food IDs
- Mealie unit IDs
- UUIDs
- database references
- internal ingredient objects

## Instructions

Use schema.org `HowToStep` objects.

Example:

```json
"recipeInstructions": [
  {
    "@type": "HowToStep",
    "text": "Heat the olive oil in a large skillet over medium-high heat."
  },
  {
    "@type": "HowToStep",
    "text": "Add the chicken and cook until browned and cooked through."
  }
]
```

Preserve the original order and meaning of the cooking instructions.

Do not add cooking steps that were not present in the source recipe unless necessary to convert fragmented instructions into complete sentences.

## Nutrition

If the source recipe includes calorie information, use schema.org `NutritionInformation`.

Example:

```json
"nutrition": {
  "@type": "NutritionInformation",
  "calories": "560 calories"
}
```

If the source recipe provides a calorie range, preserve the range rather than inventing a precise value.

Example:

```json
"calories": "540-590 calories"
```

Do not invent nutrition information that is not present in the source recipe.

## Optional Ingredients

Preserve optional ingredients.

Example:

```json
"1 tbsp chopped parsley, optional"
```

Do not silently remove optional ingredients.

## Source Information

Do not invent:

- source URLs
- author names
- publisher names
- images
- recipe IDs
- Mealie slugs
- UUIDs

If source information was explicitly provided with the original recipe, it may be preserved.

## Fidelity Check

Before producing the final JSON, verify:

- the recipe name matches the source;
- serving count matches;
- all ingredients are present;
- quantities and units match;
- optional ingredients remain optional;
- cooking instructions match the source;
- prep, cook, and total times match;
- calorie information matches;
- no substitutions or recipe improvements were introduced.

Correct any mismatch before returning the result.

## Output Behavior

For a single recipe, output one valid JSON object.

For multiple recipes, output each recipe as a separate JSON object in its own code block.

Do not automatically export the entire weekly meal plan unless the user explicitly asks for all recipes.

Keep explanatory text outside the JSON minimal.

Never place comments inside the JSON.
