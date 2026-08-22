# Mealie Recipe Export

AI Meal Planner can export generated recipes in a format suitable for importing into Mealie.

The current integration is manual.

AI Meal Planner generates a recipe as Schema.org `Recipe` JSON. The user then imports that JSON into Mealie.

Future versions of the project may support direct communication with the Mealie API.

## Current Workflow

The current workflow is:

```text
AI Meal Planner
       |
       | Generate weekly meal plan
       v
Weekly recipes
       |
       | "Export the salmon recipe for Mealie"
       v
Schema.org Recipe JSON
       |
       | Manual import
       v
Mealie
```

This keeps meal planning separate from recipe storage.

AI Meal Planner decides what to cook.

Mealie stores the recipes and can then be used for meal scheduling, shopping, and cooking.

## Requesting a Mealie Export

The normal output of AI Meal Planner is the full meal plan.

Mealie export mode is only used when explicitly requested.

Examples:

```text
Export Tuesday's recipe for Mealie.
```

```text
Give me the chicken recipe as Mealie JSON.
```

```text
Export the salmon dinner to Mealie.
```

When one recipe is requested, the planner returns one complete Schema.org `Recipe` JSON object.

## Schema

Recipe exports conform to the Schema.org Recipe vocabulary:

```text
https://schema.org/Recipe
```

Each exported recipe begins with:

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe"
}
```

The export must not use a custom outer wrapper such as:

```json
{
  "recipe": {
  }
}
```

## Property Mapping

AI Meal Planner uses standard Schema.org Recipe properties wherever possible.

| Meal Planner Value   | Schema.org Property  |
| -------------------- | -------------------- |
| Meal name            | `name`               |
| Description          | `description`        |
| Cuisine or style     | `recipeCuisine`      |
| Meal category        | `recipeCategory`     |
| Number of servings   | `recipeYield`        |
| Preparation time     | `prepTime`           |
| Cooking time         | `cookTime`           |
| Total elapsed time   | `totalTime`          |
| Ingredients          | `recipeIngredient`   |
| Cooking instructions | `recipeInstructions` |
| Calories             | `nutrition`          |
| Descriptive tags     | `keywords`           |

Custom replacements should not be used when an appropriate Schema.org property already exists.

For example, avoid properties such as:

```text
servings
ingredients
instructions
totalTimeMinutes
caloriesPerServingRange
```

## Ingredients

Ingredients are exported using `recipeIngredient`.

The value must be a flat array of human-readable strings.

Example:

```json
"recipeIngredient": [
  "2 salmon fillets (6 oz each)",
  "1 large broccoli crown, cut into florets",
  "2 tbsp olive oil, divided"
]
```

Ingredient quantities should remain understandable to a person preparing the recipe.

Ingredients must not be nested into custom objects or ingredient groups.

## Instructions

Cooking instructions use Schema.org `HowToStep` objects.

Example:

```json
"recipeInstructions": [
  {
    "@type": "HowToStep",
    "text": "Preheat the oven to 425°F."
  },
  {
    "@type": "HowToStep",
    "text": "Roast the vegetables until tender."
  }
]
```

Steps must remain in the proper cooking order.

Important cooking temperatures, timing, and food-safety instructions should be preserved.

## Recipe Times

Recipe times use ISO 8601 duration strings.

Examples:

```text
10 minutes      PT10M
35 minutes      PT35M
1 hour          PT1H
1 hour 15 min   PT1H15M
```

Example:

```json
"totalTime": "PT40M"
```

If only total elapsed time is known, the planner should provide `totalTime` rather than inventing separate preparation and cooking times.

## Nutrition

When calories were estimated in the original meal plan, they are represented using a Schema.org `NutritionInformation` object.

Example:

```json
"nutrition": {
  "@type": "NutritionInformation",
  "calories": "560-620 calories"
}
```

The planner should not invent additional nutritional values that were not calculated or provided.

For example, protein, fat, carbohydrates, sodium, and similar values should not be added merely to make the export appear more complete.

## Example Export

A simplified recipe export looks like:

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Lemon Herb Salmon with Roasted Broccoli",
  "recipeCuisine": "Mediterranean-inspired",
  "recipeCategory": "Dinner",
  "recipeYield": "2 servings",
  "totalTime": "PT35M",
  "recipeIngredient": [
    "2 salmon fillets (6 oz each)",
    "1 large broccoli crown, cut into florets",
    "1 lemon",
    "2 tbsp olive oil"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "text": "Preheat the oven to 425°F."
    },
    {
      "@type": "HowToStep",
      "text": "Arrange the broccoli on a baking sheet and season."
    },
    {
      "@type": "HowToStep",
      "text": "Add the salmon and roast until the salmon is cooked through and the broccoli is tender."
    }
  ],
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "500-560 calories"
  },
  "keywords": [
    "weeknight",
    "salmon",
    "Mediterranean-inspired"
  ]
}
```

This example demonstrates the structure only.

Actual exports should preserve the ingredients, quantities, timing, instructions, and other information from the recipe that was originally generated.

## Multiple Recipe Exports

Multiple recipes may also be requested.

For example:

```text
Export Monday, Wednesday, and Friday for Mealie.
```

Each recipe should be returned as its own complete Schema.org `Recipe` object.

Unless specifically requested, multiple recipes should not be wrapped inside one JSON array or combined into a single recipe object.

This makes each recipe independently usable.

## Validation

Before returning a Mealie export, AI Meal Planner verifies that:

* the JSON is syntactically valid
* `@context` is `https://schema.org`
* `@type` is `Recipe`
* there is no custom outer `recipe` wrapper
* `recipeIngredient` is a flat array of strings
* `recipeInstructions` contains ordered `HowToStep` objects
* recipe times use ISO 8601 duration syntax
* calorie information is contained in `NutritionInformation`
* standard Schema.org properties are used where available
* the exported recipe matches the original generated recipe

## Manual Import

At the current stage of the project, the generated JSON is imported into Mealie manually.

The exact import procedure may vary with Mealie versions, so platform-specific instructions should be kept separate from the core Schema.org export specification.

The important interface between the two systems is:

```text
AI Meal Planner
       |
       v
Schema.org Recipe JSON
       |
       v
Mealie
```

## Future API Integration

Direct Mealie integration is planned as a future enhancement.

A future integration may allow requests such as:

```text
Send Tuesday's recipe to Mealie.
```

or:

```text
Add Monday, Wednesday, and Friday to Mealie.
```

The integration layer would then:

1. Generate or retrieve the selected recipe.
2. Convert it to the required recipe representation.
3. Authenticate with the configured Mealie server.
4. Submit the recipe through the Mealie API.
5. Verify that the import succeeded.
6. Return useful information about the created recipe.

API credentials and server URLs must not be embedded in the core meal-planning prompt.

They should be handled by the integration layer using appropriate configuration or secrets management.

## Design Principle

Schema.org Recipe JSON is the boundary between meal planning and recipe management.

This allows the core AI Meal Planner prompt to remain platform-independent while Mealie-specific functionality evolves separately.

The same approach may also allow support for other recipe-management platforms in the future.
