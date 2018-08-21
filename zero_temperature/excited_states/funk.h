// Definitions of functions not contained in libraries
#ifndef _funk_h
#define _funk_h

#include "common.h"
#include "sla.h"

inline int min0(int ...);

inline int max0(int ...);

inline int max0arr(int*);

inline double max0arr(int, double*);

inline int max0arr(int, int*);

inline double dmax1(double, double);

inline int nint0(double);

inline int abs0(int);

inline double abs0(double);

//inline void errornew();

inline int deltafunk(int, int);

inline double simps(double *, int, double);

double simps2(double *, int, double);

double simps3(double *, int, int, double);


// Max-Function, number of arguments needed

inline int max0(int n1 ...) {

    va_list ap;
    
    va_start(ap,n1);

    int temp = va_arg(ap,int);
    int tempmax = temp;

    for (int i = 1; i < n1; i++) 
    {
	temp = va_arg(ap,int);
	if (temp > tempmax)
	  tempmax = temp;
	
    }

    va_end(ap);

    return (tempmax);
}


inline double dmax1(double x1, double x2) {

// Max-Function for two double-arguments

  if (x1 >= x2)
    return x1;
  else
    return x2;

}

inline int imax1(int i1, int i2) {

// Max-Function for two int-arguments

  if (i1 >= i2)
    return i1;
  else
    return i2;
}



// Min-Function, number of arguments needed

inline int min0(int n1 ...)

{

    va_list ap;
    
    va_start(ap,n1);

    int temp = va_arg(ap,int);
    int tempmin = temp;

    for (int i = 1; i < n1; i++) 
    {
	temp = va_arg(ap,int);
	if (temp < tempmin)
	  tempmin = temp;
	
    }

    va_end(ap);

    return (tempmin);
}

inline double dmin1(double x1, double x2) {

// Min-Function for two double-arguments

  if (x1 <= x2)
    return x1;
  else
    return x2;

}





// gives the 'next integer' in relation to a double value

inline int  nint0(double dzahl)
  
{
    int tempdouble = (int)dzahl;
        
    
    if (abs0(dzahl-tempdouble) < eps)
      return tempdouble;
    
    else if (abs0(dzahl - (tempdouble+1)) < eps)
      return tempdouble+1;
    
    else if (abs0(dzahl - (tempdouble-1)) < eps)
      return tempdouble-1;
    
    else
    {
      cout << "Fehler bei Argument von nint0()!\n";
      exit(1); 
      return 1;
    }
}



// abs-Functions for int- and double-values

inline double abs0(double dzahl)

{
    return fabs(dzahl);
}




inline int abs0(int izahl) 

{
    return abs(izahl);
}



// message-function for allocation of memory

//void errornew() {
//
//    cout << "Zuwenig Speicherplatz bei Allocation!\n";
//    exit(-1);
//    return;
// }




inline int deltafunk(int d1, int d2) {

    int deltaret = 0;


    if (d1 != d2)
      return deltaret;

    deltaret += 1;

    return deltaret;

}




// Simpson-Integration

inline double simps(double *f, int n, double h) {


      
    const double c3d8 = 0.375;
    int npanel, nhalf, nbegin, nend, i;
    double x, result;
    




//     Check to see if number of panels is even.  Number of panels is N-1.
    npanel = n-1;  
    nhalf  = npanel/2;
    nbegin = 1;
    result = zero;    
    if ((npanel-2*nhalf) != 0) 
    {
	
//
//     Number of panels is odd.  Use 3/8 rule on first three
//     panels, 1/3 rule on rest of them.
//
	result = h*c3d8*( f[1] + 3*(f[2]+f[3]) + f[4] );

	if (n == 4) 	       
	  return result;
	nbegin = 4;

    }
    
//
// Apply 1/3 rule - add in first, second, last values
//
    result += h*third*( f[nbegin] + 4*f[nbegin+1] + f[n] );    
    nbegin += 2;   
    if (nbegin == n) 	
      return result;	
    else 
    {	
	x = zero;	
	nend = n-2;	
        for (i = nbegin; i <= nend; i += 2)    
	  x += f[i] + 2*f[i+1];            
	result += h*two*third*x;
    }
   

    return result;
}

#endif
    
    

