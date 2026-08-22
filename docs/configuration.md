# Configuration

AI Meal Planner is designed to work with sensible defaults while allowing users to override those defaults in individual requests.

The default configuration is defined near the top of:

```text
prompt/meal-planner.md
```

## Default Settings

The initial project defaults are:

| Setting                        | Default                 |
| ------------------------------ | ----------------------- |
| Number of dinners              | 7                       |
| Servings per dinner            | 2                       |
| Maximum cooking time           | 45 minutes              |
| Location                       | Brodhead, Kentucky, USA |
| Seasonal ingredient preference | Enabled                 |

These values can be changed to match your household.

For example:

```text
Number of dinners: 5
Servings per dinner: 4
Maximum total cooking time per meal: 30 minutes
Location: Lexington, Kentucky, USA
Seasonal ingredient preference: enabled
```

## Changing Your Defaults

Edit the `Default Configuration` section in:

```text
prompt/meal-planner.md
```

For example:

```markdown
## Default Configuration

Use these defaults unless the user specifies otherwise:

* Number of dinners: 5
* Servings per dinner: 4
* Maximum total cooking time per meal: 30 minutes
* Location: Lexington, Kentucky, USA
* Seasonal ingredient preference: enabled
```

These defaults are intended to represent the user's normal household preferences.

They are not permanent restrictions.

## Per-Request Overrides

Users can override individual settings without changing the prompt.

Examples:

```text
Plan five dinners this week.
```

```text
We're feeding six people this weekend.
```

```text
Keep everything under 30 minutes.
```

```text
I'm staying in Nashville this week, so plan around ingredients I can reasonably find there.
```

```text
Don't worry about seasonal ingredients this week.
```

Only the settings mentioned by the user should be changed for that request.

All other configured defaults should remain in effect.

## Location

Location is used primarily to help the model make reasonable decisions about:

* seasonal produce
* ordinary grocery availability
* regional ingredient expectations

The location does not require exact geographic coordinates.

A city, state or province, and country is generally sufficient.

For example:

```text
Brodhead, Kentucky, USA
```

or:

```text
Toronto, Ontario, Canada
```

The planner must not claim that a particular ingredient is currently available at a specific store unless that availability has actually been verified.

## Seasonal Ingredients

When seasonal ingredient preference is enabled, the planner should favor produce that is reasonably appropriate for the current season and configured region.

Seasonality is a preference rather than a strict requirement.

It should not prevent the planner from using commonly available grocery-store produce when that produces a more practical meal.

To disable this behavior by default:

```text
Seasonal ingredient preference: disabled
```

The user can also disable it temporarily in an individual request.

## Number of Dinners

The default project configuration creates seven dinners.

This can be changed permanently in the configuration or temporarily in a request.

Examples:

```text
Plan three dinners.
```

```text
Plan meals Monday through Friday only.
```

The planner should adjust the grocery list and consistency checks to match the requested number of meals.

## Servings

Recipe quantities should be planned around the configured number of servings.

For example:

```text
Servings per dinner: 4
```

should result in ingredient quantities appropriate for approximately four servings.

A user can temporarily override this:

```text
Plan the week for two people, but make Friday's dinner serve six.
```

When individual meals use different serving counts, the grocery list should account for those quantities.

## Maximum Cooking Time

The default maximum cooking time applies to total elapsed time from beginning preparation to serving.

The default is:

```text
45 minutes
```

This can be changed globally or per request.

For example:

```text
Maximum total cooking time per meal: 30 minutes
```

Advance preparation should not be required to meet the configured cooking-time limit.

Optional prep-ahead work may still be suggested.

## Additional Preferences

Other preferences do not currently have dedicated configuration fields but can be included directly in a request.

Examples include:

* dietary restrictions
* ingredients to avoid
* preferred cuisines
* preferred proteins
* budget goals
* kitchen equipment
* leftover preferences
* vegetarian meal frequency
* spice level

Examples:

```text
Avoid pork.
```

```text
Include at least two vegetarian dinners.
```

```text
Use the slow cooker once this week.
```

```text
Keep the grocery list inexpensive.
```

These may become formal configuration options in a future version of AI Meal Planner.

## Platform-Specific Configuration

The core prompt is platform-independent.

Platform-specific installation or configuration should be documented separately.

For example, Open WebUI-specific instructions are located under:

```text
platforms/openwebui/
```

Future platforms can provide their own configuration documentation without changing the core meal-planning prompt.
