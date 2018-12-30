#include "common.h"
#include "base.h"


// writes matrix in a file for java-program

static int newline(fstream &);


void mjin(double **mata, double **matb, double *ener, 
	  char *xfile, char *yfile, char *efile) {


  fstream xin, yin, enin;  
  int k, l;
  int dcount = 0;
  int ce;
  

  enin.open(efile, ios::in);
  if (!enin) {
      cout << "error opening file " << efile << endl;
      cout << "program is terminating" << endl;
      exit(1);
  }

  enin >> ndim_o_r;
  dcount += newline(enin);
  
  enin >> ndim_o_c;
  dcount += newline(enin);

  // read number of pairs
  if ((ndim_o_c != npair) && (ndim_o_c != 2*npair))
  {
      cout << "wrong number of pairs in file " << efile << endl;
      cout << "ndim_o_r = " << ndim_o_r << endl;
      cout << "ndim_o_c = " << ndim_o_c << endl;      
      cout << "npair = " << npair << endl;      
      cout << "program is terminating" << endl;
      exit(1);
  }

  double1init(erpa,ndim_o_c);
  double2init(xrpa,ndim_o_r,ndim_o_c);
  double2init(yrpa,ndim_o_r,ndim_o_c);
  
    
  
  // read energy-eigenvalues
  for (k = 1; k <= ndim_o_c; k++)
  {
      enin >> erpa[k];
      if (k < npair)
	dcount += newline(enin);
  }
  
  ce = enin.get();
  if (ce != EOF) {
      cout << "eof not reached in file " << efile << endl;     
      cout << "program is terminating" << endl;

      exit(1);
  }

  xin.open(xfile, ios::in);
  if (!xin) {
      cout << "error opening file " << xfile << endl;
      cout << "program is terminating" << endl;
      exit(1);
  }

  yin.open(yfile, ios::in);
  if (!yin) {
      cout << "error opening file " << yfile << endl;
      cout << "program is terminating" << endl;
      exit(1);
  }

    

  // read x- and y-eigenvectors
  for (k = 1; k <= ndim_o_c; k++)
  {
      for (l = 1; l <= ndim_o_r; l++) 
      {
	  xin >> xrpa[l][k];
	  yin >> yrpa[l][k];
      }
      if (k < ndim_o_c) 
      {	  
	  dcount += newline(xin);
	  dcount += newline(yin);
      }
  }
  
  ce = xin.get();
  if (ce != EOF) {
      cout << "eof not reached in file " << xfile << endl;     
      cout << "program is terminating" << endl;
      exit(1);
  }

  ce = yin.get();
  if (ce != EOF) {
      cout << "eof not reached in file " << yfile << endl;     
      cout << "program is terminating" << endl;      
      exit(1);
  }
  
 
  return;

}


static int newline(fstream &forf) {

    int cn;
    cn = forf.get();
    if ((cn != '\n') && (cn != EOF)) {
	cout << "Fehler beim Einlesen der Daten!\n";
	cout << "cn" << cn << "Ende" << endl;
	
	exit(1);
    }
    
    return(1);
}






