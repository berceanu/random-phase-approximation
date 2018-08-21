#ifndef _init_h
#define _init_h

extern void errornew();


extern int *viinit(int);
extern double *vdinit(int);
extern void miinit(int **, int, int);
extern void mdinit(double **, int, int);
extern void dmiinit(int ***, int, int, int);
extern void dmdinit(double ***, int, int, int);

template <class T> 
void ardel(T ar)
{
    delete ar;
    return;
}



#endif
