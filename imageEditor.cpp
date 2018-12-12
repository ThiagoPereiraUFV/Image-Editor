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
    bool read;
    int maxPixels;
    string type;
    vector<vector<int> > imageP2;
    vector<vector<RGB> > imageP3, f1, f2;

    read = readFile(imageP2, imageP3, maxPixels, type);
    f1.resize(imageP3.size(), vector<RGB> (imageP3[0].size()));
    f2 = f1;

    maskP3(f1, imageP3, type, chooseFilter(0));
    maskP3(f2, imageP3, type, chooseFilter(1));

    imageP3 = unify(f1, f2);
    print(imageP2, imageP3, maxPixels, type, read);

    return 0;
}
