#include "common.h"
#include "base.h"
#include "sla.h"



void msym();


void msym() 
{
    int pa1, pa2;
    

    for (pa1 = 1; pa1 <= npair; pa1++)
    {
	for (pa2 = 1; pa2 < pa1; pa2++)
	{
	    arpa[pa2][pa1] = arpa[pa1][pa2];
	    brpa[pa2][pa1] = brpa[pa1][pa2];
	}
    }
    

    return;
    
}
