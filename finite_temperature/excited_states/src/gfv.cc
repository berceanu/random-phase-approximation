#include "common.h"
#include "sla.h"

int1(iv);
double1(fak);
double1(fad);   
double1(sq);
double1(sqi);
double1(sqh);
double1(shi);
double1(sqd);
double1(sqdd);
double1(fl);
double1(fi);
double1(wf);
double1(wfi);
double1(gm2);
double1(gmi);
double1(wg);
double1(wgi);


void gfv()
{
    
//
//     Calculates sign, sqrt, factorials, etc. of integers and half int.     
//                                                                           
//     iv(n)  =  (-1)**n                                                     
//     sq(n)  =  sqrt(n)                                                     
//     sqi(n) =  1/sqrt(n)                                                   
//     sqh(n) =  sqrt(n+1/2)                                                 
//     shi(n) =  1/sqrt(n+1/2)
//     sqd(n) =  sqrt(2*n+1)                                               
//     sqdd(n) = sqrt(2*n)
//     fak(n) =  n!                                                          
//     fad(n) =  (2*n+1)!!                                                   
//     fi(n)  =  1/n!                                                        
//     fl(n)  =  log(n!)                                                     
//     wf(n)  =  sqrt(n!)                                                    
//     wfi(n) =  1/sqrt(n!)                                                  
//     gm2(n) =  gamma(n+1/2)                                                
//     gmi(n) =  1/gamma(n+1/2)                                              
//     wg(n)  =  sqrt(gamma(n+1/2))                                          
//     wgi(n) =  1/sqrt(gamma(n+1/2))                           
//


    int1init(iv,igfv);
    double1init(fak,igfv);
    double1init(fad,igfv);   
    double1init(sq,igfv);
    double1init(sqi,igfv);
    double1init(sqh,igfv);
    double1init(shi,igfv);
    double1init(sqd,igfv);
    double1init(sqdd,igfv);
    double1init(fl,igfv);
    double1init(fi,igfv);
    double1init(wf,igfv);
    double1init(wfi,igfv);
    double1init(gm2,igfv);
    double1init(gmi,igfv);
    double1init(wg,igfv);
    double1init(wgi,igfv);





    iv[0]=1;
    sq[0]=zero;
    sqi[0]=1.E30; 
    sqh[0]=sqrt(half);
    shi[0]=1/sqh[0];
    sqd[0]=1.;
    sqdd[0]=zero;
    fak[0]=1.;
    fad[0]=1.;
    fi[0]=1.;
    wf[0]=1.;
    wfi[0]=1.;
    gm2[0]=sqrt(pi);
    gmi[0]=1/gm2[0];
    wg[0]=sqrt(gm2[0]);
    wgi[0]=1/wg[0];
    fl[0]=zero;



    for (int i=1; i <= igfv; i++) {

	iv[i] = -iv[i-1];

	sq[i] = sqrt(double(i));
    
	sqi[i] = 1/sq[i]; 

	sqh[i] = sqrt(i+half);
    
	shi[i] = 1/sqh[i];
    
	sqd[i] = sqrt(double(2*i+1));

	sqdd[i] = sqrt(double(2*i));

	fak[i] = i*fak[i-1];
    
	fad[i] = (2*i+1)*fad[i-1];
    
	fi[i] = 1/fak[i];
    
	fl[i] = log(double(i)) + fl[i-1];

	wf[i] = sq[i]*wf[i-1];
    
	wfi[i] = 1/wf[i];
    
	gm2[i] = (i-half)*gm2[i-1];
    
	gmi[i] = 1/gm2[i];
    
	wg[i] = sqh[i-1]*wg[i-1];
    
	wgi[i] = 1/wg[i];
    
    }

//    cout << "Ende der gfv-Routine\n";

}



