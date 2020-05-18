Huh?
----

So you've been reading about all the benefits of this "mindfulness" thing and you want to give it a try.
You do some research (first three google results) and learn it requires "meditation", "introspection" and
other kinds of tedious woo.

Who has time for that? It's {current_year} for christ's sake! Surely there's some turn-key solution to this
problem already.

That's what this project is for. Outsource responsibility for an ordered mind to make more time for the important things, like hedonism.

Oh
--

This project contains all you need to build your own sand drawing robot. Heavily inspired by the likes of Sandsara and {that_other_one}.
It's a robot that moves a ball around in a bed of sand to draw cool patterns. The patterns can be updated via wifi, and it can cycle through
them, you can create your own, etc etc.

Build logs
----------

https://wiki.tjhowse.com/doku.php?id=projects:sand_drawing:overview


GCODEs
------

Accepted gcodes. See source for details on valid numbers.

Move X or Y axes:
G1 X# Y#
G1 X#
G1 Y#

Home X or Y axis:
G28 X
G28 Y

Set coordinate mode:
G15 #

Set movement mode:
G16 #