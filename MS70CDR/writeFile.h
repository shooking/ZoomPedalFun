#ifndef WRITEFILE_H
    #define WRITEFILE_H
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
    int writeFile(vector<BYTE> &packed, const char* filename);
#endif