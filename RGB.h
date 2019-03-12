#ifndef RGB_H
#define RGB_H

#include <iostream>
using namespace std;

class RGB{
    public:
        RGB(const int R, const int G, const int B) : R(R), G(G), B(B) {};
        RGB(const RGB &obj) {   *this = obj;    }
        RGB() : R(0), G(0), B(0) {};
        ~RGB() {};
        RGB &operator=(const RGB &obj) {
            if(this == &obj)
                return *this;

            this->R = obj.R;
            this->G = obj.G;
            this->B = obj.B;

            return *this;
        }
        RGB &operator=(const int &obj) {
            this->R = obj;
            this->G = obj;
            this->B = obj;

            return *this;
        }
        RGB &operator+=(const int &obj) {
            this->R += obj;
            this->G += obj;
            this->B += obj;

            if(this->R > 255)
                this->R = 255;

            if(this->G > 255)
                this->G = 255;

            if(this->B > 255)
                this->B = 255;

            return *this;
        }
        RGB &operator-=(const int &obj) {
            this->R -= obj;
            this->G -= obj;
            this->B -= obj;

            if(this->R < 0)
                this->R = 0;

            if(this->G < 0)
                this->G = 0;

            if(this->B < 0)
                this->B = 0;

            return *this;
        }
        RGB operator*(const int &obj) const{
            RGB aux(0, 0, 0);

            aux.R = (this->R)*(obj);
            aux.G = (this->G)*(obj);
            aux.B = (this->B)*(obj);

            return aux;
        }
        bool operator>(const int &obj) const{
            return ((this->R > obj) || (this->G > obj) || (this->B > obj));
        }
        bool operator<(const int &obj) const{
            return ((this->R < obj) || (this->G < obj) || (this->B < obj));
        }
        friend ostream &operator<<(ostream &stream, const RGB &obj) {
            stream << obj.R << " " << obj.G << " " << obj.B;

            return stream;
        }
        friend istream &operator>>(istream &stream, RGB &obj) {
            stream >> obj.R >> obj.G >> obj.B;

            return stream;
        }
        friend RGB operator-(const int &i, const RGB &obj) {
            return RGB(i - obj.R, i - obj.G, i - obj.B);
        }
        int R, G, B;
};

#endif
