
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

This board is designed with JLC PCB's SMD service in mind. Parts selection, BOM and whatnot
are set up for easy manufacture. You should only need to solder on the ESP-WROOM-32D and headers.
All the fiddly little SMD stuff can be done for you, quite cheaply.

If you regenerate the footprint position files you'll need to manually change the header line from:

Ref,Val,Package,PosX,PosY,Rot,Side
To:
Designator,Val,Package,Mid X,Mid Y,Rotation,Layer

as per https://support.jlcpcb.com/article/84-how-to-generate-the-bom-and-centroid-file-from-kicad

Odds are you'll need to change the rotation of U2 to 180 degrees, too. Be SUPER CAREFUL at EACH STEP
of the ordering process and you should be OK.

See also https://support.jlcpcb.com/article/84-how-to-generate-the-bom-and-centroid-file-from-kicad for
instructions on how to properly format the BOM spreadsheet for JLC PCB to ingest.

As of 2020-05-30 the price to have five of these boards made, with VREG, resistors, capacitors and diodes
populated was AUD$22.60. This included some discounts and whatnot. Express postage to Australia was AUD$28.03.