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
	for (int i=0; i<18; i++)
	{
		cout << setfill ('0') << setw (2) << hex << (0xff & (BYTE) i) << " ";
	}
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
