#include "common.h"
#include "base.h"
#include "sla.h"
#include "funk.h"
#include "mesh.h"
#include "edmonds.h"


double qpmatbpp(int paar1, int paar2, double vp)
{
 double vpa,fac;
 int st1, st2, st3, st4;
 int t1, t2, t3, t4;
 
 st1 = iph[paar1][1];
 st2 = iph[paar1][2];
 st3 = iph[paar2][1];
 st4 = iph[paar2][2]; 
 t1 = t2 = iph[paar1][3];
 t3 = t4 = iph[paar2][3];  
 fac = 1.0/sqrt(double( (1+deltafunk(st1,st2))*(1+deltafunk(st3,st4)) ) );
 vpa = -vp*fac*(vo[st1][t1]*vo[st2][t2]*uo[st3][t3]*uo[st4][t4] +
		   uo[st1][t1]*uo[st2][t2]*vo[st3][t3]*vo[st4][t4]);
		
 return vpa;

}


