#include "unpack.h"

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
	BYTE numFXSeen = 0;
	for (int i = 0; i < 6; i++)
	{
		numFXSeen += ((unpacked[18*i] & 0xF0) !=0);
		// Lets try to unpick the parameters.
		// I think p[7]==Param8 is i + 16/2 or something like that.
		int p[] = {
		/* 0  ( (((unpacked[ 18* i + 4] ) << 8) +  ( ((unpacked[18* i +  3]) & 0xF0) >> 4) ) >> 5 ), */
		/* 0 */ ( (((unpacked[ 18* i + 4] ) << 4) +  ( ((unpacked[18* i +  3]) & 0xF0) >> 4) ) >> 1 ),
		/* 1 */ ( (((unpacked[ 18* i + 6] ) << 8) +  ( ((unpacked[18* i +  5])       )     ) ) >> 2 ),
		/* 2 */	( ( ((unpacked[ 18* i + 8] & 0x0F ) << 16) + ((unpacked[18* i +  7] ) << 8 ) + (unpacked[18*i + 6]) ) >> 7)  ,
		/* 3 */	( ( ((unpacked[ 18* i + 9] & 0xF) << 8) + (unpacked[18* i +  8]) ) >> 4 ),
		/* 4 */	( ( ((unpacked[18* i + 10] & 0xF) << 8) + (unpacked[18* i +  9]) ) >> 4 ),
		/* 5 */	( ( ((unpacked[18* i + 11] & 0xF) << 8) + (unpacked[18* i + 10]) ) >> 4 ),
		/* 6 */	( ( ((unpacked[18* i + 12] & 0xF) << 8) + (unpacked[18* i + 11]) ) >> 4 ),
		/* 7 */	( ( ((unpacked[18* i + 13]      ) << 8) + (unpacked[18* i + 12]) ) >> 4 ), 
		/* 8 */	    ((unpacked[18* i + 16] >> 1 ) )
		};

		// Lets try decode FX ID and group
		int FXID=(unpacked[18*i + 1] & 15)*256 + unpacked[18*i];
		int FXGroup;
		
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
		for (j = 0; j < 9; j++)
		{
			printf("\tP%d = %4d (%02x)", j+1, p[j], p[j]);
		}
	}
	cout << endl;

	printf("NumFX = %2d (%02x)\n", (unpacked[109] ) >> 2, (unpacked[109] ) >> 2);
		cout << endl;
	BYTE FXWindow = 6 - (((unpacked[109] & 0x3) << 2) + ((unpacked[108] & 0xc0) >> 6));
	printf("NumFX Seen = %2d Cursor Position %d\n", numFXSeen, FXWindow);
	int tapTempo = (((unpacked[110] )<<4) + ( (unpacked[109]& 0xF0) >> 4)) >> 1;
	printf("TapTempo = %2d (%02x)\n", tapTempo, tapTempo);
	printf("%02x %02x\n", unpacked[109], unpacked[110]);
	cout << endl;

	cout << sysex.size() << " bytes in, " << unpacked.size() <<" bytes out\n";

	return unpacked;
}