
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
// Belt length = π/2 × (DL + DS) + 2L + (DL - DS)^2/(4L)

// DL is the diameter of the larger pulley (here 20 inches);
// DS is the diameter of the smaller pulley (here 6 inches); and
// L is the distance between the center of the pulleys.

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
cross_pin_d = 1.3;

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
        if (pin_slot) cube([cross_pin_d, pin_x, 100], center=true);
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

module arm_1_lasercut_whole(arm_width=10)
{
    projection()
    {
        difference()
        {
            union()
            {
                // The centre end of the arm, glued to the drive pulley
                cylinder(r=shaft_1_drive_pulley_dia/2+wt, h = 10);
                // The length of the arm
                translate([arm1_axis_offset/2,0,5]) cube([arm1_axis_offset, arm_width, 10], center=true);
                // The bearing holder at the far end of arm1
                translate([arm1_axis_offset,0,0]) cylinder(r=shaft_1_drive_pulley_dia/2+wt, h = 10);

            }
            cylinder(r=608_od/2-laser_kerf, h = 10);
            translate([arm1_axis_offset,0,0]) cylinder(r=608_od/2-laser_kerf, h = 10);
        }

    }
}

arm_1_adjustment_range = 2;
arm_1_adjustment_slot_length = arm_1_adjustment_range*3;
arm_1_adjustment_slot_r = 1.5;
arm_1_lasercut_width = 608_od;

module arm_1_adjustment_cutouts()
{
    translate([arm_1_adjustment_slot_length/2+arm_1_adjustment_slot_r+arm_1_adjustment_range/2+wt,0,50]) cube([arm_1_adjustment_range, arm_1_lasercut_width, 100],center=true);
    hull()
    {
        translate([-arm_1_adjustment_slot_length/2,0,0]) cylinder(r=arm_1_adjustment_slot_r, h=100);
        translate([arm_1_adjustment_slot_length/2,0,0]) cylinder(r=arm_1_adjustment_slot_r, h=100);
    }
}
// !arm_1_adjustment_cutouts();
module arm_1_lasercut_adjustable()
{
    projection() difference()
    {
        linear_extrude(layer_thickness_nominal) arm_1_lasercut_whole(arm_1_lasercut_width);
        translate([arm1_axis_offset/2,0,-50]) arm_1_adjustment_cutouts();
    }
}
!arm_1_lasercut_adjustable();

// This is a bad idea, I think.
flexure_slot_x = 0.5;
// The flexure slot stops at least this far short of an edge;
flexure_min_y = 4;
flexure_slot_spacing = 2;

module arm_1_lasercut_flexure()
{
    arm_width = (shaft_1_drive_pulley_dia/2+wt)*2;
    projection() difference()
    {
        linear_extrude(layer_thickness_nominal) arm_1_lasercut_whole(arm_width);
        for (i = [shaft_1_drive_pulley_dia/2+wt:flexure_slot_spacing*2:arm1_axis_offset-shaft_1_drive_pulley_dia/2+wt-flexure_slot_spacing])
        {
            translate([i,0,0]) cube([flexure_slot_x, arm_width-2*flexure_min_y, 100],center=true);
        }
        for (i = [shaft_1_drive_pulley_dia/2+wt+flexure_slot_spacing:flexure_slot_spacing*2:arm1_axis_offset-shaft_1_drive_pulley_dia/2+wt-flexure_slot_spacing])
        {
            translate([i,flexure_min_y+(arm_width-2*flexure_min_y)/2,0]) cube([flexure_slot_x, arm_width-2*flexure_min_y, 100],center=true);
            translate([i,-flexure_min_y-(arm_width-2*flexure_min_y)/2,0]) cube([flexure_slot_x, arm_width-2*flexure_min_y, 100],center=true);
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
// This will depend on the belts connected to the stepper shafts.
stepper_separation_x = 13.5;
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
    linear_extrude(layer_thickness_nominal) base_lasercut(); // x2
    translate([0,-n17_xy/2-base_guide_edge/2,base_guide_z/2]) linear_extrude(layer_thickness_nominal) base_guide_lasercut(); // x2
    translate([0,n17_xy/2+base_guide_edge/2,base_guide_z/2]) rotate([0,0,180]) linear_extrude(layer_thickness_nominal) base_guide_lasercut(); // x2
}

module lasercut_assembled()
{
    washer_z = 1;
    translate([0,0,layer_thickness_nominal]) rotate([180,0,0]) linear_extrude(layer_thickness_nominal) top_holder_lasercut();
    translate([0,0,layer_thickness_nominal]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(true); // x2
    translate([0,0,layer_thickness_nominal*2]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(false); // x2
    translate([0,0,washer_z+layer_thickness_nominal*3]) linear_extrude(layer_thickness_nominal) arm_1_pulley_lasercut(); // x2
    translate([0,0,washer_z+layer_thickness_nominal*4]) linear_extrude(layer_thickness_nominal) arm_1_pulley_lasercut(); // x2
    translate([arm1_axis_offset,0,0]) rotate([0,0,180]) translate([0,0,washer_z+layer_thickness_nominal*5]) linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(); // x2
    translate([0,0,washer_z+layer_thickness_nominal*6]) linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(); // x2
    translate([arm1_axis_offset,0,0]) rotate([0,0,180]) translate([0,0,washer_z+layer_thickness_nominal*7]) linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(); // x2
    translate([0,0,washer_z+layer_thickness_nominal*8]) linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(); // x2
    translate([0,0,washer_z*2+layer_thickness_nominal*9]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(true); // x2
    translate([0,0,washer_z*2+layer_thickness_nominal*10]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(false); // x2
    translate([arm1_axis_offset,0,washer_z*2+layer_thickness_nominal*9]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(true); // x2
    translate([arm1_axis_offset,0,washer_z*2+layer_thickness_nominal*10]) linear_extrude(layer_thickness_nominal) shaft_1_drive_pulley_lasercut(false); // x2
    translate([arm1_axis_offset,0,washer_z*2+layer_thickness_nominal*11]) linear_extrude(layer_thickness_nominal) rotate([0,0,160]) arm_2_lasercut();
}

module belt_splitter()
{
    // This is a little jig for splitting 6mm wide timing belts into 2x3mm belts.
    blade_x = 0.4;
    blade_y = 9.14;
    belt_x = 6;
    extra_x = 10;
    extra_y_before_blade = 8;
    extra_y_after_blade = 5;
    total_x = belt_x+extra_x*2;
    difference()
    {
        cube([total_x, blade_y+extra_y_before_blade+extra_y_after_blade, 3*layer_thickness_nominal]);

        union()
        {
            translate([-belt_x/2+(total_x/2),0,layer_thickness_nominal]) cube([belt_x, extra_y_before_blade, layer_thickness_nominal]);
            translate([-(belt_x+blade_x)/2+(total_x/2),extra_y_before_blade,layer_thickness_nominal]) cube([belt_x+blade_x, blade_y+extra_y_after_blade, layer_thickness_nominal]);
            translate([total_x/2,extra_y_before_blade,-50]) cube([blade_x, blade_y, 100]);
        }
    }
}
module belt_splitter_lasercut(layer)
{
    projection(cut=true) translate([0,0,-layer*layer_thickness_nominal]) belt_splitter();
}

enc_lt = layer_thickness_nominal;
// Increase this to 128 for the final render.
enclosure_facets = 256;
enc_wt = 8;
// These are all layer counts
enc_base_l = 2;
// Extra space around the stepper motor mechanism for cables and whatnot.
enc_base_extra_r = 10;
enc_base_wt = enc_wt;
enc_base_ir = sqrt(pow(base_x, 2)+pow(base_y,2))/2+enc_base_extra_r;
// This is the distance from the top of the enc_base to the bottom of the
// platform under the bed. It's the height of the vertical walls enclosing
// the stepper motors.
enc_mechanism_z_desired = 60;
enc_mechanism_z_layers = ceil(enc_mechanism_z_desired/layer_thickness_nominal);
enc_mechanism_z = enc_mechanism_z_layers*layer_thickness_nominal;
echo("Cut ", enc_mechanism_z_layers*3, " pieces of enc_little_ring_third");

// This is the number of vertical alignment pins used to join segements
// of the enclosure rings together for the glue-up.
enc_ring_pin_n = 6;
enc_arms_z_desired = 30;
enc_arms_z_layers = ceil(enc_arms_z_desired/layer_thickness_nominal);
enc_arms_z = enc_arms_z_layers*layer_thickness_nominal;
echo("Cut ", enc_arms_z_layers*3, " pieces of enc_big_ring_third");


enc_bed_r = arm1_axis_offset*2;

module alignment_pins(rad, count=enc_ring_pin_n)
{

    for (i = [0:360/count:360-360/count])
    {
        rotate([0,0,i]) translate([rad,0,0]) cylinder(r=pin_r, h=1000);
    }
}

// This is the base of the enclosure that sits on the table.
module enc_base()
{
    difference()
    {
        cylinder(r=enc_base_ir + enc_wt, h=enc_lt*2, $fn=enclosure_facets);
        translate([0,0,enc_lt])cylinder(r=608_od/2,h=608_z);
        // Pins for aligning the little ring to the top of the base slices.
        translate([0,0,enc_lt]) alignment_pins(enc_base_ir + enc_base_wt/2);
    }
}

module enc_base_slice(n)
{
    projection(cut=true) translate([0,0,-(n+0.5)*enc_lt]) enc_base();
}

module enc_ring(od, id, height, pin_count=enc_ring_pin_n)
{
    difference()
    {
        cylinder(r=od/2,h=height, $fn=enclosure_facets);
        cylinder(r=id/2,h=1000, $fn=enclosure_facets);
        alignment_pins((id+(od-id)/2)/2, pin_count);
    }
}

// This part sits atop the base and forms the floor under the arms.
module enc_platform()
{
    difference()
    {
        cylinder(r=enc_bed_r + enc_base_wt,h=enc_lt*2, $fn=enclosure_facets);
        cylinder(r=enc_base_ir,h=608_z);
        // Pins for aligning the little ring to the top of the base slices.
        translate([0,0,enc_lt]) alignment_pins(enc_base_ir + enc_base_wt/2);
        translate([0,0,enc_lt]) alignment_pins(enc_bed_r + enc_base_wt/2, enc_ring_pin_n*2 );
    }
}

module enc_platform_slice(n)
{
    projection(cut=true) translate([0,0,-(n+0.5)*enc_lt]) enc_platform();
}

// This is the bit that encloses the bottom half of the mechanism, I.E. stepper motors and electronics.
module enc_little_ring()
{
    enc_ring((enc_base_ir + enc_base_wt)*2, enc_base_ir*2, enc_mechanism_z);
}

// This is the bit insides which the arms mode.
module enc_big_ring()
{
    enc_ring((enc_bed_r + enc_base_wt)*2, enc_bed_r*2, enc_arms_z, enc_ring_pin_n*2);
}

// This is a 120 degree arc of enc_little_ring()
module enc_little_ring_third()
{
    intersection()
    {
        rotate([0,0,30]) union()
        {
            cube([1000,1000,1000]);
            rotate([0,0,120-90]) cube([1000,1000,1000]);
        }
        enc_little_ring();
    }
}
// This is a 120 degree arc of enc_big_ring()
module enc_big_ring_third()
{
    intersection()
    {
        rotate([0,0,15]) union()
        {
            cube([1000,1000,1000]);
            rotate([0,0,120-90]) cube([1000,1000,1000]);
        }
        enc_big_ring();
    }
}

module enclosure_assembled()
{
    enc_base();
    translate([0,0,2*enc_lt]) base_lasercut_assembled();
    translate([0,0,2*enc_lt]) enc_little_ring();
    translate([0,0,2*enc_lt+enc_mechanism_z]) enc_platform();
    translate([0,0,4*enc_lt+enc_mechanism_z]) enc_big_ring();
}



batch_export = false;
part_revision_number = 1;
// These are load-bearing comments. The make script awks this file for
// lines between these markers to determine what it needs to render to a file.
// PARTSMARKERSTART
export_shaft_1_drive_pulley_slot = false; // 3
export_shaft_1_drive_pulley_noslot = false; // 3
export_top_holder_lasercut = false; // 2
export_arm_1_pulley_lasercut = false; // 2
export_arm_1_lasercut_adjustable = false; // 4
export_arm_2_lasercut = false; // 1
export_base_lasercut = false; // 2
export_base_guide_lasercut = false; // 4
export_belt_splitter_outer = false; // 2
export_belt_splitter_inner = false; // 1
export_enc_base_1 = false; // 1
export_enc_base_2 = false; // 1
export_enc_little_ring_third = false; // 60
export_enc_big_ring_third = false; // 30
export_enc_platform_1 = false; // 1
export_enc_platform_2 = false; // 1
// PARTSMARKEREND

if (batch_export) {
    if (export_shaft_1_drive_pulley_slot) shaft_1_drive_pulley_lasercut(true);
    if (export_shaft_1_drive_pulley_noslot) shaft_1_drive_pulley_lasercut(false);
    if (export_top_holder_lasercut) top_holder_lasercut();
    if (export_arm_1_pulley_lasercut) arm_1_pulley_lasercut();
    if (export_arm_1_lasercut_adjustable) arm_1_lasercut_adjustable();
    if (export_arm_2_lasercut) arm_2_lasercut();
    if (export_base_lasercut) base_lasercut();
    if (export_base_guide_lasercut) base_guide_lasercut();
    if (export_belt_splitter_outer) belt_splitter_lasercut(0);
    if (export_belt_splitter_inner) belt_splitter_lasercut(1);
    if (export_enc_base_1) enc_base_slice(0);
    if (export_enc_base_2) enc_base_slice(1);
    if (export_enc_little_ring_third) projection() enc_little_ring_third();
    if (export_enc_big_ring_third) projection() enc_big_ring_third();
    if (export_enc_platform_1) projection() enc_platform_slice(0);
    if (export_enc_platform_2) projection() enc_platform_slice(1);

} else {
    // lasercut_assembled();

    // linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(1);
    // translate([arm1_axis_offset,0,0]) rotate([0,0,180]) translate([0,0,layer_thickness_nominal]) linear_extrude(layer_thickness_nominal) arm_1_lasercut_adjustable(1);
    // shaft_1_drive_pulley_lasercut(true);
    enclosure_assembled();
    // enc_base_slice(0);
    // enc_big_ring_third();
    // arm_1_pulley_lasercut();
    // Lasercut design
    // shaft_1_drive_pulley_lasercut(true); // x2
    // shaft_1_drive_pulley_lasercut(false); // x5
    // top_holder_lasercut(); // x2
    // arm_1_pulley_lasercut(); // x2
    // arm_1_lasercut_whole(); // x3
    // arm_2_lasercut(); // x1
    // base_lasercut(); // x3
    // base_guide_lasercut(); // x4
    // base_lasercut_assembled(); // x3
    // big_ring();
    // arm_1_lasercut_whole(); // x2
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
}

