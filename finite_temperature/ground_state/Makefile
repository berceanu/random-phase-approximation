FC = gfortran

OBJ =  dis.o default.o dislib.o base.o densit.o dirac.o expect.o field.o \
inout.o iter.o occup.o plot.o potgh.o prep.o prigh.o radgh.o reader.o \
resu.o singf.o start.o dend1.o dend2.o re.o wavec.o cmcd.o cmcn.o td_out.o \
reinhard_isp.o gauleg.o osc.o rpaout.o
                         
run: $(OBJ) 
	gfortran -o run $(OBJ)

clean :
	rm *.o *.out *.wel \
           *.20 *.m run T0*
