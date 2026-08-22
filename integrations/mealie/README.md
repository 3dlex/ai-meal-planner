# Mealie Integration

This directory is reserved for direct Mealie integration with AI Meal Planner.

Direct API integration is **not implemented yet**.

The current supported workflow is documented in:

```text
docs/mealie-export.md
```

## Current Workflow

Today, AI Meal Planner can generate Schema.org Recipe JSON for recipes selected by the user.

The workflow is:

```text
AI Meal Planner
       |
       | Generate meal plan
       v
Generated recipe
       |
       | Request Mealie export
       v
Schema.org Recipe JSON
       |
       | Manual import
       v
Mealie
```

This keeps the core meal-planning prompt independent of Mealie.

## Planned Integration

A future Mealie integration may allow requests such as:

```text
Send Tuesday's recipe to Mealie.
```

or:

```text
Add Monday, Wednesday, and Friday to Mealie.
```

The integration layer would be responsible for communicating with the Mealie API.

Possible responsibilities include:

* connecting to a configured Mealie server
* authenticating securely
* submitting one or more recipes
* validating API responses
* detecting import failures
* returning information about successfully created recipes
* avoiding duplicate recipes where practical

## Configuration

Mealie-specific configuration must remain outside the canonical meal-planning prompt.

Examples include:

```text
MEALIE_URL
MEALIE_API_TOKEN
```

Exact configuration names and implementation details will be determined when API integration is developed.

Secrets such as API tokens must never be committed to the repository.

## Separation of Responsibilities

The project is designed around three separate layers:

```text
prompt/meal-planner.md
        |
        | Meal planning behavior
        v
Schema.org Recipe JSON
        |
        | Integration boundary
        v
integrations/mealie/
        |
        | Mealie-specific API behavior
        v
Mealie
```

The canonical prompt should not need to know:

* the Mealie server URL
* API credentials
* network details
* authentication implementation
* Mealie-specific API endpoints

Those details belong in the integration layer.

## Why Schema.org Recipe

AI Meal Planner currently uses Schema.org Recipe JSON as the recipe interchange format.

This provides a documented and portable structure for:

* recipe names
* serving counts
* cooking times
* ingredients
* cooking instructions
* cuisine information
* calorie estimates

Using a standard recipe representation also helps keep future integrations from becoming tightly coupled to one recipe-management application.

## Future Work

Potential Mealie integration work includes:

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

These features should remain optional.

AI Meal Planner must continue to work as a standalone prompt without requiring Mealie.

## Status

Current status:

```text
Schema.org Recipe export: supported
Manual Mealie import: supported
Direct Mealie API integration: planned
```
