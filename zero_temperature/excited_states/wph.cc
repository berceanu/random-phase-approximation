#include "common.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"



// calculates the angular-part of the ph-matrixelement

double wph(int s, int l, int j, int j1, int l1, int j2, int l2,
	   int j3, int l3, int j4, int l4) {


    double wphret = zero;




    switch (s) {

      case 0:
	
	// l=j !
	
	if (l != j) {
	    cout << "error in wph(): l not equal j for s=0!\n";
	    cout << "execution will be stopped!" << endl;	    
	    exit(1);
	}

	wphret = iv[abs0(j1-j4+l1+l2+l3+l4)]*
		 sqd[l1]*sqd[l2]*sqd[l3]*sqd[l4]*
		 sqdd[j1]*sqdd[j2]*sqdd[j3]*sqdd[j4]*
		 wigner(l2,j,l4,0,0,0)*wigner(l1,j,l3,0,0,0)*
		 racah2(l1,l3,j,j3,j1,1)*racah2(l2,l4,j,j4,j2,1);

	break;


      case 1:

	wphret = 6.*iv[abs0(l+1-j+l1+l2+j2-j4)]*
	         sqd[l1]*sqd[l2]*sqd[l3]*sqd[l4]*(2*l+1)*
		 sqdd[j1]*sqdd[j2]*sqdd[j3]*sqdd[j4]*
		 wigner(l1,l,l3,0,0,0)*wigner(l2,l,l4,0,0,0)*
		 s9jslj(1,l1,l3,l,j1,j3,j)*s9jslj(1,l2,l4,l,j2,j4,j);


	break;

      default:

	cout << "error in wph(): s not equal 0 or 1!\n";
	cout << "execution will be stopped!" << endl;	
	exit(1);

      }



    return wphret;
   



}























