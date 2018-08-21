#include "common.h"
#include "base.h"
#include "funk.h"



static char lniveau(int);
static int lcal(int, int, int);

void pairout(int j, int parity, char *filen) {




    fstream outfile;
    int chv = 0, iil, ii1, ii2, iit;
    int nst, npt;
    int iblock;
    int flauf;


    outfile.open(filen, ios::out | ios::trunc);

    if ((parity%2) == 0)
      outfile << "particle/antiparticle-hole-pairs with J = " << j
	<< " and negative parity" << endl << endl;
    else
      outfile << "particle/antiparticle-hole-pairs with J = " << j
	      << " and positive parity" << endl << endl;
    

    outfile << "parameterset: " << txtfor << endl;
    outfile << "sigma-mass: " << amsig << endl;
    outfile << "coupling constant of sigma: " << gsig << endl;
    outfile << "omega-mass: " << amome << endl;
    outfile << "coupling constant of omega: " << gome << endl;
    outfile << "rho-mass: " << amrho << endl;
    outfile << "coupling constant of rho: " << grho << endl;
    outfile << "maximum energy for particle-hole pairs: "
	  << ediffmaxu << endl;
    outfile << "maximum energy for antiparticle-hole pairs: "
	  << ediffmaxd << endl;

    outfile << endl;
    
    outfile<< "total number of pairs: " << npair 
	     << endl;

    outfile << npair_ph << "/" << npair_ah << 
      " ph-/ah-pairs" << endl << endl << endl;  


    outfile.setf(ios::fixed);


    outfile << "neutronpairs:" << endl << endl;

    int iil_ind;
    
    
    for (iil = 1; iil <= npair; iil++) 
    {   
      iit = iph[iil][3];
      if ((iit == 2) && (chv != 1))
      {
	    outfile << endl << "protonpairs:" << endl << endl;
	    chv = 1;
      }
      ii1 = iph[iil][1];
      ii2 = iph[iil][2];	
      outfile << iil << ". pair" << endl;	  
      if (ee[ii1][iit] < -1000.0) 
      {
	 outfile << "E_a = " << setw(11) << ee[ii1][iit] << " MeV \t";
	 outfile <<  "a " << nr[ii1][iit];
	 outfile << lniveau(lcal(nl[ii1][iit],nj[ii1][iit],2))
		  << 2*nj[ii1][iit]-1 << "/" 
		    << 2 << endl;
      }	    
      else 
      {
	 outfile << "E_p = " << setw(11) << ee[ii1][iit] << " MeV \t";
         outfile <<  "p " << nr[ii1][iit];
	 outfile << lniveau(lcal(nl[ii1][iit],nj[ii1][iit],1))
		  << 2*nj[ii1][iit]-1 << "/" 
		    << 2 << endl;
      }
	    
	 outfile << "E_h = " << setw(11) << ee[ii2][iit] << " MeV \t"; 
	 outfile <<  "h " << nr[ii2][iit] << lniveau(nl[ii2][iit]) 
	      << 2*nj[ii2][iit]-1 << "/" 
		<< 2 << endl; 
	  
	 outfile << "D_E = " 
	      << setw(11) << eph[iil] << " MeV" << endl << endl;
  }
	
}   




static char lniveau(int nn)
{
    

    char lang[] = {'s','p','d','f','g','h','j','k','\0'};
    char notkn[] = "?";

    if (nn > 7)
      return notkn[0];
    
    else
      return lang[nn];

}

static int lcal(int lc, int jc, int bil)
{
    

    if (bil == 1)
      return lc;
    
    else 
    {
	if (lc < jc)
	  return jc;
	else
	  return (lc-1);
    }
}

    
    
	
	


