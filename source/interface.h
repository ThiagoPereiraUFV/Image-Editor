#ifndef INTERFACE_H
#define INTERFACE_H

using namespace std;

class   Menu{
    private:
        string path;
        bool read;
        int maxPixels;
        string type;
        vector<vector<int> > imageP2, mask1P2, mask2P2;
        vector<vector<RGB> > imageP3, mask1P3, mask2P3;

    public:
        Menu() {
            system("clear");
            cout << "Write the path where your image is, including name and extension";
            cout << " (write '...' without quotes to open a default picture)\n> ";
            cin >> path;

            if(path == "...")
                read = readFile(imageP2, imageP3, maxPixels, type, "Samples/s.pnm");
            else
                read = readFile(imageP2, imageP3, maxPixels, type, path);
            system("clear");
            cout << "Image Editor v1.0 by Thiago Pereira\n\n";
        }
        void GUI() const{
            cout << "Select one option to customize your image\n\n";
            cout << "1 - Rotate\n";
            cout << "2 - Mirror\n";
            cout << "3 - Brighten\n";
            cout << "4 - Darken\n";
            cout << "5 - Make grayscale\n";
            cout << "6 - Make negative\n";
            cout << "7 - Make black and white\n";
            cout << "8 - Apply filter\n";
            cout << "9 - Save Image\n";
            cout << "10 - Change image\n";
            cout << "11 - Exit\n";
        }
        void selOption() {
            int option;

            while(true) {
                GUI();
                cout << "> ";
                cin >> option;
                switch(option) {
                    case 1:
                        rot();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 2:
                        mir();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 3:
                        system("clear");
                        brig();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 4:
                        system("clear");
                        dark();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 5:
                        gray();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 6:
                        neg();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 7:
                        bw();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 8:
                        system("clear");
                        filter();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 9:
                        system("clear");
                        save();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 10:
                        system("clear");
                        change();
                        system("clear");
                        cout << "Operation finalized!\n\n";
                        break;
                    case 11:
                        system("clear");
                        char c;
                        cout << "Are you sure? Y/N\n";
                        cout << "> ";
                        cin >> c;

                        if(c == 'Y' || c == 'y') {
                            system("clear");
                            exit(0);
                        }
                        system("clear");
                        cout << "Backing to main menu...\n";
                        break;
                    default:
                        system("clear");
                        cout << "Invalid option! Select a valid option\n";
                }
                usleep(900000);
                system("clear");
            }
        }
        void rot() {
            if(type == "P2")
                rotate(imageP2);
            else    if(type == "P3")
                        rotate(imageP3);
        }
        void mir() {
            if(this->type == "P2")
                mirror(imageP2);
            else    if(this->type == "P3")
                        mirror(imageP3);
        }
        void brig() {
            int factor;
            cout << "Enter the wished brighten factor\n> ";
            cin >> factor;

            if(this->type == "P2")
                brighten(imageP2, type, factor);
            else    if(this->type == "P3")
                        brighten(imageP3, type, factor);
        }
        void dark() {
            int factor;
            cout << "Enter the wished darken factor\n> ";
            cin >> factor;
            
            if(this->type == "P2")
                darken(imageP2, type, factor);
            else    if(this->type == "P3")
                        darken(imageP3, type, factor);
        }
        void gray() {
            if(type == "P2")
                cout << "\nThe image already is in grayscale";
            else
                imageP2 = grayScale(imageP3, type);
        }
        void neg() {
            if(type == "P2")
                negative(imageP2);
                else    if(type == "P3")
                            negative(imageP3);
        }
        void bw() {
            if(this->type == "P2")
                blackAndWhite(imageP2);
            else    if(this->type == "P3")
                        blackAndWhite(imageP3);
        }
        void filter() {
            int f;

            cout << "Select your filter by the number:\n";
            cout << "1 - Sobel operator\n";
            cout << "2 - highlight operator\n";
            cout << "3 - LaPlace operator\n";
            cout << "> ";
            cin >> f;

            if(type == "P2") {
                mask1P2.resize(imageP2.size(), vector<int> (imageP2[0].size()));
                mask2P2 = mask1P2;
                maskP2(mask1P2, imageP2, type, chooseFilter(0));
                maskP2(mask2P2, imageP2, type, chooseFilter(f));
                imageP2 = unify(imageP2, mask1P2, 3);
                imageP2 = unify(imageP2, mask2P2, 3);
            }
            if(type == "P3") {
                mask1P3.resize(imageP3.size(), vector<RGB> (imageP3[0].size()));
                mask2P3 = mask1P3;
                maskP3(mask1P3, imageP3, type, chooseFilter(0));
                maskP3(mask2P3, imageP3, type, chooseFilter(f));
                imageP3 = unify(imageP3, mask1P3, 3);
                imageP3 = unify(imageP3, mask2P3, 3);
            }
        }
        void save() const{
            string outPath;

            cout << "\nWrite the path where your image will be saved including its name and extension";
            cout << " (write '...' without quotes to save in a default folder)\n> ";
            cin >> outPath;

            if(outPath == "...")
                print(imageP2, imageP3, maxPixels, type, read, "Samples/out.pnm");
            else
                print(imageP2, imageP3, maxPixels, type, read, outPath);
        }
        void change() {
            cout << "\nWrite the name of your image including path and extension: ";
            cout << "> ";
            cin >> path;
            imageP3.clear();
            imageP2.clear();
            read = readFile(imageP2, imageP3, maxPixels, type, path);
        }
};

#endif
