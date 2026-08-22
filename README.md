# AI Meal Planner

AI Meal Planner is a platform-independent prompt and workflow for generating practical weekly meal plans with:

* healthy, weeknight-friendly recipes
* configurable servings and meal counts
* cooking-time limits
* ingredient reuse to reduce waste
* consolidated grocery lists
* seasonal ingredient preferences
* cuisine and protein variety
* Schema.org Recipe JSON export
* optional integration with recipe managers such as Mealie

Open WebUI is the first supported platform, but the core prompt is designed to work independently of any specific LLM interface.

## Why This Project Exists

Many AI meal-planning prompts generate individual recipes reasonably well but do not treat an entire week as one coordinated plan.

AI Meal Planner focuses on the week as a whole.

It tries to:

* avoid repeating the same primary protein on consecutive nights
* reuse ingredients intelligently
* reduce unnecessary specialty purchases
* plan around realistic grocery quantities
* keep meals practical for ordinary weeknights
* consolidate ingredients into one grocery list
* preserve enough recipe structure for later export

The goal is not just to answer:

```text
What should I cook tonight?
```

but also:

```text
What should I cook this week, what do I need to buy, and how can I avoid wasting ingredients?
```

## Current Workflow

The core workflow is:

```text
User
 |
 | "Plan my dinners for next week"
 v
AI Meal Planner
 |
 +-- Dinner recipes
 +-- Ingredient reuse
 +-- Grocery list
 +-- Prep opportunities
 |
 | "Export Tuesday's recipe for Mealie"
 v
Schema.org Recipe JSON
 |
 | Manual import
 v
Mealie
```

The AI handles meal planning.

Mealie can then be used for recipe storage, meal scheduling, shopping, and cooking.

Direct Mealie API integration is planned as a future enhancement.

## Portable Outputs

AI Meal Planner is intended to be useful even when the user does not use Mealie or another recipe-management system.

The next development priority is portable output that can be saved, downloaded, or used on common devices.

Planned outputs include:

* individual recipe files in Markdown
* a complete weekly meal-plan file
* a mobile-friendly shopping checklist
* a plain-text shopping list
* a downloadable meal-plan bundle containing the weekly plan, shopping list, and individual recipes

A future bundle may look like:

```text
meal-plan/
├── weekly-plan.md
├── shopping-list.md
├── shopping-list.txt
└── recipes/
    ├── sunday-chicken.md
    ├── monday-shrimp.md
    ├── tuesday-tacos.md
    └── ...
```

These files are intended to be useful on a computer, phone, or tablet without requiring users to understand JSON or APIs.

Mealie remains an optional integration for users who want recipe-management features.

## Features

### Meal Planning

AI Meal Planner can:

* generate a configurable number of dinners
* scale recipes for a configured number of servings
* enforce a maximum total cooking time
* favor reasonably healthy and balanced meals
* provide estimated calories per serving
* vary cuisines, flavors, proteins, and cooking styles
* avoid the same primary protein on consecutive nights
* reuse ingredients across recipes
* reduce unnecessary food waste
* create a consolidated grocery list
* suggest optional prep-ahead opportunities

### Configuration

The default project configuration includes:

| Setting                        | Default                 |
| ------------------------------ | ----------------------- |
| Number of dinners              | 7                       |
| Servings per dinner            | 2                       |
| Maximum cooking time           | 45 minutes              |
| Location                       | Brodhead, Kentucky, USA |
| Seasonal ingredient preference | Enabled                 |

These are defaults only.

Users can change them permanently or override them in individual requests.

For example:

```text
Plan five dinners this week for four people.
```

or:

```text
Keep everything under 30 minutes and include two vegetarian meals.
```

See:

```text
docs/configuration.md
```

for configuration details.

## Core Prompt

The canonical platform-independent prompt is located at:

```text
prompt/meal-planner.md
```

This file defines the meal-planning behavior and should remain independent of platform-specific installation details.

## Open WebUI

Open WebUI is the first supported platform.

Platform-specific files are located under:

```text
platforms/openwebui/
```

The Open WebUI integration is intended to make it easy to use AI Meal Planner as a reusable system prompt or model configuration.

Additional platforms may be added later without changing the canonical prompt.

## Mealie Support

AI Meal Planner can export generated recipes as Schema.org Recipe JSON.

Example request:

```text
Export the salmon recipe for Mealie.
```

The output uses standard Schema.org properties such as:

```text
name
recipeCuisine
recipeYield
totalTime
recipeIngredient
recipeInstructions
nutrition
```

The current workflow uses manual import into Mealie.

See:

```text
docs/mealie-export.md
```

for details.

Future versions may support direct Mealie API integration.

## Repository Layout

```text
ai-meal-planner/
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── .gitignore
│
├── prompt/
│   └── meal-planner.md
│
├── platforms/
│   └── openwebui/
│       ├── README.md
│       └── meal-planner.json
│
├── examples/
│   ├── weekly-plan.md
│   └── mealie-recipe.json
│
├── docs/
│   ├── configuration.md
│   ├── mealie-export.md
│   └── roadmap.md
│
└── integrations/
    └── mealie/
        └── README.md
```

## Getting Started

The simplest way to use AI Meal Planner is to provide the canonical prompt to a language model as its system prompt.

Start with:

```text
prompt/meal-planner.md
```

Review and adjust the default configuration near the top of the file.

Then ask the model something simple such as:

```text
Plan my dinners for next week.
```

The configured defaults will be used unless your request overrides them.

For example:

```text
Plan five dinners this week for four people.
```

or:

```text
Plan seven dinners, but keep everything under 30 minutes.
```

Platform-specific installation instructions are provided separately.

## Example Requests

### Normal Weekly Plan

```text
Plan my dinners for next week.
```

### Different Number of Meals

```text
Plan five dinners this week.
```

### Different Household Size

```text
Plan dinners this week for four people.
```

### Additional Preferences

```text
Plan seven dinners.

Include at least two vegetarian meals and avoid pork.
```

### Mealie Export

```text
Export Wednesday's recipe for Mealie.
```

## Project Philosophy

AI Meal Planner follows several design principles.

### Keep the Core Simple

The project should remain usable as a single prompt without requiring an API, database, recipe manager, or specific frontend.

### Keep Platforms Separate

Open WebUI-specific behavior belongs under `platforms/openwebui/`.

Other platforms can be added independently.

### Keep Integrations Optional

Mealie and other recipe-management integrations should extend the planner rather than become dependencies.

### Use Open Standards

Where practical, recipe interchange should use standards such as Schema.org Recipe rather than project-specific formats.

### Keep Secrets Out of Prompts

API keys, passwords, access tokens, and private server information should never be embedded in the canonical prompt or committed to the repository.

## Roadmap

Planned work includes:

* Open WebUI packaging and documentation
* example weekly meal plans
* example Mealie recipe exports
* additional user preferences
* testing with multiple language models
* direct Mealie API integration
* reuse of recipes already stored in Mealie
* other LLM platforms and recipe-management integrations

See:

```text
docs/roadmap.md
```

for the detailed roadmap.

## Contributing

Contributions, testing, issue reports, and suggestions are welcome.

See:

```text
CONTRIBUTING.md
```

for contribution guidance.

## License

This project is released under the license included in:

```text
MIT
```

