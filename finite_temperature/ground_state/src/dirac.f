c======================================================================c

      subroutine dirac(lpr)

c======================================================================c
c
c     solves the Dirac-Equation in spherical oscillator basis c
c     units:    fields and Hamiltonian in fm^(-1)
c               eigenvalues in MeV
c 
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      logical  lpr
      character*8 tb,tbb(nd2x)
      character*25 txb
c
      dimension e(nd2x),ez(nd2x)
      dimension hh(nq4x)
c
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /dimens/ n0f,n0b,nrm,nlm
      common /eeeeee/ ee(ntx,2),v2(ntx,2),vv1(ntx,2),mu(ntx)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /physco/ amu,hqc,alphi,r0
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2),vps1(ngh,1:2),
     &			vms1(ngh,1:2)
      common /single/ sp(nqx,nbx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /texblo/ tb(ntx),txb(nbx)
      common /wavefg/ fg(nq2x,nb2x)
      
      common /eerpa/ erpa(nd2x,nb2x),vvrpa(nd2x,nb2x),hhrpa(nq4x,nb2x)
     &,nrpa(2)
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DIRAC ********************************'
c
      emcc2 = 2*amu/hqc
      nrpa=0
c
c
c     loop over protons and neutrons 
C-----------------------------------
      do 10 it = it1,it2
c
c
c------- loop over the different j-blocks
         do 30 ib = 1,nb
            ibg = ib - 1 + 2*mod(ib,2)
            nf  = id(ib)
            ng  = id(ibg)
            nd  = nf + ng
            imf = ia(ib)
            img = ia(ibg)
            lf  = ilb(ib)
            lg  = ilb(ibg)
            m   = ib + (it-1)*nbx
c
c           calculation of the Dirac-Matrix:
C-------------------------------------------
            do i2 = 1,nf
            do i1 = 1,ng
               hh(nf+i1+(i2-1)*nd) = sp(i1+(i2-1)*ng,ib)
            enddo
            enddo
            call pot(nf,nd,lf,vps(1,it),hh)
            call pot(ng,nd,lg,vms(1,it),hh(nf+1+nf*nd))
            do i = nf+1,nd
               hh(i+(i-1)*nd) = hh(i+(i-1)*nd) - emcc2
            enddo
c
c           cut off large components with highest N
            if (2*(nf-1)+lf.gt.n0f) then
               do i = 1,nf
                  hh(nf+(i-1)*nd) = zero
               enddo
               do i = nf+1,nd
                  hh(i+(nf-1)*nd) = zero
               enddo
               hh(nf+(nf-1)*nd) = 1000.0
            endif 
            if (lpr) then
               do i = 1,nf
                  tbb(i) = tb(imf+i)
               enddo
               do i = 1,ng
                  tbb(nf+i) = tb(img+i)
               enddo
               write(l6,'(/,a)') txb(ib)
               call aprint(2,2,1,nd,nd,nd,hh,tbb,' ','HH') 
            endif
c
c---------- Diagonalization:
            call sdiag(nd,nd,hh,e,hh,ez,+1)
c           call aprint(1,1,1,1,1,nd,e,' ',' ','E')
c           call aprint(1,2,1,nd,nd,nd,hh,tbb,' ','XX')
            do k = 1,nf
               ee(imf+k,it) = e(ng+k)*hqc
               do i = 1,nd
                  fg(i+(k-1)*nd,m) = hh(i+(ng+k-1)*nd)
               enddo
            enddo
c-----------added for RPA
            mf=ib + (it-1)*nbx
            do k=1,nd 
               erpa(k,mf)=e(k)*hqc
            enddo
            nrpa(it)=nrpa(it)+nd
            do k=1,nd
               do i=1,nd
                  hhrpa(i+(k-1)*nd,mf)=hh(i+(k-1)*nd)
               enddo
            enddo
c----------added over            
            if (lpr) then
               call aprint(1,1,1,1,1,nf,ee(imf+1,it),' ',' ','E')
               call aprint(1,2,1,nd,nd,nf,fg(1,m),tbb,' ','FG')
            endif
   30    continue
   10 continue
 
c

      if (lpr)
     &write(l6,*) ' ****** END DIRAC **********************************'
      return
C-end-DIRAC
      end
c======================================================================c

      subroutine pot(n,nd,l,v,tt)

c======================================================================c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      dimension tt(nd,nd),v(ngh)
c
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
c
      do 10 n2 = 1,n
      do 10 n1 = n2,n
         s = 0.0
         do 20 ih = 1,ngh
            s = s + v(ih)*rnl(n1,l,ih)*rnl(n2,l,ih)
   20    continue
         tt(n1,n2) = s
   10 continue
c
      return
c-end-POT
      end
