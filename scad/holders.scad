
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
n17_xy = 42;
n17_z = 37.5;
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
belt2_z = 6.5;

shaft_1_drive_pulley_dia = 27;
shaft_1_drive_pulley_z_top_belt_guide = 0.5;
shaft_1_drive_pulley_z_bottom_belt_guide = 0.5;
shaft_1_drive_pulley_z = belt_z+shaft_1_drive_pulley_z_top_belt_guide + shaft_1_drive_pulley_z_bottom_belt_guide;

shaft_2_drive_pulley_z_top_belt_guide = 0.5;
shaft_2_drive_pulley_z_bottom_belt_guide = 0.5;
// Some extra z height to encapsulate the bearings.
shaft_2_drive_pulley_z_extra_z = 1.3;

shaft_2_driven_pulley_z_top_belt_guide = 1;
shaft_2_driven_pulley_z_bottom_belt_guide = 1;
shaft_2_driven_pulley_z = belt2_z + shaft_2_driven_pulley_z_top_belt_guide + shaft_2_driven_pulley_z_bottom_belt_guide;

shaft_2_drive_pulley_z = belt_z+belt2_z+shaft_2_drive_pulley_z_top_belt_guide+shaft_2_drive_pulley_z_bottom_belt_guide+n17_belt_guide_z+shaft_2_drive_pulley_z_extra_z;
washer_z = 1.3;
washer_d = 18.8;

// Slightly undersized for two 27mm pulleys and a 278mm belt, but the tensioner
// will let us expand it to perfection.
// https://www.omnicalculator.com/physics/belt-length
arm1_axis_offset = 95;
arm1_z = 608_z*2+bearing_retain_lip;
arm1_x = 2*wt+608_od+arm1_axis_offset+608_id;
arm1_y = 2*wt+608_od;

pin_r = 1;
pin_x = 20;


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


module bearing(fill, cut_kerf=0)
{
    difference()
    {
        cylinder(h = 608_z, r = 608_od/2-cut_kerf);
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

module shaft_1_drive_pulley(fast=false)
{
    if (!fast)
    {
        difference()
        {
            translate([0,0,shaft_1_drive_pulley_z_top_belt_guide]) pulley ( "GT2 2mm" , GT2_2mm_pulley_dia , 0.764 , 1.494, belt_z, shaft_1_drive_pulley_z_bottom_belt_guide, shaft_1_drive_pulley_z_top_belt_guide);
            translate([0,0,shaft_1_drive_pulley_z/2])rotate([90,0,0]) translate([0,0,-50]) cylinder(r=pin_r,h=100);
        }
    } else {
        cylinder(r=shaft_1_drive_pulley_dia/2, h = shaft_1_drive_pulley_z);
    }
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
module shaft_2_driven_pulley()
{
    difference()
    {
        translate([0,0,shaft_1_drive_pulley_z_top_belt_guide]) pulley ( "GT2 2mm" , GT2_2mm_pulley_dia , 0.764 , 1.494, belt2_z, shaft_2_driven_pulley_z_bottom_belt_guide, shaft_2_driven_pulley_z_top_belt_guide);
        translate([0,0,shaft_2_driven_pulley_z/2])rotate([90,0,0]) translate([0,0,-50]) #cylinder(r=pin_r,h=100);
    }
    %cylinder(r=shaft_1_drive_pulley_dia/2, h = shaft_2_driven_pulley_z);
}

module top_holder(bearing_cut_kerf=0)
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
        translate([0,0,bearing_retain_lip]) bearing(0, bearing_cut_kerf);
        cylinder(r=608_od/2-wt, h = 100);
        #cylinder(r=608_id/2, h = 100);
    }
    // bearing_holder();
    // translate([0,0,-shaft_1_drive_pulley_z-washer_z+bearing_retain_lip]) shaft_1_drive_pulley();
    // translate([0,0,-shaft_1_drive_pulley_z-shaft_2_drive_pulley_z-washer_z]) shaft_2_drive_pulley();
}

module arm1()
{
    // translate([0,0,arm1_z/2]) %cube([arm1_x, arm1_y, arm1_z], center=true);
    difference()
    {
        union()
        {
            translate([arm1_axis_offset/2,0,0]) cylinder(r=608_od/2+wt,h=arm1_z);
            hull()
            {
                translate([arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm1_z);
                translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm1_z);
            }
        }
        translate([arm1_axis_offset/2,0,bearing_retain_lip]) cylinder(r=608_od/2,h=2*608_z);
        translate([arm1_axis_offset/2,0,0]) cylinder(r=608_od/2-wt,h=arm1_z);
        translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2,h=arm1_z);
        translate([-arm1_axis_offset/2,0,arm1_z/2]) rotate([90,0,0]) translate([0,0,-50]) cylinder(r=pin_r,h=100);
    }
    translate([arm1_axis_offset/2+608_od/2+wt,0,0]) optoflag();
}
arm1_split_overlap = 30;
split_point_offset_from_centre = -30;
arm_slot_r = 1.5;
arm_slot_width = 3;
arm_slot_width_total = arm_slot_width + 2*arm_slot_r;

module slot(slot_r = arm_slot_r, slot_h = arm_slot_width)
{
    rotate([90,0,0]) translate([-slot_h/2,0,-50]) hull()
    {
        cylinder(r=slot_r, h=100);
        translate([slot_h,0,0]) cylinder(r=slot_r, h=100);
    }
}

module arm1_split_base()
{
    // This is arm1, but split into two parts for belt tensioning purposes.
    // Base
    translate([arm1_split_overlap,0,0]) difference()
    {
        translate([-arm1_split_overlap,0,0]) arm1();
        translate([0,-50,0]) cube([100,100,100]);
        translate([-arm1_split_overlap,-50,arm1_z/2]) cube([100,100,100]);
        rotate([90,0,0]) {
            translate([-arm_slot_width_total/2-wt, 0, 0]) slot();
            translate([split_point_offset_from_centre+arm_slot_width_total/2+wt+arm_slot_width_total/2, 0, 0]) slot();
        }
    }
}

module arm1_split_end()
{
    // This is arm1, but split into two parts for belt tensioning purposes.
    difference()
    {
        rotate([0,0,180]) arm1();
        translate([0,-50,0]) cube([100,100,100]);
        translate([-arm1_split_overlap,-50,arm1_z/2]) cube([100,100,100]);
        rotate([90,0,0]) {
            translate([-arm_slot_width_total/2-wt, 0, 0]) slot();
            translate([split_point_offset_from_centre+arm_slot_width_total/2+wt+arm_slot_width_total/2, 0, 0]) slot();
        }

        // translate([0,-50,0]) cube([100,100,100]);
        // translate([-arm1_split_overlap,0,0]) cube([100,100,100]);
        // translate([-arm_slot_width_total/2-wt, 0, arm1_z/2]) slot();
        // translate([split_point_offset_from_centre+arm_slot_width_total/2+wt+arm_slot_width_total/2, 0, arm1_z/2]) slot();
    }
}

bottom_holder_z = bearing_retain_lip+608_z+wt;

module bottom_hardware()
{
    union()
    {
        translate([0,0,bearing_retain_lip]) bearing(0);
        //hull()
        {
            translate([608_id/2+(n17_xy+stepper_slot)/2,0,608_z+n17_xy/2]) cube([n17_xy+stepper_slot,n17_xy,n17_xy], center=true);
            translate([-(608_id/2+(n17_xy+stepper_slot)/2),0,608_z+n17_xy/2]) cube([n17_xy+stepper_slot,n17_xy,n17_xy], center=true);
        }
        cylinder(r=608_od/2-wt, h=100);
    }
}

module bottom_bearing_holder()
{
    clampy_z = n17_xy/1.5+608_z;
    wedge_ratio = 1.5;
    stepper_gap = 12.5;
    difference()
    {
        union()
        {
            cylinder(r=608_od/2+wt, h = 608_z+bearing_retain_lip);
            translate([0,0,clampy_z/2]) cube([stepper_gap, n17_xy,clampy_z], center=true);
        }
        translate([0,0,bearing_retain_lip]) cylinder(r=608_od/2, h=100);
        cylinder(r=608_od/2-wt, h=100);
        // translate([0,n17_xy/2,50]) scale([1,wedge_ratio,1]) rotate([0,0,45]) cube([608_id/sqrt(2),608_id/sqrt(2),100], center=true);
        // translate([0,-n17_xy/2,50]) scale([1,wedge_ratio,1]) rotate([0,0,45]) cube([608_id/sqrt(2),608_id/sqrt(2),100], center=true);
    }
    echo(clampy_z);
}

arm2_hub_z = (wt+pin_r)*2;
arm2_z = wt*2/3;

module arm2()
{
    difference()
    {
        union()
        {
            hull()
            {
                translate([arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm2_z);
                translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm2_z);
            }
            translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm2_hub_z);
        }
        translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2,h=arm2_hub_z);
        translate([-arm1_axis_offset/2,0,arm2_hub_z/2]) rotate([0,-90,90]) translate([0,0,-15]) cylinder(r=pin_r,h=30);
    }
}


optoflag_x = 10;
optoflag_y = 5;
optoflag_z = 1;

module optoflag()
{
    hull()
    {
        cylinder(r=optoflag_y/2, h = optoflag_z);
        translate([optoflag_x-optoflag_y/2,0,0]) cylinder(r=optoflag_y/2, h = optoflag_z);
    }
}

optoholder_y = 15;
optoholder_gusset_z = optoholder_y/2;
optoholder_wt = 2;

// This is the distance between the optoswitch mounting surface and where the flag passes.
optoswitch_x = 4;
// This is the length of the optoswitch. The flag should pass through the centre of this volume
optoswitch_z = 15;
arm1_optoflag_holder_z = shaft_1_drive_pulley_z+washer_z-bearing_retain_lip+shaft_2_drive_pulley_z+washer_z+optoflag_z/2+optoswitch_z/2;
arm1_optoflag_holder_offset = arm1_axis_offset-holder_x/2+608_od/2+wt+optoholder_wt/2+optoflag_x + optoswitch_x;

arm2_optoflag_holder_z = shaft_1_drive_pulley_z+washer_z-bearing_retain_lip+shaft_2_drive_pulley_z+washer_z-optoflag_z/2+608_z*2+bearing_retain_lip+arm2_hub_z+optoswitch_z/2;

arm2_optoflag_holder_offset = arm1_axis_offset*2-holder_x/2+608_id/2+wt+optoholder_wt/2+optoflag_x + optoswitch_x;

optoholder_mounting_overlap = 2*wt+stepper_slot*2;
optoholder_x = arm2_optoflag_holder_offset+optoholder_mounting_overlap;

module optoswitch_holder()
{
    translate([optoholder_x/2-optoholder_mounting_overlap,0,optoholder_wt/2]) cube([optoholder_x,optoholder_y, optoholder_wt], center=true);
    translate([-optoholder_mounting_overlap, -optoholder_y/2,optoholder_gusset_z/2]) rotate([-90,0,0]) translate([optoholder_x/2,0,optoholder_wt/2]) cube([optoholder_x,optoholder_gusset_z, optoholder_wt], center=true);
    difference()
    {
        translate([-optoholder_mounting_overlap, 0 ,0]) cube([optoholder_mounting_overlap, holder_y/2, optoholder_wt]);
        translate([-stepper_slot-wt,holder_y/2-wt-arm_slot_r,0]) rotate([90,0,0]) slot();
    }

    translate([arm1_optoflag_holder_offset,0,arm1_optoflag_holder_z/2]) cube([optoholder_wt,optoholder_y, arm1_optoflag_holder_z], center=true);
    translate([arm2_optoflag_holder_offset,0,arm2_optoflag_holder_z/2]) cube([optoholder_wt,optoholder_y, arm2_optoflag_holder_z], center=true);

    lip_z = holder_z;
    translate([0,-optoholder_y/2,-lip_z+optoholder_wt]) cube([optoholder_wt,optoholder_y/2+holder_y/2, lip_z]);
}

optoarm_x = arm1_axis_offset*(2/3);
optoarm_y = 10;
optoarm_z = wt*2;

module arm2optoarm()
{
    // This part must be glued onto arm2 because the orientation makes these two parts hard to
    // print without loads of support material.
    difference()
    {
        union()
        {
            cylinder(r=608_id/2+wt*2, h=wt*2);
            hull()
            {
                cylinder(r=optoarm_y/2, h=wt);
                translate([optoarm_x-optoarm_y/2,0,0]) cylinder(r=optoarm_y/2, h=wt);
            }
            translate([optoarm_x,0,0]) optoflag();
        }
        cylinder(r=608_id/2+wt, h=100);
        translate([-100,-50,-50]) cube([100,100,100]);
    }

}

module assembled()
{
    rotate([180,0,0]) top_holder();
    shaft_1_drive_pulley();
    // This arm was only used for benchtesting the system. It is not required in the final
    // device, as the optoswitches are mounted directly to the table.
    // color("red") translate([holder_x/2,0,0]) optoswitch_holder();
    translate([0,0,shaft_1_drive_pulley_z+washer_z-bearing_retain_lip])
    {
        shaft_2_drive_pulley();
        translate([arm1_axis_offset/2,0,shaft_2_drive_pulley_z+washer_z])
        {
            // arm1();
            translate([0,0,arm1_z]) rotate([180,0,0]) arm1_split_base();
            rotate([0,0,180]) arm1_split_end();
            translate([arm1_axis_offset/2,0,-shaft_2_driven_pulley_z-washer_z]) shaft_2_driven_pulley();
            translate([arm1_axis_offset,0,arm1_z+arm2_hub_z]) rotate([180,0,0])
            {
                arm2();
                translate([-arm1_axis_offset/2,0,arm2_hub_z]) rotate([180,0,180]) arm2optoarm();
            }
        }
    }
}


laser_kerf = 0.15;
alignment_pin_offset = (2/3)*shaft_1_drive_pulley_dia;

// We'll need two of these.
module top_holder_lasercut()
{
    projection(cut=true) translate([0,0,-1]) top_holder(laser_kerf);
}

// We'll need two of these with the pin slot and two without.
module shaft_1_drive_pulley_lasercut(pin_slot=false)
{
    projection(cut=true) difference ()
    {
        union()
        {
            translate([0,0,-1]) shaft_1_drive_pulley();
            // Add a disc in the centre that fills up the original shaft hole
            cylinder(r=5, h=10);
        }
        // Add the shaft back in.
        // Kerf/2 because smaller holes need less of a kerf (?!?)
        cylinder(r=608_id/2-laser_kerf/2, h=100);
        // Add a slot in the middle for a pin that fixes the pulley to the shaft
        if (pin_slot) cube([pin_r, pin_x, 100], center=true);
        // Add a pair of vertical alignment holes that can be used to clock
        // the pulleys together during the glue-up.
        translate([-alignment_pin_offset/2,0,-50]) cylinder(r=pin_r, h=100);
        translate([alignment_pin_offset/2,0,-50]) cylinder(r=pin_r, h=100);

    }
}


module arm_1_pulley_lasercut()
{
    projection(cut=true) difference()
    {
        translate([0,0,-1]) shaft_1_drive_pulley();
        cylinder(r=608_od/2-laser_kerf,h=10);
    }
}

module arm_1_lasercut()
{
    projection()
    {
        difference()
        {
            union()
            {
                // The centre end of the arm, glued to the drive pulley
                cylinder(r=shaft_1_drive_pulley_dia/2, h = 10);
                // The length of the arm
                translate([arm1_axis_offset/2,0,5]) cube([arm1_axis_offset, 10, 10], center=true);
                // The bearing holder at the far end of arm1
                translate([arm1_axis_offset,0,0]) cylinder(r=shaft_1_drive_pulley_dia/2, h = 10);

            }
            cylinder(r=608_od/2-laser_kerf, h = 10);
            translate([arm1_axis_offset,0,0]) cylinder(r=608_od/2-laser_kerf, h = 10);
        }

    }
}

module arm_2_lasercut()
{
    projection(cut=true) difference ()
    {
        union()
        {
            hull()
            {
                cylinder(r=5, h = 10);
                translate([arm1_axis_offset,0,0]) cylinder(r=5, h = 10);
            }
            cylinder(r=shaft_1_drive_pulley_dia/2, h=10);
        }
        translate([-alignment_pin_offset/2,0,-50]) cylinder(r=pin_r, h=100);
        translate([alignment_pin_offset/2,0,-50]) cylinder(r=pin_r, h=100);
        cylinder(r=608_id/2-laser_kerf/2,h=10);
    }
}

base_x = 100;
base_y = 60;
layer_thickness_nominal = 3;
base_layers = 3;
base_guide_layers = 2;
base_guide_edge = (base_y-n17_xy)/2;
base_guide_z = base_guide_layers*layer_thickness_nominal;
base_z = base_layers*layer_thickness_nominal;
stepper_separation_x = 11;
stepper_separation_y = (base_y-608_od)/2;


// This part sits under the steppers.
module base_lasercut()
{
    projection() difference()
    {
        translate([0,0,base_z]) cube([base_x, base_y, base_z], center=true);
        cylinder(r=608_od/2-laser_kerf, h = 100);
        translate([-(base_x/2-10),-(base_y/2-base_guide_edge/2),0]) cylinder(r=pin_r, h = 100);
        translate([(base_x/2-10),-(base_y/2-base_guide_edge/2),0]) cylinder(r=pin_r, h = 100);
        translate([-(base_x/2-10),(base_y/2-base_guide_edge/2),0]) cylinder(r=pin_r, h = 100);
        translate([(base_x/2-10),(base_y/2-base_guide_edge/2),0]) cylinder(r=pin_r, h = 100);
    }

}

// These are glued on the base to stop the steppers twisting
// or getting too close.
module base_guide_lasercut()
{
    projection() difference ()
    {
        union()
        {
            cube([base_x, base_guide_edge, base_guide_z], center=true);
            translate([-stepper_separation_x/2,+base_guide_edge/2,-base_guide_z/2]) cube([stepper_separation_x, stepper_separation_y-base_guide_edge, base_guide_z]);
        }
        translate([-(base_x/2-10),0,-50]) cylinder(r=pin_r, h = 100);
        translate([(base_x/2-10),0,-50]) cylinder(r=pin_r, h = 100);
    }
}

module base_lasercut_assembled()
{
    translate([0,0,-0]) base_lasercut(); // x3
    translate([0,-n17_xy/2-base_guide_edge/2,base_guide_z/2]) base_guide_lasercut(); // x3
    translate([0,n17_xy/2+base_guide_edge/2,base_guide_z/2]) rotate([0,0,180]) base_guide_lasercut(); // x3
}

ring_wt = 10;


module big_ring()
{
    difference()
    {
        cylinder(r=ring_wt+arm1_x*2, h = 50, $fn=120);
        cylinder(r=arm1_x*2, h = 50, $fn=120);
    }
}

// Lasercut design
// shaft_1_drive_pulley_lasercut(true); // x2
// shaft_1_drive_pulley_lasercut(false); // x5
top_holder_lasercut(); // x2

// .. TODO incorporate laser kerf into top holder bearing hole
// arm_1_pulley_lasercut(); // x2
// arm_1_lasercut(); // x3
// arm_2_lasercut(); // x1
// base_lasercut(); // x3
// base_guide_lasercut(); // x4
// base_lasercut_assembled(); // x3
// big_ring();
// arm_1_lasercut(); // x2
// arm_2_lasercut(); // x1

// shaft_1_drive_pulley();

// top_holder();
// echo(holder_z);
// ball_skid();

// arm2optoarm();
// translate([0,-60,0]) assembled();
// rotate([90,0,0]) optoswitch_holder();

// optoflag();
// translate([0,30,0]) arm2();
// arm1();
// arm2();

// %bottom_hardware();
// bottom_bearing_holder();

// bottom_holder();

// echo (holder_z);
// top_holder();
// shaft_2_drive_pulley();
// translate([0,0,-3]) %cube([100,30,4], center=true);
// translate([0,0,-9]) %cube([100,30,4], center=true);
// shaft_1_drive_pulley();
// translate([0,30,0]) arm1();
// translate([-arm_slot_width_total,-5,0]) arm1_split_base();
// #arm1();

// translate([0,0,arm1_z]) rotate([180,0,0]) arm1_split_base();
// rotate([0,0,180]) arm1_split_end();
// translate([0,-20,0]) arm1_split_base();
// rotate([0,0,180]) arm1_split_end();
// shaft_2_driven_pulley();
// slot();

