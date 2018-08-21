#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "edmonds.h"
#include "mesh.h"


	       
double vphcomp(int j, int s, int t, 
	       int st1, int l1, int j1, int t1, 
	       int st2, int l2, int j2, int t2,
	       int st3, int l3, int j3, int t3, 
	       int st4, int l4, int j4, int t4,
	       int bi1, int bi2, int bi3, int bi4,
	       int masspara, int radpara) {


    double vphcompret = zero;
    
    int jexmin, jexmax, jex;
    

    if ((masspara > nmass) && (masspara != 4)) {
      cout << "wrong mass-parameter in vphcomp()" << endl;
      cout << "program is terminating" << endl;
      exit(1);
    }
   


	
    vphcompret = vphfgm(j,s,t,st1,l1,j1,t1,st2,l2,j2,t2,
			st3,l3,j3,t3,st4,l4,j4,t4,
			bi1,bi2,bi3,bi4,masspara,radpara);




    return vphcompret;

}

