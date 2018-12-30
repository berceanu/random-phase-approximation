#include "common.h"
#include "base.h"


// writes matrix in a file for java-program


void mjout(double **mat, int ndim, int nprec, char *filename) {


  fstream savfile;
  int k, l;
  const int maxprec = 15;

  if ((nprec < 0) || (nprec > maxprec)) {
      cout << "Fehler in matout(): falsche Praezision!" << endl;
      exit(1);
  }



  savfile.open(filename, ios::out | ios::trunc);
  savfile.setf(ios::scientific);
  savfile.precision(nprec);

//  savfile << ndim << endl;
  

  for (k = 1; k <= ndim; k++) {
    for (l = 1; l <= ndim; l++) {
      
      savfile << mat[k][l]; 
      if (l < ndim)
	savfile << " ";
    }
    savfile << endl;
  }

  savfile << endl;
  

  return;

}







