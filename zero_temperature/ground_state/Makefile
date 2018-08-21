FC = gfortran 
#FC = g77

OBJ =  dis.o default.o dislib.o base.o delta.o degen.o kinout.o canon.o  \
       denssh.o densit.o dirhfb.o expect.o field.o gauss.o inout.o iter.o \
       plotw.o plotd.o potgh.o prep.o prigh.o radgh.o reader.o resu.o singf.o \
       start.o dend1.o dend2.o re.o vpair.o gamma.o rdens.o  \
       canout.o osc.o
                         
#run: $(OBJ) 
#	gfortran -o run $(OBJ)

run: $(OBJ)
	$(FC) -o run $(OBJ)

clean :
	rm *.aka *.out *.plo *.o *.pot *.vpp *.wel \
           *.wplo *.txt run
