#include "common.h"
#include "base.h"
#include "sla.h"



void msym();


void msym() 
{
    int pa1, pa2;
    int st1, st2, st3, st4;
    int t1, t2, t3, t4;
    double vv1, vv2, vv3, vv4;

    for (pa1 = 1; pa1 <= npair; pa1++)
    {
	for (pa2 = 1; pa2 < pa1; pa2++)
	{
          st1 = iph[pa1][1];
          st2 = iph[pa2][2];
          st3 = iph[pa1][2];
          st4 = iph[pa2][1];

          t1 = t3 = iph[pa1][3];
          t2 = t4 = iph[pa2][3];

          vv1 = vv[st1][t1];
          vv2 = vv[st2][t2];
          vv3 = vv[st3][t3];
          vv4 = vv[st4][t4];
    
	    arpa[pa2][pa1] = arpa[pa1][pa2]*(vv3-vv1)/(vv2-vv4);
	    brpa[pa2][pa1] = brpa[pa1][pa2]*(vv1-vv3)/(vv4-vv2);
    
 	}
    }
    

    return;
    
}
