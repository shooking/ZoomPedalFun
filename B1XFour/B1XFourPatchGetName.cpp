#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
using namespace std;
typedef unsigned char BYTE;

vector<BYTE> unpack (vector<BYTE> &vi);

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
		int FXGroup= (
				 (unpacked[18*i + 3] & 15) * 16 + 
				 (unpacked[18*i + 2] & 240) / 16) / 2;
		cout << endl;
		printf("[%d][%d][%d][%d]\n", 
				unpacked[18*i + 0], 
				unpacked[18*i + 1], 
				unpacked[18*i + 2], 
				unpacked[18*i + 3]);
		printf("FXID[%d] (%s)= %d (%02x), GROUPID = %d (%02x)\n",
			       i+1,
			       (FXID & 1) == 0 ? "OFF" : "ON",
			       FXID / 32,
			       FXID / 32,
			       FXGroup,
			       FXGroup);		       
		cout << endl;
		for (j = 0; j < 9; j++)
		{
			printf("FX%d P%d = %d (%02x) ", i+1, j+1, p[j], p[j]);
		}
		cout << endl;
	}

	printf("Volume = %d (%02x)\n", unpacked[91], unpacked[91]);

	for (j = 0; j < 10; j++)
	{
		cout << unpacked[unpacked.size() - 11 + j] ;
	}
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
