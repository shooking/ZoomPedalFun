#include <iostream>
#include <fstream>
#include <iomanip>
#include <iterator>

#include <string>
#include <cmath>
#include <vector>
#include <sstream>
#include <cstdint>

#include "pack.h"
#include "unpack.h"
#include "readFile.h"
#include "writeFile.h"


int
main (int argc, char **argv)
{

	// probably better to load a ZDL and get the info from that?
	// for the moment I allow slot, FXID, GID
	if (argc != 5) {
		cout << "Usage: " << argv[0] << " sysexfile FXSlot FXID GID" << endl;	
		exit(1);
 	}
	/* read the file in, strip off header and F7 */

	cout << "Infile: " << argv[1] << endl;

	int slot;
	istringstream ss(argv[2]);

	if (!(ss >> slot)) {
		cerr << "Error parsing slot\n";
	} else if (!ss.eof()) {
		cerr << "Trailing characters after number\n";
	}
	
	if (slot < 1 || slot > 6) {
		cout << "Sorry slot must be in [1, 6]" << endl;
		exit(1);
	} 

	int fxid;
	istringstream ss1(argv[3]);

	if (!(ss1 >> fxid)) {
		cerr << "Invalid fxid:\n";
	} else if (!ss1.eof()) {
		cerr << "Trailing characters after number\n";
	}

	int gid;
	istringstream ss2(argv[4]);

	if (!(ss2 >> gid)) {
		cerr << "Invalid gid:\n";
	} else if (!ss2.eof()) {
		cerr << "Trailing characters after number\n";
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
	// pass in a 0 tempo => dont reset it
	BYTE tempo = 0;
	repacked = pack(unpacked, tempo, slot, fxid, gid);
	const char *outfile = "NEWSLOT.bin";
    cout << "Writing file " << outfile << endl;
	writeFile(repacked, (const char *)outfile);
	cout << endl;
	return 0;
}
