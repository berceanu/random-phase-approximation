#ifndef _sla_h
#define _sla_h

const int  igfv = 140;
const int ibe = 100;


// variables from gfv.cc

extern int1(iv);
extern double1(fak);
extern double1(fad);   
extern double1(sq);
extern double1(sqi);
extern double1(sqh);
extern double1(shi);
extern double1(sqd);
extern double1(sqdd);
extern double1(fl);
extern double1(fi);
extern double1(wf);
extern double1(wfi);
extern double1(gm2);
extern double1(gmi);
extern double1(wg);
extern double1(wgi);


// variables from talmi.cc 
extern double a;
extern double a5;
extern double a6;
extern double a15;
extern double a35;
extern double a26;
extern double a46;
extern double2(ak);
extern int ndt;
extern int ndh;


// variables from binom.cc 

extern double2(bc);

// variables from binomh.cc 

extern double2(bch);

// variables from gauss12.cc

extern double1(xh);
extern double1(wh);
extern double1(ph);


// declarations of functions  

extern void talmi(int);

extern double qq(int, int, int, int, int, int, double, double, int);

extern double slater(int, int, int, int, int, int, int, int, int, int, int);

extern void gfv();

extern void binom();

extern void binomh();

extern double wph(int, int, int, int, int, int, int, int, int, int, int);

extern double vph(int, int, int, int, int, int, int, int, int, int, 
		  int, int, int, int, int, int, int, int, int, int, int);

extern int isospin(int, int, int, int, int);

extern double angrel(int, int, int, int, int, int, int, int, int, int, int);

extern double sbessel(int, double);

#endif
