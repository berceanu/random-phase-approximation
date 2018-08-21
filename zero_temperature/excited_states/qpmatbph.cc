#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"

static int lcal(int, int, int);


double qpmatbph(int paar1, int paar2,double v0,double vs)

{
    
            
    int j1, j2, j3, j4;
    int l1, l2, l3, l4; 
    int l1s, l2s, l3s, l4s;
    int st1, st2, st3, st4;
    int t1, t2, t3, t4;    
    int bi1, bi2, bi3, bi4;
    int coul;
    double qpmatbph;
    double fac0,fac1,fac2;    

    st1 = iph[paar1][1];
    st2 = iph[paar2][2];
    st3 = iph[paar1][2];
    st4 = iph[paar2][1];

    t1 = t3 = iph[paar1][3];
    t2 = t4 = iph[paar2][3];
       
    l1s = nl[st1][t1];
    l2s = nl[st2][t2];
    l3s = nl[st3][t3];
    l4s = nl[st4][t4];

    j1 = nj[st1][t1];
    j2 = nj[st2][t2];
    j3 = nj[st3][t3];
    j4 = nj[st4][t4];


   
    fac0 = 1.0/sqrt(double( (1+deltafunk(st1,st3))*(1+deltafunk(st2,st4)) ) );   

    fac1 = ((uo[st1][t1]*vo[st3][t3]*uo[st4][t4]*vo[st2][t2]) +
		(vo[st1][t1]*uo[st3][t3]*vo[st4][t4]*uo[st2][t2]));
    fac2 = ((uo[st1][t1]*vo[st3][t3]*vo[st4][t4]*uo[st2][t2]) +
		(vo[st1][t1]*uo[st3][t3]*uo[st4][t4]*vo[st2][t2]));
    
    qpmatbph = (v0*iv[j]+vs*iv[j+1])*fac0*fac1+fac0*fac2*(v0+vs);


    return qpmatbph;
    


    
}



static int lcal(int lc, int jc, int bil)
{
    

    if (bil == 1)
      return lc;
    
    else 
    {
	if (lc < jc)
	  return jc;
	else
	  return (lc-1);
    }
}

