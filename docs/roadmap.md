# Roadmap

This document tracks planned improvements for AI Meal Planner.

The project should remain useful as a simple prompt-driven meal planner while allowing optional integrations and additional platforms to evolve independently.

The roadmap is intentionally divided into stages so future functionality does not complicate the core project prematurely.

# Current Scope

The current version of AI Meal Planner provides:

* configurable meal-planning defaults
* weekly dinner planning
* practical weeknight time limits
* ingredient reuse to reduce waste
* consolidated grocery lists
* seasonal ingredient preferences
* cuisine and protein variety
* consistency checks
* Schema.org Recipe JSON export
* manual import of exported recipes into Mealie
* Open WebUI as the first supported platform

The core prompt remains platform-independent.

# Version 1.0

Version 1.0 focuses on making the existing working prompt clean, documented, and reusable.

## Core Prompt

* [x] Create platform-independent canonical meal-planning prompt
* [x] Make number of dinners configurable
* [x] Make serving count configurable
* [x] Make maximum cooking time configurable
* [x] Make location configurable
* [x] Make seasonal ingredient preference configurable
* [x] Preserve per-request overrides
* [x] Preserve ingredient reuse and waste-reduction behavior
* [x] Preserve consolidated grocery-list generation
* [x] Preserve final consistency validation

# Version 1.1 — Portable Meal Plan Exports
* [x] Define a human-readable Markdown recipe export format
* [x] Define a mobile-friendly consolidated shopping checklist format

Version 1.1 focuses on making AI Meal Planner useful outside any specific AI interface or recipe-management application.

The goal is to let an ordinary user generate a meal plan and then save or use the results on a computer, phone, or tablet without needing to understand JSON, APIs, or Mealie.

## Recipe Exports

* [ ] Export each generated recipe as a separate Markdown file
* [ ] Use readable, filesystem-safe recipe filenames
* [ ] Include recipe name, servings, time, calories, ingredients, and instructions
* [ ] Preserve optional prep-ahead information
* [ ] Keep recipe files human-readable without requiring special software

Example:

```text
recipes/
    sunday-pan-seared-chicken.md
    monday-shrimp-zucchini-stir-fry.md
    tuesday-turkey-black-bean-tacos.md
```

## Shopping List Exports

* [ ] Export the consolidated shopping list as Markdown
* [ ] Format the Markdown version as a mobile-friendly checklist
* [ ] Export the shopping list as plain text
* [ ] Preserve grocery-store section organization
* [ ] Use practical purchase quantities
* [ ] Make the output easy to copy into common notes and checklist applications
* [ ] Support shopping lists scoped to one recipe, selected recipes, or the full weekly plan

Example:

```markdown
## Produce

- [ ] 1 pint cherry tomatoes
- [ ] 2 ears corn
- [ ] 1 bunch basil
- [ ] 1 red onion
```

## Weekly Plan Export

* [ ] Export the complete weekly plan as Markdown
* [ ] Preserve all generated recipes
* [ ] Include the consolidated shopping list
* [ ] Include weekly prep opportunities
* [ ] Keep the file readable independently of the AI chat that created it

## Meal Plan Bundle

A future portable export may create a complete meal-plan package such as:

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

Possible goals include:

* [ ] create all files from one generated weekly plan
* [ ] keep filenames predictable and readable
* [ ] package the files into a downloadable archive when supported
* [ ] ensure the bundle remains useful without Open WebUI or Mealie

## Relationship to Mealie

Mealie remains a supported integration, but direct API integration is no longer the immediate next development priority.

Portable recipe and shopping-list exports should be implemented first because they are useful to everyone, whether or not they use Mealie.

The current manual Schema.org JSON export to Mealie remains supported.

## Mealie Export

* [x] Support Schema.org Recipe output
* [x] Support single-recipe export
* [x] Support multiple-recipe export
* [x] Use Schema.org Recipe property names
* [x] Use ISO 8601 recipe durations
* [x] Use Schema.org HowToStep instructions
* [x] Use NutritionInformation for calorie estimates
* [x] Validate JSON structure before returning exports
* [x] Document current manual Mealie workflow

## Documentation

* [x] Add configuration documentation
* [x] Add Mealie export documentation
* [ ] Add project README
* [ ] Add Open WebUI installation instructions
* [ ] Add sample weekly meal plan
* [ ] Add sample Mealie recipe export
* [ ] Add contributing guidelines
* [ ] Add changelog

# Version 1.x

Version 1.x improvements should remain prompt-focused and should not require external services.

Possible enhancements include:

* [ ] dietary restriction preferences
* [ ] ingredient exclusions
* [ ] preferred cuisines
* [ ] preferred proteins
* [ ] configurable vegetarian meal frequency
* [ ] budget preference
* [ ] kitchen-equipment preferences
* [ ] leftover-night support
* [ ] spice-level preference
* [ ] configurable pantry staples
* [ ] configurable grocery-list categories
* [ ] optional nutrition goals
* [ ] test prompt behavior with multiple language models

These may begin as natural-language request options before becoming formal configuration values.

# Platform Support

Open WebUI is the first supported platform.

Future platform-specific packaging may include:

* [ ] generic system-prompt instructions
* [ ] Ollama examples
* [ ] LM Studio examples
* [ ] ChatGPT usage examples
* [ ] other LLM front ends

Platform-specific configuration should live under:

```text
platforms/
```

The canonical meal-planning behavior should remain in:

```text
prompt/meal-planner.md
```

# Mealie Integration

Direct Mealie API integration is a future enhancement.

The current workflow remains:

```text
AI Meal Planner
       |
       v
Schema.org Recipe JSON
       |
       v
Manual Mealie Import
```

A future workflow may become:

```text
AI Meal Planner
       |
       | "Send this recipe to Mealie"
       v
Mealie Integration
       |
       v
Mealie API
       |
       v
Recipe Created
```

## Initial API Goals

* [ ] configure Mealie server URL outside the prompt
* [ ] configure authentication securely
* [ ] send one selected recipe to Mealie
* [ ] send multiple selected recipes to Mealie
* [ ] validate API responses
* [ ] report import failures clearly
* [ ] return information about successfully created recipes
* [ ] avoid storing credentials in source code
* [ ] document configuration and security requirements

## Additional Mealie Features

Possible later enhancements include:

* [ ] detect existing recipes before creating duplicates
* [ ] query recipes already stored in Mealie
* [ ] reuse existing Mealie recipes in weekly plans
* [ ] create or update Mealie meal plans
* [ ] create shopping lists
* [ ] interact with pantry or food inventory data when available

These features should not become requirements for using the core project.

# Other Integrations

The project architecture should allow recipe-management integrations other than Mealie.

Future integrations could live under:

```text
integrations/
```

For example:

```text
integrations/
    mealie/
    another-platform/
```

Any new integration should remain optional.

The core planner should continue to work without external APIs.

# Testing

Because language-model output is nondeterministic, testing should distinguish between strict structural requirements and qualitative planning behavior.

## Completed Manual Tests

* [x] Generate a seven-dinner weekly meal plan using the default configuration
* [x] Export a selected generated recipe as Schema.org Recipe JSON
* [x] Confirm exported recipe JSON is syntactically valid
* [x] Import generated Schema.org Recipe JSON into a real Mealie installation
* [x] Confirm Mealie creates the imported recipe successfully

The initial end-to-end Mealie test used a generated chicken recipe exported from AI Meal Planner and imported through Mealie's JSON import workflow.

An initial failed import was traced to an expired or invalid Mealie session returning HTTP `401 Unauthorized`. After logging out and back in, the same recipe JSON imported successfully.

This confirmed that the generated Schema.org Recipe structure was accepted by the tested Mealie installation.

## Future Repeatable Tests

* [ ] correct number of meals generated
* [ ] correct serving quantities
* [ ] cooking-time limit respected
* [ ] no repeated primary protein on consecutive nights
* [ ] grocery-list ingredients match recipes
* [ ] ingredient quantities are reasonably consolidated
* [ ] significant ingredients are reused where practical
* [ ] valid single-recipe Schema.org export
* [ ] valid multiple-recipe exports
* [ ] ISO 8601 time formatting
* [ ] valid JSON syntax
* [ ] automated Schema.org structure validation
* [ ] repeat Mealie import testing after major prompt changes
* [ ] test with multiple language models
* [ ] test with future Mealie versions

Because language-model output is nondeterministic, future automated tests may need to distinguish between structural failures and qualitative planning differences.

# Non-Goals

AI Meal Planner is not intended to:

* replace professional medical or nutritional advice
* guarantee exact grocery-store inventory
* guarantee exact food prices
* calculate medically precise nutrition data
* require Mealie
* require Open WebUI
* require a particular language model
* require external APIs for basic meal planning

# Design Principles

Future development should follow these principles.

## Keep the Core Simple

A user should always be able to use AI Meal Planner by giving a language model the core prompt.

## Keep Platforms Separate

Open WebUI and other platform-specific configuration should not become part of the canonical prompt unless the behavior is genuinely universal.

## Keep Integrations Optional

Recipe managers such as Mealie should extend the planner rather than become dependencies.

## Keep Secrets Out of Prompts

API keys, passwords, tokens, and private server configuration must never be embedded in the canonical prompt or committed to the repository.

## Preserve Interoperability

Where practical, use open standards such as Schema.org Recipe rather than creating project-specific recipe formats.

## Avoid Premature Complexity

New features should solve real workflow problems before being promoted into the core design.
