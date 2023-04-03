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
	repacked = pack(unpacked, newTempo, -1, -1, -1);
	const char *outfile = "NEWTEMPO.bin";
    cout << "Writing file " << outfile << endl;
	writeFile(repacked, outfile);
	cout << endl;
	return 0;
}
