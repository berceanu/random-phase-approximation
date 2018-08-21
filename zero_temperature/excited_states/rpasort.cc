#include "common.h"
#include "base.h"
#include "funk.h"
#include "sla.h"


double2(erpa_im);
int im_count;


void rpasort(int np, double **xx, double **yy, double *e, double *c_e) {


    // sorting energy-eigenvalues

    int n, i1, i2;    
    int i, l, j;
    double w1, w2;
    double c_w1;    
    double1(xcop);
    double1(ycop);
    


    n = 2*np;

    double1init(xcop,np);
    double1init(ycop,np);
    
    
    for (i = 1; i < n; i++) 
    {
	w1 = e[i];
	w2 = w1;	
	i1 = i;
	i2 = i1;
	

	for (l = i+1; l <= n; l++)
	{
	    if (e[l] < w1) 
	    {		
		w1 = e[l];
		i1 = l;
	    }	    
	}
	
	if (w1 != w2) 
	{
	    
	    e[i2] = w1;
	    e[i1] = w2;
	    c_w1 = c_e[i1];
	    c_e[i1] = c_e[i2];
	    c_e[i2] = c_w1;
	    
	    for (j = 0; j <= np; j++) {
		xcop[j] = xx[j][i2];
		xx[j][i2] = xx[j][i1];
		xx[j][i1] = xcop[j];		
		ycop[j] = yy[j][i2];
		yy[j][i2] = yy[j][i1];
		yy[j][i1] = ycop[j];		
	    }
	    
	}
    }

    
    
    // check for imaginary eigenvalues

    for (i = 1; i <= n; i++)
    {
	if (c_e[i] != 0.0) 
	{
	    cout << "imaginary eigenvalue: " << c_e[i] << endl;
	    cout << "corresponding real part: " << e[i] << endl;
	    im_count++;	    
	}
    }
    

    double2init(erpa_im,im_count,2);
    
    int imc = 0;
    

    for (i = 1; i <= n; i++)
    {
	if (c_e[i] != 0.0) 
	{
	    imc++;	    
	    erpa_im[imc][1] = c_e[i];
	    erpa_im[imc][2] = e[i];
	}
    }
    

    cout << im_count << " imaginary eigenvalues found!" << endl;
    



}


	


