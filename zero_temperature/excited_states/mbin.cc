#include "common.h"
#include "bin.h"
#include "base.h"

// reads binary matrices and vectors


void mbin(double **mat, int ndim, char *filename) {
	

    int k, l;


    ifstream infile(filename);
    if (!infile) {
	cout << "\n*** Error opening file " << filename << endl;
	cout << "Execution terminated !" << endl;
	exit(-1);
    }
  
    
    bread(infile, mat, ndim, ndim);
    

    return;

}

void mbin(double **mat, int ndim_1, int ndim_2, char *filename) {
	

    int k, l;


    ifstream infile(filename);
    if (!infile) {
	cout << "\n*** Error opening file " << filename << endl;
	cout << "Execution terminated !" << endl;
	exit(-1);
    }
  
    
    bread(infile, mat, ndim_1, ndim_2);
    

    return;

}

void vbin(double *vec, int ndim, char *filename) {
	

    ifstream infile(filename);
    if (!infile) {
	cout << "\n*** Error opening file " << filename << endl;
	cout << "Execution terminated !" << endl;
	exit(-1);
    }
  
    
    bread(infile, vec, ndim);
    

  
  


    return;

}

