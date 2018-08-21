#include "common.h"
#include "base.h"
#include "funk.h"



static void sortier(int, double ***, int ***, int);


static char lniveau(int);
static int lcal(int, int, int);


double enpartmax;
double enpartmin;
double enholemax;
double enholemin;




void level() {

    fstream levfile;
    fstream wavefile;
    int il = 0, laufp;
    int it, i1, i2;
    int l1, j1, l2, j2, kl;
    int nal;
    double ediff = zero;
    int nst;
    double ecut = 50.;
    int npartneu, npartprot;
    int nholeneu, nholeprot;
    double1(wfgnorm);
    int hztemp = 0;    
    int pztemp = 0;
        

    

    int1(npart);
    int1(nhole);
    int3(partic); 
    int3(hole);
    double3(enpart);
    double3(enhole);
           
    int1init(npart,2);
    int1init(nhole,2);
    int3init(partic,ntmax,3,2); 
    int3init(hole,ntmax,3,2);
    double3init(enpart,ntmax,2,2);
    double3init(enhole,ntmax,2,2);
        
  

    for (it = 1; it <= 2; it++) {

	for (i1 = 1; i1 <= ntpar[it]; i1++) {

	    if (vv[i1][it] < half) {

		    
		npart[it] += 1;
		partic[npart[it]][1][it] = nr[i1][it];		
		partic[npart[it]][2][it] = nl[i1][it];
		partic[npart[it]][3][it] = nj[i1][it];
		enpart[npart[it]][1][it] = ee[i1][it];
	   
		if (pztemp == 0)
		{
		    pztemp = 1;
		    enpartmax = enpartmin = enpart[npart[it]][1][it];
		}
		
		if ((pztemp == 1) && (enpart[npart[it]][1][it] > enpartmax))
		  enpartmax = enpart[npart[it]][1][it]; 

		if ((pztemp == 1) && (enpart[npart[it]][1][it] < enpartmin))
		  enpartmin = enpart[npart[it]][1][it]; 


	    
	    }
	    
	    
	    else if (vv[i1][it] > half) 
	    {
		
		

		nhole[it] += 1;
	       
		hole[nhole[it]][1][it] = nr[i1][it];		
		hole[nhole[it]][2][it] = nl[i1][it];
		hole[nhole[it]][3][it] = nj[i1][it];
		enhole[nhole[it]][1][it] = ee[i1][it];

		if (hztemp == 0)
		{
		    hztemp = 1;
		    enholemax = enholemin = enhole[nhole[it]][1][it];
		}
		
		if ((hztemp == 1) && (enhole[nhole[it]][1][it] > enholemax))
		  enholemax = enhole[nhole[it]][1][it];
		
		if ((hztemp == 1) && (enhole[nhole[it]][1][it] < enholemin))
		  enholemin = enhole[nhole[it]][1][it];


	    }
	    
	    else 
	    {
		cout << "error in level: must be particle or hole!" << endl;
		exit(-1);
	    }
	    


	}

	if (it == 1) 
	{	    
	    npartneu = npart[1];
	    nholeneu = nhole[1];
	}
	
	
	else if (it == 2) 
	{	    
	    npartprot = npart[2];
	    nholeprot = nhole[2];
	}
	
	
    }
    


    // Sortieren nach Energie
 
    sortier(nholeneu,enhole,hole,1);
    sortier(npartneu,enpart,partic,1);
    sortier(nholeprot,enhole,hole,2);
    sortier(npartprot,enpart,partic,2);
        

    levfile.open("level.out", ios::out | ios::trunc);
    

    levfile << "levels in " << nucnam << nama << endl << endl;
    levfile << "parameterset: " << txtfor << endl;
    levfile << "sigma-mass: " << amsig << endl;
    levfile << "coupling constant of sigma: " << gsig << endl;
    levfile << "omega-mass: " << amome << endl;
    levfile << "coupling constant of omega: " << gome << endl;
    levfile << "rho-mass: " << amrho << endl;
    levfile << "coupling constant of rho: " << grho << endl;
    
    levfile.setf(ios::fixed);

    int start_particles = 0;
    int ln_value;
    
    levfile << "*********" << endl;   
    levfile << "neutrons: " << endl;
    levfile << "*********" << endl << endl;    
    it = 1;
    

    levfile << "antiparticles: " << endl;
    
    for (il = 1; il <= npartneu; il++)
    {
	if ((enpart[il][1][it] > -1000.0) && (start_particles == 0))
	{
	    levfile << endl << "particles: " << endl;
	    start_particles = 1;  
	}
	    
	levfile << "E = " 
	  << setw(11) << enpart[il][1][it] << " MeV \t";
	

	if (enpart[il][1][it] < -1000.0) 
	{
	    ln_value = lcal(partic[il][2][it],partic[il][3][it],2);
	    levfile << "a " << partic[il][1][it] << lniveau(ln_value); 
	    levfile << 2*partic[il][3][it]-1 << "/" 
		<< 2 << endl;
	}
	else 
	{  
	    
	    ln_value = lcal(partic[il][2][it],partic[il][3][it],1);
	    levfile << "p " << partic[il][1][it] << lniveau(ln_value);
	    levfile << 2*partic[il][3][it]-1 << "/" 
	      << 2 << endl;
	}
    }
    
    levfile << endl << "holes: " << endl;
    
    
    for (il = 1; il <= nholeneu; il++)
    {
	levfile << "E = "
	  << setw(11) << enhole[il][1][it] << " MeV \t";

	levfile << "h " << hole[il][1][it] << lniveau(hole[il][2][it]) 
	  << 2*hole[il][3][it]-1 << "/" 
	  << 2 << endl;
    }


    levfile << endl << endl;
    
    it = 2;
    
    levfile << "*********" << endl;   
    levfile << "protons: " << endl;
    levfile << "*********" << endl << endl;    

    levfile << "antiparticles: " << endl;
    start_particles = 0;
    

    for (il = 1; il <= npartprot; il++)
    {
	if ((enpart[il][1][it] > -1000.0) && (start_particles == 0))
	{
	    levfile << endl << "particles: " << endl;
	    start_particles = 1;  
	}
	    
	levfile << "E = " 
	  << setw(11) << enpart[il][1][it] << " MeV \t";
	

	if (enpart[il][1][it] < -1000.0) 
	{
	    ln_value = lcal(partic[il][2][it],partic[il][3][it],2);
	    levfile << "a " << partic[il][1][it] << lniveau(ln_value); 
	    levfile << 2*partic[il][3][it]-1 << "/" 
		<< 2 << endl;
	}
	else 
	{  
	    
	    ln_value = lcal(partic[il][2][it],partic[il][3][it],1);
	    levfile << "p " << partic[il][1][it] << lniveau(ln_value);
	    levfile << 2*partic[il][3][it]-1 << "/" 
	      << 2 << endl;
	}
    }

    levfile << endl << "holes: " << endl;
    
    
    for (il = 1; il <= nholeprot; il++)
    {
	levfile << "E = " 
	  << setw(11) << enhole[il][1][it] << " MeV \t";

	levfile << "h " << hole[il][1][it] << lniveau(hole[il][2][it]) 
	  << 2*hole[il][3][it]-1 << "/" 
	  << 2 << endl;
    }



    int3del(partic); 
    int3del(hole);
    double3del(enpart);
    double3del(enhole);


    return;
}




static char lniveau(int nn)
{
    

    char lang[] = {'s','p','d','f','g','h','i','j','k','l','m','n','\0'};
    char notkn[] = "?";

    if (nn > 11)
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


static void sortier(int len, double ***ens, int ***levs, int itt)
{    

    // sorting energies of levels

    int n, i1, i2;    
    int i, l, j;
    double w1, w2;
    int nrcop, nlcop, njcop; 

    n = len;
        
 
    for (i = 1; i < n; i++) 
    {
	
	w1 = ens[i][1][itt];
	w2 = w1;	
	i1 = i;
	i2 = i1;
	

	for (l = i+1; l <= n; l++)
	{
	    if (ens[l][1][itt] < w1) 
	    {		
		w1 = ens[l][1][itt];
		i1 = l;
	    }	    
	}
	
	if (w1 != w2) 
	{
	    
	    ens[i2][1][itt] = w1;
	    ens[i1][1][itt] = w2;

	    nrcop = levs[i2][1][itt];
	    nlcop = levs[i2][2][itt];
	    njcop = levs[i2][3][itt];
	  

	    levs[i2][1][itt] = levs[i1][1][itt];
	    levs[i2][2][itt] = levs[i1][2][itt];
	    levs[i2][3][itt] = levs[i1][3][itt];

	    
	    levs[i1][1][itt] = nrcop;
	    levs[i1][2][itt] = nlcop;
	    levs[i1][3][itt] = njcop;


	}

    }
        

    return;
    
}
    



