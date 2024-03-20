#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>
#include <map>

#include <string>
#include <cmath>
#include <vector>
using namespace std;
typedef unsigned char BYTE;

typedef map< pair<int, int>, string> FXMap;

vector<BYTE> unpack (vector<BYTE> &vi);

string findFX(int a1, int a2);

string findFX(int a1, int a2)
{

	FXMap knownFX;

	// we need this to be even - the bit 0 signifies effect on - we dont care when we match
	if (a1 & 1) a1--;

	knownFX.insert( FXMap::value_type( {0x00, 0x00}, "BYPASS") );				// 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00

	// Filter
	knownFX.insert( FXMap::value_type( {0x010, 0x0200}, "COMP") );				// discovered from ToneLib G1On
	knownFX.insert( FXMap::value_type( {0x060, 0x0200}, "OPTCOMP") );			// 61 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x030, 0x0200}, "D COMP") );				// 31 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x0200}, "M COMP") ); 			// 41 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0200}, "DUAL COMP") ); 			// 41 01 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x06a, 0x0200}, "160 COMP") ); 			// 6b 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x074, 0x0200}, "Limiter") ); 			// 75 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x0200}, "Slow ATTCK") ); 		// 81 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x0200}, "ZNR") ); 				// a1 00 00 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0c0, 0x0200}, "NoiseGate") );				// discovered from ToneLib G1On

	knownFX.insert( FXMap::value_type( {0x020, 0x0400}, "GraphicEQ") );				// discovered from ToneLib G1On
	knownFX.insert( FXMap::value_type( {0x030, 0x0400}, "BassGraphicEQ") ); 		// 31 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x048, 0x0400}, "BasParaEQ") ); 			// 49 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x050, 0x0400}, "Splitter") ); 			// 51 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x058, 0x0400}, "Bottom B") ); 			// 59 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x0400}, "Exciter") ); 			// 61 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0b0, 0x0400}, "BassAutoWah" ) ); 		// b1 00 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00
	knownFX.insert( FXMap::value_type( {0x110, 0x0400}, "ZTRON" ) ); 			// 11 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x0400}, "M-Filter" ) ); 			// 21 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x12a, 0x0400}, "A-FILTER" ) ); 			// 2b 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x134, 0x0400}, "Bass CRY" ) ); 			// 35 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0400}, "STEP" ) ); 				// 41 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x160, 0x0400}, "SEQ FILTER" ) ); 		// 61 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x180, 0x0400}, "RANDOM FILTER" ) ); 	// 81 01 00 04 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x280, 0x0600}, "Aco.Sim") );				// discovered from ToneLib G1On

	// AMP SIM
	knownFX.insert( FXMap::value_type( {0x020, 0x0800}, "DELUXE-R") );				// discovered from ToneLib G1On

	knownFX.insert( FXMap::value_type( {0x020, 0x0280}, "BASS BOOSTER" ) ); 		// 21 00 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x0280}, "BassOverDrive" ) ); 	// 41 00 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x0280}, "BASS MUFF" ) ); 		// 61 00 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0280}, "T Scream" ) ); 			// 41 01 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x0280}, "Bass Dist" ) ); 		// a1 00 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x160, 0x0280}, "BassSqueak" ) ); 		// 61 01 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x180, 0x0280}, "BassFuzzSmile" ) ); 	// 81 01 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x0280}, "Bass Metal" ) ); 		// 21 01 80 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x020, 0x02c0}, "BASS DRIVE" ) ); 		// 21 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x02c0}, "D.I+" ) ); 			// 41 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x02c0}, "Bass BB" ) ); 			// 61 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x02c0}, "DI5" ) ); 				// 81 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x02c0}, "BassPre" ) ); 			// a1 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0c0, 0x02c0}, "Ac Bs Pre" ) ); 		// c1 00 c0 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x020, 0x0a20}, "SVT" ) ); 				// 21 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x0a20}, "B-MAN" ) ); 			// 41 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x0a20}, "Hrt-3500" ) ); 		// 61 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x0a20}, "SMR" ) ); 				// 81 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x0a20}, "Flip Top" ) ); 		// a1 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0c0, 0x0a20}, "acoustic" ) ); 		// c1 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0e0, 0x0a20}, "agamp" ) ); 			// e1 00 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x100, 0x0a20}, "monotone" ) ); 		// 01 01 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x0a20}, "SUPER B" ) ); 			// 21 01 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0a20}, "G-KRUEGER" ) ); 		// 41 01 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x160, 0x0a20}, "Heaven" ) ); 			// 61 01 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x180, 0x0a20}, "Mark B" ) ); 			// 81 01 20 0a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x010, 0x0c00}, "Tremolo" ) ); 			// 11 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x0c00}, "Slicer" ) ); 			// 41 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x0c00}, "Phaser" ) ); 			// 61 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x06a, 0x0c00}, "Duo-Phase" ) ); 		// 6b 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x074, 0x0c00}, "WarpPhaser" ) ); 		// 75 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x200, 0x0c00}, "Vibrato" ) ); 			// 01 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x0c00}, "TheVibe" ) ); 			// 81 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0f0, 0x0c00}, "Bass CHORUS" ) ); 		// f1 00 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x110, 0x0c00}, "Bass Detune" ) ); 		// 11 01 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0c00}, "StereoCho" ) ); 		// 41 01 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x170, 0x0c00}, "Bass Ensemble" ) ); 	// 71 01 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x400, 0x0c00}, "Corona Tri" ) ); 		// 01 04 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x1d0, 0x0c00}, "Bass Flanger" ) ); 	// d1 01 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x1b0, 0x0c00}, "Vin FLNGR" ) ); 		// b1 01 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x230, 0x0c00}, "Bass Octave" ) ); 		// 31 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x240, 0x0c00}, "Pitch SHFT" ) ); 		// 41 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x270, 0x0c00}, "Bass Pitch" ) ); 		// 71 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x280, 0x0c00}, "HPS" ) ); 				// 81 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x2a0, 0x0c00}, "BEND CHO" ) ); 		// a1 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x2c0, 0x0c00}, "MojoRoller" ) ); 		// c1 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x2e0, 0x0c00}, "RingMod" ) ); 			// e1 02 00 0c 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x020, 0x0e00}, "Bit Crush" ) ); 		// 21 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x0e00}, "BOMBER" ) ); 			// 41 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x0e00}, "AUTOPAN" ) ); 			// a1 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x070, 0x0e00}, "BassSynth" ) ); 		// 71 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0e0, 0x0e00}, "StdSyn" ) );			// e1 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x100, 0x0e00}, "Syn Tlk" ) ); 			// 01 01 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x180, 0x0e00}, "V-SYN" ) ); 			// 81 01 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x1a0, 0x0e00}, "4VoiceSyn" ) ); 		// a1 01 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x0e00}, "Z-SYN" ) ); 			// 21 01 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x0e00}, "Z-Organ") );			// 81 00 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x0e00}, "Defret") );			// 41 01 00 0e 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x010, 0x1000}, "DELAY") ); 			// 11 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x020, 0x1000}, "TapeEcho") ); 			// 21 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x180, 0x1000}, "StompDly") ); 			// 81 01 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x050, 0x1000}, "ModDelay2") ); 		// 51 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x080, 0x1000}, "ReverseDelay") ); 		// 81 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x1000}, "Multi Tap Delay") ); 	// a1 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0e0, 0x1000}, "Filter Dly") ); 		// e1 00 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x100, 0x1000}, "Pitch Delay") ); 		// 01 01 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x160, 0x1000}, "TRIGGER HOLD DELAY") );// 61 01 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x1000}, "STEREO DELAY") ); 		// 21 01 00 10 00 00 00 00 00 00 00 00 00 00 00 00 00 00 

	knownFX.insert( FXMap::value_type( {0x010, 0x1200}, "HD Hall") ); 			// 11 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x020, 0x1200}, "HALL") ); 				// 21 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x040, 0x1200}, "ROOM") ); 				// 41 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x060, 0x1200}, "Tiled Rm") ); 			// 61 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0a0, 0x1200}, "Arena Reverb") ); 		// a1 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x120, 0x1200}, "Plate") ); 			// 21 01 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0e0, 0x1200}, "AIR") ); 				// e1 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x0c0, 0x1200}, "Early Reflection") ); 	// c1 00 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x140, 0x1200}, "MOD REVERB") ); 		// 41 01 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x160, 0x1200}, "Slap Back Reverb") ); 	// 61 01 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 
	knownFX.insert( FXMap::value_type( {0x320, 0x1200}, "PARTICLE REVERB") ); 	// 21 03 00 12 00 00 00 00 00 00 00 00 00 00 00 00 00 00 


	if (knownFX.find(std::make_pair(a1, a2)) != knownFX.end())
	{
		return (knownFX.find(std::make_pair(a1, a2)))->second;
	} else {
		return "UKNOWN FX!!";
	}
}

vector<BYTE> unpack ( vector<BYTE> &sysex )
{
	// Unpack data 7bit to 8bit, MSBs in first byte
	//data = bytearray(b"")
	int loop = -1;
	uint8_t hibits = 0;

	int j = 0;
	vector<BYTE>	unpacked;

	// We expect this unpacked sysex to start from byte 5 (0 bias)
	for (size_t i = 5; i < sysex.size() - 1; i++)
	{	
		//byte in packet:
		uint8_t byt = sysex[i];
		if (loop != -1)
		{
			uint8_t p = pow (2, loop);
			if (hibits & p)
			{
				byt = 0x80 + byt; //data.append(128 + byte)
				unpacked.push_back(byt);
			}
			else
		       	{
				unpacked.push_back(byt);
			}
			loop = loop - 1;
		}
		else
		{
			hibits = byt;
			// do we need to acount for short sets (at end of block block)?
			loop = 6;
		}
	}

	for (j = 0; j < 10; j++)
	{
		cout << unpacked[unpacked.size() - 11 + j] ;
	}
	cout << endl;
	
	// Start to summarize what we know
	for (int i = 0; i < 5; i++)
	{
		// Lets try to unpick the parameters.
		// I think p[7]==Param8 is i + 16/2 or something like that.
		int p[] = {
		/* 0 */ ( ( ((unpacked[ 18* i + 4]      ) << 8) + (unpacked[18* i +  3]) ) >> 6 ),
		/* 1 */	( ( ((unpacked[ 18* i + 6]      ) << 8) + (unpacked[18* i +  5]) ) >> 3 ),
		/* 2 */	( ( ((unpacked[ 18* i + 8] & 0xF) << 8) + (unpacked[18* i +  7]) )     ),
		/* 3 */	( ( ((unpacked[ 18* i + 9] & 0xF) << 8) + (unpacked[18* i +  8]) ) >> 5 ),
		/* 4 */	( ( ((unpacked[18* i + 10] & 0xF) << 8) + (unpacked[18* i +  9]) ) >> 5 ),
		/* 5 */	( ( ((unpacked[18* i + 11] & 0xF) << 8) + (unpacked[18* i + 10]) ) >> 5 ),
		/* 6 */	( ( ((unpacked[18* i + 12] & 0xF) << 8) + (unpacked[18* i + 11]) ) >> 5 ),
		/* 7 */	( ( ((unpacked[18* i + 13]      ) << 8) + (unpacked[18* i + 12]) ) >> 5 ), 
		/* 8 */	    ((unpacked[18* i + 16] >> 1 ) )
		};

		// Lets try decode FX ID and group
		int FXID=(unpacked[18*i + 1] & 15)*256 + unpacked[18*i];
		int FXGroup;
		int rawFXGroup = (unpacked[18*i + 3] & 0x3F )*256 + unpacked[18*i + 2]; // I want most of the bits
		
		cout << endl;
		if ((unpacked[18 * i + 2] & 0XC0) == 0)
		{
			FXGroup= (unpacked[18*i + 3] & 0x0F) / 2;
		} else {
			FXGroup= (
				 ( (unpacked[18*i + 3] & 0x0F) << 8 )+ 
				 ( (unpacked[18*i + 2] & 0xC0))
			     ) >> 5;
		}
		cout << endl;
		/*
		printf("[%d][%d][%d][%d]\n", 
				unpacked[18*i + 0], 
				unpacked[18*i + 1], 
				unpacked[18*i + 2], 
				unpacked[18*i + 3]);
		*/
		printf("FXID[%d] (%.3s) = %3d (%02x), GROUPID = %d (%02x)\n",
			       i+1,
			       (FXID & 1) == 0 ? "OFF" : "ON",
			       FXID,
			       FXID,
			       FXGroup,
			       FXGroup);		       
		cout << endl;
		cout << "FX = " << findFX(FXID,  rawFXGroup) << endl;
		for (j = 0; j < 9; j++)
		{
			printf("\tP%d = %4d (%02x)", j+1, p[j], p[j]);
		}
	}
	cout << endl;

	printf("NumFX = %2d (%02x)\n", (unpacked[90] & 0xF0) >> 5, (unpacked[90] & 0xF0) >> 5);
		cout << endl;
	printf("Volume = %2d (%02x)\n", unpacked[91] & 0x7F, unpacked[91] & 0x7F);
		cout << endl;


	return unpacked;
}

vector<BYTE> readFile(char* filename)
{
    // open the file:
    ifstream file(filename, ios::binary | ios::in);

    // Stop eating new lines in binary mode!!!
    file.unsetf(ios::skipws);

    // get its size:
    streampos fileSize;

    file.seekg(0, ios::end);
    fileSize = file.tellg();
    file.seekg(0, ios::beg);

    vector<BYTE> vec;
    // reserve capacity
    vec.reserve(fileSize);

    // read the data:
    vec.insert(vec.begin(),
               istream_iterator<BYTE>(file),
               istream_iterator<BYTE>());
    file.close();
    return vec;
}

int
main (int argc, char **argv)
{
	/* read the file in, strip off header and F7 */

	cout << "Infile: " << argv[1] << endl;
	ifstream in_f(argv[1], ios::in | ios::binary);

	vector<BYTE> vo;
	vector<BYTE> vi = readFile(argv[1]);

	cout << "INPUT\n";
	int ctr = 0;
	for(auto i: vi)
	{
		if (ctr == 5) cout << endl;
		if (ctr > 5 && ((ctr - 5) % 16 == 0)) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;

	vo = unpack (vi);

	ctr = 0;
	// we expect 5 x 18 bytes then rest.
	cout << "OUTPUT\n";
	for (auto i: vo)
	{
		if (ctr % 18 == 0) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;
	return 0;
}