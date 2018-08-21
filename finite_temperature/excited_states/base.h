#ifndef _base_h
#define _base_h

//
// parameters for spherical Dirac-Program
//


// variables from pair.cc

extern int2(iph); 
extern int2(kpp);
extern double1(eph);
extern int npair;
extern int jphmax;
extern int npair_ph;
extern int npair_ah;
extern int lphmax;

// variables from rpa.cc

extern double2(arpa);
extern double2(brpa);
extern double2(xrpa);
extern double2(yrpa);
extern double2(arpas);
extern double2(brpas);
extern double2con(arpac);
extern double2con(brpac);
extern double2con(xrpac);
extern double2con(yrpac);
extern double1con(erpac);
extern double1con(c_erpac);
extern double1(erpa);
extern double1(erpas);
extern double2(rpa_full);
extern double2(xyrpa);
extern double1(c_erpa);
extern double1(c_erpas);
extern int ndim_o_c;
extern int ndim_o_r;

// Variables from incanon.cc
//nucleus
extern char nucnam[3];
extern char dummy[100];
extern int nama, nneu, npro;
//parameters
extern char txtfor[11];
extern double amsig, amome, amrho, amu;
extern double gsigs, gomes, grhos;
extern double a_s, b_s, c_s, d_s;
extern double a_v, b_v, c_v, d_v;
extern double a_tv;
extern double dsat;
// gogny
extern char gogtxt[11];
extern double1(gogw);
extern double1(gogb);
extern double1(gogh);
extern double1(gogm);
extern double1(gogr);
extern double gogt3;
extern double gogwls;
extern double vfac;
//mesh
extern double rmax;
extern double hmesh;
extern int nmesh;
extern double rms_2;
extern double1(rmeshorig);
extern double1(dens0);
extern double dens0_integ;
//coupling constants and their derivatives
extern double1(gsig);
extern double1(gome);
extern double1(grho);
extern double1(dgsig);
extern double1(dgome);
extern double1(dgrho);
extern double1(ddgsig);
extern double1(ddgome);
extern double1(ddgrho);
extern double1(denss);
extern double1(densv);
extern double1(denstv);
extern double2(coupl);
extern double2(dcoupl);
extern double2(ddcoupl);
extern double2(dens);
// states and wave functions
extern int ntmax;
extern int1(ntpar);
extern int2(nr);	    
extern int2(nl);	    
extern int2(nj);
extern int2(kap);
extern double3(wfg);
extern double3(wfg_zero);
// energies and ...
extern double2(ee);
extern double2(eeqp);
extern double2(de);
extern double2(vv);
extern double2(vo);
extern double2(uo);
extern double1(ala);
// blocks and h11
extern int nhx,nb2x,nblock;
extern int2(indinbl);
extern int2(iblock);
extern double3(h11);


// Variables from paramet.cc
extern int j;
extern int parity;
extern double ediffmaxu;
extern double ediffmaxd;
extern int calc;
extern int xyprint; 
extern int lorchange;
extern double lorswidth;
extern double lorvwidth;
extern double hlorswidth;
extern double hlorvwidth;
extern int xyread;
extern int hartree;
extern int matprint;
extern int xyprobe;
extern int exccalc;
extern int transdens;
extern int transiso;
extern double transerg;
extern int tc_cur;
extern int tc_iso;
extern double tc_erg;
extern double qptresh;
extern int respair;
extern int calc_j;
extern int calc_parity;
extern double calc_ediffmaxu;
extern double calc_ediffmaxd;
extern int calc_hartree;
extern int calc_calc;
extern int calc_xyprint; 
extern int calc_lorchange;
extern double calc_lorswidth;
extern double calc_lorvwidth;
extern double calc_hlorswidth;
extern double calc_hlorvwidth;
extern int calcfile_found;


// variables from relqrpa.cc  
extern int nmass;
extern int npot;
extern double1(rmass);
extern int lmax;
extern double2(arpas);
extern double2(brpas);
extern int ljmax;
extern double gcoul;
extern int natural_parity;

// variables from qplevel.cc
extern double enpartmax;
extern double enpartmin;
extern double enholemax;
extern double enholemin;
extern int2(spur);

// variables from rpasort.cc
extern double2(erpa_im);
extern int im_count;

// variables from transcur.cc
extern double3(wfgdev);


// declarations of functions

extern void pair(int, int);

extern void incanon();

extern void mbout(double **, int, char *);

extern void mbout(double **, int, int, char *);

extern void mbin(double **, int, char *);

extern void mbin(double **, int, int, char *);

extern void vbin(double *, int, char *);

extern void vbout(double *, int, char *);

extern void rpa(int);

extern void qppairout(int, int, char *);

extern void paramet(char *);

extern void msym();

extern double elred(int, int, int, int, int, int, int, int, int, int, int);

extern double magred(int, int, int, int, int, int, int, 
		     int, int, int, int);

extern double monred(int, int, int, int, int, int, int, int, int, int);

extern double dipskalred(int, int, int, int, int, int, int, int, int, int);

extern double dipskalred1(int, int, int, int, int, int, int, int, int, int);

extern double diptoroidred(int, int, int, int, int, int, int, int, int, int);

extern double sinrad(int, int, int, int, int, int, int, int, int);

extern void check();

extern double vphcomp(int, int, int, int, int, int, int, int ,int ,int,
		      int, int, int, int, int, int, int, int, int, int,
		      int, int, int, int, int);

extern double vphrel(int, int, int, int, int, int, int, int ,int ,int,
		     int, int, int, int, int, int, int);

extern void qplevel();

extern void prepint();

extern void testint();

extern void lorneu(char *, char *, char *, char *);

extern void rpasort(int, double **, double **, double *, double *);

extern void rpaout(double **, double **, double *, int, int, char *);

extern void rpaprobe(int, double **, double **, double **, double **, 
		     double *);

extern void excstr(double *, double **, double **, int, int, 
		   char *, char *, char *, char *, char *, char *,
		   char *, char *, char *, char *, char *, 
		   double, double, int);

void trans(double *, double **, double **, int, int, char *, char *, int);

void transcur(double *, double **, double **, int, int, char *, char *, int);

extern void mjout(double **, int, int, char *);

extern void mjin(double **, double **, double *, char *, char *, char *);

extern void mout(double **, int, int, char *, char *);



#endif
