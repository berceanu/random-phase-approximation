#include "common.h"
#include "funk.h"
#include "mesh.h"
#include "base.h"

double vphfgm(int, int, int, int, int, int, int, int ,int ,int,
	      int, int, int, int, int, int, int, int, int, int, 
	      int, int, int, int, int);




double vphfgm(int j, int s, int t, int nt1, int l1, int j1, int t1, 
	      int nt2, int l2, int j2, int t2,
	      int nt3, int l3, int j3, int t3,
	      int nt4, int l4, int j4, int t4,
	      int bi1, int bi2, int bi3, int bi4, int masspara, int radpara) {


    double vphfgmret = zero;
    int vpll, vpj1, vpj2;



    switch (s) {

	// ohne Spin-Term
      case 0:

	vphfgmret = radialfg(nt1,l1,t1,nt2,l2,t2,nt3,l3,t3,
			     nt4,l4,t4,j,bi1,bi2,bi3,bi4,masspara,radpara)*
			       wph(0,j,j,j1,l1,j2,l2,j3,l3,j4,l4);
				// *isospin(t,t1,t2,t3,t4);



	break;


      case 1:

	// mit Spin-Term

	vpj1 = min0(2,abs0(j-1),j);
	vpj2 = j+1;

	for (vpll = vpj1; vpll <= vpj2; vpll++)  { 
	    
	    vphfgmret += radialfg(nt1,l1,t1,nt2,l2,t2,nt3,l3,t3,nt4,l4,t4,
				  vpll,bi1,bi2,bi3,bi4,masspara,radpara)*
				    wph(1,vpll,j,j1,l1,j2,l2,j3,l3,j4,l4);


	}
	
	//vphfgmret *= isospin(t,t1,t2,t3,t4);


    
	break;

      default:
	cout << "Fehler in vph(): s ungleich 0 oder 1!\n";
	exit(1);

    }


// Yukawa has to be multiplied by hqc

    vphfgmret *= hqc;

    


    return vphfgmret;
    

}

    








