#include "common.h"
#include "bin.h"

// gibt Matrizen zum Zwischenspeichern aus

void msout(double **, int, char *);


void msout(double **mat, int ndim, char *filename) {



    ofstream savfile(filename);
  

    bwrite(savfile,mat,ndim,ndim );
      
  


    return;

}







