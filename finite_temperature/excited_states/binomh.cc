#include "common.h"
#include "sla.h"

// globale Variablen

double2(bch);


void binomh();



void binomh()


//
//     Calculates binomial coefficients                                  
//                                                                       
//     bch(n,m) = (n-1/2,m) = gamma(n+1/2) / ( m! gamma(n-m+1/2))        
// 

{
    int k, i;
    
    double2init(bch,ibe,ibe);
    

    bch[0][0] = one;
    

    for (k = 1; k <= ibe; k++)
      bch[0][k] = bch[0][k-1]*(half-k)/k;
    
    for (i = 1; i<= ibe; i++)
    {
	bch[i][0] = one;
	
	for (k = 1; k<= ibe; k++)
	  bch[i][k] = bch[i-1][k-1]+bch[i-1][k];
    }
}
