
#ifndef _common_h
#define _common_h


//#include <iostream.h>
#include <iomanip>
//#include <stdiostream.h>
#include <fstream>
#include <math.h>
#include <stdlib.h>
#include <stdarg.h> 
#include <string.h>
#include <iostream>
using namespace std;

// Definition for constants 
 
const double pi = 3.141592653589793;
const double zero = 0.0;
const double one = 1.0;
const double two = 2.0;
const double half = 0.5;
const double third = 1.0/3.0;
const double eps = 0.001;
const double hqc = 197.328284;


// Definition for Routine spline

#define YP 1.e31


extern void errornew();
extern int *viinit(int);
extern double *vdinit(int);
extern int **miinit(int, int);
extern double **mdinit(int, int);
extern int ***dmiinit(int, int, int);
extern double ***dmdinit(int, int, int);

#define double1(var) double *var
#define double2(var) double **var
#define double3(var) double ***var
#define int1(var) int *var
#define int2(var) int **var
#define int3(var) int ***var

#define double1init(var1,var2) { var1=vdinit(var2); }
#define double2init(var1,var2,var3) { var1=mdinit(var2,var3); }
#define double3init(var1,var2,var3,var4) { var1=dmdinit(var2,var3,var4); }

#define double1del(var1) { delete [] var1; }  
#define double2del(var1) { delete [] var1; } 
#define double3del(var1) { delete [] var1; }  

#define int1init(var1,var2) { var1=viinit(var2); }
#define int2init(var1,var2,var3) { var1=miinit(var2,var3); }
#define int3init(var1,var2,var3,var4) { var1=dmiinit(var2,var3,var4); }

#define int1del(var1) { delete [] var1; } 
#define int2del(var1) { delete [] var1; }
#define int3del(var1) { delete [] var1; } 


#define double1con(var) double *var
#define double2con(var) double **var
#define double3con(var) double ***var
#define int1con(var) int *var
#define int2con(var) int **var
#define int3con(var) int ***var 
#define double1initcon(var1,var2) { var1=vdinit(var2); }
#define double2initcon(var1,var2,var3) { var1=mdinit(var2,var3); }
#define double3initcon(var1,var2,var3,var4) { var1=dmdinit(var2,var3,var4); }
#define int1initcon(var1,var2) { var1=viinit(var2); }
#define int2initcon(var1,var2,var3) { var1=miinit(var2,var3); }
#define int3initcon(var1,var2,var3,var4) { var1=dmiinit(var2,var3,var4); }



#endif
