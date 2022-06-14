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

#include "unpack.h"
#include "pack.h"
#include "readFile.h"
#include "writeFile.h"

vector<BYTE> unpack (vector<BYTE> &vi);
vector<BYTE> pack (vector<BYTE> &vi);
vector<BYTE> readFile(char* filename);
int writeFile(vector<BYTE> &packed, char* filename);

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

	printf("NumFX = %2d (%02x)\n", (unpacked[90] & 0xF0) >> 5, (unpacked[90] & 0xF0) >> 5);
		cout << endl;
	printf("Volume = %2d (%02x)\n", unpacked[91], unpacked[91]);
		cout << endl;
	int tapTempo = (((unpacked[110] )<<4) + ( (unpacked[109]& 0xF0) >> 4)) >> 1;
	printf("TapTempo = %2d (%02x)\n", tapTempo, tapTempo);
	printf("%02x %02x\n", unpacked[109], unpacked[110]);
	// I think to reverse this tempo
	// newT = tempo * 2; (newT & 0xF0) >> 4 gets bitwise OR in 110
	// (newT & 0x0F) << 4 and bitwise OR into 109 then Xform back to normal space`
	cout << endl;

	cout << sysex.size() << " bytes in, " << unpacked.size() <<" bytes out\n";

	return unpacked;
}


vector<BYTE> pack ( vector<BYTE> &unpacked, int newTempo )
{
	// patch the tempo in unpacked (8 bit) space
	int offset = 0;

	BYTE by109 = unpacked[109];
	BYTE by110 = unpacked[110];

	// 0x80 = 10000000
	// 0x07 = 00000111
	// 0x0F = 00001111
	// 0xE0 = 11100000
	// 0xF8 = 11111000
	unpacked[109] = (by109 & 0x80) + ((newTempo & 0x07) << 5) + (by109 & 0x0F);
	unpacked[110] = (by110 & 0xE0) + (((newTempo & 0xF8)<<1) >> 4);

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
	// now we need to pick up the spares
	// https://github.com/Barsik-Barbosik/Zoom-Firmware-Editor/issues/16
	packed.push_back(0xF7);
	return packed;
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
    // cout << "vec was " << vec.size() << endl;
    file.close();
    return vec;
}

int writeFile(vector<BYTE> &packed, const char* filename)
{
    // open the file:
    ofstream output_file(filename, ios::binary | ios::out);

    // write the data:
    ostream_iterator<BYTE> output_iterator(output_file);
    copy(packed.begin(), packed.end(), output_iterator);
    output_file.close();
    return 1;
}


int
main (int argc, char **argv)
{

	if (argc != 3) {
		cout << "Usage: " << argv[0] << " sysexfile tempo" << endl;	
		exit(1);
 	}
	/* read the file in, strip off header and F7 */

	cout << "Infile: " << argv[1] << endl;

	int newTempo;
	istringstream ss(argv[2]);

	if (!(ss >> newTempo)) {
		cerr << "Invalid tempo: needs to be in [40, 250]\n";
	} else if (!ss.eof()) {
		cerr << "Trailing characters after number\n";
	}
	
	if (newTempo < 40 || newTempo > 250) {
		cout << "Sorry tempo must be between 40 and 250." << endl;
		cerr << "Invalid tempo: needs to be in [40, 250]\n";
		exit(1);
	} 

	cout << "Reading file " << argv[1] << endl;

	vector<BYTE> vi = readFile(argv[1]);

	vector<BYTE> unpacked;
	cout << "Unpacking" << endl;
	unpacked = unpack (vi);

	int ctr = 0;
	// we expect 5 x 18 bytes then rest.
	cout << "OUTPUT\n";
	for (int i=0; i<18; i++)
	{
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) i) << " ";
	}
	for (auto i: unpacked)
	{
		if (ctr % 18 == 0) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;

	vector<BYTE> repacked;
	cout << "Packing with " << newTempo << endl;
	repacked = pack(unpacked, newTempo);
	const char *outfile = "NEWTEMPO.bin";
    cout << "Writing file " << outfile << endl;
	writeFile(repacked, outfile);
	cout << endl;
	return 0;
}
