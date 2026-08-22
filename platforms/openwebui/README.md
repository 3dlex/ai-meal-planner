# Open WebUI

Open WebUI is the first supported platform for AI Meal Planner.

The core meal-planning behavior is defined in:

```text
prompt/meal-planner.md
```

The files in this directory contain Open WebUI-specific packaging and usage guidance.

## Recommended Setup

AI Meal Planner works best when the contents of:

```text
prompt/meal-planner.md
```

are used as the system prompt for a dedicated Open WebUI model or prompt configuration.

The canonical prompt should remain the source of truth.

Platform-specific exports should be treated as convenience files rather than the authoritative copy of the prompt.

## Basic Installation

In Open WebUI:

1. Create a dedicated model or prompt configuration.
2. Select the language model you want to use.
3. Copy the contents of:

```text
prompt/meal-planner.md
```

into the system prompt field.
4. Save the configuration.
5. Start a new chat using that configuration.
6. Ask:

```text
Plan my dinners for next week.
```

The default configuration in the prompt will be used unless the request overrides it.

## Changing Defaults

Before installing the prompt, review the `Default Configuration` section near the top of:

```text
prompt/meal-planner.md
```

The default project configuration includes:

```text
Number of dinners: 7
Servings per dinner: 2
Maximum total cooking time per meal: 45 minutes
Location: Brodhead, Kentucky, USA
Seasonal ingredient preference: enabled
```

Change these values to suit your household.

See:

```text
docs/configuration.md
```

for more information.

## Example Requests

### Normal Weekly Plan

```text
Plan my dinners for next week.
```

### Different Serving Count

```text
Plan my dinners for next week for four people.
```

### Fewer Meals

```text
Plan five dinners this week.
```

### Additional Preferences

```text
Plan seven dinners this week.

Avoid pork and include at least two vegetarian meals.
```

### Mealie Export

After a meal plan has been generated:

```text
Export Wednesday's recipe for Mealie.
```

The model should return Schema.org Recipe JSON for the selected recipe.

See:

```text
docs/mealie-export.md
```

for the export format.

## Open WebUI Export File

This directory may also contain:

```text
meal-planner.json
```

This file is an Open WebUI export intended to make installation easier.

It may contain Open WebUI-specific metadata such as:

* model identifiers
* feature capabilities
* prompt configuration
* internal object metadata

Because those values may vary between Open WebUI installations and versions, the exported JSON is not the canonical definition of AI Meal Planner.

The canonical prompt remains:

```text
prompt/meal-planner.md
```

## Model Selection

AI Meal Planner does not require a specific language model.

Different models may vary in their ability to:

* follow the requested meal count
* preserve cooking-time limits
* consolidate grocery quantities accurately
* reuse ingredients intelligently
* follow Schema.org Recipe formatting
* return syntactically valid JSON

Models with stronger instruction-following and structured-output behavior will generally perform better.

Users should test the planner with the models available in their Open WebUI installation.

## Web Search

The core prompt does not require web search.

If web search is available, it may be useful for verifying current or location-specific information.

The planner should not claim that a particular ingredient is available at a specific grocery store unless that availability has actually been verified.

## Mealie Integration

The current Open WebUI workflow is:

```text
Open WebUI
    |
    | Generate meal plan
    v
AI Meal Planner
    |
    | Request Mealie export
    v
Schema.org Recipe JSON
    |
    | Manual import
    v
Mealie
```

Direct Mealie API integration is a future enhancement.

That functionality should be implemented separately from the core prompt.

## Updating the Prompt

When changes are made to:

```text
prompt/meal-planner.md
```

the Open WebUI configuration or exported JSON may also need to be updated.

The recommended workflow is:

1. Update the canonical prompt.
2. Test the change.
3. Update the Open WebUI configuration.
4. Re-export the Open WebUI configuration if needed.
5. Update examples or documentation affected by the change.
6. Record the change in `CHANGELOG.md`.

This prevents the Open WebUI export from becoming a separate, conflicting version of the prompt.
