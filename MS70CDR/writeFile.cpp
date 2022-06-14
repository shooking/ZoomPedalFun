#include "writeFile.h"

int writeFile(vector<BYTE> &packed, char* filename);


int writeFile(vector<BYTE> &packed, const char* filename)
{
    // open the file:
    ofstream output_file(filename, ios::binary | ios::out);

    // write the data:
    ostream_iterator<BYTE> output_iterator(output_file);
    copy(packed.begin(), packed.end(), output_iterator);
    output_file.close();
    return 1;
}