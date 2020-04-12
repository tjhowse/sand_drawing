
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
stepper_1_offset = 608_id/2+n17_xy/2;
stepper_2_offset = stepper_1_offset;

bearing_retain_lip = 0.5;

holder_z = 608_z+bearing_retain_lip;
holder_x = stepper_1_offset + stepper_2_offset + n17_hole_spacing + n17_hole_dia + 2*wt + stepper_slot/2;
holder_y = n17_hole_spacing + n17_hole_dia + 2*wt;

belt_z = 4;
belt_guide_z = 1;

shaft_1_drive_pulley_dia = 27;
shaft_1_drive_pulley_z = belt_z+belt_guide_z;
washer_z = 0.5;

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
    }
    // bearing_holder();
    // translate([0,0,-shaft_1_drive_pulley_z-washer_z]) #cylinder(r=shaft_1_drive_pulley_dia/2, h=shaft_1_drive_pulley_z);
    // translate([0,0,-shaft_1_drive_pulley_z*2-washer_z*2]) #cylinder(r=shaft_1_drive_pulley_dia/2, h=shaft_1_drive_pulley_z);
}
top_holder();