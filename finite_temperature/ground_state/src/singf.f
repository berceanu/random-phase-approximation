c======================================================================c

      subroutine singf(lpr)

c======================================================================c
c
c     calculates single particle matrix elements for Fermions       
c     in the spherical oscillator basis
c
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /single/ sp(nqx,nbx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN SINGF ********************************'
c
      do 10 ib = 1,nb,2
         np = id(ib)
         nm = id(ib+1)
c
c        SIGMA*P
c----------------
         call sigp(nm,np,ib,sp(1,ib),lpr)
         if (ib+1.gt.nbx) stop ' in SINGF: nbx too small'
         do k = 1,nm
         do i = 1,np
            sp(i+(k-1)*np,ib+1) = -sp(k+(i-1)*nm,ib)
         enddo
         enddo
c
   10 continue
C
      if (lpr)
     &write(l6,*) ' ****** END SINGF **********************************'
      return
c-end-SINGF
      end  
c=====================================================================c

      subroutine sigp(nm,np,ib,tt,lpr)

c=====================================================================c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical lpr
      character*8 tb
      character*25 txb
c
      dimension tt(nm,np)
c
      common /baspar/ hom,hb0,b0
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /physco/ amu,hqc,alphi,r0
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /texblo/ tb(ntx),txb(nbx)
c
      j  = ijb(ib)
      lp = j - mod(j,2)
      lm = j - mod(j+1,2)
      if (lp.eq.j) then
         kk =-j
      else
         kk = j
      endif
c
      kk = kk - 1
      f  = one/b0
      do n2 = 1,np
      do n1 = 1,nm
         s = zero
         do ih =1,ngh
            s = s + rnl(n1,lm,ih) * 
     &              ( - rnl1(n2,lp,ih) + kk*rnl(n2,lp,ih)/xh(ih))    
         enddo
         tt(n1,n2) = f*s
      enddo
      enddo
c
      if (lpr) then
         write(l6,'(a)') txb(2*j-1)
         iap = ia(2*j-1) + 1
         iam = ia(2*j) + 1
         call aprint(1,3,1,nm,nm,np,tt,tb(iam),tb(iap),'Sigma * P')
      endif
c
      return
c-end-SIGP
      end
