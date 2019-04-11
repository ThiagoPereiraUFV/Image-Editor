int avg(const int x1, const int x2, const int option) {
    switch(option) {
        case 1: {
            return sqrt(x1*x2);
            break;
        }
        case 2: {
            return sqrt(x1*x1 + x2*x2);
            break;
        }
        default: {
            return (x1 + x2)/2;
            break;
        }
    }
}

template <class t>
void readImage(t &image, fstream &inputImage) {
    for(int i = 0; i < image.size(); i++)
        for(int j = 0; j < image[i].size(); j++)
            inputImage >> image[i][j];
}

bool readFile(vector<vector<int> > &imageP2, vector<vector<RGB> > &imageP3, int &maxPixels, string &type, const string path) {
    fstream inputImage(path, fstream::in);
    int height, width;

    if(inputImage.is_open()) {
        inputImage >> type;

        if(type != "P2" && type != "P3") {
            cerr << "This file isn't supported yet!\n";
            return false;
        }

        string line;
        inputImage >> line;

        if(line[0] != '#') {
            stringstream number(line);
            number >> width;
        }
        else {
            getline(inputImage, line);
            inputImage >> width;
        }
    
        inputImage >> height >> maxPixels;
    }
    else {
        cerr << "The picture couldn't be read!\n";
        return false;
    }

    if(type == "P2") {
        imageP2.resize(height, vector<int>(width));
        readImage(imageP2, inputImage);
    }
    else    if(type == "P3") {
                imageP3.resize(height, vector<RGB>(width, RGB(0, 0, 0)));
                readImage(imageP3, inputImage);
            }
    inputImage.close();

    return true;
}

template <class t>
void printImage(const t &image, const int maxPixels, const string &type, const string path) {
    fstream outputImage(path, fstream::out);

    if(type == "P2") {
        outputImage << "P2\n" << image[0].size() << ' ' << image.size() << '\n' << maxPixels << '\n';
    }   
    else    if(type == "P3")
                outputImage << "P3\n" << image[0].size() << ' ' << image.size() << '\n' << maxPixels << '\n';
    
    for(int i = 0; i < image.size(); i++){
        for(int j = 0; j < image[i].size(); j++)
            outputImage << image[i][j] << " ";
        outputImage << '\n';
    }

    outputImage.close();
}

void print(const vector<vector<int> > &imageP2, const vector<vector<RGB> > &imageP3, const int &maxPixels, const string &type, const bool read, const string path) {
    if(read && type == "P2")
            printImage(imageP2, maxPixels, type, path);
    else    if(read && type == "P3")
                printImage(imageP3, maxPixels, type, path);
            else
                cerr << "Image couldn't be printed" << endl;
}

template <class t>
void brighten(t &image, const string &type, const int factor) {
    if(type == "P2") {
        for(int i = 0; i < image.size(); i++)
            for(int j = 0; j < image[i].size(); j++) {
                image[i][j] += factor;
                if(image[i][j] > 255)
                    image[i][j] = 255;
            }
    }
    else    if(type == "P3") {
                for(int i = 0; i < image.size(); i++)
                    for(int j = 0; j < image[i].size(); j++){
                        image[i][j] += factor;
                    }
            }
}

template <class t>
void darken(t &image, const string &type, const int factor) {
    if(type == "P2") {
        for(int i = 0; i < image.size(); i++)
            for(int j = 0; j < image[i].size(); j++) {
                image[i][j] -= factor;
                if(image[i][j] < 0)
                    image[i][j] = 0;
            }
    }
    else    if(type == "P3") {
                for(int i = 0; i < image.size(); i++)
                    for(int j = 0; j < image[i].size(); j++){
                        image[i][j] -= factor;
                    }
            }
}

template <class t>
void negative(t &image) {
    for(int i = 0; i < image.size(); i++)
        for(int j = 0; j < image[i].size(); j++)
            image[i][j] = 255-image[i][j];
}

template <class t>
vector<vector<int> > grayScale(const t &image, string &type) {
    vector<vector<int> > gs(image.size(), vector<int> (image[0].size()));

    if(type == "P3") {
        for(int i = 0; i < image.size(); i++)
            for(int j = 0; j < image[i].size(); j++){
                gs[i][j] = (image[i][j].R + image[i][j].G + image[i][j].B)/3;
            }
    }

    type = "P2";
    return gs;
}

template <class t>
void blackAndWhite(t &image) {
    for(int i = 0; i < image.size(); i++)
        for(int j = 0; j < image[i].size(); j++){
            if(image[i][j] > 127)
                image[i][j] = 255;
            else
                image[i][j] = 0;
        }
}

template <class t>
void mirror(t &image) {
    for(int i = 0; i < image.size(); i++)
        for(int j = 0, k = image[i].size()-1; j < k; j++, k--)
            swap(image[i][j], image[i][k]);
}

template <class t>
void rotate(vector<vector<t> > &image) {
    vector<vector<t> > rotated(image[0].size(), vector<t> (image.size()));

    for(int i = 0, k = image.size()-1; i < image.size(); i++, k--)
        for(int j = 0; j < image[i].size(); j++)
            rotated[j][k] = image[i][j];

    image = rotated;
}

vector<vector<int> > chooseFilter(const int option) {
    switch(option) {
        case 0: {   //Gy mask
            return vector<vector<int> > ({{1, 2, 1}, {0, 0, 0}, {-1, -2, -1}});
            break;
        }
        case 1: {   //Gx mask/Sobel operator
            return vector<vector<int> > ({{1, 0, -1}, {2, 0, -2}, {1, 0, -1}});
            break;
        }
        case 2: {   //Highlight operator
            return vector<vector<int> > ({{0, -1, 0}, {-1, 5, -1}, {0, -1, 0}});
            break;
        }
        case 3: {   //LaPlace operator
            return vector<vector<int> > ({{0, -1, 0}, {-1, 4, -1}, {0, -1, 0}});
            break;
        }
        default: {  //Standard
            return vector<vector<int> > ({{1, 1, 1}, {1, 1, 1}, {1, 1, 1}});
            break;
        }
    }
}

void maskP2(vector<vector<int> > &newP2, const vector<vector<int> > &image, const string &type, const vector<vector<int> > &filter) {
    if(type == "P2") {
        for(int i = 0; i < image.size(); i++)
            for(int j = 0; j < image[i].size(); j++) {
                vector<int> f;
                f.push_back(image[i][j]*filter[1][1]);
                
                if(i-1 >= 0 && j-1 >= 0)
                    f.push_back(image[i-1][j-1]*filter[0][0]);
                if(i+1 < image.size() && j+1 < image[i].size())
                    f.push_back(image[i+1][j+1]*filter[2][2]);
                if(i-1 >= 0 && j+1 < image[i].size())
                    f.push_back(image[i-1][j+1]*filter[0][2]);
                if(i+1 < image.size() && j-1 >= 0)
                    f.push_back(image[i+1][j-1]*filter[2][0]);
                if(i-1 >= 0)
                    f.push_back(image[i-1][j]*filter[0][1]);
                if(j-1 >= 0)
                    f.push_back(image[i][j-1]*filter[1][0]);
                if(i+1 < image.size())
                    f.push_back(image[i+1][j]*filter[2][1]);
                if(j+1 < image[i].size())
                    f.push_back(image[i][j+1]*filter[1][2]);

                int sum = accumulate(f.begin(), f.end(), 0);

                if(sum > 255)
                    sum = 255;
                else    if(sum < 0)
                            sum = 0;

                newP2[i][j] = sum;
            }
    }
}

void maskP3(vector<vector<RGB> > &newP3, const vector<vector<RGB> > &image, const string &type, const vector<vector<int> > &filter) {
    if(type == "P3") {
        for(int i = 0; i < image.size(); i++)
            for(int j = 0; j < image[i].size(); j++) {
                vector<RGB> f;
                f.push_back(image[i][j]*filter[1][1]);
                
                if(i-1 >= 0 && j-1 >= 0)
                    f.push_back(image[i-1][j-1]*filter[0][0]);
                if(i+1 < image.size() && j+1 < image[i].size())
                    f.push_back(image[i+1][j+1]*filter[2][2]);
                if(i-1 >= 0 && j+1 < image[i].size())
                    f.push_back(image[i-1][j+1]*filter[0][2]);
                if(i+1 < image.size() && j-1 >= 0)
                    f.push_back(image[i+1][j-1]*filter[2][0]);
                if(i-1 >= 0)
                    f.push_back(image[i-1][j]*filter[0][1]);
                if(j-1 >= 0)
                    f.push_back(image[i][j-1]*filter[1][0]);
                if(i+1 < image.size())
                    f.push_back(image[i+1][j]*filter[2][1]);
                if(j+1 < image[i].size())
                    f.push_back(image[i][j+1]*filter[1][2]);
                
                int sumR = 0, sumG = 0, sumB = 0;

                for(int k = 0; k < f.size(); k++){
                    sumR += f[k].R;
                    sumG += f[k].G;
                    sumB += f[k].B;
                }

                if(sumR > 255)
                    sumR = 255;
                else    if(sumR < 0)
                            sumR = 0;
                            
                if(sumG > 255)
                    sumG = 255;
                else    if(sumG < 0)
                            sumG = 0;

                if(sumB > 255)
                    sumB = 255;
                else    if(sumB < 0)
                            sumB = 0;

                newP3[i][j] = RGB(sumR, sumG, sumB);
            }
    }
}

vector<vector<RGB> > unify(const vector<vector<RGB> > &f1, const vector<vector<RGB> > &f2, const int nAvg) {
    vector<vector<RGB> > final(f1.size(), vector<RGB> (f1[0].size()));

    for(int i = 0; i < f1.size(); i++)
        for(int j = 0; j < f1[i].size(); j++){
            final[i][j].R = avg(f1[i][j].R, f2[i][j].R, nAvg);
            final[i][j].G = avg(f1[i][j].G, f2[i][j].G, nAvg);
            final[i][j].B = avg(f1[i][j].B, f2[i][j].B, nAvg);
        }

    return final;
}

vector<vector<int> > unify(const vector<vector<int> > &f1, const vector<vector<int> > &f2, const int nAvg) {
    vector<vector<int> > final(f1.size(), vector<int> (f1[0].size()));

    for(int i = 0; i < f1.size(); i++)
        for(int j = 0; j < f1[i].size(); j++){
            final[i][j] = avg(f1[i][j], f2[i][j], nAvg);
        }

    return final;
}
