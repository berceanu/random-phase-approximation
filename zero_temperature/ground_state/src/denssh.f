c======================================================================c

      subroutine denssh(it,lpr)

c======================================================================c
c
c     calculates densities in oscillator basis 
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*8 tb,tit
      character*25 txb
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /kappa / aka(nqx,nb2x)
      common /kappag/ akag(nqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /rhoshe/ rrf(nqx,nb2x),rrg(nqx,nb2x)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /wavefg/ fg(2*nhq2x,nb2x)
c
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DENSSH *******************************'
c
c
c---- loop over the j-blocks
      ibl = nbl(it)
      kbl = nrbl(it)
      sp  = zero
      do ib = 1,nb
         nf  = id(ib,1)
         ng  = id(ib,2)
         nh  = nf + ng
         nhfb= nh + nh
         imf = ia(ib,1)+1
         img = ia(ib,2)+1
         m   = ib  + (it-1)*nbx
         mul = 2*ijb(ib)
         lf  = ilb(ib,1)
         lg  = ilb(ib,2)
c
c------- contributions of large components
         il = 0
         do n2 =  1,nf
            do n1 = n2,nf
               i12 = (2 - n2/n1)
               il  = il + 1
c
               rf = zero
               tf = zero
               do k = 1,nf
                  rf = rf + fg(nh+n1+(k-1)*nhfb,m)* 
     &                      fg(nh+n2+(k-1)*nhfb,m) 
                  tf = tf + fg(   n1+(k-1)*nhfb,m)* 
     &                      fg(nh+n2+(k-1)*nhfb,m) 
               enddo
               rf =  mul*rf 
               tf =  mul*tf 
c
c------------- blocking
	       if (ib.eq.ibl) then
                  rf = rf  
     &            - fg(nh+n1+(kbl-1)*nhfb,m)*fg(nh+n2+(kbl-1)*nhfb,m) 
     &            + fg(   n1+(kbl-1)*nhfb,m)*fg(   n2+(kbl-1)*nhfb,m) 
                  tf = tf  
     &            - fg(   n1+(kbl-1)*nhfb,m)*fg(nh+n2+(kbl-1)*nhfb,m) 
	       endif
c
               rrf(il,m) =   i12*rf 
               aka(il,m) = - i12*tf 
            enddo
         enddo
c
c------- contributions of small components
         il = 0
         do n2 =  1,ng
            do n1 = n2,ng
               i12 = (2 - n2/n1)
               il  = il + 1
c
               rg = zero
               tg = zero
               do k = 1,nf
                  rg = rg + fg(nh+nf+n1+(k-1)*nhfb,m)* 
     &                      fg(nh+nf+n2+(k-1)*nhfb,m) 
                  tg = tg + fg(   nf+n1+(k-1)*nhfb,m)* 
     &                      fg(nh+nf+n2+(k-1)*nhfb,m) 
               enddo
               rg  =  mul*rg    
               tg  = -mul*tg 
c
c------------- blocking
	       if (ib.eq.ibl) then
                  rg = rg - fg(nh+nf+n1+(kbl-1)*nhfb,m)*
     &                      fg(nh+nf+n2+(kbl-1)*nhfb,m) 
     &                    + fg(   nf+n1+(kbl-1)*nhfb,m)*
     &                      fg(   nf+n2+(kbl-1)*nhfb,m) 
                  tg = tg - fg(   nf+n1+(kbl-1)*nhfb,m)*
     &                      fg(nh+nf+n2+(kbl-1)*nhfb,m) 
	       endif
c
               rrg(il,m)  = i12*rg 
               akag(il,m) = i12*tg 
            enddo
         enddo
c
c
         if (lpr) then
            write(l6,'(/,a,1x,a)') txb(ib),tis(it)
            call aprint(3,3,1,nf,nf,nf,rrf(1,m),tb(imf),' ','RRF ')
            call aprint(3,3,1,nf,nf,nf,rrg(1,m),tb(imf),' ','RRG ')
            call aprint(3,3,1,nf,nf,nf,aka(1,m),tb(imf),' ','AKA ')
            call aprint(3,3,1,ng,ng,ng,akag(1,m),tb(img),' ','AKAG ')
         endif
      enddo
      sp = half*sp
c     write(l6,*) ' DENSH: spk =',it,sp
c
      if (lpr)
     &write(l6,*) ' ****** END DENSSH *********************************'
      return
c-end-DENSSH
      end      
