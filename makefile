editor.o : ./source/imageEditor.cpp
	g++  ./source/imageEditor.cpp -w --std=c++11 -O3 -o main.out && ./main.out

clean:
	rm -f -r *.out *.o