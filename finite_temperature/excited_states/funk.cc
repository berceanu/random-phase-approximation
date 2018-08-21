#include "common.h"
#include "sla.h"
#include "funk.h"
#include "base.h"






/*

// Error-Function, needed for Yukawa-Terms in Slaterintegrals


double erfcc(double x) {



    double t, z, ans;

    z = abs0(x);

    t = one/(one+half*z);

    ans = t*exp(-z*z-1.26551223+t*(1.00002368+t*(0.37409196+t*(0.09678418+
	  t*(-0.18628806+t*(0.27886807+t*(-1.13520398+t*(1.48851587+
	  t*(-0.82215223+t*0.17087277)))))))));

// Def. aus Wegner-Paper
    ans = ans*sqrt(pi)/2.;

    if (x >= zero) 
      return ans;

    else
      return (2.0-ans);


}


*/


// needed for integrals from 0 to "r"

double simps2(double *f, int n, double h) {


    double simps2ret = zero;
    int nst;


    if (n == 0)
      return simps2ret;
    
    

    if ((n%2) == 0) 
    {	
    
	for (nst = 0; nst <= (n/2-1); nst++)
	  simps2ret += f[2*nst]+4*f[2*nst+1]+f[2*nst+2];
    
	simps2ret *= h*third;
	return simps2ret;
    }
    
    else if ((n%3) == 0)
    {
	for (nst = 0; nst <= (n/3-1); nst++)
	 simps2ret += f[3*nst]+3*f[3*nst+1]+3*f[3*nst+2]+f[3*nst+3];

	simps2ret *= 3./8.*h;
	return simps2ret;
    }
    
 
    else 
    {
	switch(n) 
	{
	    	
	  case 1:
	   
	    simps2ret = h/2.*(f[0]+f[1]);
	    return simps2ret;
	
	  default:
	    

	    for (nst = 0; nst <= ((n-3)/2-1); nst++)
	      simps2ret += f[2*nst]+4*f[2*nst+1]+f[2*nst+2];
    
	    simps2ret *= h*third;

	    simps2ret += 3*h/8.*(f[n-3]+3*f[n-2]+3*f[n-1]+f[n]);    	
	    return simps2ret;
	}
	

    }
    
}

 

// needed for integrals from r to "infinity"


double simps3(double *f, int nstart, int ndiff, double h) {


    double simps3ret = zero;
    int nst;
        



    if (ndiff == 0)
      return simps3ret;


    if ((ndiff%2) == 0) 
    {	
	
	
	for (nst = 0; nst <= (ndiff/2-1); nst++)
	{
	    	    
	    simps3ret += f[2*nst+nstart]+4*f[2*nst+1+nstart]+f[2*nst+2+nstart];
	     
	}
	

	simps3ret *= h*third;
	return simps3ret;
    }
    
    else if ((ndiff%3) == 0)
    {
	for (nst = 0; nst <= (ndiff/3-1); nst++)
	 simps3ret += f[3*nst+nstart]+3*f[3*nst+1+nstart]
	   +3*f[3*nst+2+nstart]+f[3*nst+3+nstart];

	simps3ret *= 3./8.*h;
	return simps3ret;
    }
    
 
    else 
    {
	switch(ndiff) 
	{
	    	
	  case 1:
	   
	    simps3ret = h/2.*(f[0+nstart]+f[1+nstart]);
	    return simps3ret;
	
	  default:
	    

	    for (nst = 0; nst <= ((ndiff-3)/2-1); nst++)
	      simps3ret += f[2*nst+nstart]+4*f[2*nst+1+nstart]
		+f[2*nst+2+nstart];
    
	    simps3ret *= h*third;

	    simps3ret += 3*h/8.*(f[ndiff-3+nstart]+3*f[ndiff-2+nstart]
			      +3*f[ndiff-1+nstart]+f[ndiff+nstart]); 	    
	    return simps3ret;
	}
	

    }
    
}

 




