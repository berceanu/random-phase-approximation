c======================================================================c

      subroutine gamma(it,lpr)

c======================================================================c
c
c     calculats the Dirac-Matrix in the HFB-equation
c     IT = 1:  neutrons
c          2:  protons
c
c     units:    fields and Hamiltonian in fm^(-1)
c               eigenvalues in MeV
c 
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical  lpr
      character*8 tb,tbb(nhx)
      character*25 txb
c
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /single/ sp(nqx,nbx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN GAMMA ********************************'
c
      emcc2 = 2*amu
c
c
c------- loop over the different j-blocks
         do 30 ib = 1,nb
            nf  = id(ib,1)
            ng  = id(ib,2)
            nh  = nf + ng
            imf = ia(ib,1)
            img = ia(ib,2)
            lf  = ilb(ib,1)
            lg  = ilb(ib,2)
            m   = ib + (it-1)*nbx
c
c           calculation of the Dirac-Matrix:
c-------------------------------------------
            do i2 = 1,nf
            do i1 = 1,ng
               hh(nf+i1+(i2-1)*nh,m) = sp(i1+(i2-1)*ng,ib)
            enddo
            enddo
            call pot(nf,nh,lf,vps(1,it),hh(1,m))
            call pot(ng,nh,lg,vms(1,it),hh(nf+1+nf*nh,m))
            do i = nf+1,nh
               hh(i+(i-1)*nh,m) = hh(i+(i-1)*nh,m) - emcc2
            enddo
c
c           symmetrize HH
            do i2 = 1,nh
            do i1 = i2+1,nh
               hh(i2+(i1-1)*nh,m) = hh(i1+(i2-1)*nh,m)
            enddo
            enddo
c
c           printout
            if (lpr) then
               do i = 1,nf
                  tbb(i) = tb(imf+i)
               enddo
               do i = 1,ng
                  tbb(nf+i) = tb(img+i)
               enddo
               write(l6,'(/,a)') txb(ib)
               call aprint(1,3,6,nh,nh,nh,hh(1,m),tbb,tbb,'HH') 
            endif
c
   30    continue
c
      if (lpr)
     &write(l6,*) ' ****** END GAMMA **********************************'
      return
C-end-GAMMA
      end
