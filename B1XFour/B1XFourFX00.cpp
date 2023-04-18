#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
#include <bitset>
#include <cstdio>
#include <cstring>

using namespace std;
typedef unsigned char BYTE;

struct MyFileException : public exception {
   const char * what () const throw () {
      return "File size Exception";
   }
};
size_t l_padding	= 72;
size_t l_pad 		=  6;
size_t l_p8 		=  8;
size_t l_p7 		=  8;
size_t l_p6 		=  8;
size_t l_p5 		=  12;
size_t l_p4 		=  12;
size_t l_p3 		=  12;
size_t l_p2 		=  12;
size_t l_p1 		=  12;
size_t l_unknown	=  1;
size_t l_id			=  28;
size_t l_enabled	=  1;

size_t o_padding 	=  0;
size_t o_pad 		=  o_padding + l_padding;
size_t o_p8 		=  o_pad + l_pad;
size_t o_p7 		=  o_p8 + l_p8;
size_t o_p6 		=  o_p7 + l_p7;
size_t o_p5 		=  o_p6 + l_p6;
size_t o_p4 		=  o_p5 + l_p5;
size_t o_p3 		=  o_p4 + l_p4;
size_t o_p2 		=  o_p3 + l_p3;
size_t o_p1 		=  o_p2 + l_p2;
size_t o_unknown	=  o_p1 + l_p1;
size_t o_id			=  o_unknown + l_unknown;
size_t o_enabled	=  o_id + l_id;

typedef struct t_bits {
		bitset<72> 	blank;
		bitset<6> 	pad;
		bitset<8> 	p8;
		bitset<8> 	p7;
		bitset<8> 	p6;
		bitset<12> 	p5;
		bitset<12> 	p4;
		bitset<12> 	p3;
		bitset<12> 	p2;
		bitset<12> 	p1;
		bitset<1> 	t;
		bitset<28> 	id;
		bitset<1> 	onoff;
} myBits;


void pValue(BYTE *b, size_t offset, size_t len)
{
	printf("%s", b[offset] == 0 ? "0" : "1");
	for (size_t i = offset + 1; i < offset + len; i++)
	{
		printf("%s", b[i] == 0 ? "0" : "1");
	}
	printf("\n");
}

void dumpValue(BYTE *v)
{
	// v is 24 byte char
	// p8 is 8 bits at bits 72 + 6 -1 to 72 + 6 - 1 + 8
	BYTE raw[192];
	for (size_t i = 0; i < 24; i++)
	{
		for(size_t j = 0; j < 8; j++)
		{
			raw[i * 8 + j ] = ( (v[i] & (1 << (8 - j))) ? 1 : 0);
		}
	}
	bitset<192> mb;
	memmove(&mb, v, 24);
	BYTE b[192];
	printf("DUMPING\n");
	for (size_t i = 0; i < 192; i++)
	{
		if (i % 8 == 0) printf("\n");
		printf("%s", mb[i] == 0 ? "0" : "1");
		b[i] = mb[i];
	}
	printf("\nEND\n");
	pValue(b, o_p8, l_p8);
	pValue(b, o_p7, l_p7);
	pValue(b, o_p6, l_p6);
	pValue(b, o_p5, l_p5);
	pValue(b, o_p4, l_p4);
	pValue(b, o_p3, l_p3);
	pValue(b, o_p2, l_p2);
	pValue(b, o_p1, l_p1);
	pValue(b, o_unknown, l_unknown);
	pValue(b, o_id, l_id);
	pValue(b, o_enabled, l_enabled);

	bool same = true;
	for (size_t i = 0; i < 192; i++)
	{
		same = same && (b[i] == raw[i]);
		if (same == false) {
			printf("Different at %d\n", i);
			break;
		}
	}
}

int getValue(BYTE *v, size_t offset, size_t len)
{
	int retval = 0;
	static bool local_debug = false;
	// v is 24 byte char
	// p8 is 8 bits at bits 72 + 6 -1 to 72 + 6 - 1 + 8
	if (local_debug == true)
	{
		printf("Offset = %ld ", offset);
		printf("Len %ld\n", len);
	}
	if ((offset >= 8 * 24) || (offset + len > 8 * 24)) 
	{
		printf("Hit limit\n");
		return retval;
	}

	BYTE mb[192];
	for (size_t i = 0; i < 24; i++)
	{
		for(size_t j = 0; j < 8; j++)
		{
			mb[i * 8 + j ] = ( (v[i] & (1 << (7 - j))) ? 1 : 0);
		}
	}

	retval = mb[offset];
	if (local_debug == true) printf("%s", mb[offset] == 0 ? "0" : "1");
	for (size_t i = offset + 1; i < offset + len; i++)
	{
		if (local_debug == true) printf("%s", mb[i] == 0 ? "0" : "1");
		retval = (retval << 1) + mb[i];
	}
	if (local_debug == true) printf("\n");
	return retval;
}

typedef union t_int {
	int x;
	BYTE v[4];
	struct t_2short {
		short fx;
		short id;
	} s;
} myInt;

vector<BYTE> unpack (vector<BYTE> &vi);

vector<BYTE> unpack ( vector<BYTE> &sysex )
{
	int j = 0;
	vector<BYTE>	unpacked;

	// Check this is the right sysex
	bool rightSysex = 
		sysex[0] == 0xF0 &&
		sysex[1] == 0x52 &&
		sysex[2] == 0x00 &&
		(sysex[3] == 0x6e // B1XFour?? Add more IDs here
	       		|| 
		 sysex[3] == 0x6e // B1XFour my pedal 
		) &&
		sysex[4] == 0x64
        && sysex[5] == 0x06;

	if (!rightSysex)
	{
		cout << "Sorry I do not recognize this sysex. Your pedal ID is ";
		printf("%02x", sysex[3]);
		cout << ". Exiting\n";
		exit(-1);
	}

	// We expect this unpacked sysex to start from byte 6 (0 bias)
    // 0x64 0x06 is an unpacked format
    for (size_t i = 0; i < sysex.size() - 6 - 1; i++)
    {
        unpacked.push_back(sysex[i+6]);
    }

    // Name of FX is first 12 chars
    printf("Patch name\n");
	for (j = 0; j < 12; j++)
	{
		printf("%c", unpacked[j]);
	}
	printf("\n");
    // so if 06, then we seem to get 06 near end
    // and   0b, then we seem to get 05 ... 6 + 5 == 11 = b?
    printf("[%d]: (%02x)\n",
				30, unpacked[30]);
	// seems param values start 33,34,35, 36 and ++1 until end
    // 0b 00 00 00 50 00 00 00 00 0a 00
    // [ val     ] [ max     ] [ ??] end
	// we seed at 44 but for default there are less than 44 chars!
    for (size_t i = 44; i < unpacked.size() - 8; i += 11)
    {
        for (int bias = -2; bias < 8; bias += 2)
		{
			if (bias == -2 )
			{
				printf("MAX\n");				
			} else if (bias == 0)
			{
				printf("Current\n");
			} else {
				printf("\n");
			}
        	printf("\t[%3d, %3d]: (%02x) (%02x) = %4d\n",
				bias + i, bias + i +1,
                unpacked[bias + i], unpacked[bias + i+1],
                (unpacked[bias + i+1] << 8) + unpacked[bias + i] );
		}
    }
    // so if 06 01, then we seem to get 06 00 near end
    // and   0b 01, then we seem to get 05 00 ... 6 + 5 == 11 = b?

    printf("[%d]: (%02x)\n",
				unpacked.size() - 5,
				unpacked[unpacked.size() - 5]);

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
	// ofstream out_f(argv[1], ios::out | ios::binary);

	vector<BYTE> vo;
	vector<BYTE> vi = readFile(argv[1]);

	cout << "INPUT\n";
	int ctr = 0;
	for(auto i: vi)
	{
		if (ctr == 6) cout << endl;
		if (ctr > 6 && ((ctr - 6) % 16 == 0)) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;

	vo = unpack (vi);

	ctr = 0;
	// we expect 22 bytes then rest.
	cout << "OUTPUT\n";
	for (auto i: vo)
	{
		if (ctr % 22 == 0) cout << endl;
		ctr++;
		int value = i;
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) value) << " ";
	}
	cout << endl;
	return 0;
}