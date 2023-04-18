#include "readFile.h"


vector<BYTE> readFile(const char* filename)
{
    // open the file:
    ifstream file(filename, ios::binary | ios::in);

    // Stop eating new lines in binary mode!!!
    file.unsetf(ios::skipws);

    // get its size:
    streampos fileSize;

    file.seekg(0, ios::end);
    fileSize = file.tellg();
    file.seekg(0, ios::beg);

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
