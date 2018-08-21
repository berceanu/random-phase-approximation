#include "common.h"
#include "base.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"

#define NRANSI
#include "nr.h"


void prepint();

double2(coupl);
double2(dcoupl);
double2(ddcoupl);
double2(dens);
double3(wfgderiv);
double1(radf1i);
double1(radf1e);
double1(radf2i);
double1(radf2e);
double1(radint);
double3(wfgauss);
double1(rmeshex);
double1(wlex);
double2(rmeshin);
double2(wlin);
int1(point);
int nmixmesh;
double1(rmesh);
int1(mapex);
int2(mapin);

double3(wflag);
double1(wlag);
double1(xlag);
int n_lag;

int n_maingauss;
int n_intergauss;
int nfe;



void prepint() 
{

    int n, m, l;
    fstream pointtest;
    fstream pointtest2;
    int pcount = 0;
    int pcurr;
    double x;
    

    // constant used for gaussian integration
    n_maingauss = 45;
    n_intergauss =6;

    nfe = n_maingauss+1;
    
    n_lag = 30;
        

    
    // temporary variables for outer and inner mesh-points

    double1(xltempin);
    double1(wltempin);
    double1(rmeshtempout);
    
    // gauss-laguerre integration
    double1init(wlag,n_lag);
    double1init(xlag,n_lag);

    // temporary variables for interpolation of wave-functions
    
    double1(wfgcop);    
    double1(wfgdecop);

    // derivatives for coupling constants and densities interpolation
    double1(gsigderiv);
    double1(gomederiv);
    double1(grhoderiv);
    double1(dgsigderiv);
    double1(dgomederiv);
    double1(dgrhoderiv);
    double1(ddgsigderiv);
    double1(ddgomederiv);
    double1(ddgrhoderiv);    
    double1(denssderiv);
    double1(densvderiv);
    double1(denstvderiv);
    double1init(gsigderiv,nmesh);
    double1init(gomederiv,nmesh);
    double1init(grhoderiv,nmesh);
    double1init(dgsigderiv,nmesh);
    double1init(dgomederiv,nmesh);
    double1init(dgrhoderiv,nmesh);
    double1init(ddgsigderiv,nmesh);
    double1init(ddgomederiv,nmesh);
    double1init(ddgrhoderiv,nmesh);    
    double1init(denssderiv,nmesh);
    double1init(densvderiv,nmesh);
    double1init(denstvderiv,nmesh);
       
    // derivatives on original mesh for interpolation and copy-arrays
    // large and small components
    
    double3init(wfgderiv,ntmax,2*nmesh,2);
    double1init(wfgcop,nmesh)
    double1init(wfgdecop,nmesh);

    // variable for outer mesh

    double1init(rmeshex,nfe-1);
    double1init(wlex,nfe-1);
    int1init(mapex,nfe-1);
    
      
    // variable for inner mesh

    double2init(rmeshin,nfe,n_intergauss);
    double2init(wlin,nfe,n_intergauss);
    int2init(mapin,nfe,n_intergauss);
    
    // points per finite element

    int1init(point,nfe);
    
    // inserting values, value for first element lower than ngauss

    point[1] = 6;
    for (n = 2; n <= nfe; n++)
      point[n] = n_intergauss;
    

    // total value of inner and outer points

    for (n = 1; n <= nfe; n++)
      pcount += point[n];
    
    nmixmesh = pcount + (nfe-1);
    
    // initialization for interpolated coupling constants and densities
    double2init(coupl,3,nmixmesh);
    double2init(dcoupl,3,nmixmesh);
    double2init(ddcoupl,3,nmixmesh);   
    double2init(dens,3,nmixmesh);
        
    // initialization for interpolated functions
   
    double1init(radf1i,nmixmesh); 
    double1init(radf1e,nmixmesh);    
    double1init(radf2i,nmixmesh);
    double1init(radf2e,nmixmesh);

    // interpolated wave-functions

    double3init(wfgauss,ntmax,2*nmixmesh,2);
    double3init(wflag,ntmax,2*n_lag,2);


    // initialization for temporary variables

    
    double1init(rmeshtempout,(nfe+1));    
    double1init(xltempin,n_intergauss);
    double1init(wltempin,n_intergauss);
    
    // initialization for common mesh

    double1init(rmesh,nmixmesh);

    // derivatives for coupling constants and densities interpolation

    dspline(rmeshorig,gsig,nmesh,YP,YP,gsigderiv);
    dspline(rmeshorig,gome,nmesh,YP,YP,gomederiv);	
    dspline(rmeshorig,grho,nmesh,YP,YP,grhoderiv);
    dspline(rmeshorig,dgsig,nmesh,YP,YP,dgsigderiv);
    dspline(rmeshorig,dgome,nmesh,YP,YP,dgomederiv);
    dspline(rmeshorig,dgrho,nmesh,YP,YP,dgrhoderiv);
    dspline(rmeshorig,ddgsig,nmesh,YP,YP,ddgsigderiv);
    dspline(rmeshorig,ddgome,nmesh,YP,YP,ddgomederiv);
    dspline(rmeshorig,ddgrho,nmesh,YP,YP,ddgrhoderiv);    
    dspline(rmeshorig,denss,nmesh,YP,YP,denssderiv);
    dspline(rmeshorig,densv,nmesh,YP,YP,densvderiv);	
    dspline(rmeshorig,denstv,nmesh,YP,YP,denstvderiv);    
    

    // derivatives for wave-function-interpolation

   
    for (n = 1; n <= 2; n++) 
    {
	for (m = 1; m <= ntpar[n]; m++) 
	{
	    // large components

	    for (l = 1; l <= nmesh; l++) 
	    {		
		wfgcop[l] = wfg[m][l][n];
	    }
	    
	    dspline(rmeshorig,wfgcop,nmesh,YP,YP,wfgdecop);
		
	    for (l = 1; l <= nmesh; l++) 
	    {		
		wfgderiv[m][l][n] = wfgdecop[l];
	    }
	    
	    // small components
	    for (l = 1; l <= nmesh; l++) 
	    {		
		wfgcop[l] = wfg[m][l+nmesh][n];
	    }
	    
	    dspline(rmeshorig,wfgcop,nmesh,YP,YP,wfgdecop);
		
	    for (l = 1; l <= nmesh; l++) 
	    {		
		wfgderiv[m][l+nmesh][n] = wfgdecop[l];
	    }
	}
    }


    // new outer Gaussian-Meshpoints and weights

    gauleg(0.,rmax,rmeshex,wlex,(nfe-1));
    gaulag(xlag,wlag,n_lag,0.25);
     
    for (n = 1; n < nfe; n++) 
    {	
	rmeshtempout[n+1] = rmeshex[n];	
	
    }


    rmeshtempout[1] = zero;
    rmeshtempout[nfe+1] = rmax;
    

    // new inner Gaussian-Meshpoints and weights
    
    for (n = 1; n <= nfe; n++) 
    {
	pcurr = point[n];
	
	gauleg(rmeshtempout[n],rmeshtempout[n+1],xltempin,wltempin,pcurr);

	for (m = 1; m <= pcurr; m++) 
	{
	    rmeshin[n][m] = xltempin[m];
	    wlin[n][m] = wltempin[m];
	    
	}
    }


    
    // putting together the inner and outer mesh points to a common mesh

    pcount = 0;
    
    for (n = 1; n <= nfe; n++) 
    {
	for (m = 1; m <= point[n]; m++) {
	    pcount++;
	    rmesh[pcount] = rmeshin[n][m];
	    mapin[n][m] = pcount;	    
	}
	if (n < nfe) 
	{
	    pcount++;
	    rmesh[pcount] = rmeshex[n];
	    mapex[n] = pcount;	    
	}
    }
    

    // check

    if (pcount != nmixmesh) 
    {
	cout << "Error in bulding common mesh!" << endl;
	cout << "Program will be terminated!" << endl;
	exit(1);
	
    }
    
    // interpolation of coupling constants and densities over mesh
    for (l = 1; l <= nmixmesh; l++)
    {
        coupl[1][l] = dsplint(rmeshorig,gsig,gsigderiv,nmesh,rmesh[l]);
	coupl[2][l] = dsplint(rmeshorig,gome,gomederiv,nmesh,rmesh[l]);
	coupl[3][l] = dsplint(rmeshorig,grho,grhoderiv,nmesh,rmesh[l]);
        dcoupl[1][l] = dsplint(rmeshorig,dgsig,dgsigderiv,nmesh,rmesh[l]);
        dcoupl[2][l] = dsplint(rmeshorig,dgome,dgomederiv,nmesh,rmesh[l]);
        dcoupl[3][l] = dsplint(rmeshorig,dgrho,dgrhoderiv,nmesh,rmesh[l]);
        ddcoupl[1][l] = dsplint(rmeshorig,ddgsig,ddgsigderiv,nmesh,rmesh[l]);
        ddcoupl[2][l] = dsplint(rmeshorig,ddgome,ddgomederiv,nmesh,rmesh[l]);
        ddcoupl[3][l] = dsplint(rmeshorig,ddgrho,ddgrhoderiv,nmesh,rmesh[l]);	
        dens[1][l] = dsplint(rmeshorig,denss,denssderiv,nmesh,rmesh[l]);
	dens[2][l] = dsplint(rmeshorig,densv,densvderiv,nmesh,rmesh[l]);
	dens[3][l] = dsplint(rmeshorig,denstv,denstvderiv,nmesh,rmesh[l]); 	
    }

    // interpolation of wave-functions over rmesh 


    for (n = 1; n <= 2; n++) 
    {
	for (m = 1; m <= ntpar[n]; m++) 
	{

	    // large components

	    // first loop over input-mesh

	    for (l = 1; l <= nmesh; l++)
	    {
		wfgdecop[l] = wfgderiv[m][l][n];
		wfgcop[l] = wfg[m][l][n];
	    }
	    
	    // second loop over integration-mesh

	    for (l = 1; l <= nmixmesh; l++)
	    {		
		wfgauss[m][l][n] = 
		  dsplint(rmeshorig,wfgcop,wfgdecop,nmesh,rmesh[l]);
	    }

	    // small components

	    for (l = 1; l <= nmesh; l++)
	    {
		wfgdecop[l] = wfgderiv[m][l+nmesh][n];
		wfgcop[l] = wfg[m][l+nmesh][n];
	    }
	    
	    // second loop over integration-mesh

	    for (l = 1; l <= nmixmesh; l++)
	    {		
		wfgauss[m][l+nmixmesh][n] = 
		  dsplint(rmeshorig,wfgcop,wfgdecop,nmesh,rmesh[l]);
	    }	    
	    // gauss-laguerre
	    for (l = 1; l <= nmesh; l++)
	    {
		wfgdecop[l] = wfgderiv[m][l][n];
		wfgcop[l] = wfg[m][l][n];
	    }
	    // first gaussian
	    for (l=1; l <= n_lag; l++)
	    {
	       x = sqrt(xlag[l])*gogr[1]; 
	       wflag[m][l][n] = 
	         dsplint(rmeshorig,wfgcop,wfgdecop,nmesh,x); 
	      //  if(n==1 && m == 5) 
		//      cout << x << " " << wflag[m][l][n] << endl;	        
            }
	    // second gaussian
	    for (l=1; l <= n_lag; l++)
	    {
	       x = sqrt(xlag[l])*gogr[2]; 
	       wflag[m][n_lag+l][n] = 
	         dsplint(rmeshorig,wfgcop,wfgdecop,nmesh,x); 	        
            }	    
	}
    }

    // freeing allocated space 

    double3del(wfgderiv);
    double1del(wfgcop);
    double1del(wfgdecop);
    double1del(xltempin);
    double1del(wltempin);
    double1del(rmeshtempout);
    double1del(gsigderiv);
    double1del(gomederiv);
    double1del(grhoderiv);
    double1del(dgsigderiv);
    double1del(dgomederiv);
    double1del(dgrhoderiv);
    double1del(ddgsigderiv);
    double1del(ddgomederiv);
    double1del(ddgrhoderiv);   
    double1del(denssderiv);
    double1del(densvderiv);
    double1del(denstvderiv);    
}

	
	
	
    
