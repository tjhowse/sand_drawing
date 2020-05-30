# Huh?

So you've been reading about all the benefits of this "mindfulness" thing and you want to give it a try.
You do some research and learn it requires "meditation", "introspection" and other kinds of tedious woo.
Who has time for that? It's {current_year} for christ's sake! I don't want a tiny tray of rocks and sand
on my desk to rake around. Surely there's some turn-key solution to this problem already.

That's what this project is for. Outsource responsibility for an ordered mind to make more time for the important things, like computer games. And croissants.

# Oh

This project (will contain/contains) all the knowledge you will need to build your own sand drawing robot. Heavily inspired by the likes of [Sandsara](https://www.kickstarter.com/projects/edcano/sandsara) and [Sisyphus](https://sisyphus-industries.com/). It's a robot that moves a ball around in a bed of sand to draw cool patterns. The patterns can be updated via wifi, and it can cycle through them, you can create your own, etc, etc. This project is open source, cheap, and hopefully as easy as possible to build.

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
| Microcontroller | ESP-WROOM-32D | 1 | Wifi and bluetooth built-in |
| Stepper motor | NEMA-17 | 2 | 200 steps/revolution, around 40mm long, at least 30 N.cm of holding torque. It's not critical, really. |
| Stepper driver | Pololu pinout | 2 | A4988, DRV8825 or TMC2100 in [increasing order of preference](https://github.com/tjhowse/sand_drawing/issues/6) |
| PCB | Custom made | 1 | The design is [here](./pcb/sand_drawing). It's easier and cheaper to have one made than you [might imagine](./pcb/sand_drawing/README_PCB.md).
| Optoswitch | ?? | 2 | Used for detecting arm position. Current design uses slotted optoswitches, but reflective might be better? Watch this space. |
| PSU | 12v DC 1A | 1 | A wall wart should be fine. |
| Stepper driver socket | 16x1 2.54mm female | 2 | https://au.rs-online.com/web/p/pcb-sockets/2304893/ |
| Stepper motor socket | 4x1 3.5mm | 2 | https://au.rs-online.com/web/p/pcb-headers/8971039/ |
| Stepper motor plug | 4x1 3.5mm | 2 | https://au.rs-online.com/web/p/pcb-terminal-blocks/8971004/ |
| Optoswitch socket | 3x1 3.5mm | 2 | https://au.rs-online.com/web/p/pcb-headers/8971020/ |
| Optoswitch plug | 3x1 3.5mm | 2 | https://au.rs-online.com/web/p/pcb-terminal-blocks/8971001/ |
| Power socket | 2x1 3.5mm | 1 | https://au.rs-online.com/web/p/pcb-headers/8971026/ |
| Power plug | 2x1 3.5mm | 1 | https://au.rs-online.com/web/p/pcb-terminal-blocks/8970998/ |
| Buttons | 6mm | 2 | https://au.rs-online.com/web/p/tactile-switches/1359534/ |
| UART Header | 3x1 2.54mm male | 1 | https://au.rs-online.com/web/p/pcb-headers/8967364/ |

## Enclosure
| Item | Type | Count | Note |
| ---- | ---- | ----- | ---- |
| Base | Wooood? | 1 | Holds the steppers and circuitry. |
| Top | Wooood? | 1 | Any convex polygon should work. |
| Bed | Glass? | 1 | |
| Lid | Glass | 1 | |
| Sand | Sand | 31378908 | < 100 μm grains, dry.

# Communication
The ESP-WROOM-32 has wifi and BLE built in. Currently the robot connects to a wifi network, then an MQTT server, to receive commands. Bluetooth should also be possible in the future.

## MQTT Topics
There are a few topics that the robot listens to. Each topic starts with `{secrets.mqtt_root}/sand_drawing/`. I suggest you publish patterns/generators with the retain bit so the robot starts up and then begins that pattern.
| Topic | Example payload | Description |
| ----  | ------- | ----------- |
| `pattern` | `G28 X,G28 Y,G1 X0 Y175,G1 X123 Y123,G1 X175 Y0,J0 2` | Starts drawing the pattern defined by the GCODE in the payload. |
| `generator` | [Here](./pub_gen.py#L82) | Starts drawing the pattern defined by the generator in the payload. See below for details on generators. |
| `save_generator` | `1.pat {generator string}` | Saves the generator to a file in the robot's flash storage. The file extension must be `.pat`. A blank string will erase the generator. |
| `run_generator` | `1.pat` | Starts drawing the previously saved generators. |
| `delete_generator` | `1.pat` | Deletes a generator saved to the robot. |
| `list_generators` | N/A | Publishes a list of filenames to `generator_list` topic. |
| `shuffle_generators` | `3600` | Randomly picks a saved generator and starts drawing it. Optionally provide a number of seconds before choosing another random generator |

# Configuration
There are some files you'll need to edit before your robot will work for you, probably.
[#TODO populate this section.](https://github.com/tjhowse/sand_drawing/issues/13)

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
| Absolute coordinate mode | G90 | `G90` | Puts the robot into absolute movement mode. Coordinates in G0/G1 commands are interpreted as absolute position references. (Default) |
| Relative coordinate mode | G91 | `G91` | Puts the robot into relative movement mode. Coordinates in G0/G1 commands are interpreted as movement vectors from the previous position. |

## Generators
You can define a pattern using a python generator function. [Examples here](./pub_gen.py). This is probably the best option for non-trivial patterns.

### Tread lightly
Keep the target hardware in mind when writing generators. It's very resource-constrained. Try to limit RAM usage, and think hard before `import`ing anything. There are some [helper functions](./generator_libs.py) and [constants](./constants.py) in-scope that you can use.