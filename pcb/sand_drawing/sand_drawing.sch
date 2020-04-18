EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A1
U 1 1 5E9864AE
P 8000 1600
F 0 "A1" H 7750 2500 50  0000 C CNN
F 1 "Driver1" H 7750 2400 50  0000 C CNN
F 2 "Modules:Pololu_Breakout-16_15.2x20.3mm" H 8200 800 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 8100 1300 50  0001 C CNN
	1    8000 1600
	1    0    0    -1  
$EndComp
$Comp
L Driver_Motor:Pololu_Breakout_DRV8825 A2
U 1 1 5E987B88
P 5600 4200
F 0 "A2" H 5300 5050 50  0000 C CNN
F 1 "Driver2" H 5300 4950 50  0000 C CNN
F 2 "Modules:Pololu_Breakout-16_15.2x20.3mm" H 5800 3400 50  0001 L CNN
F 3 "https://www.pololu.com/product/2982" H 5700 3900 50  0001 C CNN
	1    5600 4200
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x04_Male J1
U 1 1 5E98CB20
P 8900 1750
F 0 "J1" H 8872 1632 50  0000 R CNN
F 1 "Stepper1" H 8872 1723 50  0000 R CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x04_Pitch2.54mm" H 8900 1750 50  0001 C CNN
F 3 "~" H 8900 1750 50  0001 C CNN
	1    8900 1750
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x04_Male J2
U 1 1 5E98E54C
P 6500 4350
F 0 "J2" H 6472 4232 50  0000 R CNN
F 1 "Stepper2" H 6472 4323 50  0000 R CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x04_Pitch2.54mm" H 6500 4350 50  0001 C CNN
F 3 "~" H 6500 4350 50  0001 C CNN
	1    6500 4350
	-1   0    0    1   
$EndComp
Wire Wire Line
	8400 1500 8550 1500
Wire Wire Line
	8400 1800 8550 1800
Wire Wire Line
	8550 1800 8550 1750
Wire Wire Line
	8550 1750 8700 1750
Wire Wire Line
	8400 1900 8550 1900
Wire Wire Line
	8550 1900 8550 1850
Wire Wire Line
	8550 1850 8700 1850
Wire Wire Line
	6000 4100 6150 4100
Wire Wire Line
	6000 4400 6150 4400
Wire Wire Line
	6150 4400 6150 4350
Wire Wire Line
	6150 4350 6300 4350
Wire Wire Line
	6000 4500 6150 4500
Wire Wire Line
	6150 4500 6150 4450
Wire Wire Line
	6150 4450 6300 4450
Wire Wire Line
	7500 1200 7400 1200
Wire Wire Line
	5200 4200 5100 4200
Wire Wire Line
	5200 4000 5100 4000
Wire Wire Line
	5100 4000 5100 4200
Wire Wire Line
	5200 3900 5100 3900
Wire Wire Line
	5100 3900 5100 4000
Connection ~ 5100 4000
Wire Wire Line
	5100 3800 5100 3900
Connection ~ 5100 3900
Wire Wire Line
	7600 1600 7500 1600
Wire Wire Line
	7600 1400 7500 1400
Wire Wire Line
	7500 1400 7500 1600
Wire Wire Line
	7600 1300 7500 1300
Wire Wire Line
	7500 1300 7500 1400
Connection ~ 7500 1400
Wire Wire Line
	7600 1200 7500 1200
Wire Wire Line
	7500 1200 7500 1300
Connection ~ 7500 1300
$Comp
L power:GND #PWR0101
U 1 1 5E9A89B2
P 5650 5100
F 0 "#PWR0101" H 5650 4850 50  0001 C CNN
F 1 "GND" H 5655 4927 50  0000 C CNN
F 2 "" H 5650 5100 50  0001 C CNN
F 3 "" H 5650 5100 50  0001 C CNN
	1    5650 5100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR0102
U 1 1 5E9A9913
P 8050 2500
F 0 "#PWR0102" H 8050 2250 50  0001 C CNN
F 1 "GND" H 8055 2327 50  0000 C CNN
F 2 "" H 8050 2500 50  0001 C CNN
F 3 "" H 8050 2500 50  0001 C CNN
	1    8050 2500
	1    0    0    -1  
$EndComp
Wire Wire Line
	8050 2500 8050 2450
Wire Wire Line
	8050 2450 8000 2450
Wire Wire Line
	8000 2450 8000 2400
Wire Wire Line
	8050 2450 8100 2450
Wire Wire Line
	8100 2450 8100 2400
Connection ~ 8050 2450
Wire Wire Line
	5600 5000 5600 5050
Wire Wire Line
	5600 5050 5650 5050
Wire Wire Line
	5650 5050 5650 5100
Wire Wire Line
	5650 5050 5700 5050
Wire Wire Line
	5700 5050 5700 5000
Connection ~ 5650 5050
$Comp
L power:+12V #PWR0103
U 1 1 5E9C6646
P 5600 3450
F 0 "#PWR0103" H 5600 3300 50  0001 C CNN
F 1 "+12V" H 5615 3623 50  0000 C CNN
F 2 "" H 5600 3450 50  0001 C CNN
F 3 "" H 5600 3450 50  0001 C CNN
	1    5600 3450
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR0104
U 1 1 5E9C7343
P 8000 850
F 0 "#PWR0104" H 8000 700 50  0001 C CNN
F 1 "+12V" H 8015 1023 50  0000 C CNN
F 2 "" H 8000 850 50  0001 C CNN
F 3 "" H 8000 850 50  0001 C CNN
	1    8000 850 
	1    0    0    -1  
$EndComp
Connection ~ 7500 1200
Wire Wire Line
	5200 3800 5100 3800
Wire Wire Line
	5000 3800 5100 3800
Connection ~ 5100 3800
$Comp
L Connector:Conn_01x03_Male J3
U 1 1 5E9E0F06
P 1750 5250
F 0 "J3" H 1722 5182 50  0000 R CNN
F 1 "Opto 1" H 1722 5273 50  0000 R CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x03_Pitch2.54mm" H 1750 5250 50  0001 C CNN
F 3 "~" H 1750 5250 50  0001 C CNN
	1    1750 5250
	-1   0    0    1   
$EndComp
$Comp
L Connector:Conn_01x03_Male J4
U 1 1 5E9E28A1
P 1750 5550
F 0 "J4" H 1722 5482 50  0000 R CNN
F 1 "Opto 2" H 1722 5573 50  0000 R CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x03_Pitch2.54mm" H 1750 5550 50  0001 C CNN
F 3 "~" H 1750 5550 50  0001 C CNN
	1    1750 5550
	-1   0    0    1   
$EndComp
$Comp
L power:GND #PWR0105
U 1 1 5E9E4C25
P 1300 5800
F 0 "#PWR0105" H 1300 5550 50  0001 C CNN
F 1 "GND" H 1305 5627 50  0000 C CNN
F 2 "" H 1300 5800 50  0001 C CNN
F 3 "" H 1300 5800 50  0001 C CNN
	1    1300 5800
	1    0    0    -1  
$EndComp
Wire Wire Line
	1300 5800 1300 5650
Connection ~ 1300 5650
Wire Wire Line
	1300 5650 1300 5350
Wire Wire Line
	1550 5250 1500 5250
$Comp
L power:+3.3V #PWR0106
U 1 1 5E9FBEF7
P 3400 1250
F 0 "#PWR0106" H 3400 1100 50  0001 C CNN
F 1 "+3.3V" H 3415 1423 50  0000 C CNN
F 2 "" H 3400 1250 50  0001 C CNN
F 3 "" H 3400 1250 50  0001 C CNN
	1    3400 1250
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0107
U 1 1 5E9FCFD5
P 7400 1200
F 0 "#PWR0107" H 7400 1050 50  0001 C CNN
F 1 "+3.3V" H 7415 1373 50  0000 C CNN
F 2 "" H 7400 1200 50  0001 C CNN
F 3 "" H 7400 1200 50  0001 C CNN
	1    7400 1200
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0108
U 1 1 5E9FDAD5
P 5000 3800
F 0 "#PWR0108" H 5000 3650 50  0001 C CNN
F 1 "+3.3V" H 5015 3973 50  0000 C CNN
F 2 "" H 5000 3800 50  0001 C CNN
F 3 "" H 5000 3800 50  0001 C CNN
	1    5000 3800
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR0109
U 1 1 5E9FE0CA
P 900 4900
F 0 "#PWR0109" H 900 4750 50  0001 C CNN
F 1 "+3.3V" H 915 5073 50  0000 C CNN
F 2 "" H 900 4900 50  0001 C CNN
F 3 "" H 900 4900 50  0001 C CNN
	1    900  4900
	1    0    0    -1  
$EndComp
Wire Wire Line
	1400 5550 1550 5550
Wire Wire Line
	1200 5450 1550 5450
Wire Wire Line
	1550 5150 1200 5150
Connection ~ 1200 5150
Wire Wire Line
	1200 5150 1200 5450
Wire Wire Line
	1300 5350 1550 5350
Wire Wire Line
	1300 5650 1550 5650
$Comp
L Regulator_Linear:LD1117S33TR_SOT223 U2
U 1 1 5EA1C344
P 1200 1350
F 0 "U2" H 1200 1592 50  0000 C CNN
F 1 "LD1117" H 1200 1501 50  0000 C CNN
F 2 "Power_Integrations:TO-220" H 1200 1575 50  0001 C CIN
F 3 "http://www.fairchildsemi.com/ds/LM/LM7805.pdf" H 1200 1300 50  0001 C CNN
	1    1200 1350
	1    0    0    -1  
$EndComp
$Comp
L power:+12V #PWR0110
U 1 1 5EA2246B
P 700 1050
F 0 "#PWR0110" H 700 900 50  0001 C CNN
F 1 "+12V" H 715 1223 50  0000 C CNN
F 2 "" H 700 1050 50  0001 C CNN
F 3 "" H 700 1050 50  0001 C CNN
	1    700  1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	900  1350 700  1350
Wire Wire Line
	700  1350 700  1050
$Comp
L power:GND #PWR0111
U 1 1 5EA25D30
P 1200 1950
F 0 "#PWR0111" H 1200 1700 50  0001 C CNN
F 1 "GND" H 1205 1777 50  0000 C CNN
F 2 "" H 1200 1950 50  0001 C CNN
F 3 "" H 1200 1950 50  0001 C CNN
	1    1200 1950
	1    0    0    -1  
$EndComp
Wire Wire Line
	1200 1650 1200 1850
Wire Wire Line
	1500 1350 1650 1350
$Comp
L Device:C C1
U 1 1 5EA37812
P 700 1650
F 0 "C1" H 815 1696 50  0000 L CNN
F 1 "0.1µF" H 815 1605 50  0000 L CNN
F 2 "Capacitors_THT:C_Axial_L3.8mm_D2.6mm_P7.50mm_Horizontal" H 738 1500 50  0001 C CNN
F 3 "~" H 700 1650 50  0001 C CNN
	1    700  1650
	1    0    0    -1  
$EndComp
$Comp
L Device:C C2
U 1 1 5EA38946
P 1650 1650
F 0 "C2" H 1765 1696 50  0000 L CNN
F 1 "10µF" H 1765 1605 50  0000 L CNN
F 2 "Capacitors_THT:C_Axial_L3.8mm_D2.6mm_P7.50mm_Horizontal" H 1688 1500 50  0001 C CNN
F 3 "~" H 1650 1650 50  0001 C CNN
	1    1650 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	700  1800 700  1850
Wire Wire Line
	700  1850 1200 1850
Connection ~ 1200 1850
Wire Wire Line
	1200 1850 1200 1950
Wire Wire Line
	1650 1800 1650 1850
Wire Wire Line
	1650 1850 1200 1850
Wire Wire Line
	700  1500 700  1350
Connection ~ 700  1350
Wire Wire Line
	1650 1500 1650 1350
Connection ~ 1650 1350
$Comp
L power:+12V #PWR0112
U 1 1 5EA54B15
P 1100 2500
F 0 "#PWR0112" H 1100 2350 50  0001 C CNN
F 1 "+12V" V 1115 2628 50  0000 L CNN
F 2 "" H 1100 2500 50  0001 C CNN
F 3 "" H 1100 2500 50  0001 C CNN
	1    1100 2500
	0    1    1    0   
$EndComp
$Comp
L power:GND #PWR0113
U 1 1 5EA5546C
P 1100 2600
F 0 "#PWR0113" H 1100 2350 50  0001 C CNN
F 1 "GND" V 1105 2472 50  0000 R CNN
F 2 "" H 1100 2600 50  0001 C CNN
F 3 "" H 1100 2600 50  0001 C CNN
	1    1100 2600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	850  2500 1100 2500
Wire Wire Line
	850  2600 1100 2600
$Comp
L power:GND #PWR0114
U 1 1 5EA82D35
P 3300 3550
F 0 "#PWR0114" H 3300 3300 50  0001 C CNN
F 1 "GND" H 3305 3377 50  0000 C CNN
F 2 "" H 3300 3550 50  0001 C CNN
F 3 "" H 3300 3550 50  0001 C CNN
	1    3300 3550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3300 3550 3300 3400
$Comp
L Connector:Conn_01x02_Male J0
U 1 1 5EA53D0B
P 650 2500
F 0 "J0" H 758 2681 50  0000 C CNN
F 1 "12V GND" H 758 2590 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 650 2500 50  0001 C CNN
F 3 "~" H 650 2500 50  0001 C CNN
	1    650  2500
	1    0    0    -1  
$EndComp
$Comp
L Connector:Conn_01x02_Male J5
U 1 1 5EA90E62
P 3700 1550
F 0 "J5" H 3672 1432 50  0000 R CNN
F 1 "ESP POWER" H 3672 1523 50  0000 R CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 3700 1550 50  0001 C CNN
F 3 "~" H 3700 1550 50  0001 C CNN
	1    3700 1550
	-1   0    0    1   
$EndComp
$Comp
L power:+3.3V #PWR0115
U 1 1 5EA91F40
P 1650 1050
F 0 "#PWR0115" H 1650 900 50  0001 C CNN
F 1 "+3.3V" H 1665 1223 50  0000 C CNN
F 2 "" H 1650 1050 50  0001 C CNN
F 3 "" H 1650 1050 50  0001 C CNN
	1    1650 1050
	1    0    0    -1  
$EndComp
Wire Wire Line
	1650 1350 1650 1050
Wire Wire Line
	3500 1450 3400 1450
Wire Wire Line
	3400 1450 3400 1250
Wire Wire Line
	3500 1550 3400 1550
Wire Wire Line
	3400 1550 3400 1800
$Comp
L MCU_Module:WeMos_D1_mini U1
U 1 1 5E984ADF
P 3300 2600
F 0 "U1" H 3950 3500 50  0000 C CNN
F 1 "WeMos_D1_mini" H 3950 3400 50  0000 C CNN
F 2 "Custom:WEMOS_D1_mini_light" H 3300 1450 50  0001 C CNN
F 3 "https://wiki.wemos.cc/products:d1:d1_mini#documentation" H 1450 1450 50  0001 C CNN
	1    3300 2600
	1    0    0    -1  
$EndComp
Wire Wire Line
	8550 1650 8700 1650
Wire Wire Line
	8550 1500 8550 1650
Wire Wire Line
	8400 1600 8600 1600
Wire Wire Line
	8600 1600 8600 1550
Wire Wire Line
	8600 1550 8700 1550
Wire Wire Line
	6150 4250 6300 4250
Wire Wire Line
	6150 4100 6150 4250
Wire Wire Line
	6300 4150 6250 4150
Wire Wire Line
	6250 4150 6250 4200
Wire Wire Line
	6250 4200 6000 4200
$Comp
L Connector_Generic:Conn_02x04_Top_Bottom J6
U 1 1 5EAD9D17
P 2100 3450
F 0 "J6" H 2150 3767 50  0000 C CNN
F 1 "Unused Pins" H 2150 3676 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_2x04_Pitch2.54mm" H 2100 3450 50  0001 C CNN
F 3 "~" H 2100 3450 50  0001 C CNN
	1    2100 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 1800 2350 1800
Wire Wire Line
	2350 1800 2350 2800
Wire Wire Line
	2350 2800 1550 2800
Wire Wire Line
	1550 2800 1550 3450
Wire Wire Line
	2900 2200 2400 2200
Wire Wire Line
	2400 2200 2400 2850
Wire Wire Line
	1600 2850 1600 3550
Wire Wire Line
	1600 3550 1900 3550
Wire Wire Line
	2900 2500 2450 2500
Wire Wire Line
	2450 2500 2450 2900
Wire Wire Line
	2450 2900 1650 2900
Wire Wire Line
	2900 2600 2500 2600
Wire Wire Line
	2500 2600 2500 2950
Wire Wire Line
	2500 2950 1700 2950
Wire Wire Line
	3700 3000 4000 3000
Wire Wire Line
	4000 3000 4000 3850
Wire Wire Line
	4000 3850 2800 3850
Wire Wire Line
	2800 3850 2800 3550
Wire Wire Line
	3700 2900 4050 2900
Wire Wire Line
	4050 2900 4050 3900
Wire Wire Line
	3700 2200 4100 2200
Wire Wire Line
	4100 2200 4100 3950
Wire Wire Line
	4100 3950 2700 3950
Wire Wire Line
	3700 2100 4150 2100
Wire Wire Line
	4150 2100 4150 4000
Wire Wire Line
	4150 4000 2650 4000
$Comp
L Connector:Conn_01x02_Male D2M1
U 1 1 5E9C5CF2
P 4600 5250
F 0 "D2M1" H 4450 5150 50  0000 C CNN
F 1 "Driver 2 M1" H 4350 5250 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 4600 5250 50  0001 C CNN
F 3 "~" H 4600 5250 50  0001 C CNN
	1    4600 5250
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x02_Male D2M2
U 1 1 5E9C5F13
P 4800 5250
F 0 "D2M2" H 4650 5150 50  0000 C CNN
F 1 "Driver 2 M2" H 4550 5250 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 4800 5250 50  0001 C CNN
F 3 "~" H 4800 5250 50  0001 C CNN
	1    4800 5250
	0    -1   -1   0   
$EndComp
Text GLabel 3700 2700 2    50   Input ~ 0
Opto1
Text GLabel 3700 2800 2    50   Input ~ 0
Opto2
Text GLabel 1400 4800 0    50   Input ~ 0
Opto2
Text GLabel 1500 4800 2    50   Input ~ 0
Opto1
Wire Wire Line
	1500 4800 1500 5250
Wire Wire Line
	1200 5150 900  5150
Wire Wire Line
	900  5150 900  4900
Wire Wire Line
	1400 5550 1400 4800
Wire Wire Line
	5200 4600 4400 4600
Wire Wire Line
	4400 4600 4400 5050
Wire Wire Line
	4600 5050 4600 4700
Wire Wire Line
	4600 4700 5200 4700
Wire Wire Line
	5200 4800 4800 4800
Wire Wire Line
	4800 4800 4800 5050
$Comp
L power:+3.3V #PWR0116
U 1 1 5EA0D498
P 4200 4850
F 0 "#PWR0116" H 4200 4700 50  0001 C CNN
F 1 "+3.3V" H 4215 5023 50  0000 C CNN
F 2 "" H 4200 4850 50  0001 C CNN
F 3 "" H 4200 4850 50  0001 C CNN
	1    4200 4850
	1    0    0    -1  
$EndComp
Wire Wire Line
	4500 4850 4500 5050
Wire Wire Line
	4900 4850 4900 5050
Wire Wire Line
	4500 4850 4700 4850
Connection ~ 4500 4850
Wire Wire Line
	4700 5050 4700 4850
Connection ~ 4700 4850
Wire Wire Line
	4700 4850 4900 4850
Wire Wire Line
	4200 4850 4500 4850
Wire Wire Line
	8000 850  8000 1000
Wire Wire Line
	5600 3600 5600 3450
$Comp
L Connector:Conn_01x02_Male D1M0
U 1 1 5EA4E3CF
P 6800 2650
F 0 "D1M0" H 6650 2550 50  0000 C CNN
F 1 "Driver 1 M0" H 6500 2650 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 6800 2650 50  0001 C CNN
F 3 "~" H 6800 2650 50  0001 C CNN
	1    6800 2650
	0    -1   -1   0   
$EndComp
$Comp
L Connector:Conn_01x02_Male D1M1
U 1 1 5EA4E3D5
P 7000 2650
F 0 "D1M1" H 6850 2550 50  0000 C CNN
F 1 "Driver 1 M1" H 6700 2650 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 7000 2650 50  0001 C CNN
F 3 "~" H 7000 2650 50  0001 C CNN
	1    7000 2650
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6800 2000 6800 2450
Wire Wire Line
	7000 2450 7000 2100
Wire Wire Line
	7200 2200 7200 2450
$Comp
L power:+3.3V #PWR0117
U 1 1 5EA4E3E7
P 6600 2250
F 0 "#PWR0117" H 6600 2100 50  0001 C CNN
F 1 "+3.3V" H 6615 2423 50  0000 C CNN
F 2 "" H 6600 2250 50  0001 C CNN
F 3 "" H 6600 2250 50  0001 C CNN
	1    6600 2250
	1    0    0    -1  
$EndComp
Wire Wire Line
	6900 2250 6900 2450
Wire Wire Line
	7300 2250 7300 2450
Wire Wire Line
	6900 2250 7100 2250
Connection ~ 6900 2250
Wire Wire Line
	7100 2450 7100 2250
Connection ~ 7100 2250
Wire Wire Line
	7100 2250 7300 2250
Wire Wire Line
	6600 2250 6900 2250
Wire Wire Line
	7200 2200 7600 2200
Wire Wire Line
	6800 2000 7600 2000
Wire Wire Line
	7000 2100 7600 2100
$Comp
L Connector:Conn_01x02_Male D2M0
U 1 1 5E99CB34
P 4400 5250
F 0 "D2M0" H 4250 5150 50  0000 C CNN
F 1 "Driver 2 M0" H 4150 5250 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 4400 5250 50  0001 C CNN
F 3 "~" H 4400 5250 50  0001 C CNN
	1    4400 5250
	0    -1   -1   0   
$EndComp
Wire Wire Line
	4050 3900 2750 3900
Wire Wire Line
	2650 3450 2650 4000
Wire Wire Line
	2650 3450 2400 3450
Wire Wire Line
	2750 3650 2750 3900
Wire Wire Line
	2400 3650 2750 3650
Wire Wire Line
	2400 3550 2800 3550
Wire Wire Line
	2700 3950 2700 3350
Wire Wire Line
	2700 3350 2400 3350
Wire Wire Line
	1650 2900 1650 3350
Wire Wire Line
	1650 3350 1900 3350
Wire Wire Line
	2400 2850 1600 2850
Wire Wire Line
	1700 2950 1700 3650
Wire Wire Line
	1700 3650 1900 3650
Wire Wire Line
	1900 3450 1550 3450
Text GLabel 3700 2300 2    50   Input ~ 0
D1Dir
Text GLabel 3700 2400 2    50   Input ~ 0
D1Step
Text GLabel 7450 1800 0    50   Input ~ 0
D1Dir
Text GLabel 7450 1700 0    50   Input ~ 0
D1Step
Wire Wire Line
	7600 1700 7450 1700
Wire Wire Line
	7450 1800 7600 1800
Text GLabel 3700 2500 2    50   Input ~ 0
D2Dir
Text GLabel 3700 2600 2    50   Input ~ 0
D2Step
Text GLabel 5050 4400 0    50   Input ~ 0
D2Dir
Text GLabel 5050 4300 0    50   Input ~ 0
D2Step
Wire Wire Line
	5200 4300 5050 4300
Wire Wire Line
	5200 4400 5050 4400
$Comp
L Connector:Conn_01x02_Male D1M2
U 1 1 5EA4E3DB
P 7200 2650
F 0 "D1M2" H 7050 2550 50  0000 C CNN
F 1 "Driver 1 M2" H 6900 2650 50  0000 C CNN
F 2 "Socket_Strips:Socket_Strip_Straight_1x02_Pitch2.54mm" H 7200 2650 50  0001 C CNN
F 3 "~" H 7200 2650 50  0001 C CNN
	1    7200 2650
	0    -1   -1   0   
$EndComp
$EndSCHEMATC
