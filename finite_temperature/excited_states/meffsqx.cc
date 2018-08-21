#include "common.h"
#include "sla.h"
#include "base.h"
#include "funk.h"
#include "mesh.h"

#define NRANSI
#include "nr.h"


static double sigpol(double);

double meffsqx(double, int);


double meffsqx(double xx, int mapar) 
{



    // returns square of effective mass at arbitrary
    // radius-point xx


    double meffxret = zero;
    double sigosc = zero;

    
    if ((mapar == 1) && (nonlin == 1))
    {
                  
	sigosc = sigpol(xx);

	meffxret = rmass[1]*rmass[1]+2.*g2*sigosc+3.*g3*pow(sigosc,2.);
    
    }
    
    else
      meffxret = rmass[mapar]*rmass[mapar];
    

    return meffxret;
    

}


static double sigpol(double xpol)
{
    
    double y;
    

    y = dsplint(rmeshorig,sigf,sigfderiv,nmesh,xpol);


    return y;
    

}

    
    

