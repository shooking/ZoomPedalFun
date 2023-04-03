#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
#include <sstream>

using namespace std;
typedef unsigned char BYTE;

#include "pack.h"


// default it to 0 - which means leave alone!
vector<BYTE> pack ( vector<BYTE> &unpacked, int newTempo = 0, int slot = -1, int fxid = -1, int gid = -1 )
{
	// patch the tempo in unpacked (8 bit) space
	int offset = 0;

    if (!(newTempo < 40 || newTempo > 240))
	{
		BYTE by109 = unpacked[109];
		BYTE by110 = unpacked[110];

		// 0x80 = 10000000
		// 0x07 = 00000111
		// 0x0F = 00001111
		// 0xE0 = 11100000
		// 0xF8 = 11111000
		unpacked[109] = (by109 & 0x80) + ((newTempo & 0x07) << 5) + (by109 & 0x0F);
		unpacked[110] = (by110 & 0xE0) + (((newTempo & 0xF8)<<1) >> 4);
	}

	if (slot != -1)
	{
		cout << "Injecting " << fxid << " " << gid << " into slot " << slot << endl;
		int NumFX = (unpacked[109] ) >> 2;
		
		bool emptySlot = ( unpacked[18 * (slot - 1)] == 0);

		if (emptySlot) {
			NumFX++;
			if (NumFX > 6) NumFX = 6;
		}

		BYTE i18p1 = unpacked[18 * (slot - 1) + 1];
		unpacked[18*(slot -1)] = (fxid * 2) & 0xFF;
		unpacked[18*(slot -1) + 1] = (i18p1 & 0xF0) + ( ((fxid * 2) >> 8) & 0x0F);

		BYTE i18p2 = unpacked[18 * (slot - 1) + 2];
		BYTE i18p3 = unpacked[18 * (slot - 1) + 3];
		unpacked[18 * (slot - 1) + 2] = (((gid) << 5) & 0xC0) | (i18p2 & 0x3F);
		cout << "gid = " << gid << endl;
		cout << (((gid << 5) ) ) << endl;
		unpacked[18 * (slot - 1) + 3] = ( ( (((gid) << 5) >> 8 ) & 0xF0)) | (i18p3 & 0x0F);
		// Adjust the numFX where necessary
		if (!emptySlot) {
			BYTE b109mask = unpacked[109] & 0x03; // grab 2 LSB bits
			unpacked[109] = (NumFX <<2) + b109mask;
		}
	}

	vector<BYTE>	packed;

	// so we patched the newTempo into 8 bit space.
	// Now we got to create the 7 bit version	
	packed.push_back(0xf0);
	packed.push_back(0x52);
	packed.push_back(0x00);
	packed.push_back(0x61);
	packed.push_back(0x28);
	

	size_t remainderBytes = (unpacked.size() - offset) % 7;
	size_t numLoops = (unpacked.size() - offset)/ 7;
	for (size_t i = 0; i < numLoops; i++)
	{	
		BYTE packet[8], bv = 0;

		cout << "   ";
		for (size_t j = 0; j < 7; j++)
		{
			cout << setfill ('0') << setw (2) << hex << (0xff & (unpacked[i*7 + j])) << " ";
			if ( unpacked[i*7 + j + offset] >= 128 )
			{
				// printf("HIT!! %d %d\n", j, (1 << j));
				bv |= (1 << (6 - j));
			}
			packet[j+1] = (unpacked[i*7 + j + offset] & 0x7F);
		}
		packed.push_back(bv);
		cout << "\n" << setfill ('0') << setw (2) << hex << (0xff & bv) << " ";
		for (size_t j = 1; j < sizeof(packet); j++)
		{
			packed.push_back(packet[j]);
			cout << setfill ('0') << setw (2) << hex << (0xFF & packet[j]) << " ";
		}
		cout << "\n";
	}

	// we are at an expansion byte boundary - so output one
	packed.push_back(0x00);
	
	cout << remainderBytes << " left.\n";
	for (size_t i = 0; i < remainderBytes; i++)
	{
		packed.push_back(unpacked[7 * numLoops + i]);
		/*
		cout << setfill ('0') << setw (2) << hex << (0xFF & unpacked[7 * numLoops + i]);
		cout << endl;
		*/
	}
	packed.push_back(0xF7);
	return packed;
}