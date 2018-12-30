#include "common.h"
#include "sla.h"

// globale Variablen


double2(bc);

void binom();


void binom()

  

//
//     Calculates binomial coefficients                                
//                                                                     
//     bc(n,m)  = (n , m) = n! / (m! (n-m)!)                           
// 
  

{
    
    int i, k;
    
    double2init(bc,ibe,ibe);
    


    bc[0][0] = one;
    
    for (k = 1; k <= ibe; k++)
      bc[0][k] = zero;
    
    for (i = 1; i <= ibe; i++)
    {
	bc[i][0] = one;
	
	for (k = 1; k <= ibe; k++)
	  bc[i][k] = bc[i-1][k-1]+bc[i-1][k];
    }

}








