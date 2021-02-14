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

	vector<BYTE>	unpacked;

	// Check this is the right sysex
	bool rightSysex = 
		sysex[0] == 0xF0 &&
		sysex[1] == 0x52 &&
		sysex[2] == 0x00 &&
		(sysex[3] == 0x63 // G1On?? Add more IDs here
	       		|| 
		 sysex[3] == 0x65 // B1On my pedal 
		) &&
		sysex[4] == 0x28;

	if (!rightSysex)
	{
		cout << "Sorry I do not recognize this sysex. Your pedal ID is ";
		printf("%02x", sysex[3]);
		cout << ". Exiting\n";
		exit(-1);
	}
	// f0 52 00 65|63 28
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
    // cout << "vec was " << vec.size() << endl;
    file.close();
    return vec;
}

int
main (int argc, char **argv)
{
	/* read the file in, strip off header and F7 */

	if (argc != 3)
	{
		cout << "Usage: " << argv[0] << " patchfilename patchNumber " << endl;
		exit(-1);
	}
	ifstream in_f(argv[1], ios::in | ios::binary);
	// ofstream out_f(argv[1], ios::out | ios::binary);

	vector<BYTE> vo;
	vector<BYTE> vi = readFile(argv[1]);

	vo = unpack (vi);

	// we expect 5 x 18 bytes then rest.
	cout << argv[2] << " " ;
	// Here was ONLY want the name.
	// We know the ID from the caller
	// So we will get PatchName[i] = Name
	for (int j = 0; j < 10; j++)
	{
		cout << vo[vo.size() - 11 + j] ;
	}
	cout << endl;

	return 0;
}
