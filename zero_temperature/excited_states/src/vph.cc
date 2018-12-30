#include "common.h"
#include "sla.h"
#include "funk.h"

double vph(int, int, int, int, int, int, int, int ,int ,int,
	   int, int, int, int, int, int, int, int, int, int, int);




double vph(int j, int s, int t, int n1, int l1, int j1, int t1, 
	   int n2, int l2, int j2, int t2,
	   int n3, int l3, int j3, int t3,
	   int n4, int l4, int j4, int t4,
	   int potpara, int masspara) {


    double vphret = zero;
    int vpll, vpj1, vpj2;



    switch (s) {

	// ohne Spin-Term
      case 0:


	vphret = slater(n1,l1,n2,l2,n3,l3,n4,l4,j,potpara,masspara)*
	  wph(0,j,j,j1,l1,j2,l2,j3,l3,j4,l4)*
	    isospin(t,t1,t2,t3,t4)*(4*pi);

//	vphret = slater(n1,l1,n2,l2,n3,l3,n4,l4,j,potpara,masspara)*
//	  one*isospin(t,t1,t2,t3,t4)*(4*pi);

	


	break;


      case 1:

	// mit Spin-Term

	vpj1 = min0(2,abs0(j-1),j);
	vpj2 = j+1;

	for (vpll = vpj1; vpll <= vpj2; vpll++)  { 
	    
	    vphret += slater(n1,l1,n2,l2,n3,l3,n4,l4,vpll,
			     potpara,masspara)*
			       wph(1,vpll,j,j1,l1,j2,l2,j3,l3,j4,l4);


	}
	
	vphret *= isospin(t,t1,t2,t3,t4)*(4*pi);


    
	break;

      default:
	cout << "Fehler in vph(): s ungleich 0 oder 1!\n";
	exit(1);

    }

    return vphret;

}

    








