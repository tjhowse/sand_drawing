# Huh?

So you've been reading about all the benefits of this "mindfulness" thing and you want to give it a try.
You do some research and learn it requires "meditation", "introspection" and other kinds of tedious woo.
Who has time for that? It's {current_year} for christ's sake! Surely there's some turn-key solution to this problem already.

That's what this project is for. Outsource responsibility for an ordered mind to make more time for the important things, like hedonism.

# Oh

This project contains all you need to build your own sand drawing robot. Heavily inspired by the likes of [Sandsara](https://www.kickstarter.com/projects/edcano/sandsara) and [Sisyphus](https://sisyphus-industries.com/). It's a robot that moves a ball around in a bed of sand to draw cool patterns. The patterns can be updated via wifi, and it can cycle through them, you can create your own, etc, etc. This project is open source, cheap, and hopefully as easy as possible to build.

# Videos

[Playlist on Youtube.](https://www.youtube.com/playlist?list=PLT7ckgz8vcoY2YFqqQTA0kUofwehtqQul) Maybe worth watching.

# Build logs

For now the build logs are on [my wiki](https://wiki.tjhowse.com/doku.php?id=projects:sand_drawing:overview). Over time they'll morph into actual instructions and end up in this repo.

# Bill of materials

## Mechanical
| Item | Type | Count | Note |
| ---- | ---- | ----- | ---- |
| Printed parts | Various | 8? | Basic parts. Small and easy to print. |
| Stepper pulley | GT2-20, 12.35mm high | 2 | My steppers had pulleys from the factory. |
| Belt | S2M belt 120mm | 2 | S2M ≈ GT2. |
| Belt | S2M belt 278mm | 1 | |
| Shaft 1 | 8mm x 90mm | 1 | Mild steel is easier to cross-drill than stainless. |
| Shaft 2 | 8mm x 33mm | 1 | |
| Bearing | 608 | 6 | Cheap skate bearings are fine. |
| Washers | 8mm ID, 15.7mm OD | 5 | OD not critical, but it must not rub on outer race of bearings. |
| Washers | 3mm ID, 6.8mm OD | 12 | |
| Bolts | M3x12mm | 8 | I used all 20mm and cut them to length. |
| Bolts | M3x20mm | 2 | |
| Nylock nuts | M3 | 2 | Nylock not critical. |
| Pins | 2mm diameter | 5 | Roll pins would be best, I used nails. +1 extra for pinning shaft 1 into the bearings. |
| Magnets | 12mm diameter, 2mm high neodymium | 2 | Dimensions not critical. |
| Cable ties | 200mm x 4.6mm Nylon | 2 | Dimensions not critical. |

## Electrical
| Item | Type | Count | Note |
| ---- | ---- | ----- | ---- |
| Microcontroller | ESP-WROOM-32 | 1 | The brains |
| Stepper motor | NEMA-17 | 2 | The brawn |
| Stepper driver | Pololu pinout | 2 | A4988, DRV8825 or TMC2100 in [increasing order of preference](https://github.com/tjhowse/sand_drawing/issues/6) |
| PCB | Custom made | 1 | The design is [here](./pcb/sand_drawing). It's easier and cheaper to have one made than you might imagine.
| Optoswitch | ?? | 2 | Used for detecting arm position. Current design uses slotted optoswitches, but reflective might be better? Watch this space. |
| 12v PSU | ?? | 1 | A wall wart should be fine. |
| Other bits | ?? | ? | Voltage regulators, capacitors, etc. Watch this space. |

## Enclosure
| Item | Type | Count | Note |
| ---- | ---- | ----- | ---- |
| Base | Wooood? | 1 | Holds the steppers and circuitry. |
| Top | Wooood? | 1 | Any convex polygon should work. |
| Bed | Glass? | 1 | |
| Lid | Glass | 1 | |
| Sand | Sand | 31378908 | < 100 μm grains, dry.

# Communication
Currently the robot receives patterns via MQTT. Bluetooth should also be possible in the future.

# Pattern definition

There are currently two ways to design patterns for the robot.

## GCODEs

This is a sequence of coordinates that define the path of the ball, as well as changing modes and looping. The following GCODES are currently supported. GCODES are separated by a comma.

| Name | GCODE | Example | Description |
| ---- | ----- | ------- | ----------- |
| Home axis| G28 | `G28 X,G28 Y,` | Home either the X or Y axis. Any command that needs an absolute position reference will fail unless both axes have been homed first. |
| Move | G1 | `G1 X10 Y50 S100,` | Go to the X and Y coordinates specified at 100mm/s. Currently the [speed field is ignored](https://github.com/tjhowse/sand_drawing/issues/4). The G1 movement mode carefully tracks every step and should be perfectly accurate if your steppers do not slip. |
| Fast move | G0 |  `G0 X10 Y50 S100,` | Same as G1 however the step signal square wave is generated using PWM so some resolution is lost. At time of writing it is not well-supported. It's really fast though. |
| Coordinate mode | G16 | `G16 0,` | This setting is used to control the interpretation of the `X` and `Y` parameters in the G0 and G1 commands. `0`: Raw speed, `1`: Raw angle, `2`: Cartesian (Default), `3`: Polar (unimplemented) |
| Jump | J0 | `J0 3,` | This jumps to the specified line in the GCODE-defined pattern. Used for creating loops. |
| Absolute coordinate mode | G90 | `G92` | ([Unimplemented](https://github.com/tjhowse/sand_drawing/issues/11)) Puts the robot into absolute movement mode. Coordinates in G0/G1 commands are interpreted as absolute position references. (Default) |
| Relative coordinate mode | G91 | `G91` | ([Unimplemented](https://github.com/tjhowse/sand_drawing/issues/11)) Puts the robot into relative movement mode. Coordinates in G0/G1 commands are interpreted as movement vectors from the previous position. |

## Generators

You can define a pattern using a python generator function. [Examples here](./pub_gen.py). This is probably the best option for non-trivial patterns.

### Tread lightly
Keep the target hardware in mind when writing generators. It's very resource-constrained. Try to limit RAM usage, and think hard before `import`ing anything. There are some [helper functions](./generator_libs.py) and [constants](./constants.py) in-scope that you can use.