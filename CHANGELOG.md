# Changelog

All notable changes to AI Meal Planner will be documented in this file.

The format is based loosely on Keep a Changelog, with an emphasis on practical project history rather than strict release-process requirements.

## Unreleased

### Added

* Platform-independent canonical meal-planning prompt
* Configurable number of dinners
* Configurable serving count
* Configurable maximum cooking time
* Configurable location
* Configurable seasonal ingredient preference
* Consolidated grocery-list generation
* Ingredient reuse and waste-reduction guidance
* Weekly prep suggestions
* Final consistency checks
* Schema.org Recipe JSON export
* Single-recipe Mealie export support
* Multiple-recipe Mealie export support
* Dedicated `skills/mealie-recipe-export.md` selective Mealie export skill
* Explicit recipe-fidelity validation for Mealie exports
* Open WebUI platform documentation
* Cleaned Open WebUI export
* Configuration documentation
* Mealie export documentation
* Project roadmap
* Example weekly meal plan
* Example Mealie-compatible recipe JSON
* Mealie integration placeholder and future design notes
* Contribution guidelines
* Initial end-to-end Mealie import testing with generated Schema.org Recipe JSON
* Successful validation of the selective Mealie Recipe Export skill against a real Mealie installation

### Changed

* Refactored the original Open WebUI-specific meal planner into a platform-independent core prompt
* Moved household-specific behavior into configurable defaults
* Renamed the project to AI Meal Planner
* Renamed the Open WebUI model export to use the `ai-meal-planner` identifier
* Removed user-specific and runtime metadata from the public Open WebUI export
* Reframed Mealie as an optional integration rather than the primary user workflow
* Prioritized portable recipe, shopping-list, and meal-plan exports ahead of direct Mealie API integration
* Changed Mealie export behavior to an explicit, selective workflow rather than automatically exporting every generated recipe
* Separated Mealie recipe conversion from normal weekly meal-planning behavior

### Planned

* Direct Mealie API integration
* Additional user preferences
* Additional platform support
* Repeatable prompt testing
* Reuse of recipes already stored in Mealie
