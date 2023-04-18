#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
using namespace std;
typedef unsigned char BYTE;
#include "readFile.h"
#include "unpack.h"

int
main (int argc, char **argv)
{
	/* read the file in, strip off header and F7 */

	ios oldState(nullptr);
	oldState.copyfmt(cout);

	cout << "Infile: " << argv[1] << endl;
	ifstream in_f(argv[1], ios::in | ios::binary);


	vector<BYTE> vo;
	vector<BYTE> vi = readFile((const char *)argv[1]);

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
	cout << "OUTPUT in reverse byte order\n";
	
	for (int i=17; i> -1; i--)
	{
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) i) << " ";
	}
	cout << endl;
	cout.copyfmt(oldState);

	for (int i=17; i> -1; i--)
	{
		cout << setfill ('0') << setw (2) <<  i << " ";
	}
	cout << endl << endl;

	for (size_t fx=0; fx < 6; fx++)
	{
		for (int i = 17; i > -1; i--)
		{
			cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) vo[i + fx * 18]) << " ";
		}		
		cout.copyfmt(oldState);
		cout << " | " << setfill ('0') << setw (2) << (fx * 18) ;
		cout << " " << setfill ('0') << setw (2) << hex << (fx * 18) ;
		cout << endl;
	}

	int remainderBytes = 18 - (vo.size() % 18);
	for (int i = 0; i < remainderBytes; i++)
	{
		// 3 space pad for 'XX '
		cout << "   ";
		
	}
	for (int i = vo.size() - 1; i > 6*18 - 1; i--)
	{
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) vo[i]) << " ";
		
	}
	cout << endl;
	return 0;
}
