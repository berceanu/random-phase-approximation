#include "common.h"
#include "bin.h"
#include "base.h"

// writes binary matrices and vectors

void mbout(double **, int, char *);

void vbout(double *, int, char *);


void mbout(double **mat, int ndim, char *filename) {



    ofstream savfile(filename);
  

    bwrite(savfile,mat,ndim,ndim );
      
    savfile.flush();
    savfile.close();
    


    return;

}

void mbout(double **mat, int ndim_1, int ndim_2, char *filename) {



    ofstream savfile(filename);
  

    bwrite(savfile,mat,ndim_1,ndim_2);
      
    savfile.flush();
    savfile.close();
    


    return;

}




void vbout(double *vec, int ndim, char *filename) {
	

    ofstream savfile(filename);
  

    bwrite(savfile,vec,ndim );
      
    savfile.flush();
    savfile.close();
    


    return;

}







