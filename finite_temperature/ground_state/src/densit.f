c=====================================================================c

      subroutine densit(lpr)

c=====================================================================c
C
C     density at the radius r = xh(ih)*b0 is given by
C     b0**(-3) * rv(ih) / ( 4*pi * r**2 ) in units of fm**(-3)
C
c---------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
c
      dimension frs(2),frv(2)
c
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,npr(2),jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /rhoshe/ rrs(nqx,nb2x),rrv(nqx,nb2x)
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DENSIT *******************************'
c
c
      do it = it1,it2
         do ih = 1,ngh
            dro(ih)   = zero
            rs(ih,it) = zero
            rv(ih,it) = zero
         enddo
      enddo
c
c     loop over j-blocks
      do 10 ib = 1,nb
         j   = ijb(ib)
         l   = ilb(ib)
         nd  = id(ib)
         ll  = l*(l+1)
c
         do 20 n2 =  1,nd
         do 20 n1 = n2,nd
            i12 = 2 - n2/n1
c
            do it = it1,it2
               frs(it) = rrs(n1+(n2-1)*nd,ib+(it-1)*nbx)*i12
               frv(it) = rrv(n1+(n2-1)*nd,ib+(it-1)*nbx)*i12
            enddo   
c
            nn = 2*(n1+n2+l)-1
            do ih = 1,ngh
               s         = rnl(n1,l,ih)*rnl(n2,l,ih)
               do it = it1,it2
                  rs(ih,it) = rs(ih,it) + frs(it)*s
                  rv(ih,it) = rv(ih,it) + frv(it)*s
               enddo
               if (icou.gt.0) then
                  xx = xh(ih)*xh(ih)
                  dro(ih) = dro(ih) + 2*frv(2) * ( s*(xx+ll/xx-nn) 
     &                              + rnl1(n1,l,ih)*rnl1(n2,l,ih)) 
               endif
            enddo
   20    continue
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
      if (lpr) call prigh(0,rb,one,'x(fm) ')
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
            rs(ih,it)  = f*rs(ih,it)
            rv(ih,it)  = f*rv(ih,it)
            if (it.eq.2) dro(ih) = f*dro(ih)*bi2
         enddo
         if (lpr) then
            call prigh(1,rs(1,it),one,'ROS '//tis(it))
            call prigh(1,rv(1,it),one,'ROV '//tis(it))
            if (it.eq.2) call prigh(1,dro(1),one,'DRO  ')
         endif
      enddo
c
c
      if (lpr)
     &write(l6,*) ' ****** END DENSIT *********************************'
      return
C-end-DENSIT
      end
c======================================================================c

      subroutine denssh(lpr)

c======================================================================c
c
c     calculates densities in oscillator basis 
c
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*8 tb
      character*25 txb
c
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /rhoshe/ rrs(nqx,nb2x),rrv(nqx,nb2x)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /texblo/ tb(ntx),txb(nbx)
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /wavefg/ fg(nq2x,nb2x)
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DENSSH *******************************'
c
c---- loop over the j-blocks
      do 10 ib = 1,nb
         ibg = ib - 1 + 2*mod(ib,2)
         nf  = id(ib)
         ng  = id(ibg)
         nd  = nf + ng
         imf = ia(ib)
         img = ia(ibg)
c
c------- loop over neutron and proton
         do 20 it = it1,it2
            mf  = ib  + (it-1)*nbx
            mg  = ibg + (it-1)*nbx
c
c---------- loop over the n-quantum numbers
            do 30 n2 =  1,nf
            do 30 n1 = n2,nf
               i12 = 2 - n2/n1
c
               sf = zero
               do k = 1,nf  
                     sf = sf + fg(n1+(k-1)*nd,mf) 
     &                    *fg(n2+(k-1)*nd,mf)*vv(imf+k,it)
               enddo
               sg = zero
               do k = 1,ng
                     sg = sg + fg(ng+n1+(k-1)*nd,mg) 
     &                    *fg(ng+n2+(k-1)*nd,mg)*vv(img+k,it)
c               write(l6,*)'ib= ', ib, '  k= ',k,'  ', vv(img+k,it)
               enddo
               rrs(n1+(n2-1)*nf,mf) = sf-sg
               rrv(n1+(n2-1)*nf,mf) = sf+sg 
   30       continue
c
            if (lpr) then
               write(l6,'(/,a,1x,a)') txb(ib),tis(it)
               call aprint(2,2,1,nf,nf,nf,rrs(1,mf),
     &                     tb(imf+1),' ','RRS ')
               call aprint(2,2,1,nf,nf,nf,rrv(1,mf),
     &                     tb(imf+1),' ','RRV ')
            endif
   20    continue
   10 continue
c
      if (lpr)
     &write(l6,*) ' ****** END DENSSH *********************************'
      return
c-end-DENSSH
      end      
