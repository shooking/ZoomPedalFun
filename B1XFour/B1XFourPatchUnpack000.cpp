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
#include <cstdint>

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
			printf("Different at %ld\n", i);
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
	// Unpack data 7bit to 8bit, MSBs in first byte
	//data = bytearray(b"")
	int loop = -1;
	uint8_t hibits = 0;

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
		sysex[4] == 0x28;

	if (!rightSysex)
	{
		cout << "Sorry I do not recognize this sysex. Your pedal ID is ";
		printf("%02x", sysex[3]);
		cout << ". Exiting\n";
		exit(-1);
	}

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

	/*
	** OK so B1XFour seems to have
	**
	** 50 54 43 46 == PTCF
	** 54 58 4a 31 == TXJ1
	** 54 58 45 31 == TXE1
	** 45 44 54 42 == EDTB
	** 50 50 52 4d == PPRM // seems to be a couple
	*/
	// Look for where the above are
	int PTCFstart=-1;
	int TXJ1start=-1;
	int TXE1start=-1;
	int EDTBstart=-1;
	int PPRMstart=-1;
	
	for (unsigned int i = 0; i < unpacked.size() - 4; i++)
	{
		if (
			unpacked[i]   == 0x50 && unpacked[i+1] == 0x54 &&
			unpacked[i+2] == 0x43 && unpacked[i+3] == 0x46
			)
		{
			PTCFstart = i + 4;
		}
		else if 
		(
			unpacked[i]   == 0x54 && unpacked[i+1] == 0x58 &&
			unpacked[i+2] == 0x4a && unpacked[i+3] == 0x31
		)
		{
			TXJ1start = i + 4;
		}
		else if 
		(
			unpacked[i]   == 0x54 && unpacked[i+1] == 0x58 &&
			unpacked[i+2] == 0x45 && unpacked[i+3] == 0x31
		)
		{
			TXE1start = i + 4;
		}
		else if 
		(
			unpacked[i]   == 0x45 && unpacked[i+1] == 0x44 &&
			unpacked[i+2] == 0x54 && unpacked[i+3] == 0x42
		)
		{
			EDTBstart = i + 4;
		}
		else if 
		(
			unpacked[i]   == 0x50 && unpacked[i+1] == 0x50 &&
			unpacked[i+2] == 0x52 && unpacked[i+3] == 0x4d
		)
		{
			printf("Seen PPRM start\n");
			PPRMstart = i + 4;
		}
	}

	if (PTCFstart != -1) 
	{
		myInt a;
		printf("Patch name\n");
		for (j = PTCFstart+22; j < PTCFstart + 22 + 10; j++)
		{
			printf("%c", unpacked[j]);
		}
		printf("\n");
		for (int i=0; i<4; i++)
		{
			a.v[i] = unpacked[PTCFstart + 8 + i];
		}
		printf("FX: %d\n", a.x);
		for (int jj = 0; jj < 5; jj++)
		{
			for (int i=0; i<4; i++)
			{
				a.v[i] = unpacked[PTCFstart + 8 + 4 + 10 + 10 + 4 * jj + i];
			}
			/*
			** Both big and little endian form. Seems to be "a" form
			** printf("FX: %d (%08x) %d (%08x)\n", a.x, a.x, b.x, b.x);
			*/
			printf("FX: %d (%08x)\tFXID: %4d (%04x)\tFXGP: %4d (%04x)\n",
				a.x, a.x,
				a.s.fx,
				a.s.fx,
				a.s.id / 256,
				a.s.id / 256);
		}
	}
	
	if (TXJ1start != -1) 
	{
		myInt a;
		for (int i=0; i<4; i++)
		{
			a.v[i] = unpacked[TXJ1start + i];
		}
		printf("\tTXJ1 Length: %d\n", a.x);
		for (int i = 0; i <  a.x; i++)
		{
			if (i % 16 == 0) printf("\n");
			printf("%02x (%c)", unpacked[TXJ1start + 4 + i], unpacked[TXJ1start + 4 + i]);
		}
		printf("\n");

	}

	if (TXE1start != -1) 
	{
		myInt a;
		for (int i=0; i<4; i++)
		{
			a.v[i] = unpacked[TXE1start + i];
		}
		printf("\tTXE1 Length: %d\n", a.x);
		for (int i=0; i < a.x; i++)
		{
			printf("%c", unpacked[TXE1start + 4 + i]);
		}
		printf("\n");
	}

	if (EDTBstart != -1) 
	{
		myInt a;

		for (int i=0; i<4; i++)
		{
			a.v[i] = unpacked[EDTBstart + i];
		}
		printf("\tEDBT Length: %d\n", a.x);

		bitset<192> mb;
		BYTE v[24];

		for (j = 0; j < 5; j++)
		{

			for (int i=0; i<24; i++)
			{
				v[24 - 1 - i] = unpacked[EDTBstart + 4 + j * 24 + i];
			}

			for (int i=0; i<24; i++)
			{
				printf("%02x ", v[i]);
			}
			printf("\n");

			// TO DO - I should process the raw data into byte array
			// since bit array seems problematic
			// do it once and use it to lookup values.

			int my_p8 		= getValue(v, o_p8, l_p8);
			int my_p7 		= getValue(v, o_p7, l_p7);
			int my_p6 		= getValue(v, o_p6, l_p6);
			int my_p5 		= getValue(v, o_p5, l_p5);
			int my_p4 		= getValue(v, o_p4, l_p4);
			int my_p3 		= getValue(v, o_p3, l_p3);
			int my_p2 		= getValue(v, o_p2, l_p2);
			int my_p1		= getValue(v, o_p1, l_p1);
			int my_unknown	= getValue(v, o_unknown, l_unknown);
			int my_id		= getValue(v, o_id, l_id);
			a.x = my_id;
			int my_enabled 	= getValue(v, o_enabled, l_enabled);
			
			printf("Enabled: %s\n", (my_enabled == 1)? "true" : "false");
			printf("Unknown: %d\n", my_unknown);
			
			printf("P1: %d\n", my_p1);
			printf("P2: %d\n", my_p2);
			printf("P3: %d\n", my_p3);
			printf("P4: %d\n", my_p4);
			printf("P5: %d\n", my_p5);
			printf("P6: %d\n", my_p6);
			printf("P7: %d\n", my_p7);
			printf("P8: %d\n", my_p8);
			printf("FX: %d (%08x)\tFXID: %4d (%04x)\tFXGP: %4d (%04x)\n",
				a.x, a.x,
				a.s.fx,
				a.s.fx,
				a.s.id / 256,
				a.s.id / 256);

			// used for diagnostics and debugging
			// dumpValue(v);
		}
	}
	
	if (PPRMstart != -1)
	{
		myInt a;

		for (int i=0; i<4; i++)
		{
			a.v[i] = unpacked[PPRMstart + i];
		}
		printf("\tPPRM Length: %d\n", a.x);
		for (int i = 0; i <  a.x; i++)
		{
			if (i % 16 == 0) printf("\n");
			printf("%02x ", unpacked[PPRMstart + 4 + i]);
		}
		printf("\n");

		for (int i = 0; i <  a.x; i++)
		{
			printf("%c", unpacked[PPRMstart + 4 + i]);
		}
		printf("\n");

	}
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
