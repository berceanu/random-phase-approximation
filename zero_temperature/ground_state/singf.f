c======================================================================c

      subroutine singf(lpr)

c======================================================================c
c
c     calculates single particle matrix elements for Fermions       
c     in the spherical oscillator basis
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /single/ sp(nqx,nbx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN SINGF ********************************'
c
      do 10 ib = 1,nb
         nf = id(ib,1)
	 if (nf.eq.0) goto 10
         ng = id(ib,2)
c
c        SIGMA*P
c----------------
         call sigp(nf,ng,ib,sp(1,ib),lpr)
c
   10 enddo
C
      if (lpr)
     &write(l6,*) ' ****** END SINGF **********************************'
      return
c-end-SINGF
      end  
c=====================================================================c

      subroutine sigp(nf,ng,ib,tt,lpr)

c=====================================================================c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
      character*8 tb
      character*25 txb
c
      dimension tt(ng,nf)
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /physco/ amu,hqc,alphi,r0
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
c
      j  = ijb(ib)
      ip = ipb(ib)
      ik = ikb(ib)
      lf = ilb(ib,1)
      lg = ilb(ib,2)
c
      kk = -ik - 1
      f  = hqc/b0
      do n2 = 1,nf
      do n1 = 1,ng
         s = zero
         do ih =1,ngh
            s = s + rnl(n1,lg,ih) * 
     &              ( - rnl1(n2,lf,ih) + kk*rnl(n2,lf,ih)/xh(ih))    
         enddo
         tt(n1,n2) = f*s
      enddo
      enddo
c
      if (lpr) then
	 if (mod(ib,2).eq.1) then
	    iba = ib + 1
	 else
	    iba = ib - 1
	 endif
         write(l6,'(a)') txb(ib)
         i0f = ia(ib,1) + 1
         i0g = ia(ib,2) + 1
         call aprint(1,3,6,ng,ng,nf,tt,tb(i0g),tb(i0f),'Sigma * P')
      endif
c
      return
c-end-SIGP
      end
