// variables from prepint.cc
extern int n_maingauss;
extern int n_intergauss;
extern int nmixmesh;
extern int nfe;
extern double1(sigfderiv);
extern double3(wfgderiv);
extern double1(radf1i);
extern double1(radf1e);
extern double1(radf2i);
extern double1(radf2e);
extern double1(radint);
extern double3(wfgauss);
extern double1(rmeshex);
extern double1(wlex);
extern double2(rmeshin);
extern double2(wlin);
extern int1(point);
extern int nmixmesh;
extern double1(rmesh);
extern int1(mapex);
extern int2(mapin);
extern double3(wflag);
extern double1(wlag);
extern double1(xlag);
extern int n_lag;

// variables from potdif.cc

extern double3(fxi);
extern double3(fxe); 
extern double3(dxi);
extern double3(dxe);
extern double2(wro);
extern double2(wroerr);
extern int istart;
extern int iende;

// variables from qpbess.cc
extern double3(bess);


// variables from intdif.cc

extern int gloma;

// variables form nrcfunk.cc

extern double dxsav,*xp,**yp;
extern int kmax,kount;
extern int nrhs;


// declarations of functions 


extern void potdif();

extern void sigcof();

extern void qpbess();

extern void radx(double);

extern double sigo(double);

extern double matcon0(int, int);

extern double matcons(int, int);

extern double qpmataph(int, int, double, double);

extern double qpmatbph(int, int, double, double);

extern double qpmatpair(int,int);

extern double qpmatapp(int, int, double);

extern double qpmatbpp(int, int, double);

extern double vphfgm(int, int, int, int, int, int, int, int ,int ,int,
	      int, int, int, int, int, int, int, int, int, int, 
	      int, int, int, int, int);

extern double radialfg(int, int, int, int, int, int, int, int, int,
		       int, int, int, int, int, int, int, int, int, int);

extern double radrel(int, int, int, int, int, int, 
		     int, int, int, int, int);

extern void prepint();
