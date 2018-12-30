#C++ = cxx -O2 
C++ = g++ -Wno-deprecated

OBJ = relqrpa.o binom.o binomh.o eigenval.o excstr.o funk.o gfv.o incanon.o \
isospin.o qplevel.o lorneu.o  \
mout.o mjin.o mjout.o mbin.o mbout.o  multred.o msym.o nrcfunk.o pair.o  \
qppairout.o paramet.o potdif.o prepint.o racah.o racahs.o radialfg.o rpa.o \
rpaprobe.o rpasort.o s9jslj.o  testint.o trans.o qpbess.o\
transcur.o vphcomp.o vphfgm.o wigner.o wph.o  init.o matcon0.o matcons.o \
qpmatpair.o qpmataph.o qpmatapp.o qpmatbph.o qpmatbpp.o


run: $(OBJ) 
	$(C++) -o $@ $(OBJ) -lm 


relqrpa.o : relqrpa.cc common.h base.h sla.h funk.h edmonds.h mesh.h eigenval.h

binom.o : binom.cc common.h sla.h

binomh.o : binomh.cc common.h sla.h

eigenval.o : eigenval.cc common.h eigenval.h funk.h

excstr.o : excstr.cc base.h common.h edmonds.h funk.h sla.h

funk.o : funk.cc common.h funk.h base.h sla.h

gfv.o : gfv.cc common.h sla.h

incanon.o : incanon.cc common.h base.h funk.h nr.h

isospin.o : isospin.cc base.h common.h funk.h sla.h edmonds.h

qplevel.o : qplevel.cc base.h common.h funk.h

lorneu.o : lorneu.cc base.h common.h

matcon0.o :  matcon0.cc common.h base.h sla.h funk.h mesh.h

matcons.o :  matcons.cc common.h base.h sla.h funk.h mesh.h

mbin.o : mbin.cc bin.h base.h common.h

mbout.o : mbout.cc bin.h base.h common.h

mout.o : mout.cc base.h common.h

mjin.o : mjin.cc base.h common.h

mjout.o : mjout.cc base.h common.h

multred.o : multred.cc base.h common.h edmonds.h funk.h sla.h 

msym.o : msym.cc base.h common.h sla.h

nrcfunk.o : nrcfunk.cc common.h base.h sla.h funk.h mesh.h nr.h nrutil.h

pair.o : pair.cc base.h common.h funk.h

qppairout.o : qppairout.cc base.h common.h

paramet.o : paramet.cc base.h common.h funk.h sla.h

potdif.o : potdif.cc common.h base.h sla.h funk.h mesh.h nr.h nrutil.h

prepint.o: prepint.cc common.h base.h funk.h edmonds.h mesh.h nr.h nrutil.h

qpbess.o : qpbess.cc common.h base.h sla.h funk.h mesh.h nr.h nrutil.h

qpmatpair.o : qpmatpair.cc common.h base.h sla.h funk.h mesh.h nr.h nrutil.h

qpmataph.o : qpmataph.cc common.h base.h sla.h funk.h mesh.h

qpmatapp.o : qpmatapp.cc common.h base.h sla.h funk.h mesh.h

qpmatbph.o : qpmatbph.cc common.h base.h sla.h funk.h mesh.h

qpmatbpp.o : qpmatbpp.cc common.h base.h sla.h funk.h mesh.h

racah.o : racah.cc common.h sla.h funk.h edmonds.h

racahs.o : racahs.cc common.h sla.h funk.h edmonds.h

radialfg.o : radialfg.cc common.h sla.h base.h funk.h mesh.h

rpa.o : rpa.cc common.h base.h funk.h

rpaout.o : rpaout.cc common.h base.h

rpadia.o : rpadia.cc common.h base.h funk.h sla.h 

rpaprobe.o : rpaprobe.cc common.h base.h funk.h sla.h

rpasort.o : rpasort.cc common.h base.h funk.h sla.h

s9jslj.o : s9jslj.cc common.h funk.h sla.h edmonds.h

sdiag.o : sdiag.cc common.h base.h sla.h funk.h

sninj0.o : sninj0.cc common.h sla.h funk.h edmonds.h

testint.o: testint.cc common.h base.h sla.h funk.h edmonds.h mesh.h

trans.o : trans.cc common.h base.h sla.h funk.h edmonds.h

transcur.o : transcur.cc common.h base.h sla.h funk.h edmonds.h

vphcomp.o : vphcomp.cc common.h base.h sla.h funk.h mesh.h edmonds.h

vphfgm.o : vphfgm.cc common.h base.h funk.h mesh.h

wigner.o : wigner.cc common.h sla.h funk.h edmonds.h

wph.o : wph.cc common.h sla.h funk.h edmonds.h

zerleg.o : zerleg.cc common.h base.h sla.h funk.h

init.o : init.cc common.h

clean :
	rm *.bin *.con *.o *.out \
           *.wel run
