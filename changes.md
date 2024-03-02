# CQSpoolTerrain changelog

## Main wip

## 1.3.0
* Added SpoolLogoStack and example.

## 1.2.3
* Added ControlPlatformPrint
* Added example for ControlPlatformPrint and generated stl's
* Fixed ControlPlatform and ControlPlatformPrint not setting height for frame in make method.
* Fix bug where steelFrame was not taking y_height into account when placing corner joins.

## 1.2.2
* Hollowed out stairlift
* Fix stairs example
* Added a render flag to hollow out the stairs.
* Refactored SteelFrame to accomodate length and width correctly duplicating frame structure
* Added control platform alt example.
* Upped cqindustry version 0.1.1

## 1.2.1
* Spool added build_no_center() method to make the spool without the center hole cut out.
* Upgdated Cradle to use the spool build_no_center build method when generating it's cut spool.
* Added example spool_no_center.py
* Added example cradle_tall.py example
* Updated cradle example to pass in the spool as a parent on the make() call.

## 1.2.0
* Split SteelFrame class from ControlPlatform
* Changed Control platform constructor (__init__) method signature

## 1.1.0
* Upped cqindustry version to 0.1.0
* Removed local Base class and instead resolve Base from cadqueryhelper
* Fix ControlPlatform Example not respecting parameter changes.
* Refactor StairLift to use Stairs component
* Remove cradle print statement

## 1.0.0
* Refactored powerLine.py to pipe module, Created:
  * pipe.straight
  * pipe.curve
  * pipe.end
* Update pipe examples
* Updated cradle to use pipe module
* Added license blocks
* Updated README.md
* Added pipe.connector
* added initial pipe.hatch
* changed default chevron size on control platform
* Broke out industrial_stairs
* Added pipe.platform
* Update the cqindustry version to 0.0.8
  * Brings in newest features from cqdqueryhelper 0.1.6 and cqterrain 0.2.0
* Added hollow cut out option to pipe.straight
* pipe.curve added parameters.
* pipe.platform added parameters
* Added stairs component
  * Added example

## 0.0.5
* Added ladders to the powerStation.
* Added render flags.
* Added StairLift tiles.
* Updated dependencies requires cqindustry 0.0.7
* Added initial powerLine code. 
* Added powerline straight example.
* Added curved power lines and example.
* Added power lines end cap* Greebled the StairLift.
* PowerStation added Spefic build method for cladding.

## 0.0.4
* Made SpoolCladdingGreebled class.
* Made SpoolCladdingGreebledUnique class.
* Added examples.
* Added stls.

## 0.0.3
* Made SpoolCladding class.
* Integrated SpoolCladding into PowerStation class.

## 0.0.2
* Upped cqterrain verison 0.1.8
* Made PowerStation class.

## 0.0.1
* Added Initial Spool Mockup.
* Added Initial Cradle and example.
