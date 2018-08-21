#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"


// enthaelt spezielle Racahfunktionen

extern double racah1(int, int, int, int, int, int);

extern double racah2(int, int, int, int, int, int);

extern double sdsq10(int, int, int);

extern double sdsq0(int, int, int);

extern double sdsh0(int, int, int);



double sdsq10(int a, int b, int c) {

// Definition nur fuer racah1() gueltig !!
// von a und b muss jeweils 1/2 abgezogen werden

    int i1, i2, i3, i4;
    double sdsq1ret = zero;


    i1 = a+b-c-1;
    i2 = a-b+c;
    i3 = -a+b+c;
    i4 = a+b+c;


    if ((i1 < 0) || (i2 < 0) || (i3 < 0))
      return sdsq1ret;



    sdsq1ret = wf[i1]*wf[i2]*wf[i3]*wfi[i4];

    return sdsq1ret;
}
    

double sdsq0(int a, int b, int c) {

// Definition wie in racah.cc!!


    int i1, i2, i3, i4;
    double sdsqret = zero;

    
    i1 = a+b-c;
    i2 = a-b+c;
    i3 = -a+b+c;
    i4 = a+b+c+1;

    if ((i1 < 0) || (i2 < 0) || (i3 < 0))
      return sdsqret;

  

    sdsqret = wf[i1]*wf[i2]*wf[i3]*wfi[i4];


    return sdsqret;
}


double sdsh0(int a, int b, int c) {

// Definition nur fuer racah2() gueltig!
// von b und c muessen jeweils 1/2 abgezogen werden


    int i1, i2, i3, i4;
    double sdshret = zero;



    i1 = a+b-c;
    i2 = a-b+c;
    i3 = -a+b+c-1;
    i4 = a+b+c;

    if ((i1 < 0) || (i2 < 0) || (i3 < 0))
      return sdshret;




    sdshret = wf[i1]*wf[i2]*wf[i3]*wfi[i4];


    return sdshret;
}





double racah1(int j1, int j2, int j, int l1, int l2, int l) {

// Achtung: j1,j2,l1 und l2 wurden als j1+1/2, j2+1/2 etc. uebergeben!


    int i1, i2, i3, i4, i5, i6, i7, n1, n2;
    double racah1ret = zero, trs;
    
   
    trs = sdsq10(j1,j2,j)*sdsq10(j1,l2,l)*sdsq10(l1,j2,l)*
          sdsq10(l1,l2,j);
 
    if (trs == 0)
      return racah1ret;



    i1 = j1+j2+j-1;
    i2 = j1+l2+l-1;
    i3 = l1+j2+l-1;
    i4 = l1+l2+j-1;
    i5 = j1+j2+l1+l2-2;
    i6 = j2+j+l2+l-1;
    i7 = j+j1+l+l1-1;

    n1 = max0(4,i1,i2,i3,i4);
    n2 = min0(3,i5,i6,i7);

    if (n1 > n2)
      return racah1ret;

    for (int n = n1; n <= n2; n++) {
	
	racah1ret = racah1ret+iv[n]*fak[n+1]*
	            fi[n-i1]*fi[n-i2]*fi[n-i3]*fi[n-i4]*
		    fi[i5-n]*fi[i6-n]*fi[i7-n];
    }


    return (trs*racah1ret);

}



double racah2(int j1, int j2, int j3, int l1, int l2, int l3) {

// Achtung: l1,l2 und l3 wurden als l1+1/2, l2+1/2 etc. uebergeben!



    double trs, racah2ret = zero;
    int i1, i2, i3, i4, i5, i6, i7, n1, n2;



    trs = sdsq0(j1,j2,j3)*sdsh0(j1,l2,l3)*sdsh0(j2,l1,l3)*
          sdsh0(j3,l1,l2);


 
    if (trs == 0)
      return racah2ret;


    i1 = j1+j2+j3;
    i2 = j1+l2+l3-1;
    i3 = l1+j2+l3-1;
    i4 = l1+l2+j3-1;
    i5 = j1+j2+l1+l2-1;
    i6 = j2+j3+l2+l3-1;
    i7 = j3+j1+l3+l1-1;

    n1 = max0(4,i1,i2,i3,i4);
    n2 = min0(3,i5,i6,i7);


    for (int n = n1; n <= n2; n++) {

	racah2ret = racah2ret + iv[n]*fak[n+1]*
	            fi[n-i1]*fi[n-i2]*fi[n-i3]*fi[n-i4]*
		    fi[i5-n]*fi[i6-n]*fi[i7-n];
    }


    return (trs*racah2ret);

}



