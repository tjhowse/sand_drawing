
# PCB Changelog

## v1.2
### Changes
* Fixing footprints for new vreg circuits
* Updated electronics BoM

## v1.1
### Changes
* Connected all stepper driver control pins to ESP
* Changed vreg circuit from an AMS1117-3.3 to an AP63203 with higher current capacity
* Add thermal relief to ESP32 ground pins for easier hand soldering

## v1.0
### Changes
Initial implementation

### Bugs
* Shouldn't use GPIO9 - it is used internally too.
* Pin 7 (IO35) is input-only, can't use that for A2D. - Done.
* Must pull SLP and RST on stepper drivers high. - Done.
* vreg too small, or wired wrong? Only outputs 2.7 Vout at 12 Vin - Done.
* Make sure opto inputs are on ADC-friendly pins. - Done
* Reduce width of ground tie on ESP for easier soldering. - Done.

# ESP-WROOM-32 notes

Minimal implementation on page 15:
https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32d_esp32-wroom-32u_datasheet_en.pdf
A minimal wiring demo:
https://www.youtube.com/watch?v=J10J_7Ap6Oo

# EMC2100 SilentStepStick

These things seem like a bit of a pain in the arse, TBH. I hope they're good.

FAQ:
https://learn.watterott.com/silentstepstick/faq/


# Manufacture

This board is designed for manufacture with PCBWay or JLC. Parts selection, BOM and whatnot are set up for easy manufacture. You should only need to solder on the ESP-WROOM-32D (if using JLC) and headers. All the fiddly little SMD stuff can be done for you, quite cheaply.

## PCBWay-specific notes

You should be able to order a PCB with all the SMD components, including the ESP32) with (this)[https://www.pcbway.com/project/shareproject/Sand_Drawing_Robot_control_board_344d0ab2.html] link. I get a 10% cut.

## JLC-specific notes

If you regenerate the footprint position files you'll need to manually change the header line from:
```
Ref,Val,Package,PosX,PosY,Rot,Side
```
To:
```
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer
```
as per https://support.jlcpcb.com/article/84-how-to-generate-the-bom-and-centroid-file-from-kicad

Odds are you'll need to change the rotation of U2 to 180 degrees, too. Be SUPER CAREFUL at EACH STEP
of the ordering process and you should be OK.

See also https://support.jlcpcb.com/article/84-how-to-generate-the-bom-and-centroid-file-from-kicad for
instructions on how to properly format the BOM spreadsheet for JLC PCB to ingest.

As of 2020-05-30 the price to have five of these boards made, with VREG, resistors, capacitors and diodes
populated was AUD$22.60. This included some discounts and whatnot. Express postage to Australia was AUD$28.03.