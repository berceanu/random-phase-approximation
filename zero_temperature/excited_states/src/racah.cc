#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"


extern double racah(double, double, double, double, double, double);

extern double racah(int, int, int, int, int, int);

extern double dsq0(double, double, double);

extern double dsq0(int, int, int);



double dsq0(double a, double b, double c)

{

    int i1, i2, i3, i4;
    double dsqret = zero;


    i1 = nint0(a+b-c);
    i2 = nint0(a-b+c);
    i3 = nint0(-a+b+c);
    i4 = nint0(a+b+c)+1;

    if ((i1 < 0) || (i2 < 0) || (i3 < 0))
      return dsqret;

    dsqret = wf[i1]*wf[i2]*wf[i3]*wfi[i4];

    return dsqret;
}


double dsq0(int a, int b, int c)

{

    int i1, i2, i3, i4;
    double dsqret = zero;


    i1 = a+b-c;
    i2 = a-b+c;
    i3 = -a+b+c;
    i4 = a+b+c+1;

    if ((i1 < 0) || (i2 < 0) || (i3 < 0))
      return dsqret;
    

    dsqret = wf[i1]*wf[i2]*wf[i3]*wfi[i4];

    return dsqret;
}




//
// berechnet 6j-Symbole fuer ganz- und halbzahlige Argumente      
// (Formel (6.3.7) aus Edmonds p.99)
//


double racah(double j1, double j2, double j3,
	     double l1, double l2, double l3)

{
    int i1, i2, i3, i4, i5, i6, i7, n1, n2;
    double racahret = zero, trs;
    


    trs = dsq0(j1, j2, j3)*dsq0(j1, l2, l3)*dsq0(l1, j2, l3)*
          dsq0(l1, l2, j3);
 
    if (trs == 0)
      return racahret;


    i1 = nint0(j1+j2+j3);
    i2 = nint0(j1+l2+l3);
    i3 = nint0(l1+j2+l3);
    i4 = nint0(l1+l2+j3);
    i5 = nint0(j1+j2+l1+l2);
    i6 = nint0(j2+j3+l2+l3);
    i7 = nint0(j3+j1+l3+l1);


    n1 = max0(4, i1, i2, i3, i4);
    n2 = min0(3, i5, i6, i7);

    if (n1 > n2)
      return racahret;



    for (int n = n1; n <= n2; n++) {

	racahret = racahret + iv[n]*fak[n+1]*
	           fi[n-i1]*fi[n-i2]*fi[n-i3]*fi[n-i4]*
		   fi[i5-n]*fi[i6-n]*fi[i7-n];
	
    }

    racahret = racahret * trs;

    return racahret;
}




//
// berechnet 6j-Symbole nur fuer ganzzahlige Argumente      
// (Formel (6.3.7) aus Edmonds p.99)
//


double racah(int j1, int j2, int j3,
	     int l1, int l2, int l3)

{
    int i1, i2, i3, i4, i5, i6, i7, n1, n2;
    double racahret = zero, trs;
    

    trs = dsq0(j1, j2, j3)*dsq0(j1, l2, l3)*dsq0(l1, j2, l3)*
          dsq0(l1, l2, j3);
 
    if (trs == 0)
      return racahret;

    
    i1 = j1+j2+j3;
    i2 = j1+l2+l3;
    i3 = l1+j2+l3;
    i4 = l1+l2+j3;
    i5 = j1+j2+l1+l2;
    i6 = j2+j3+l2+l3;
    i7 = j3+j1+l3+l1;

    n1 = max0(4, i1, i2, i3, i4);
    n2 = min0(3, i5, i6, i7);

    if (n1 > n2)
      return racahret;

        
    for (int n = n1; n <= n2; n++) {

	racahret = racahret + iv[n]*fak[n+1]*
	           fi[n-i1]*fi[n-i2]*fi[n-i3]*fi[n-i4]*
		   fi[i5-n]*fi[i6-n]*fi[i7-n];
	
    }

    racahret = racahret * trs;

    return racahret;
}



   


