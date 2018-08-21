c=====================================================================c

      subroutine densit(lpr)

c=====================================================================c
C
C     density at the radius r = xh(ih)*b0 is given by
C     b0**(-3) * rv(ih) / ( 4*pi * r**2 ) in units of fm**(-3)
C
c---------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*8 tit
      character*10 txtfor
c
      dimension rf(2),rg(2)
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no      
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /kappa / aka(nqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,npr(2),jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /rhoshe/ rrf(nqx,nb2x),rrg(nqx,nb2x)
      common /rhorho/ rs(ngh,1:2),rv(ngh,1:2),dro(ngh)
      common /rhoro2/ rs2(ngh,1:2),rv2(ngh,1:2)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DENSIT *******************************'
c
      do it = it1,it2
         do ih = 1,ngh
            dro(ih)    = zero
            rs(ih,it)  = zero
            rv(ih,it)  = zero
         enddo
      enddo
c
c     loop over j-blocks
      do 10 ib = 1,nb
         j   = ijb(ib)
         lf  = ilb(ib,1)
         lg  = ilb(ib,2)
         nf  = id(ib,1)
         ng  = id(ib,2)
c
c------- large components
         ll  = lf*(lf+1)
         il = 0
         do n2 =  1,nf
         do n1 = n2,nf
            il = il + 1
c
            do it = it1,it2
               rf(it) = rrf(il,ib+(it-1)*nbx)
            enddo   
c
            nn = 2*(n1+n2+lf)-1
            do ih = 1,ngh
               s  = rnl(n1,lf,ih)*rnl(n2,lf,ih)
               do it = it1,it2
                  rs(ih,it)  = rs(ih,it)  + rf(it)*s
                  rv(ih,it)  = rv(ih,it)  + rf(it)*s
               enddo
c
c------------- Delta-rho for calculation of Coulomb field
               if (icou.gt.0) then
                  xx = xh(ih)*xh(ih)
                  dro(ih) = dro(ih) + 2*rf(2) * ( s*(xx+ll/xx-nn) 
     &                              + rnl1(n1,lf,ih)*rnl1(n2,lf,ih)) 
               endif
            enddo
         enddo
         enddo
c
c------- small components
         ll = lg*(lg+1)
         il = 0
         do n2 =  1,ng
         do n1 = n2,ng
            il = il + 1
c
            do it = it1,it2
               rg(it) = rrg(il,ib+(it-1)*nbx)
            enddo   
c
            nn = 2*(n1+n2+lg)-1
            do ih = 1,ngh
               s  = rnl(n1,lg,ih)*rnl(n2,lg,ih)
               do it = it1,it2
                  rs(ih,it)  = rs(ih,it)  - rg(it)*s
                  rv(ih,it)  = rv(ih,it)  + rg(it)*s
               enddo
c
c------------- Delta-rho for calculation of Coulomb field
               if (icou.gt.0) then
                  xx = xh(ih)*xh(ih)
                  dro(ih) = dro(ih) + 2*rg(2) * ( s*(xx+ll/xx-nn) 
     &                              + rnl1(n1,lg,ih)*rnl1(n2,lg,ih)) 
               endif
            enddo
         enddo
         enddo
   10 continue
c
c
c---- check, whether integral over dro vanishes
      s = zero
      do ih = 1,ngh
         s = s + dro(ih)
      enddo
      if (lpr) write(l6,*) 'integral over dro',s
c
c
c---- normalization and renormalization to particle number
      do it = it1,it2
         s  = zero
         do ih = 1,ngh
            s  =  s + rv(ih,it)
         enddo
         if (lpr) write(l6,'(a,i3,2f15.8)') 
     &                  ' norm of the vector density = ',it,s
         s = npr(it)/s
         bi2 = one/(b0*b0)
         do ih = 1,ngh
            f  = s/wdcor(ih)
            rs(ih,it)   = f*rs(ih,it)
            rv(ih,it)   = f*rv(ih,it)
            if (it.eq.2) dro(ih) = f*dro(ih)*bi2
         enddo
         if (lpr) then
            call prigh(0,ro,b0,'x(fm) ')
            call prigh(1,rs(1,it),one,'ROS '//tis(it))
            call prigh(1,rv(1,it),one,'ROV '//tis(it))
            if (it.eq.2) call prigh(1,dro,one,'DRO  ')
         endif
      enddo
c
c
      if (lpr)
     &write(l6,*) ' ****** END DENSIT *********************************'
      return
C-end-DENSIT
      end
