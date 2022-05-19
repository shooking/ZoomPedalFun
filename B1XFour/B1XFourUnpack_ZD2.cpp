#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
#include <cstdio>
#include <cstring>

using namespace std;
typedef unsigned char BYTE;

struct MyFileException : public exception {
   const char * what () const throw () {
      return "File size Exception";
   }
};

vector<BYTE> unpack (vector<BYTE> &vi);

vector<BYTE> unpack ( vector<BYTE> &sysex )
{
	// Unpack data 7bit to 8bit, MSBs in first byte
	//data = bytearray(b"")
	int loop = -1;
	uint8_t hibits = 0;

	int j = 0;
	unsigned int offset_bias = 0;
	vector<BYTE>	unpacked;

	// look up to 3 chars of 0's before we call time.
	while (sysex[offset_bias] != 0xF0)
	{
		offset_bias++;
		if (offset_bias > 3)
		{
			throw MyFileException();
		}
	}
	cout << "Offset_bias == " << offset_bias << endl;

	// Check this is the right sysex
	bool rightSysex = 
		sysex[0 + offset_bias] == 0xF0 &&
		sysex[1 + offset_bias] == 0x52 &&
		sysex[2 + offset_bias] == 0x00 &&
		(sysex[3 + offset_bias] == 0x6e // B1XFour?? Add more IDs here
	       		|| 
		 sysex[3 + offset_bias] == 0x6e // B1XFour my pedal 
		) &&
		sysex[4 + offset_bias] == 0x60
		&& sysex[5 + offset_bias] == 0x04
        && sysex[6 + offset_bias] == 0x22;

	if (!rightSysex)
	{
		cout << "Sorry I do not recognize this sysex. Your pedal ID is ";
		printf("%02x", sysex[3]);
		cout << ". Exiting\n";
		exit(-1);
	}

	// this is a file block unpacker
	int currByte = 0;
	const int dataLen = sysex[9] + 128 * sysex[10];
	int	expectedBytes = 1 + ceil( (dataLen / 7) ) * 7 ;
	int	theCount = 0;
    // We expect this packed sysex to start from byte 11 (0 bias)
	for (size_t i = 11; i < sysex.size() - 1; i++)
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
			theCount++;
			if (theCount == expectedBytes) break;
		}
		else
		{
			hibits = byt;
			// do we need to acount for short sets (at end of block block)?
			loop = 6;
		}
	}
	printf("Processed: %d Expected: %d\n", theCount, expectedBytes);

	return unpacked;
}

vector<BYTE> readFile(char* filename)
{
	try 
	{

	    // open the file:
	    ifstream file(filename, ios::binary | ios::in);

	    // Stop eating new lines in binary mode!!!
	    file.unsetf(ios::skipws);

	    // get its size:
	    streampos fileSize;

	    file.seekg(0, ios::end);
	    fileSize = file.tellg();
		if (fileSize <= 0) {
			throw MyFileException();
		}
	    file.seekg(0, ios::beg);
		cout << "Filesize: " << fileSize << endl;

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
	catch (const ifstream::failure & e) 
	{
		cout << "Exception opening file " << endl;
		exit(-1);
	}
	catch (MyFileException& e) 
	{
		cout << "Exception " << e.what() << endl;
		exit(-1);
	}
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

	// cout << "file size: " << vi.size() << endl;
	vo = unpack (vi);

    // open a file for the unpacked file
    char outname[100];
	snprintf(outname, sizeof(outname), "%s.unp", argv[1]);
	printf("outname: %s\n", outname);
	ofstream out_f(outname, ios::out | ios::binary);
    // the important part
    for (const auto &e : vo) out_f << e ;
    out_f.close();

	ctr = 0;
	// we expect 26 bytes then rest.
	cout << "OUTPUT\n";
	for (auto i: vo)
	{
		if (ctr % 26 == 0) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;
	return 0;
}