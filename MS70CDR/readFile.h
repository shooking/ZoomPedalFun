#ifndef READFILE_H
    #define READFILE_H
    #include <fstream>
    #include <iostream>
    #include <iomanip>
    #include <iterator>

    #include <string>
    #include <cmath>
    #include <vector>
    using namespace std;
    typedef unsigned char BYTE;


    vector<BYTE> readFile(const char* filename);
#endif