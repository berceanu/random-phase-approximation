#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"

//
// berechnet 3j-Symbole fuer ganz- und halbzahlige Argumente            
//


double wigner(double j1, double j2, double j3, double m1,
	      double m2, double m3)

{

    int i0, i1, i2, i3, i4, i5, i6, i7, n1, n2;
    double wigret = zero;

    

    i3 = nint0(j2+m2);
    i4 = nint0(j3-j2+m1);
    i7 = nint0(j3-m3);
    
    if (i7 != (i3+i4))
      return wigret;
    
    i0 = nint0(j1+j2+j3+1);
    i1 = nint0(j1+j2-j3);
    i2 = nint0(j1-m1);
    i5 = nint0(j3-j1-m2);
    i6 = nint0(j3+m3);
    
    n1 = max0(3, 0, -i4, -i5);
    n2 = min0(3, i1, i2, i3); 
    

    if (n1 > n2)
      return wigret;
    

    for (int n = n1; n <= n2; n++)
    {
	wigret = wigret+iv[n]*
	         fi[n]*fi[i1-n]*fi[i2-n]*fi[i3-n]*fi[i4+n]*fi[i5+n];
    }
    
    

    wigret *= iv[i2+i4+i6]*
	     wfi[i0]*wf[i1]*wf[i2+i4]*wf[i3+i5]*
	     wf[i1+i4]*wf[i2]*wf[i3]*wf[i1+i5]*wf[i6]*wf[i7];
	
    
    
    return wigret;

}


//
// berechnet 3j-Symbole fuer ganzzahlige Argumente            
//


double wigner(int j1, int j2, int j3, int m1,
	      int m2, int m3)

{

    int i0, i1, i2, i3, i4, i5, i6, i7, n1, n2;
    double wigret = zero;


    if ((m1+m2+m3) != 0)
      return wigret;
    

    i3 = j2+m2;
    i4 = j3-j2+m1;
    
    
    i0 = j1+j2+j3+1;
    i1 = j1+j2-j3;
    i2 = j1-m1;
    i5 = j3-j1-m2;
    
    n1 = max0(3, 0, -i4, -i5);
    n2 = min0(3, i1, i2, i3); 
    

    if (n1 > n2)
      return wigret;
    

    for (int n = n1; n <= n2; n++)
    {
	wigret += iv[n]*
	         fi[n]*fi[i1-n]*fi[i2-n]*fi[i3-n]*fi[i4+n]*fi[i5+n];
    }
    
    

    wigret *= iv[i2+i3]*
	     wfi[i0]*wf[i1]*wf[i2+i4]*wf[i3+i5]*
	     wf[i2]*wf[j1+m1]*wf[j2-m2]*wf[i3]*wf[j3-m3]*wf[j3+m3];
	
    
    
    return wigret;

}

    

