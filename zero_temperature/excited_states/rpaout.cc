#include "common.h"
#include "base.h"

// gibt RPA-Eigenvektoren und -werte  aus


void rpaout(double **xxr, double **yyr, double *er,
	    int ndim, int nprec, char *filename) {


  fstream savfile;
  int k, l, m;
  int spaltnorm, spaltrest;
  int numlen, spaltnum;
  const int maxspalten = 80;
  const int maxprec = 15;

  if ((nprec < 0) || (nprec > maxprec)) {
      cout << "Fehler in rpaout(): falsche Praezision!" << endl;
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


  // printing of parameters

  savfile << "RPA-Results:" << endl;
  savfile << "Nucleus: " << nucnam << " " << nama << endl;  
  savfile << "b0 = " << b0 << endl;  
  savfile << "Excitation: ";
  savfile << j;
  
  if (parity == 0)
    savfile << " -" << endl;
  else
    savfile << " +" << endl;
  
  savfile << "Used parameterset: " << txtfor << endl;
  savfile << "Mass Sigma: " << amsig << endl;
  savfile << "Coupling Sigma Saturation: " << gsigs << endl;
  savfile << "Mass Omega: " << amome << endl;
  savfile << "Coupling Omega Saturation: " << gomes << endl;
  savfile << "Mass Rho: " << amrho << endl;
  savfile << "Coupling Rho Saturation: " << grhos << endl;
  savfile << "Mass Pion: " << ampi << endl;
  savfile << "Coupling Pion: " << gpi << endl;
  savfile << "Fermi-cut-off: " << fermcut << endl;
  savfile << "Number of pairs: " << npair << endl;  
  savfile << "Number of shells: " << n0f << endl;
  savfile << "Maximal j in base: " << jmax << endl;
  savfile << "Maximal excitation-energy for ph-pairs: " << int(ediffmax)
    << endl;
  savfile << "Expansion cut-off for slater-integrals: " << nx << endl;
  savfile << endl << endl;
  savfile << "Number of meshpoints: " << ngh << endl;
//  savfile << "gpi = " << gpi << endl;
//  savfile << "ampi = " << ampi << endl;
//  savfile << "gsig = " << gsig << endl;
//  savfile << "amsig = " << amsig << endl;
//  savfile << "grho = " << grho << endl;
//  savfile << "amrho = " << amrho << endl;
//  savfile << "gome = " << gome << endl;
//  savfile << "amome = " << amome << endl;

  for (k = 1; k <= spaltnorm; k++) {

      savfile << "Eigenwerte " << (k-1)*spaltnum+1 << " - "
	      << k*spaltnum << endl;

      for (m = 1; m <= spaltnum; m++) {
	  savfile << setw(numlen-1) << er[(k-1)*spaltnum + m];
	  if (m < spaltnum) 
	    savfile << " ";
      }
      savfile << endl << endl;
      savfile << "X-Eigenvektoren" << endl;

      for (l = 1; l <= ndim; l++) {
	
	  for (m = 1; m <= spaltnum; m++) {

	      savfile << setw(numlen-1)
		      << xxr[l][(k-1)*spaltnum + m];
	      if (m < spaltnum)
		savfile << " ";
	  }
	  savfile << endl;
      }
      
      savfile << endl;

      savfile << "Y-Eigenvektoren" << endl;

      for (l = 1; l <= ndim; l++) {
	
	  for (m = 1; m <= spaltnum; m++) {

	      savfile << setw(numlen-1)
		      << yyr[l][(k-1)*spaltnum + m];
	      if (m < spaltnum)
		savfile << " ";
	  }
	  savfile << endl;
      }

      savfile << endl;
  }

  if (spaltrest > 0) {


      if (spaltrest > 1) 
	  savfile << "Eigenwerte " << spaltnum*spaltnorm+1 
		  << " - " << spaltnum*spaltnorm+spaltrest
		  << endl;

      else
	savfile << "Eigenwert " << spaltnum*spaltnorm+1
		<< endl;

      for (m = 1; m <= spaltrest; m++) {

	  savfile << setw(numlen-1)
		 << er[spaltnum*spaltnorm + m];
	  if (m < spaltrest)
	    savfile << " ";
      }
      savfile << endl << endl;


      if (spaltrest > 1)
	savfile << "X-Eigenvektoren" << endl;
      else 
	savfile << "X-Eigenvektor" << endl;


  for (l = 1; l <= ndim; l++) {


      for (m = 1; m <= spaltrest; m++) {

	  savfile << setw(numlen-1)
		 << xxr[l][spaltnum*spaltnorm + m];
	  if (m < spaltrest)
	    savfile << " ";
      }
      savfile << endl;

  }

      savfile << endl;

      if (spaltrest > 1)
	savfile << "Y-Eigenvektoren" << endl;
      else
	savfile << "Y-Eigenvektor" << endl;

      for (l = 1; l <= ndim; l++) {


	  for (m = 1; m <= spaltrest; m++) {

	      savfile << setw(numlen-1)
		      << yyr[l][spaltnum*spaltnorm + m];
	      if (m < spaltrest)
		savfile << " ";
	  }
	  savfile << endl;

      }
  }


  return;

}





