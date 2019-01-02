#ifdef _WIN32
#include <direct.h>
// MSDN recommends against using getcwd & chdir names
#define cwd _getcwd
#define cd _chdir
#else
#include "unistd.h"
#define cwd getcwd
#define cd chdir
#endif

#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"
#include "eigenval.h"

int matnum, matnumsav;
int nmass;
double1(rmass);
int lmax;
double gcoul;
int natural_parity;

char buf[4096]; // never know how much is needed

int main(int argc, char **argv) {

    int pa1, pa2;
    long count;
    unsigned long int nmatsav = 0;
    int nl;
    int str1, str3, tr1, tr3;
    double vh, vp, v0,vs;
    double vpp,a_mat_ph,a_mat_pp,b_mat_ph,b_mat_pp;
    int n, m, pottype;
    double1(sigcheck);
    double darg;
    int i, l;
    int iii;
    long mat_tot;
    fstream xrpafile;
    fstream yrpafile;
    fstream erpafile;
    fstream c_erpafile;
    fstream arpafile;
    fstream brpafile;
    int ab_read = 0;
    void qppair(int, int);
    
    if (argc > 1) {
        cout  << "CWD: " << cwd(buf, sizeof buf) << endl;

        // Change working directory and test for success
        if (0 == cd(argv[1])) {
        cout << "CWD changed to: " << cwd(buf, sizeof buf) << endl;
        }
    } else {
        cout << "No directory provided." << endl;
    }    

    Eigenvalue *ev;
    
    
    // Coulomb-Coupling (e*e)/(4*pi) = 1/alpha
    gcoul = (1./137.03602);
    
    
    // Einlesen von start.dat

    paramet("start.dat");


    if (lorchange == 1) 
    {
	cout << "### only calculating new lorentz-curves ###" << endl;
	cout << "### other parameters except of excitation properties are " 
	  << "ignored ###" << endl; 
	goto lorenzneu;
    }
    
    if (xyread == 1) 
    {
	cout << "*** first reading rpa-results for further calculation ***" 
	  << endl;
    }


    // check of parameters

    if ( ((xyread == 1) && (calc == 1))
	|| ((xyread == 1) && (xyprint == 1)))
    {
	cout << "wrong combination of parameters, please correct" << endl;
	cout << "xyread: " << xyread << endl;
	cout << "xyprint: " << xyprint << endl;
	cout << "calc: " << calc << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }
    

    if (xyread != 1) 
    {    
	if (calc > 1) 
	{
	    cout << "parameters not valid, please correct" << endl;
	    cout << "calc: " << calc << endl;
	    cout << "program is terminating" << endl;
	    exit(1);
	
	}
    }
    



    // three mesons 
    nmass = 3; 


    // allocation

    double1init(rmass,nmass);
    

    // maximal l-Value
    
    lmax = j + 1;
        

    // reading file qrpa.wel
    incanon(); 

    // preparing the Gaussian-integration on double-mesh
    prepint();
   
    testint();
    
// natural parity?

    if (((j+parity+1)%2) == 0)
      natural_parity = 1;
    else 
      natural_parity = 0;
    

    
// Values of rmass`

    rmass[1] = amsig/hqc;
    rmass[2] = amome/hqc;
    rmass[3] = amrho/hqc;
    

    gfv();    

    binom();
    binomh();
    

    qplevel();


    qppair(j, parity);
    qppairout(j, parity, "qpair.out");
        
    cout << npair << " pairs found!" << endl;
    cout << npair_ph << "/" << npair_ah << 
	  " ph-/ah-pairs" << endl;	
	  
    cout << "...calculating bessel function for pairing" << endl;
    qpbess();
    	  
    rpa(npair);
    
    cout << "nmesh = " << nmesh << endl;

    // calculation starts
    if (calc == 1) 
    {
	cout << "full calculation" << endl;

	// calculation of modified spherical besselfunctions
	// for nonlinear terms of sigmamesons
	

	potdif();				      

	count = 0;
	
	// total number of matrixelements to be calculated
	
	mat_tot = npair*(npair+1);
				
	for (pa1 = 1; pa1 <= npair; pa1++)
	{
            for (pa2 = 1; pa2 <= pa1; pa2++)
//	      for (pa2 = 1; pa2 <= npair; pa2++) 
              {
                 v0 = matcon0(pa1,pa2);
		 vs = matcons(pa1,pa2);
               // pp interaction
//	       if ((respair == 1) && (iph[pa1][4] == 1) && (iph[pa2][4] == 1))
//	       {  vpp = qpmatpair(pa1,pa2);
		 // cout << pa1 << " " << pa2 << " " << vpp << endl;
//	       }  
//               else
//	          vpp = 0.0;
		  
               // quasiparticle A matrix	           
	       a_mat_ph = qpmataph(pa1,pa2,v0,vs);
//	       a_mat_pp = qpmatapp(pa1,pa2,vpp);
	       arpa[pa1][pa2] = a_mat_ph; //+ a_mat_pp;;
	       
	       // quasiparticle B matrix

	       b_mat_ph = qpmatbph(pa1,pa2,v0,vs);     //?
//	       b_mat_pp = qpmatbpp(pa1,pa2,vpp);
	       brpa[pa1][pa2] = b_mat_ph; //+ b_mat_pp;
		count += 2;
		
		if (count%1000 == 0) 
		{
		    cout << "pa1 = " << pa1 << " pa2 = " << pa2 << 
		      " " << ((double)count/(double)mat_tot)*100. << endl;
		}
		

	    }
	}
    	      	
	msym();
	
	if (matprint == 1)
        {
            mout(arpa,npair,6,"rel. RPA-Matrix A","arpa.con");
            mout(brpa,npair,6,"rel. RPA-Matrix B","brpa.con");
        }
        
	        		
	for (n = 0; n <= npair; n++) 
	{
	    for (m = 0; m <= npair; m++) 
	    {
		arpac[n][m] = arpa[n][m];
		brpac[n][m] = brpa[n][m];
	    }
	}
	
	mbout(arpac,npair,"arpa.bin");
	mbout(brpac,npair,"brpa.bin");
	
	
    }
    else 
    {
	mbin(arpac,npair,"arpa.bin");
	mbin(brpac,npair,"brpa.bin");
	
	for (n = 0; n <= npair; n++) {
	    for (m = 0; m <= npair; m++) 
	    {
		arpa[n][m] = arpac[n][m];
		brpa[n][m] = brpac[n][m];
	    }
	}

	ab_read = 1;
	

    }

    if (xyread == 1)
      goto xy_read;
    

    		    
    double1init(erpa,2*npair);
    double1init(erpas,2*npair-1);
    double1init(c_erpas,2*npair-1);
    double1init(c_erpa,2*npair);
    double2init(rpa_full,2*npair-1,2*npair-1);
    double2init(xyrpa,2*npair-1,2*npair-1);
    double2init(xrpa,npair,2*npair);
    double2init(yrpa,npair,2*npair);


    // needed for printing of x- and y-matrices
    if ((xyprint == 1) && (xyread == 0))
    {
	double2initcon(xrpac,npair,2*npair);
	double2initcon(yrpac,npair,2*npair);
	double1initcon(erpac,2*npair);
	double1initcon(c_erpac,2*npair);	
    }
    
	
    delete[] arpac;
    delete[] brpac;
	


    for (i = 0; i < npair; i++) 
    {
	for (l = 0; l < npair; l++) 
	{
	    rpa_full[i][l] = arpa[i+1][l+1];
	    rpa_full[i+npair][l] = -brpa[i+1][l+1];
	    rpa_full[i][l+npair] = brpa[i+1][l+1];
	    rpa_full[i+npair][l+npair] = -arpa[i+1][l+1];
	}
    }

    cout << "calculating eigenvalues" << endl;
    cout << "...diagonalizing " << 2*npair << "x" << 2*npair 
         << " matrix" << endl;	    
    ev = new Eigenvalue(rpa_full,2*npair);
	
    erpas = ev->getRealEigenvalues();
    c_erpas = ev->getImagEigenvalues();
    xyrpa = ev->getV();

	
    
    for (i = 0; i < 2*npair; i++)
    {
	erpa[i+1] = erpas[i];
	c_erpa[i+1] = c_erpas[i];
	    
	for (l = 0; l < npair; l++)
	{		
	    xrpa[l+1][i+1] = xyrpa[l][i];
	    yrpa[l+1][i+1] = xyrpa[l+npair][i];
	}
    }


    cout << "sorting rpa-solution" << endl;
    rpasort(npair,xrpa,yrpa,erpa,c_erpa);	
   
    // prints out x- and y- and energy-matrices
    if (xyprint == 1) 
    {
	for (n = 0; n <= npair; n++) {
	    for (m = 0; m <= 2*npair; m++) 
	    {
		xrpac[n][m] = xrpa[n][m];
		yrpac[n][m] = yrpa[n][m];
	    }
	}

	for (n = 0; n <= 2*npair; n++) 
	{
	    erpac[n] = erpa[n];
	    c_erpac[n] = c_erpa[n];	  
	}
	
	cout << "saving x- and y-matrices and energies on disk" << endl;
		  
	mbout(xrpac,npair,2*npair,"xrpa.bin");
	mbout(yrpac,npair,2*npair,"yrpa.bin");
	vbout(erpac,2*npair,"erpa.bin");
	vbout(c_erpac,2*npair,"c_erpa.bin");
	
        	
// add print out

            mout(xrpa,npair,6,"rel. RPA-X","xrpa.con");
            mout(yrpa,npair,6,"rel. RPA-Y","yrpa.con");


    
//	delete[] xrpac;
//	delete[] yrpac;
//	delete erpac;
//	delete c_erpac;
    }


    cout << "testing rpa-solution" << endl;    
    rpaprobe(npair,arpa,brpa,xrpa,yrpa,erpa);


    cout << "calculating excitation-strength" << endl;	
    excstr(erpa,xrpa,yrpa,npair,j,"excskal.out","excvec.out",
	   "curve.out","neudens.out","prodens.out",
	   "totdens.out", "lorskal.out", 
	   "lorvec.out","pskal.out", "pvec.out", 
	   "strength.out", 
	   lorswidth, lorvwidth, 0);
  
    


    // excitations without interaction
    if (hartree == 1)
    {
	
	for (i = 0; i <= npair; i++) 
	{
	    for (l = 0; l <= npair; l++)
	    {
		arpa[i][l] = zero;
		brpa[i][l] = zero;
	    }
	}
	

	// just h11 matrix 

        for (i = 1; i <= npair; i++)
        {
           for (l = 1; l <= npair; l++)
           {
               arpa[i][l] = qpmataph(i,l,0.0,0.0);
               brpa[i][l] = 0.0;
           }
        }
	

	for (i = 0; i < npair; i++) 
	{
	    for (l = 0; l < npair; l++) 
	    {
		rpa_full[i][l] = arpa[i+1][l+1];
		rpa_full[i+npair][l] = -brpa[i+1][l+1];
		rpa_full[i][l+npair] = brpa[i+1][l+1];
		rpa_full[i+npair][l+npair] = -arpa[i+1][l+1];
	    }
	}
	
	cout << "calculating unperturbed eigenvalues" << endl;	    
	ev = new Eigenvalue(rpa_full,2*npair);
	
	erpas = ev->getRealEigenvalues();
	c_erpas = ev->getImagEigenvalues();
	xyrpa = ev->getV();

	
    
	for (i = 0; i < 2*npair; i++)
	{
	    erpa[i+1] = erpas[i];
	    c_erpa[i+1] = c_erpas[i];
	    
	    for (l = 0; l < npair; l++)
	    {		
		xrpa[l+1][i+1] = xyrpa[l][i];
		yrpa[l+1][i+1] = xyrpa[l+npair][i];
	    }
	}


	cout << "sorting hartree-solution" << endl;
	rpasort(npair,xrpa,yrpa,erpa,c_erpa);
		
       	
	cout << "testing hartree-solution" << endl;    
	rpaprobe(npair,arpa,brpa,xrpa,yrpa,erpa);

	cout << "calculating hartree excitation-strength" << endl;	
	excstr(erpa,xrpa,yrpa,npair,j,"harexcskal.out","harexcvec.out", 
	       "harcurve.out","harneudens.out","harprodens.out",
	       "hartotdens.out", "harlorskal.out", 
	       "harlorvec.out", "harpskal.out", "harpvec.out", 
	       "harstrength.out", hlorswidth, hlorvwidth, 1);
    }
    
    goto ende;
    
    

    // calculating new lorenz-curves
  lorenzneu:
    if (lorchange == 1) 
    {	
	lorneu("pskal.out", "pvec.out", "nlorskal.out",
	       "nlorvec.out");
	
	if (hartree == 1)
	  lorneu("harpskal.out", "harpvec.out",
		 "nharlorskal.out", "nharlorvec.out");

	goto ende;	
    }
    

	
    // this part reads x and y and energies from disk for further  
    // calculations
  xy_read:
  
    // test if x and y and energies are on disk-file

    xrpafile.open("xrpa.bin", ios::in);
    yrpafile.open("yrpa.bin", ios::in);
    erpafile.open("erpa.bin", ios::in);
    c_erpafile.open("c_erpa.bin", ios::in);
    
    if ((!xrpafile) || (!yrpafile) || (!erpafile) ||
	(!c_erpafile)) {
	cout << "x- and y-matrices and energies are not all on disk" << endl;
	cout << "please make a new run and save these matrices" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }
    else 
      cout << "reading x- and y-matrices and energies" << endl;
    
    
  
    double2initcon(xrpac,npair,2*npair);
    double2initcon(yrpac,npair,2*npair);
    double1initcon(erpac,2*npair);
    double1initcon(c_erpac,2*npair);	
    double2init(xrpa,npair,2*npair);
    double2init(yrpa,npair,2*npair);
    double1init(erpa,2*npair);
    double1init(c_erpa,2*npair);

    mbin(xrpac,npair,2*npair,"xrpa.bin");
    mbin(yrpac,npair,2*npair,"yrpa.bin");
    vbin(erpac,2*npair,"erpa.bin");
    vbin(c_erpac,2*npair,"c_erpa.bin");	
    

    for (n = 0; n <= npair; n++) {
	for (m = 0; m <= 2*npair; m++) 
	{
	    xrpa[n][m] = xrpac[n][m];
	    yrpa[n][m] = yrpac[n][m];
	}
    }

    
    for (n = 0; n <= 2*npair; n++) 
    {
	erpa[n] = erpac[n];
	c_erpa[n] = c_erpac[n];
    }


    if (ab_read == 1) 
    {	
	if (xyprobe == 1) 
	{	    
	    cout << "testing rpa-solution after reading matrices" << endl;    
	    rpaprobe(npair,arpa,brpa,xrpa,yrpa,erpa);
	}
	else 
	  ndim_o_c = 2*npair;	
	
    }
    else 
    {
	cout << "a and b-matrices not read in" << endl;
	cout << "program is terminating" << endl;
	exit(1);
    }


    if (exccalc == 1)
    {
	cout << "### calculating excitation-strength ###" << endl;	
	excstr(erpa,xrpa,yrpa,npair,j,"excskal.out","excvec.out",
	       "curve.out","neudens.out","prodens.out",
	       "totdens.out", "lorskal.out", 
	       "lorvec.out","pskal.out", "pvec.out", 
	       "strength.out", 
	       lorswidth, lorvwidth, 0);
    }


    
    if (transdens == 1) 
    {	
	cout << "### calculating transitiondensities ###" << endl;	
	trans(erpa,xrpa,yrpa,npair,j,"transdens.out","transsum.out",0);
    }
    
    if (tc_cur == 1)
    {
	cout << "### calculating transition-currents ###" << endl;	
	transcur(erpa,xrpa,yrpa,npair,j,"t_cur.out","t_vel.out",0);
    }
    


  ende:
    cout << "program terminated without errors" << endl;
   
    double2del(xyrpa);
 
    return 0;
}












