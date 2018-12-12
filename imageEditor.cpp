#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <numeric>
#include <cmath>
#include "RGB.h"
#include "functions.cpp"

using namespace std;

int main() {
    bool read1, read2;
    int maxPixels;
    string type;
    vector<vector<int> > imageP2;
    vector<vector<RGB> > imageP3;
    vector<vector<RGB> > f1, f2;

    read1 = readFile(imageP2, f1, maxPixels, type);
    read2 = readFile(imageP2, f2, maxPixels, type);

    filters(f1, type, chooseFilter(2));
    filters(f2, type, chooseFilter(2));

    imageP3 = unify(f1, f2);

    print(imageP2, imageP3, maxPixels, type, read1);

    return 0;
}