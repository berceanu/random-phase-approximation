#include "common.h"
#include "base.h"


// gibt Matrizen aus


void mout(double **mat, int ndim, int nprec,  char *text, 
	 char *filename) {


  fstream savfile;
  int k, l, m;
  int spaltnorm, spaltrest;
  int numlen, spaltnum;
  const int maxspalten = 80;
  const int maxprec = 15;

  if ((nprec < 0) || (nprec > maxprec)) {
      cout << "Fehler in matout(): falsche Praezision!" << endl;
      exit(1);
  }



  savfile.open(filename, ios::out | ios::trunc);
  savfile.setf(ios::scientific);
  savfile.precision(nprec);


// Bedarf an Spalten fuer eine Zahl scientific mit nprec
  numlen = nprec + 6 + 1 + 1;
  
// Anzahl der Matrixspalten pro Seite
  spaltnum = maxspalten/numlen;
  

  spaltnorm = ndim/spaltnum;
  spaltrest = (ndim%spaltnum);


  savfile << text << endl << endl; 


  for (k = 1; k <= spaltnorm; k++) {

      savfile << "Spalten " << (k-1)*spaltnum+1 << " - "
	      << k*spaltnum << endl;

      for (l = 1; l <= ndim; l++) {
	
	  for (m = 1; m <= spaltnum; m++) {

	      savfile << setw(numlen-1)
		      << mat[l][(k-1)*spaltnum + m];
	      if (m < spaltnum)
		savfile << " ";
	  }
	  savfile << endl;
      }
      savfile << endl;
  }

  if (spaltrest > 0) {


      if (spaltrest > 1) 
	  savfile << "Spalten " << spaltnum*spaltnorm+1 
		  << " - " << spaltnum*spaltnorm+spaltrest
		  << endl;

      else
	savfile << "Spalte " << spaltnum*spaltnorm+1
		<< endl;

  for (l = 1; l <= ndim; l++) {


      for (m = 1; m <= spaltrest; m++) {

	  savfile << setw(numlen-1)
		 << mat[l][spaltnum*spaltnorm + m];
	  if (m < spaltrest)
	    savfile << " ";
      }
      savfile << endl;

  }
  }

  savfile.flush();
  savfile.close();
  

  return;

}







