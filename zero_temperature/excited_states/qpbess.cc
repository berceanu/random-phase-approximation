#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"

#define float double
#define NRANSI
#include "nr.h"
#include "nrutil.h"

double3(bess);

void qpbess()
{

    int lam,n1,n2;
    double x,z;
    double fxinumr, dxinumr,fxenumr,dxenumr;  
          
     // bessel function in gaussian mesh-points
    double3init(bess,lphmax+1,n_lag,n_lag);
    
     // bessel function in gauss-laguerre mesh points
    for(lam = 0; lam <= lphmax; lam++)
    {
       for(n1 = 1; n1 <= n_lag; n1++)
       {
          for(n2 = 1; n2 <= n_lag; n2++)
          {
	     z = 2.0*sqrt(xlag[n1]*xlag[n2]);
	     bessik(z,(lam+half),&fxinumr,&fxenumr,
			      &dxinumr,&dxenumr);
             bess[lam+1][n1][n2] = fxinumr;
	  }
       }
    } 
}    
      	              
