#ifndef PACK_H
    #define PACK_H
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
    vector<BYTE> pack ( vector<BYTE> &unpacked, int newTempo, int slot, int fxid, int gid);
#endif