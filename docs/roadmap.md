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

Future releases should introduce repeatable prompt tests.

Possible test cases include:

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

Because language-model output is nondeterministic, tests may need to distinguish between strict structural requirements and qualitative planning behavior.

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
