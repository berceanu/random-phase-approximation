#include "common.h"
#include "base.h"
#include "funk.h"


 
static char lniveau(int);
static int lcal(int, int, int);

void qppairout(int j, int parity, char *filen) {




    fstream outfile;
    int chv = 0, iil, ii1, ii2, iit;
    int nst, npt;
    int flauf;
    int pr_ok;
    int ib1,ib2,ih1,ih2;
    

    outfile.open(filen, ios::out | ios::trunc);

    outfile.precision(5);

    if ((parity%2) == 0)
      outfile << "particle/antiparticle-hole-pairs with J = " << j
	<< " and negative parity" << endl << endl;
    else
      outfile << "particle/antiparticle-hole-pairs with J = " << j
	      << " and positive parity" << endl << endl;
    

    outfile << "parameterset: " << txtfor << endl;

    outfile << "maximum energy for particle-hole pairs: "
	  << ediffmaxu << endl;
    outfile << "maximum energy for antiparticle-hole pairs: "
	  << ediffmaxd << endl;

    outfile << endl;
    
    outfile<< "total number of pairs: " << npair  << endl;

    outfile << npair_ph << "/" << npair_ah << 
      " ph-/ah-pairs" << endl;  

    outfile.setf(ios::fixed);


    outfile << "neutronpairs:" << endl << endl;

    int iil_new = 0;
    int iil_ind;
    
    
    for (iil = 1; iil <= npair; iil++) {

    pr_ok = 1;
    iil_ind = iil;
      
    iit = iph[iil][3];

    if ((iit == 2) && (chv != 1)) 
    {
	    outfile << endl << "protonpairs:" << endl << endl;
	    chv = 1;
    }
    ii1 = iph[iil][1];
    ii2 = iph[iil][2];
    ih1 = indinbl[ii1][iit];  //?
    ib1 = iblock[ii1][iit];   //?
    ih2 = indinbl[ii2][iit];
    ib2 = iblock[ii2][iit];
	
	if (pr_ok == 1) {
	    outfile << iil_ind << ". pair    en_ok = " << iph[iil][4] << endl;
	  
	    if (ee[ii1][iit] < -1000.0) 
	    {
		outfile << "E_a = " << " " << ee[ii1][iit] << " MeV \t";
		outfile <<  "a " << nr[ii1][iit];
		outfile << lniveau(lcal(nl[ii1][iit],nj[ii1][iit],2))
		  << 2*nj[ii1][iit]-1 << "/" 
		    << 2  //<< "   " << de[ii1][iit] << " " << eeqp[ii1][iit]
		    //<< "   " <<  h11[ih1][ih1][ib1]
		    << "   " << vv[ii1][iit] << endl;
	    }
	    
	    else 
	    {
		outfile << "E_p = " << " " << ee[ii1][iit] << " MeV \t";
		outfile <<  "p " << nr[ii1][iit];
		outfile << lniveau(lcal(nl[ii1][iit],nj[ii1][iit],1))
		  << 2*nj[ii1][iit]-1 << "/" 
		    << 2 
		    //<< "   " << de[ii1][iit] << "   " << eeqp[ii1][iit]
		    //<< "   " <<  h11[ih1][ih1][ib1] 
		    << "   " << vv[ii1][iit] << endl;
	    }
	    
	    outfile << "E_h = " << " " << ee[ii2][iit] << " MeV \t"; 
	    outfile <<  "h " << nr[ii2][iit] << lniveau(nl[ii2][iit]) 
	      << 2*nj[ii2][iit]-1 << "/" 
		<< 2 //<< "   " << de[ii2][iit] << "   " << eeqp[ii2][iit] 
		//<< "   " << h11[ih2][ih2][ib2]  
		<< "   " << vv[ii2][iit] << endl; 
           
           outfile << "-Eqp_ini+Eqp_fin = "
		  << " " << ee[ii1][iit] - ee[ii2][iit] << " MeV  "
	      //    << "H11_ini+H11_fin(diag) = "
		  //<< h11[ih1][ih1][ib1]+h11[ih2][ih2][ib2]
		  << endl << endl;

	}
  }
	
}   




static char lniveau(int nn)
{
    

    char lang[] = {'s','p','d','f','g','h','i','j','\0'};
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

    
    
	
	


