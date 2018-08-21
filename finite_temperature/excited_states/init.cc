#include "common.h"


int *viinit(int dim1)
{
    int na1;
    int *vec;
    
    vec = new int [dim1+1];
    if (!vec) errornew();
    
    for (na1 = 0; na1 <= dim1; na1++)
      vec[na1] = 0;
    
    return vec;
}


double *vdinit(int dim1)
{
    int na1;
    double *vec;
    
    
    vec = new double [dim1+1];
    if (!vec) errornew();
    
    for (na1 = 0; na1 <= dim1; na1++)    
      vec[na1] = 0.0;
 
        
    
    return vec;
}


int **miinit(int dim1, int dim2)
{
    int na1, na2;
    int **mat;
    

    mat = new int *[dim1+1];
    if (!mat) errornew();
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	mat[na1] = new int [dim2+1];
	if (!mat[na1]) errornew();
    }
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	for (na2 = 0; na2 <= dim2; na2++)
	  mat[na1][na2] = 0;
    }

    return mat;
    
}

    
double **mdinit(int dim1, int dim2)
{
    int na1, na2;
    double **mat;
    

    mat = new double *[dim1+1];
    if (!mat) errornew();
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	mat[na1] = new double [dim2+1];
	if (!mat[na1]) errornew();
    }
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	for (na2 = 0; na2 <= dim2; na2++)
	  mat[na1][na2] = zero;
    }

    return mat;
    
}


int ***dmiinit(int dim1, int dim2, int dim3)
{ 

    int na1, na2, na3;
    int ***mat;
    

    mat = new int **[dim1+1];
    if (!mat) errornew();
    for (na1 = 0; na1 <= dim1; na1++)
    {
	mat[na1] = new int *[dim2+1];
	if (!mat[na1]) errornew();
	for (na2 = 0; na2 <= dim2; na2++)
	{
	    mat[na1][na2] = new int [dim3+1];
	    if (!mat[na1][na2]) errornew();
	}
    }
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	for (na2 = 0; na2 <= dim2; na2++)
	{
	    for (na3 = 0; na3 <= dim3; na3++)
	      mat[na1][na2][na3] = 0;
	}
    }
    
    return mat;

}


double ***dmdinit(int dim1, int dim2, int dim3)
{ 

    int na1, na2, na3;
    double ***mat;
    

    mat = new double **[dim1+1];
    if (!mat) errornew();
    for (na1 = 0; na1 <= dim1; na1++)
    {
	mat[na1] = new double *[dim2+1];
	if (!mat[na1]) errornew();
	for (na2 = 0; na2 <= dim2; na2++)
	{
	    mat[na1][na2] = new double [dim3+1];
	    if (!mat[na1][na2]) errornew();
	}
    }
    
    for (na1 = 0; na1 <= dim1; na1++)
    {
	for (na2 = 0; na2 <= dim2; na2++)
	{
	    for (na3 = 0; na3 <= dim3; na3++)
	      mat[na1][na2][na3] = 0.0;
	}
    }
    
    return mat;

}





// message-function for allocation of memory

void errornew() {

    cout << "Zuwenig Speicherplatz bei Allocation!\n";
    exit(-1);
    return;
}
