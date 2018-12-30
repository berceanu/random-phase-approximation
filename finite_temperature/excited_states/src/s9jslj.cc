#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"


double s9jslj(int, int, int, int, int, int);



//
// berechnet das 9j-Symbol    1/2   1/2  S
//                             l1    l2  L      
//                             j1    j2  J
//  
//

double s9jslj(int s, int l1, int l2, int l,
	      int j1, int j2, int j)

// Achtung: j1 und j2 wurden als j1=j1+1/2 und j2=j2+1/2 uebergeben!
// j bleibt gleich!

{

    int la;
    double s9ret = zero, s0, s1, s2;


    // Test der Parameter
    // alle Drehimpulse positiv?

    if ((l1 < 0) || (l2 < 0) || (l < 0) || (j1 < 0) 
	|| (j2 < 0) || (j < 0)) {
	
	cout << "Fehler bei lj-Argumenten von s9jslj()!\n";
	exit(1); 
    }

    // Dreiecksungleichungen erfuellt?


    if ( (l < abs0(l1-l2)) || (l > (l1+l2)) 
	 || (j < abs0(j1-j2)) || (j > (j1+j2-1))
	 || (l1 < abs0(j1-1)) || (l1 > j1)
	 || (l2 < abs0(j2-1)) || (l2 > j2)
         || (j < abs0(l-s)) || (j > (l+s)))
      return s9ret;






    
    switch (s) {
      case 0:
// l=j !!

	s9ret = iv[j1+l2+j]*sqi[4*j+2]*
	        racah2(j,l2,l1,1,j1,j2);
	
	break;

      case 1:


	if (j == l)
	{
	    la = l+1;
	    s0 = -sq[2*l+1]*sq[l+1]*sqi[l]*shi[1];
	    s2 = iv[j1+l2+la]*racah2(l1,l2,l,j2,j1,1)/(4*l+2);

	}
    

	else
	{
	    la = max0(2,l,j);
	    s0 = sq[la]*shi[1];
	    s2 = zero;
	}
	
	s1 = -racah2(l1,l2,l,1,la,j2)*racah1(j1,j2,j,la,1,l1);
	s9ret = (s1-s2)*s0;

       	break;


      default:

	cout << "Fehler bei s-Argument von s9jslj()!\n" ;
	exit(1);
    }

    return s9ret;

}

