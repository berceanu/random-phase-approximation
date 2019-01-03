#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"


static int lcal(int, int, int);
static double Yred(int, int , int, int, int);
static void write_head(fstream &, int, int);
static double trans_rad(int, int, int, int, int, int, int, int, int);


void trans(double *erpa, double **xrpa,
	    double **yrpa, int npair, int j, char *filetrans,
	    char * filetranssum, int hp)
{
    

    int pairc;
    int energyc;
    int st1, l1, j1;
    int st2, l2, j2;
    int l1g, l2g;    
    int iso;
    int n;
    fstream transfile;  
    fstream transfilep;
    fstream transfilen;  
    fstream transsumfile;
    int nl1, nl2;
    double xwidth, xl;    
    double strength_1, strength_2, strength_3;
    char filetransn[30], filetransp[30];
 

    double1(trans_r_neutron);
    double1(trans_r_proton);
    double1(trans_r); 
    double1(tdensn);
    double1(tdensp);
    double1(xcoord);
    double1(ycoord);

    double1init(trans_r_neutron,nmixmesh);
    double1init(trans_r_proton,nmixmesh);
    double1init(trans_r,nmixmesh);    
    double1init(tdensn,2500);
    double1init(tdensp,2500);
    double1init(xcoord,2500);
    double1init(ycoord,2500);
    double neufact;
    double profact;
    double facocc;
    
    
    int energy_start;
    
    
    energy_start = 1;
    
    int erp_ok_1;
        
    int erp_ok_2;
        
    int tr_st_ind;
    int tr_st_set = 0;
    
    int i, k, index;


    strcpy(filetransn,"ftes_transn.out");
    strcpy(filetransp,"ftes_transp.out");
    
    // for j=1 transition- isovector dipole-operator
    neufact = (double(npro))/(double(npro+nneu));
    profact = (double(nneu))/(double(npro+nneu));
    

    // counting of imaginary eigenvalues

    im_count = 0;
    
    //for automatic calculating of transition densities
   // transerg = erpa[npair+2];
    

    for (energyc = energy_start; energyc <= ndim_o_c; energyc++)
    {
	if (c_erpa[energyc] != zero)
	  im_count++;
    }
    double2init(erpa_im,im_count,2);
    
    im_count = 0;    
    for (energyc = energy_start; energyc <= ndim_o_c; energyc++)
    {
	if (c_erpa[energyc] != zero)
	{
	    erpa_im[im_count][1] = erpa[energyc];  
	    erpa_im[im_count][2] = c_erpa[energyc];
	}	
    }

    for (energyc = energy_start; energyc <= ndim_o_c; energyc++) 
    {

	if (abs0(erpa[energyc]-transerg) < 1.e-2)
	{	
	    tr_st_set++;	    
	    tr_st_ind = energyc;
	    break;
	}
    }   

    cout << "Energy for transition densities = " << transerg
         << " " << erpa[tr_st_ind] << endl;

    if (tr_st_set != 1)
    {
	cout << tr_st_set << " valid energies found!" << endl;
	cout << "exact one matching energy is allowed" << endl;	
	cout << "program is terminating" << endl;
	cout << "Transition-energy in ftes_start.dat = " << transerg << endl;
	exit(1);
    }
    
    // no imaginary states
    if ((c_erpa[tr_st_ind] == zero) && (erpa[tr_st_ind] > 0.0))
      erp_ok_1 = 1;
    else
      erp_ok_1 = 0;
     
    if (erp_ok_1 != 1)
    {
	cout << "wrong values for matching energy" << endl;
	cout << "index = " << tr_st_ind << endl;	
	cout << "erpa = " << erpa[tr_st_ind] << endl;
	cout << "c_erpa = " << c_erpa[tr_st_ind] << endl;
	cout << "energy should be positive and real" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }
    

    energyc = tr_st_ind;

           	       
    for (pairc = 1; pairc <= npair; pairc++) 
    {    
				    	    
	iso = iph[pairc][3];
		    

	st1 = iph[pairc][1];
	l1 = nl[st1][iso];		  
	j1 = nj[st1][iso];
	l1g = lcal(l1,j1,2);
		  
       // holes:
	st2 = iph[pairc][2];
	l2 = nl[st2][iso];
	j2 = nj[st2][iso];
	l2g = lcal(l2,j2,2);
		  		  

	strength_1 = xrpa[pairc][energyc]
	  +iv[abs0(j)]*yrpa[pairc][energyc];

	strength_2 = Yred(l1,j1,l2,j2,j);
	strength_3 = Yred(l1g,j1,l2g,j2,j);
	
	facocc = (uo[st1][iso]*vo[st2][iso]
		       +iv[j]*vo[st1][iso]*uo[st2][iso]);

		
	for (i = 1; i <= nfe; i++)
	{
    
    for (k = 1; k <= point[i]; k++)
	    {	
		index = mapin[i][k];

		if (iso == 1)
		{
		    trans_r_neutron[index] += 
		    (strength_2*trans_rad(st1,l1,iso,1,
					  st2,l2,iso,1,index)
		    +strength_3
		    *trans_rad(st1,l1g,iso,2,
				st2,l2g,iso,2,index))
		    *strength_1*facocc;
	         }
		 else
		 {
		    trans_r_proton[index] += 
		    (strength_2*trans_rad(st1,l1,iso,1,
					  st2,l2,iso,1,index)
		    +strength_3
		    *trans_rad(st1,l1g,iso,2,
				st2,l2g,iso,2,index))
		    *strength_1*facocc;
		 } 
	         if (transiso == 0)
		    trans_r[index] = trans_r_proton[index]
		    +trans_r_neutron[index];
		 else
		    trans_r[index] = trans_r_proton[index]
		    -trans_r_neutron[index];
	    }
	 }			       
     }

    transfile.open(filetrans, ios::out | ios::trunc);    
    write_head(transfile,0,hp);
    transfile << "#Transitiondensity for " << erpa[tr_st_ind] << " MeV" 
      << endl;
    transfile << "#x\t total " 
      << "\tneutron \t proton" << endl;

    transfile.setf(ios::scientific);

    transfilen.open(filetransn, ios::out | ios::trunc);
    transfilep.open(filetransp, ios::out | ios::trunc);

    double theta;
    int nd = 1;
    int ndmax;
    int nd1, nd2;
    double xc;
    double old=0;

    cout << "nmixmesh = " << nmixmesh << endl;

    transfilen << 0.0 << " " << 0.0 << endl;
    transfilep << 0.0 << " " << 0.0 << endl;

    for (i = 1; i <= nfe; i++)
    {
	for (k = 1; k <= point[i]; k++)
	{	
	    index = mapin[i][k];
	
	// TRANSITION DENSITIES:
    /* 
       transfile << rmeshin[i][k] << "\t"
              << pow(rmeshin[i][k],2)*trans_r[index] << "\t"
                << pow(rmeshin[i][k],2)*trans_r_neutron[index] << "\t"
                  << pow(rmeshin[i][k],2)*trans_r_proton[index] << endl;
    */

       transfile << rmeshin[i][k] << "\t"
              << -trans_r[index] << "\t"
                << -trans_r_neutron[index] << "\t"
                  << -trans_r_proton[index] << endl;
                                        

            transfilen << rmeshin[i][k] << " " << trans_r_neutron[index] << endl;
            transfilep << rmeshin[i][k] << " " << trans_r_proton[index] << endl;



      /*
        theta = 0.0;

        while(theta <= pi)
        {
 
         tdensn[nd] = trans_r_neutron[index];
         tdensp[nd] = trans_r_proton[index];
         rcoord[nd] = rmeshin[i][k];
 
         transfilen << xcoord[nd] << "\t" << ycoord[nd] << "\t" << tdensn[nd] << endl;
         nd++;
         theta += pi/2.0;

       }//theta 
       transfilen << "r = " << rmeshin[i][k] << endl;
       */
      }//k
     }//i

/*    ndmax = nd - 1;
    cout << "ndmax = " << ndmax << endl;
    cout << "nmixmesh = " << nmixmesh << endl;

    for(nd1 = 1; nd1 <= ndmax; nd1++)
    {
     xc = xcoord[nd1];
     for(nd2 = 1; nd2 <= ndmax; nd2++)
     {
      if (xc == xcoord[nd2])
      {
       cout << "usao xc" << tdensn[nd2] << endl;
       transfilen << xcoord[nd2] << " " << ycoord[nd2] << " " << tdensn[nd2] ; 
       transfilep << tdensp[nd2] ; 
      }
     }
     transfilen << "end x" << endl;
     transfilep << "end x" << endl;
    }
*/ 
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



static void write_head(fstream &resfile, int ispar, int ihar)
{
    int i;
    
    
    resfile << "#RPA-results:" << endl;
    resfile << "#Nucleus: " << nucnam << " " << nama << endl;
    resfile << "#Excitation: ";
    resfile << j;
      
    if (parity == 0)
      resfile << " -" << endl;
    else
      resfile << " +" << endl;
    
      resfile << "#Total number of pairs: " << npair << endl; 
      resfile << "#Number of ph-/ah-pairs: " <<
	  npair_ph << "/" << npair_ah << endl;
      resfile 
	  << "#Maximal excitation-energy for particle-hole-pairs: " 
	    << int(ediffmaxu)
	      << endl;
      resfile 
	  << "#Maximal excitation-energy for antiparticle-hole-pairs: " 
	    << int(ediffmaxd)
	      << endl;

    if (im_count > 0)
      resfile << "#" << im_count << " imaginary eigenvalues" << endl;
    else
      resfile << "#No imaginary eigenvalues" << endl;

    if (im_count > 0) 
    {
	resfile << "#Listing imaginary eigenvalues:" << endl;
	
	for (i = 1; i <= im_count; i++)
	{
	    resfile << "#Imaginary part: " << erpa_im[i][1] << endl;
	    resfile << "#Real part: " << erpa_im[i][2] << endl;
	}
    }    
    
    resfile << "#Parameterset: " << txtfor << endl;

    if (natural_parity == 1)
      resfile << "#natural parity: yes" << endl;
    else
      resfile << "#natural parity: no" << endl;
    
    if (ispar == 0)
      resfile << "#Isoscalar transition:" << endl;
    else if (ispar == 1)
      resfile << "#Isovector transition:" << endl;

       
    if (calc == 0)
    {
	if (calcfile_found == 1) 
	{	    
	    resfile << "#relevant interaction parameters " 
	      << "from the original calculation:"
		<< endl;
	    resfile << "#calc_j = " << calc_j << endl;
	    resfile << "#calc_parity = " << calc_parity << endl;
	    resfile << "#calc_ediffmaxu = " << calc_ediffmaxu << endl;
	    resfile << "#calc_ediffmaxd = " << calc_ediffmaxd << endl;
	    resfile << "#calc_xyprint = " << calc_xyprint << endl;
	    resfile << "#calc_hartree = " << calc_hartree << endl;
	}
	else 
	{
	    resfile << "#original file calc.out not found" << endl;
	    resfile << "#please makes sure that binary matrices" 
	      << "matching your calculation" << endl;
	    resfile << "#relevant interaction parameters " 
	      << "from file ftes_start.dat"
		<< endl;
	    resfile << "#j = " << j << endl;
	    resfile << "#parity = " << parity << endl;
	    resfile << "#ediffmaxu = " << ediffmaxu << endl;
	    resfile << "#ediffmaxd = " << ediffmaxd << endl;
	    resfile << "#xyprint = " << xyprint << endl;
	    resfile << "#hartree = " << hartree << endl;
	}
    }    
}

static double Yred(int l1, int j1, int l2, int j2, int j) 
{

    double yred_ret;
    
    yred_ret = (1.+iv[abs0(l1+l2+j)])/2.*
      sqrt((2*j+1)*(2*j1)*(2*j2)/(4*pi))*iv[j1-1]
	*wigner((j1-half),double(j),j2-half,-half,0.,half);

    return yred_ret;
    
}

static double trans_rad(int st1, int l1, int t1, int b1,
			int st2, int l2, int t2, int b2, int r_index) 

{
    
    double trans_rad_ret;
		    	    
    trans_rad_ret = wfgauss[st1][r_index+(b1-1)*nmixmesh][t1]
      *wfgauss[st2][r_index+(b2-1)*nmixmesh][t2];
    
    return trans_rad_ret;
    
}



