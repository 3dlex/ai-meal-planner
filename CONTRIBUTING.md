# Contributing

Contributions to AI Meal Planner are welcome.

The project is intentionally designed to keep the core meal-planning prompt simple while allowing platform support, integrations, documentation, examples, and testing to evolve separately.

## Ways to Contribute

Useful contributions include:

* testing the prompt with different language models
* reporting prompt-following problems
* improving meal-planning behavior
* improving Schema.org Recipe exports
* improving documentation
* adding examples
* improving Open WebUI support
* developing optional integrations
* identifying portability issues
* reporting bugs or inconsistencies

## Before Making Changes

Please review:

```text
README.md
```

and:

```text
docs/roadmap.md
```

before making major changes.

The roadmap describes the intended project boundaries and future direction.

## Core Prompt Changes

The canonical prompt is:

```text
prompt/meal-planner.md
```

Changes to meal-planning behavior should be made there first.

Examples include:

* meal-count behavior
* serving-count behavior
* cooking-time rules
* grocery-list behavior
* ingredient reuse
* meal variety
* Schema.org Recipe export behavior

Platform-specific copies should not become independent versions of the prompt.

If the canonical prompt changes, any platform-specific exports that embed it may also need to be regenerated or updated.

## Platform-Specific Changes

Platform-specific files belong under:

```text
platforms/
```

For example:

```text
platforms/openwebui/
```

Platform-specific behavior should not be added to the canonical prompt unless it is genuinely useful across platforms.

## Integration Changes

Optional integrations belong under:

```text
integrations/
```

For example:

```text
integrations/mealie/
```

Integrations should remain optional.

The core meal planner must continue to work without external services.

## Secrets and Private Information

Do not commit:

* API keys
* passwords
* access tokens
* private server URLs when they expose personal infrastructure
* user identifiers
* authentication headers
* private configuration files
* other sensitive information

Use environment variables, local configuration files, or another appropriate secrets-management mechanism for integrations.

If local configuration files are introduced, they should be excluded through `.gitignore`.

## Schema.org Recipe Export

Recipe export changes should preserve compatibility with Schema.org Recipe where practical.

The current export behavior is documented in:

```text
docs/mealie-export.md
```

Changes should avoid introducing custom fields when an appropriate Schema.org property already exists.

## Testing Prompt Changes

Because language-model output is nondeterministic, testing should focus on both structural requirements and overall behavior.

Useful checks include:

* requested number of meals is generated
* serving quantities are appropriate
* maximum cooking time is respected
* primary proteins are not repeated on consecutive nights
* meals have reasonable variety
* grocery-list ingredients match the recipes
* significant ingredients are reused where practical
* Mealie exports are valid JSON
* Schema.org property names are used correctly
* recipe times use ISO 8601 durations
* recipe instructions use ordered `HowToStep` objects

When reporting a prompt-related issue, it is helpful to include:

* model name
* platform
* user request
* relevant output
* expected behavior
* actual behavior

Do not include private credentials or sensitive information in issue reports.

## Documentation

Documentation should describe current behavior accurately.

Future or experimental functionality should be clearly identified as planned or experimental rather than presented as already supported.

## Pull Requests

Keep pull requests focused on one logical change where practical.

A useful pull request description should explain:

1. what changed
2. why the change is useful
3. whether the canonical prompt changed
4. whether examples or platform exports were updated
5. how the change was tested

## Changelog

User-visible changes should be recorded in:

```text
CHANGELOG.md
```

Examples include:

* prompt behavior changes
* new configuration options
* new platform support
* new integrations
* export-format changes
* important bug fixes

Small documentation corrections do not always require a changelog entry.

## Project Principles

Contributions should preserve these principles:

* keep the core prompt simple
* keep platform-specific behavior separate
* keep integrations optional
* keep secrets out of the repository
* prefer open standards where practical
* avoid unnecessary complexity
* document current behavior honestly

