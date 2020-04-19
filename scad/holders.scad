
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
        translate([0,0,shaft_1_drive_pulley_z/2])rotate([90,0,0]) translate([0,0,-50]) #cylinder(r=pin_r,h=100);
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
module shaft_2_driven_pulley()
{
    difference()
    {
        translate([0,0,shaft_1_drive_pulley_z_top_belt_guide]) pulley ( "GT2 2mm" , GT2_2mm_pulley_dia , 0.764 , 1.494, belt2_z, shaft_2_driven_pulley_z_bottom_belt_guide, shaft_2_driven_pulley_z_top_belt_guide);
        translate([0,0,shaft_2_driven_pulley_z/2])rotate([90,0,0]) translate([0,0,-50]) #cylinder(r=pin_r,h=100);
    }
    %cylinder(r=shaft_1_drive_pulley_dia/2, h = shaft_2_driven_pulley_z);
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

arm2_z = (wt+pin_r)*2;
module arm2()
{
    difference()
    {
        union()
        {
            hull()
            {
                translate([arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=wt);
                translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=wt);
            }
            translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2+wt,h=arm2_z);
        }
        translate([-arm1_axis_offset/2,0,0]) cylinder(r=608_id/2,h=arm2_z);
        translate([-arm1_axis_offset/2,0,arm2_z/2]) rotate([0,-90,90]) translate([0,0,-15]) cylinder(r=pin_r,h=30);
    }
    translate([arm1_axis_offset/2+608_id/2+wt,0,0]) optoflag();
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

arm2_optoflag_holder_z = shaft_1_drive_pulley_z+washer_z-bearing_retain_lip+shaft_2_drive_pulley_z+washer_z-optoflag_z/2+608_z*2+bearing_retain_lip+arm2_z+optoswitch_z/2;

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

module assembled()
{
    rotate([180,0,0]) top_holder();
    shaft_1_drive_pulley();
    color("red") translate([holder_x/2,0,0]) optoswitch_holder();
    translate([0,0,shaft_1_drive_pulley_z+washer_z-bearing_retain_lip])
    {
        shaft_2_drive_pulley();
        translate([arm1_axis_offset/2,0,shaft_2_drive_pulley_z+washer_z])
        {
            arm1();
            translate([arm1_axis_offset/2,0,-shaft_2_driven_pulley_z-washer_z]) shaft_2_driven_pulley();
            translate([arm1_axis_offset,0,arm1_z+arm2_z]) rotate([180,0,0]) arm2();
        }
    }
}

// translate([0,-60,0]) assembled();
// rotate([90,0,0]) optoswitch_holder();

// optoflag();
// translate([0,30,0]) arm2();
// arm1();

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
translate([0,-20,0]) arm1_split_base();
rotate([0,0,180]) arm1_split_end();
// shaft_2_driven_pulley();
// slot();

