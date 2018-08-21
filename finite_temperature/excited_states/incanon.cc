#include "common.h"
#include "base.h"
#include "funk.h"

#define NRANSI
#include "nr.h"

static int ik(int, int, int);

int newline(fstream &);
static int kappaj(int);
static int kappal(int, int);

char nucnam[3];
char dummy[100];
int nama, nneu, npro;
int nhx, nb2x, nblock;
char txtfor[11];
double amsig, amome, amrho, amu;
double gsigs, gomes, grhos;
double a_s,b_s,c_s,d_s;
double a_v,b_v,c_v,d_v;
double a_tv,dsat;
double1(gsig);
double1(gome);
double1(grho);
double1(dgsig);
double1(dgome);
double1(dgrho);
double1(ddgsig);
double1(ddgome);
double1(ddgrho);
double1(denss);
double1(densv);
double1(denstv);
double rmax;
double hmesh;
int nmesh;
double rms_2;
int1(ntpar);
int2(nr);	    
int2(nl);	    
int2(nj);
int2(kap);
int1(nf);
double3(wfg);
double3(wfg_zero);
double2(ee);
double2(eeqp);
double2(de);
double2(vv);
double2(vo);
double2(uo);
int2(indinbl);
int2(iblock);
double3(h11);
double1(ala);
int ntmax;
double1(rmeshorig);
double1(dens0);
double1(dens0_n);
double1(dens0_p);
double dens0_integ;
// gogny
char gogtxt[11];
double1(gogw);
double1(gogb);
double1(gogh);
double1(gogm);
double1(gogr);
double gogt3, gogwls;
double vfac;

void incanon() {

    fstream infile;    
    fstream testfile;   
    fstream wffile; 
    fstream densfile;
    fstream densfile2;
    fstream wffileg;
    fstream occfile;
    fstream denssfile;
    fstream densvfile;
    fstream denstvfile;
    int n, it, i;
    int imesh;
    int dcount, rcount, nlinecount;
    int ce;
    int msp;
    int i1, i2;
    double fsum = zero;
    double gsum = zero;
    double1(testsum);
    char* filename1 = "rpa.wel";    
    fstream savfile;
    int nmeshpro;
    double rmaxpro;
    int istemp;
    int ntemp;
    int kappa, kappatemp;
    int ib,ih,mf,nh,kh;
    double meshtemp;
    int large_only;
    double zpoint;
    double rms_2_in;
    
    int ib34,ib12,n3,n4,n1,n2,nf34,nf12,ipb12,ipb34,i34,i12,mvx;
    double1(dens0_test);    
    int1init(ntpar,2);
    double1init(ala,2);
    //gogny
    double1init(gogw,2);
    double1init(gogb,2);
    double1init(gogh,2);
    double1init(gogm,2);
    double1init(gogr,2);
        
    dcount = 0;
    
    infile.open(filename1, ios::in);
    if (!infile) {
	cerr << "\n*** Error opening file " << filename1 << " ***\n";
	cerr << "program is terminating" << endl;
	exit(1);
    }

    cout.precision(12);
	
    infile >> nucnam >> nama >> nneu >> npro;    
    dcount += newline(infile);
    
    infile >> txtfor >> amsig >> amome >> amrho >> amu;
    dcount += newline(infile);
    
    infile >> gsigs >> gomes >> grhos ;
    dcount += newline(infile);
    
    infile >> a_s >> b_s >> c_s >> d_s;
    dcount += newline(infile);

    infile >> a_v >> b_v >> c_v >> d_v;
    dcount += newline(infile);

    infile >> a_tv;
    dcount += newline(infile);

    infile >> dsat;
    dcount += newline(infile);    

/*
    infile >> gogtxt;
    dcount += newline(infile);
    infile >> gogw[1] >> gogw[2] >> gogb[1] >> gogb[2];
    dcount += newline(infile);
    infile >> gogh[1] >> gogh[2] >> gogm[1] >> gogm[2];
    dcount += newline(infile);
    infile >> gogr[1] >> gogr[2] >> gogt3 >> gogwls;
    dcount += newline(infile);

    infile >> vfac;
    dcount += newline(infile);
*/
    cout << "parameters for nucleus read" << endl;
    
    cout << "nucnam = " << nucnam << endl;
    cout << "nama = " << nama << endl;
    cout << "nneu = " << nneu << endl;
    cout << "npro = " << npro << endl;
    cout << "txtfor = " << txtfor << endl;
    cout << "amsig = " << amsig << endl;
    cout << "amome = " << amome << endl;
    cout << "amrho = " << amrho << endl;
    cout << "gsigs = " << gsigs << endl;
    cout << "gomes = " << gomes << endl;
    cout << "grhos = " << grhos << endl;
    cout << "a_s = " << a_s << endl;
    cout << "b_s = " << b_s << endl;
    cout << "c_s = " << c_s << endl;
    cout << "d_s = " << d_s << endl;    
    cout << "a_v = " << a_v << endl;
    cout << "b_v = " << b_v << endl;
    cout << "c_v = " << c_v << endl;
    cout << "d_v = " << d_v << endl;
    cout << "a_tv = " << a_tv << endl;
    cout << "dsat = " << dsat << endl;
    cout << "vfac = " << vfac << endl;

/*             
    cout << gogtxt << endl;
    cout << "gogw = " << gogw[1] << "   " << gogw[2] << endl;
    cout << "gogb = " << gogb[1] << "   " << gogb[2] << endl;
    cout << "gogh = " << gogh[1] << "   " << gogh[2] << endl;
    cout << "gogm = " << gogm[1] << "   " << gogm[2] << endl;
    cout << "gogr = " << gogr[1] << "   " << gogr[2] << endl;
    cout << "gogt3 = " << gogt3 << endl;
    cout << "gogwls = " << gogwls << endl;
    cout << "vfac   = " << vfac << endl;
*/

    infile >> nmesh >> hmesh >> rmax;
    dcount += newline(infile);

    cout << "nmesh = " << nmesh << endl;
    cout << "hmesh = " << hmesh << endl;
    cout << "rmax = " << rmax << endl;
    cout << "qptresh= " << qptresh << endl;   
    
 
    if (((nmesh*hmesh)-rmax) > 1.0E-8)
    {
	cout << "error while reading mesh" << endl;
	cout << "program is terminating" << endl;
	exit(1);	
    }
    
    infile >> rms_2_in;
    dcount += newline(infile);
    
    cout << "sqrt(rms_2_in) = " << rms_2_in << endl;
    cout << "... Quasiparticle state partially occupied if vv > qptresh=" << qptresh << endl;

    infile >> ala[1] >> ala[2];
    dcount += newline(infile);
    infile >> nhx >> nb2x >> nblock;
    
    int1init(nf,nblock);
    
    dcount += newline(infile);
    cout << "... nhx=" << nhx << " nb2x=" << nb2x << " nblock=" << nblock 
	 << endl;
    cout << "... Lambda: n " << ala[1] << "  p " << ala[2] << endl;

    infile >> ntpar[1] >> ntpar[2]; 
    dcount += newline(infile);

    // building mesh
    double1init(rmeshorig,nmesh);    
    for (i = 0; i <= nmesh; i++)
      rmeshorig[i] = hmesh*i;
        

    // Number of states for neutron (it = 1) and protons (it = 2)
    ntmax = max0(2,ntpar[1],ntpar[2]);
    

    // Initialization of arrays for states
    int2init(nr,ntmax,2);
    int2init(nl,ntmax,2);
    int2init(nj,ntmax,2);
    int2init(kap,ntmax,2);
    double2init(ee,ntmax,2);
    double2init(eeqp,ntmax,2);
    double2init(de,ntmax,2);
    double2init(vv,ntmax,2);
    double2init(vo,ntmax,2);
    double2init(uo,ntmax,2);
    int2init(indinbl,ntmax,2);
    int2init(iblock,ntmax,2);
    double3init(h11,nhx,nhx,nb2x);
    double3init(wfg,ntmax,2*nmesh,2);
//    double3init(wfg_zero,2*nmesh,2,2);    
    double3init(wfg_zero,ntmax,2,2); 
    double1init(dens0,nmesh);
    
    double1init(dens0_n,nmesh);
    double1init(dens0_p,nmesh);
    
    // initialization for coupling constants etc.
    double1init(gsig,nmesh);
    double1init(gome,nmesh);
    double1init(grho,nmesh);
    double1init(dgsig,nmesh);
    double1init(dgome,nmesh);
    double1init(dgrho,nmesh);
    double1init(ddgsig,nmesh);
    double1init(ddgome,nmesh);
    double1init(ddgrho,nmesh);   
    double1init(denss,nmesh);
    double1init(densv,nmesh);
    double1init(denstv,nmesh);

    for (i = 0; i <= nmesh; i++)
    {
        infile >> denss[i] >> densv[i] >> denstv[i];
        dcount += newline(infile);
    }
    for (i = 0; i <= nmesh; i++)
    {
        infile >> gsig[i] >> gome[i] >> grho[i];
        dcount += newline(infile);
    }     
    for (i = 0; i <= nmesh; i++)
    {
        infile >> dgsig[i] >> dgome[i] >> dgrho[i];
        dcount += newline(infile);
    }
    for (i = 0; i <= nmesh; i++)
    {
        infile >> ddgsig[i] >> ddgome[i] >> ddgrho[i];
        dcount += newline(infile);
    }    

    
    int kappa_temp;
    int nr_c;
    double tproba;
    

    for (it = 1; it <= 2; it++)
    {
    
    
/*
     // H11 matrix and block parameters 
     for (ib = 1; ib <= nblock; ib++)
     {
      infile >> mf >> nh;
      dcount += newline(infile);
      for (ih = 1; ih <= nh ; ih++)
      {
	for (kh = 1; kh <= nh; kh++)
	{
         infile >> h11[ih][kh][mf];
	 dcount += newline(infile);
	}
      }
     }
     cout << "... read H11 matrix" << endl; 
*/

	for (n = 1; n <= ntpar[it]; n++) { 
	    infile >> kappa >> ee[n][it]  >> vo[n][it]
		   >> indinbl[n][it] >> iblock[n][it] ;
	    kap[n][it] = kappa;
	    dcount += newline(infile);
     
    vo[n][it]=sqrt(vo[n][it]);  
     
        // occupation probabilities for antiparticles 
	vv[n][it]  = pow(vo[n][it],2.0);   
	if(vv[n][it] > 1.0)  //antiparticles   
	{
	   vv[n][it] = 0.0;
	   vo[n][it] = 0.0;
	   uo[n][it] = 1.0;
	}
	uo[n][it] = sqrt(1.0-vv[n][it]); 
	
	
	if(ee[n][it] > -1000.0)
	{
	  eeqp[n][it] = sqrt(pow(ee[n][it]-ala[it],2.0) + 
	                pow(de[n][it],2.0));                      //??
        }
	else
	{
	  eeqp[n][it] = ee[n][it]-ala[it];
	} 
	
	
	if (n == 1) 
	{		
           kappatemp = kappa;
           nr_c = 1;
	}	    
	else if (kappa != kappatemp) 
	{		
	   kappatemp = kappa;
           nr_c = 1;
	}
	else
	   nr_c++;
	    		
        // number nr is used as a label only (it does not correspond
        // to the number of nodes in the wave functions)
 
	    nr[n][it] = nr_c;

	    nj[n][it] = kappaj(kappa);

	 // for antiparticles the kappa which is read in
	 // belongs to the upper component !!
	    nl[n][it] = kappal(kappa, nj[n][it]);

	 // large components
	    rcount = 0;	    
	    // read zero-point
	    rcount++;	    
	    infile >> zpoint;

	    wfg_zero[n][it][1] = zpoint;
	    

	    for (imesh = 1; imesh <= nmesh; imesh++)
	    {
		rcount++;		
		infile >> wfg[n][imesh][it];
		if (((rcount%4) == 0) && (imesh < nmesh))
		  dcount += newline(infile);
	    }
	    dcount += newline(infile);

	    //small components
	    rcount = 0;
	    // read zero-point
	    rcount++;	    
	    infile >> zpoint;

	    wfg_zero[n][it][2] = zpoint;
	    
	    for (imesh = 1; imesh <= nmesh; imesh++)
	    {
		rcount++;		
		infile >> wfg[n][imesh+nmesh][it];
		if (((rcount%4) == 0) && (imesh < nmesh))
		  dcount += newline(infile);
	    }
	    dcount += newline(infile);

	}
    }
    
    ce = infile.get();
    if (ce != EOF) {
	cout << "EOF not reached" << endl
	     << "error while reading file " << filename1 << endl;
	cout << "program is terminating" << endl; 
	exit(1);
    }

    cout << "wave-functions read" << endl;
    
    infile.close();
    
    // test the wave functions

    testfile.open("normtest.out",ios::out | ios::trunc);
    if (!testfile) {
	cerr << "\n*** Error opening file " << "normtest.out" << " ***\n";
	cerr << "Execution terminated !" << endl;
	exit(1);
    }

    wffile.open("wf.out",ios::out | ios::trunc);
    if (!testfile) {
        cerr << "\n*** Error opening file " << "wf.out" << " ***\n";
        cerr << "Execution terminated !" << endl;
        exit(1);
    }
    
    wffileg.open("wfg.out",ios::out | ios::trunc);
    if (!testfile) {
        cerr << "\n*** Error opening file " << "wfg.out" << " ***\n";
        cerr << "Execution terminated !" << endl;
        exit(1);
    }
    
    occfile.open("EV.out",ios::out | ios::trunc);
    if (!testfile) {
        cerr << "\n*** Error opening file " << "EV.out" << " ***\n";
        cerr << "Execution terminated !" << endl;
        exit(1);
    }


    // only for test !!!!

    large_only = 0;
    

    if (large_only == 1) {

	cout << "attention!" << endl;
	cout << "only large components" << endl;
	
	for (it = 1; it <= 2; it++)
	{
	    for (i = 1; i <= ntpar[it]; i++)
	    {
		for (imesh = 0; imesh <= nmesh; imesh++)
		  {

		      wfg[i][imesh+nmesh][it] = zero;
		      
		  }
	    }
	}
    }

    double err_norm_max = zero;
    double res_norm;
    double err_ort_max = zero;
    double res_ort;
	
    // norm-tests

    double1init(testsum,nmesh);

    for (it = 1; it <= 2; it++) 
    {
	for (i = 1; i <= ntpar[it]; i++)
	{
	          
	    testsum[0] = zero;
	    
	    for (imesh = 1; imesh <= nmesh; imesh++)
	    {

		      
		testsum[imesh] = (wfg[i][imesh][it]*wfg[i][imesh][it]
				  +wfg[i][imesh+nmesh][it]
				  *wfg[i][imesh+nmesh][it])
		  *rmeshorig[imesh]*rmeshorig[imesh];

	    }	
	    res_norm = abs0(simps(testsum,nmesh,hmesh)-1);
		    if (res_norm > err_norm_max)
		      err_norm_max = res_norm;	
	}
    }


   // write wave function

    int it_write;
    int j_write;
    int l_write;

    it_write = 2;
    j_write = 3;
    l_write = 3; 
    
    for (i = 1; i <= ntpar[it_write]; i++)
      {
                                                                            
       if(nj[i][it_write] == j_write && nl[i][it_write] == l_write 
          && vv[i][it_write] > 0.5 )
       {                                   
        wffile << "# it= " << it_write << " j = " << j_write << " l = "
               << l_write << " vv = " << vv[i][it_write] << endl;
             
             wffile << zero << " " << wfg[i][1][it_write] << endl;                
             for (imesh = 1; imesh <= nmesh; imesh++)
             {
                                                                            
                wffile << rmeshorig[imesh] << " " 
                       << wfg[i][imesh][it_write] << endl;                                                            
             }
             wffile << zero << " " << zero << endl;
        }
      }
 
 // write small component of wave function
      for (i = 1; i <= ntpar[it_write]; i++)
      {
                                                                            
       if(nj[i][it_write] == j_write && nl[i][it_write] == l_write 
          && vv[i][it_write] > 0.5 )
       {                                   
        wffileg << "# it= " << it_write << " j = " << j_write << " l = "
               << l_write << " vv = " << vv[i][it_write] << endl;
             
             wffileg << zero << " " << wfg[i][1+nmesh][it_write] << endl;                
             for (imesh = 1; imesh <= nmesh; imesh++)
             {
                                                                            
                wffileg << rmeshorig[imesh] << " " 
                       << wfg[i][imesh+nmesh][it_write] << endl;                                                            
             }
             wffileg << zero << " " << zero << endl;
        }
      }
      
 // write single particle energy and occupation probability
 

    // test for orthogonality
    for (it = 1; it <= 2; it++) 
        {
	       for (i1 = 1; i1 <= ntpar[it]; i1++)
	           {
	              occfile << ee[i1][it] <<"  " << vv[i1][it] << "  "<< 2*nj[i1][it] << endl;
	            }
	    }
	    
	    
	    
	
    for (it = 1; it <= 2; it++) 
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++)
	{
	    for (i2 = 1; i2 <= ntpar[it]; i2++)
	    {
	      
	      		
		testsum[0] = zero;
		
		// same kappa-block !
		if ((kap[i1][it] == kap[i2][it]) 
		    && (i1 != i2))
		{
			
	  
		    for (imesh = 1; imesh <= nmesh; imesh++)
		    {

		      
			testsum[imesh] = (wfg[i1][imesh][it]
					  *wfg[i2][imesh][it]
					  +wfg[i1][imesh+nmesh][it]
					  *wfg[i2][imesh+nmesh][it])
			  *rmeshorig[imesh]*rmeshorig[imesh];


		    }
		    res_ort = abs0(simps(testsum,nmesh,hmesh));
		    if (res_ort > err_ort_max)
		      err_ort_max = res_ort;			
		}
		    
	    }
		
	}
	    
    }
    
    

// test for different blocks

	    for (i2 = 1; i2 <= ntpar[1]; i2++)
	    {
	      
	      		
		testsum[0] = zero;
		
		
		if ((i2 != 1))
		{
			
	  
		    for (imesh = 1; imesh <= nmesh; imesh++)
		    {

		      
			testsum[imesh] = (wfg[1][imesh][1]
					  *wfg[i2][imesh][1]
					  +wfg[1][imesh+nmesh][1]
					  *wfg[i2][imesh+nmesh][1])
			  *rmeshorig[imesh]*rmeshorig[imesh];


		    }
		    res_ort = abs0(simps(testsum,nmesh,hmesh));
		    cout << "orthogonality: 1   " << i2 <<"  "<< res_ort << endl;		
		}
	}	    
	    
		


    
    cout << "maximum error in norm on equidistant mesh: " 
      << err_norm_max << endl;
    cout << "maximum error in orthogonality on equidistant mesh: " 
      << err_ort_max << endl;
    
    testfile << "maximum error in norm on equidistant mesh: " 
      << err_norm_max << endl;
    testfile << "maximum error in orthogonality on equidistant mesh: " 
      << err_ort_max << endl;
    

    testfile.close();
    

    // calculating density in ground-state 

    double rms_0 = zero;
    
    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{		   	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],2.0);
		}	
		rms_0 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it]*vv[i1][it];		
	    }
	}
    }


    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    // only occupied states
	//  if (vv[i1][it] > half)
	    {
		for (imesh = 0; imesh <= nmesh; imesh++) 
		{	
		   
             
           if (imesh == 0)
		      dens0[imesh] += (wfg_zero[i1][it][1]
				       *wfg_zero[i1][it][1]+
				       wfg_zero[i1][it][2]
				       *wfg_zero[i1][it][2])
			*2*nj[i1][it]*vv[i1][it]/(4.*pi); 
		    else
                      dens0[imesh] += (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				       wfg[i1][imesh+nmesh][it]
				       *wfg[i1][imesh+nmesh][it])
			*2*nj[i1][it]*vv[i1][it]/(4.*pi);
		}
	    }
	}
    }
    


    double1init(dens0_test,nmesh);    
    densfile.open("dens0.out",ios::out | ios::trunc);
    if (!densfile) {
	cout << "\n*** Error opening file " << "dens0.out" << " ***\n";
	cout << "program is terminating" << endl;
	exit(1);
    }
    densfile << "#ground-state-density for " << nucnam << nama << endl;
    densfile << "#parameter-set: " << txtfor << endl;  

    
    for (imesh = 1; imesh <= nmesh; imesh++) 
    {
	densfile << rmeshorig[imesh] << "\t" << dens0[imesh] << endl;	
	dens0_test[imesh] = dens0[imesh]*pow(rmeshorig[imesh],2.0); 
    }

    dens0_integ = simps(dens0_test,nmesh,hmesh)*4.*pi;
    
    cout << "dens0 integrated = " 
      << dens0_integ << endl;
    


    // calculating r^1 in ground-state 

    double rms_1 = zero;
    
    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    // only occupied states
	 //   if (vv[i1][it] > half)
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{
	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],3.0);
		}
		rms_1 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it]*vv[i1][it];
		
	    }
	}
    }

    rms_1 /= rms_0;
    

    // calculating r^2 in ground-state 

    rms_2 = zero;
    
    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    // only occupied states
	//    if (vv[i1][it] > half)
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{
	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],4.0);
		}
		rms_2 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it]*vv[i1][it];
		
	    }
	}
    }

    rms_2 /= rms_0;
    

    cout << "rms_0 = " << rms_0 << endl;
    cout << "rms_2 = " << rms_2 << endl;
    cout << "sqrt(rms_2)= " << sqrt(rms_2) << endl;
    cout << "rms_1= " << rms_1 << endl;
    
//  print out density changed from Gaussian points, directly read from ground state    
    
    densfile2.open("dens02.out",ios::out | ios::trunc);
    if (!densfile2) {
	cout << "\n*** Error opening file " << "dens02.out" << " ***\n";
	cout << "program is terminating" << endl;
	exit(1);
    }
    
    densfile2 << "# total vector density:" << endl;
    for (imesh = 1; imesh <= nmesh; imesh++) 
    {
	densfile2 << rmeshorig[imesh] << "\t" << densv[imesh] << endl;	
    }
    
    densfile2 << " # total scalar density:" << endl;
    for (imesh = 1; imesh <= nmesh; imesh++) 
    {
	densfile2 << rmeshorig[imesh] << "\t" << denss[imesh] << endl;	
    }
    
    densfile2 << "# total isoscalar density: rhop-rhon" << endl;
    
    for (imesh = 1; imesh <= nmesh; imesh++) 
    {
	densfile2 << rmeshorig[imesh] << "\t" << denstv[imesh] << endl;
    }
    
    densfile2.close();
    

// calculate the rms radius to check the density from Gaussian points

   
    double rms_ch = zero;
    

		for (imesh = 1; imesh <= nmesh; imesh++) 
		{
	
		    testsum[imesh] = densv[imesh]*pow(rmeshorig[imesh],4.0);
		}
		rms_ch = simps(testsum,nmesh,hmesh)*4.*pi;
		

      rms_ch /= rms_0;
//    rms_ch = sqrt(rms_ch);
    cout << "rms from Gaussian density:  " << rms_ch << "  "<< sqrt(rms_ch)<< endl;
    
    
//   use the density calculated from the wave function 

    denssfile.open("denss.out",ios::out | ios::trunc);
    if (!denssfile) {
	cout << "\n*** Error opening file " << "denss.out" << " ***\n";
	cout << "program is terminating" << endl;
	exit(1);
    }
    
    
    
    densvfile.open("densv.out",ios::out | ios::trunc);
    if (!densfile2) {
	cout << "\n*** Error opening file " << "densv.out" << " ***\n";
	cout << "program is terminating" << endl;
	exit(1);
    }
    
    
    denstvfile.open("denstv.out",ios::out | ios::trunc);
    if (!densfile2) {
	cout << "\n*** Error opening file " << "denstv.out" << " ***\n";
	cout << "program is terminating" << endl;
	exit(1);
    }
    
//  vector density    
    for (imesh=0; imesh <= nmesh; imesh++)
    {
      densv[imesh]= dens0[imesh];
      densvfile << rmeshorig[imesh] << "  " << densv[imesh] << endl;
    }
    
//  scalar density

    for (imesh=0; imesh <= nmesh; imesh++)
    {
      denss[imesh]= 0;
      dens0_p[imesh]=0;
      dens0_n[imesh]=0;
    }
       for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{


		for (imesh = 0; imesh <= nmesh; imesh++) 
		{	
		   
             
           if (imesh == 0)
		      denss[imesh] += (wfg_zero[i1][it][1]
				       *wfg_zero[i1][it][1]-
				       wfg_zero[i1][it][2]
				       *wfg_zero[i1][it][2])
			*2*nj[i1][it]*vv[i1][it]/(4.*pi); 
		    else
                      denss[imesh] += (wfg[i1][imesh][it]*wfg[i1][imesh][it]-
				       wfg[i1][imesh+nmesh][it]
				       *wfg[i1][imesh+nmesh][it])
			*2*nj[i1][it]*vv[i1][it]/(4.*pi);
		}
	    
	}
    }
   
    for (imesh=0; imesh <= nmesh; imesh++)
    {
     
      denssfile << rmeshorig[imesh] << "  " << denss[imesh] << endl;
    }
   
   
   	
// isoscalar density

	for (i1 = 1; i1 <= ntpar[1]; i1++) 
	{
	   	    
		for (imesh = 0; imesh <= nmesh; imesh++) 
		{	
		   
             
           if (imesh == 0)
		      dens0_n[imesh] += (wfg_zero[i1][1][1]
				       *wfg_zero[i1][1][1]+
				       wfg_zero[i1][1][2]
				       *wfg_zero[i1][1][2])
			*2*nj[i1][1]*vv[i1][1]/(4.*pi); 
		    else
                      dens0_n[imesh] += (wfg[i1][imesh][1]*wfg[i1][imesh][1]+
				       wfg[i1][imesh+nmesh][1]
				       *wfg[i1][imesh+nmesh][1])
			*2*nj[i1][1]*vv[i1][1]/(4.*pi);
		}
	    
	}


	for (i1 = 1; i1 <= ntpar[2]; i1++) 
	{
	   	    
		for (imesh = 0; imesh <= nmesh; imesh++) 
		{	
		   
             
           if (imesh == 0)
		      dens0_p[imesh] += (wfg_zero[i1][2][1]
				       *wfg_zero[i1][2][1]+
				       wfg_zero[i1][2][2]
				       *wfg_zero[i1][2][2])
			*2*nj[i1][2]*vv[i1][2]/(4.*pi); 
		    else
                      dens0_p[imesh] += (wfg[i1][imesh][2]*wfg[i1][imesh][2]+
				       wfg[i1][imesh+nmesh][2]
				       *wfg[i1][imesh+nmesh][2])
			*2*nj[i1][2]*vv[i1][2]/(4.*pi);
		}
	    
	}
    
   for (imesh=0; imesh <= nmesh; imesh++)
    {
      denstv[imesh]= -dens0_n[imesh]+dens0_p[imesh];
      denstvfile << rmeshorig[imesh] << "  " << denstv[imesh] << endl;
    } 
    
    return;
    

}


 



int newline(fstream &forf) {

    int cn;
    cn = forf.get();
    if ((cn != '\n') && (cn != EOF)) {
	cout << "Fehler beim Einlesen der Daten!\n";
	cout << "cn" << cn << "Ende" << endl;
	
	exit(1);
    }
    
    return(1);
}

int kappaj(int ka) 
{
    int jr;
    
    if (ka < 0)
      jr = -ka;
    else if (ka > 0)
      jr = ka;
    else 
    {
	cout << "Fehler bei Kappa!" << endl;
	exit(1);
    }
    return jr;
	

}
    
int kappal(int ka, int ja) 
{
    int lr;
	
    if (ka < 0)
      lr = ja - 1;
    else if (ka > 0) 
      lr = ja;
    else
    {
	cout << "Fehler bei Kappa!" << endl;
	exit(1);
    }
	    
    return lr;
}
    
static int ik(int i, int k, int n)
{
    
   return i+(k-1)*(2*n-k)/2;
}	     







