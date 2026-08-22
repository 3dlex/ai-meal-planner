# Mealie Integration

Mealie is an optional recipe-management integration for AI Meal Planner.

AI Meal Planner does not require Mealie.

The core project is intended to work as a standalone meal planner with portable recipe and shopping-list outputs.

Mealie support extends that workflow for users who want recipe storage, meal scheduling, shopping, and other recipe-management features.

## Current Status

The current Mealie workflow is supported and has been tested successfully.

```text
AI Meal Planner
       |
       | Generate meal plan
       v
Generated recipe
       |
       | Export as Mealie JSON
       v
Schema.org Recipe JSON
       |
       | Manual import
       v
Mealie
```

Current status:

```text
Schema.org Recipe export: supported
Manual Mealie import: tested and supported
Direct Mealie API integration: planned
```

The current export format is documented in:

```text
docs/mealie-export.md
```

## Tested Workflow

A generated recipe was exported by AI Meal Planner as Schema.org Recipe JSON and imported successfully into a real Mealie installation.

During initial testing, the import first returned HTTP `401 Unauthorized` because the Mealie browser session was no longer valid.

After logging out and back in, the same recipe JSON imported successfully.

This confirmed that the generated Schema.org Recipe structure was accepted by the tested Mealie installation.

## Relationship to Portable Exports

Mealie is no longer the immediate next development priority.

The next major project direction is portable output that benefits all users, including those who do not use a recipe manager.

Planned portable outputs include:

* individual Markdown recipe files
* a complete weekly meal-plan file
* mobile-friendly shopping checklists
* plain-text shopping lists
* downloadable meal-plan bundles

A typical future workflow may look like:

```text
AI Meal Planner
       |
       v
Weekly Meal Plan
       |
       +--> weekly-plan.md
       |
       +--> shopping-list.md
       |
       +--> shopping-list.txt
       |
       +--> recipes/
       |      sunday-chicken.md
       |      monday-shrimp.md
       |      ...
       |
       +--> optional Mealie export
```

This keeps Mealie useful without making it a requirement.

## Why Schema.org Recipe

AI Meal Planner uses Schema.org Recipe JSON for Mealie recipe export.

This provides a documented and portable structure for:

* recipe names
* serving counts
* cooking times
* ingredients
* cooking instructions
* cuisine information
* calorie estimates

Using a standard recipe representation helps keep the project from becoming tightly coupled to Mealie.

It may also make future recipe-management integrations easier to support.

## Separation of Responsibilities

The project keeps meal planning, portable output, and external integrations separate.

```text
prompt/meal-planner.md
        |
        | Meal-planning behavior
        v
Generated meal plan
        |
        +--> Portable human-readable files
        |
        +--> Schema.org Recipe JSON
                    |
                    v
            integrations/mealie/
                    |
                    v
                  Mealie
```

The canonical prompt should not need to know:

* the Mealie server URL
* API credentials
* network details
* authentication implementation
* Mealie-specific API endpoints

Those details belong in the Mealie integration layer.

## Direct API Integration

Direct Mealie API integration remains a future enhancement.

A future integration may allow requests such as:

```text
Send Tuesday's recipe to Mealie.
```

or:

```text
Add Monday, Wednesday, and Friday to Mealie.
```

The integration layer would then be responsible for:

* connecting to a configured Mealie server
* authenticating securely
* submitting one or more recipes
* validating API responses
* detecting import failures
* returning information about successfully created recipes
* avoiding duplicate recipes where practical

## Configuration

When direct API integration is implemented, Mealie-specific configuration must remain outside the canonical meal-planning prompt.

Possible configuration values may include:

```text
MEALIE_URL
MEALIE_API_TOKEN
```

Exact names and implementation details will be determined when the integration is developed.

Secrets such as API tokens must never be committed to the repository.

## Future Work

Potential Mealie-specific work includes:

* [ ] determine the supported Mealie API workflow for recipe creation
* [ ] create a reusable API client
* [ ] support API token authentication
* [ ] securely configure the Mealie server URL
* [ ] send one selected recipe to Mealie
* [ ] send multiple selected recipes
* [ ] validate successful recipe creation
* [ ] return the created recipe identifier or URL
* [ ] detect likely duplicate recipes
* [ ] query recipes already stored in Mealie
* [ ] reuse existing Mealie recipes in future meal plans
* [ ] interact with Mealie meal plans
* [ ] interact with Mealie shopping lists when appropriate

These features remain optional.

AI Meal Planner must continue to work without Mealie.
