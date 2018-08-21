#include "common.h"
#include "base.h"
#include "funk.h"

#define NRANSI
#include "nr.h"

int newline(fstream &);
static int kappaj(int);
static int kappal(int, int);


char nucnam[3];
char dummy[100];
int nama, nneu, npro;
char txtfor[11];
double amsig, amome, amrho;
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
double3(wfg);
double3(wfg_zero);
double2(ee);
double2(vv);
int ntmax;
double1(rmeshorig);
double1(dens0);
double dens0_integ;
int indic_ph;


void in() {

    fstream infile;    
    fstream testfile;    
    fstream densfile;    
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
    double meshtemp;
    int large_only;
    double zpoint;
    double rms_2_in;
    double1(dens0_test);    
    int1init(ntpar,2);
        

    dcount = 0;
    

    infile.open(filename1, ios::in);
    if (!infile) {
	cerr << "\n*** Error opening file " << filename1 << " ***\n";
	cerr << "program is terminating" << endl;
	exit(1);
    }


	
    infile >> nucnam >> nama >> nneu >> npro;    
    dcount += newline(infile);
    
    infile >> txtfor >> amsig >> amome >> amrho;
    dcount += newline(infile);
    
    infile >> gsigs >> gomes >> grhos;
    dcount += newline(infile);

    infile >> a_s >> b_s >> c_s >> d_s;
    dcount += newline(infile);

    infile >> a_v >> b_v >> c_v >> d_v;
    dcount += newline(infile);

    infile >> a_tv;
    dcount += newline(infile);

    infile >> dsat;
    dcount += newline(infile);

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
    cout << "a_s   = " << a_s   << endl;
    cout << "b_s   = " << b_s   << endl;
    cout << "c_s   = " << c_s   << endl;
    cout << "d_s   = " << d_s   << endl;
    cout << "a_v   = " << a_v   << endl;
    cout << "b_v   = " << b_v   << endl;
    cout << "c_v   = " << c_v   << endl;
    cout << "d_v   = " << d_v   << endl;
    cout << "a_tv  = " << a_tv  << endl;
    cout << "dsat  = " << dsat  << endl;

    infile >> nmesh >> hmesh >> rmax;
    dcount += newline(infile);

    cout << "nmesh = " << nmesh << endl;
    cout << "hmesh = " << hmesh << endl;
    cout << "rmax = " << rmax << endl;
    

    if (((nmesh*hmesh)-rmax) > 1.0E-8)
    {
	cout << "error while reading mesh" << endl;
	cout << "program is terminating" << endl;
	exit(1);	
    }
    
    infile >> rms_2_in;
    dcount += newline(infile);
    
    cout << "sqrt(rms_2_in) = " << rms_2_in << endl;

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
    double2init(vv,ntmax,2);
    double3init(wfg,ntmax,2*nmesh,2);
    double3init(wfg_zero,2*nmesh,2,2);    
    double1init(dens0,nmesh);
    
    int kappa_temp;
    int nr_c;
    

    for (it = 1; it <= 2; it++)
    {
	for (n = 1; n <= ntpar[it]; n++) { 
	    infile >> indic_ph >> kappa >> ee[n][it] >> vv[n][it];

	    kap[n][it] = kappa;
	    
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
	    
		
	    dcount += newline(infile);
	    if ((vv[n][it] > half) && (indic_ph == 1))
	      vv[n][it] = 1.0;
	    else if ((vv[n][it] == zero) && (indic_ph == 2))
	      vv[n][it] = 0.0;
	    else if ((vv[n][it] == zero) && (indic_ph == 3)) 
	      vv[n][it] = -1.0;
	    
	    else 
	    {
		cout << "error while reading occupation number" << endl;
		cout << "program is terminating" << endl;
		exit(1);
	    }
	    
		      
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
    

    double1init(testsum,nmesh);


    // calculating density in ground-state 

    double rms_0 = zero;
    
    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    // only occupied states
	    if (vv[i1][it] > half)
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{		   	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],2.0);
		}
		rms_0 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it];		
	    }
	}
    }


    for (it = 1; it <= 2; it++)
    {
	for (i1 = 1; i1 <= ntpar[it]; i1++) 
	{
	    // only occupied states
	    if (vv[i1][it] > half)
	    {
		for (imesh = 0; imesh <= nmesh; imesh++) 
		{	
		    if (imesh == 0)
		      dens0[imesh] += (wfg_zero[i1][it][1]
				       *wfg_zero[i1][it][1]+
				       wfg_zero[i1][it][2]
				       *wfg_zero[i1][it][2])
			*2*nj[i1][it]/(4.*pi); 
		    else
		      dens0[imesh] += (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				       wfg[i1][imesh+nmesh][it]
				       *wfg[i1][imesh+nmesh][it])
			*2*nj[i1][it]/(4.*pi);
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
	    if (vv[i1][it] > half)
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{
	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],3.0);
		}
		rms_1 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it];
		
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
	    if (vv[i1][it] > half)
	    {
		for (imesh = 1; imesh <= nmesh; imesh++) 
		{
	
		    testsum[imesh] = (wfg[i1][imesh][it]*wfg[i1][imesh][it]+
				      wfg[i1][imesh+nmesh][it]
				      *wfg[i1][imesh+nmesh][it])
		      *pow(rmeshorig[imesh],4.0);
		}
		rms_2 += simps(testsum,nmesh,hmesh)
		  *2*nj[i1][it];
		
	    }
	}
    }

    rms_2 /= rms_0;
    

    cout << "rms_0 = " << rms_0 << endl;
    cout << "rms_2 = " << rms_2 << endl;
    cout << "sqrt(rms_2)= " << sqrt(rms_2) << endl;
    cout << "rms_1= " << rms_1 << endl;
    


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
    
	    







