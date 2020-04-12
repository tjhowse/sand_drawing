
include <Pulley_T-MXL-XL-HTD-GT2_N-tooth.scad>

id_fudge = 0.2;
608_z = 7;
608_id = 8;
608_od = 22+id_fudge;
$fn=50;
stepper_slot = 3;
wt = 3;


n17_hole_spacing = 31;
n17_hole_dia = 3+id_fudge;
n17_center_hole_dia = 22+id_fudge;
n17_xy = 42.5;
n17_pulley_d = 12.25;
n17_pulley_z = 10.7;
n17_pulley_z_offset = 6.8;
n17_belt_guide_z = 1.7;

stepper_1_offset = 608_id/2+n17_xy/2+stepper_slot/2;
stepper_2_offset = stepper_1_offset;

bearing_retain_lip = 0.5;

holder_z = 608_z+bearing_retain_lip;
holder_x = stepper_1_offset + stepper_2_offset + n17_hole_spacing + n17_hole_dia + 2*wt + stepper_slot;
holder_y = n17_hole_spacing + n17_hole_dia + 2*wt;

belt_z = 4.5;
belt2_z = 6;

shaft_1_drive_pulley_dia = 27;
shaft_1_drive_pulley_z_top_belt_guide = 0.5;
shaft_1_drive_pulley_z_bottom_belt_guide = 0;
shaft_1_drive_pulley_z = belt_z+shaft_1_drive_pulley_z_top_belt_guide + shaft_1_drive_pulley_z_bottom_belt_guide;

shaft_2_drive_pulley_z_top_belt_guide = 0.5;
shaft_2_drive_pulley_z_bottom_belt_guide = 0.5;
// Some extra z height to encapsulate the bearings.
shaft_2_drive_pulley_z_extra_z = 1.3;

shaft_2_drive_pulley_z = belt_z+belt2_z+shaft_2_drive_pulley_z_top_belt_guide+shaft_2_drive_pulley_z_bottom_belt_guide+n17_belt_guide_z+shaft_2_drive_pulley_z_extra_z;
washer_z = 1.5;
washer_d = 18.8;

module n17_holes(slot = 0)
{
    translate([-slot/2,0,0])
    {
        hull()
        {
            cylinder(r=n17_center_hole_dia/2,h=100);
            translate([slot,0,0]) cylinder(r=n17_center_hole_dia/2,h=100);
        }
        hull()
        {
            translate([-n17_hole_spacing/2,-n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
            translate([-n17_hole_spacing/2+slot,-n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
        }
        hull()
        {
            translate([-n17_hole_spacing/2,n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
            translate([-n17_hole_spacing/2+slot,n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
        }
        hull()
        {
            translate([n17_hole_spacing/2,-n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
            translate([n17_hole_spacing/2+slot,-n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
        }
        hull()
        {
            translate([n17_hole_spacing/2,n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
            translate([n17_hole_spacing/2+slot,n17_hole_spacing/2,0]) cylinder(r=n17_hole_dia/2,h=100);
        }
    }
    translate([0,0,-n17_pulley_z+holder_z-n17_pulley_z_offset]) #cylinder(r=n17_pulley_d/2, h=n17_pulley_z);
    translate([0,0,-n17_pulley_z+holder_z-n17_pulley_z_offset-n17_belt_guide_z]) #cylinder(r=16/2, h=n17_belt_guide_z);
    // translate([-stepper_slot/2,0,0]) %cube([n17_xy, n17_xy,100], center =true);

}


module bearing(fill)
{
    difference()
    {
        cylinder(h = 608_z, r = 608_od/2);
        if (fill != 0) cylinder(h = 608_z, r = 608_id/2);
    }
}

module bearing_holder()
{
    difference()
    {
        cylinder(r=608_od/2+wt, h=608_z);
        bearing(1);
    }
}

// bearing(0);

module shaft_1_drive_pulley()
{
    difference()
    {
        translate([0,0,shaft_1_drive_pulley_z_top_belt_guide]) pulley ( "GT2 2mm" , GT2_2mm_pulley_dia , 0.764 , 1.494, belt_z, shaft_1_drive_pulley_z_bottom_belt_guide, shaft_1_drive_pulley_z_top_belt_guide);
        translate([0,0,shaft_1_drive_pulley_z/2])rotate([90,0,0]) translate([0,0,-50]) #cylinder(r=1,h=100);
    }
    %cylinder(r=shaft_1_drive_pulley_dia/2, h = shaft_1_drive_pulley_z);
}

module shaft_2_drive_pulley()
{
    difference()
    {
        translate([0,0,shaft_2_drive_pulley_z_bottom_belt_guide]) pulley ( "GT2 2mm" , GT2_2mm_pulley_dia , 0.764 , 1.494,belt_z+belt2_z+n17_belt_guide_z+shaft_2_drive_pulley_z_extra_z, shaft_2_drive_pulley_z_bottom_belt_guide, shaft_2_drive_pulley_z_top_belt_guide);
        translate([0,0,bearing_retain_lip]) cylinder(r=608_od/2,h=100);
        cylinder(r=(washer_d*1.1)/2,h=100);
    }
    // %cylinder(r=shaft_1_drive_pulley_dia/2, h = shaft_2_drive_pulley_z);
    // translate([0,0,bearing_retain_lip]) #bearing();
    // translate([0,0,bearing_retain_lip+608_z]) #bearing();
}

module top_holder()
{
    difference()
    {
        union()
        {
            translate([0,0,holder_z/2]) cube([holder_x, holder_y, holder_z], center = true);
            // cylinder(r=608_od/2+wt, h = 608_z+wt);
        }
        translate([stepper_1_offset,0,0]) n17_holes(stepper_slot);
        translate([-stepper_2_offset,0,0]) n17_holes(stepper_slot);
        translate([0,0,bearing_retain_lip]) bearing(0);
        cylinder(r=608_od/2-wt, h = 100);
        #cylinder(r=608_id/2, h = 100);
    }
    // bearing_holder();
    translate([0,0,-shaft_1_drive_pulley_z-washer_z+bearing_retain_lip]) shaft_1_drive_pulley();
    translate([0,0,-shaft_1_drive_pulley_z-shaft_2_drive_pulley_z-washer_z]) shaft_2_drive_pulley();
}
// echo (holder_z);
// top_holder();
shaft_2_drive_pulley();
// translate([0,0,-3]) %cube([100,30,4], center=true);
// translate([0,0,-9]) %cube([100,30,4], center=true);
// shaft_1_drive_pulley();