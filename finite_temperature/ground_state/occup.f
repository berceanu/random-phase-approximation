c======================================================================c

      subroutine occup(is,lpr)

c======================================================================c
C
C     IS=1  occupation in fixed j-blocks
C        2  occupation from the bottom of the well
C        3  occupation by lambda-iteration
C        4  occupation by temperature     
C
c----------------------------------------------------------------------c
      include 'paramet'
      parameter (ndwork = nwork-2*ntx)
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
      common /fermi / ala(2),tz(2)
      common /nucnuc/ amas,nama,npr(2),jmax
      common /fixocc/ ioc(nbx,2)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /quaqua/ nt,nr(ntx),nl(ntx),nj(ntx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /work  / ex(ntx),mx(ntx),mxdum(ntx),dwork(ndwork)
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN OCCUP ********************************'
c
c
c     loop over neutron-proton
c-----------------------------
      do 10 it = it1,it2
c
c
c     fixed occupation within the differten j-blocks
c---------------------------------------------------
      if (is.eq.1) then
         do 20 ib = 1,nb
            im  = ia(ib)
            nd  = id(ib)
            ifx = ioc(ib,it)
            do i = 1,ifx
               vv(im+i,it) = 2*ijb(ib)      
            enddo
            do i = ifx+1,nd
               vv(im+i,it) = zero
            enddo
   20    continue
      endif
C
C
C     occupation from the bottom of the well
C-------------------------------------------
      if (is.eq.2) then
         do i = 1,nt
            mx(i) = mu(i)
            ex(i) = ee(i,it)
         enddo
         call ordi(nt,ex,mx)
         ntz = 0
         do i = 1,nt
            ntz = ntz + mx(i)
            if (ntz.ge.npr(it)) goto 32
         enddo             
   32    al  = ex(i)
         vtz = npr(i) - (ntz-mx(i))
         do i = 1,nt
            if (ee(i,it).lt.al) vv(i,it) = mu(i)
            if (ee(i,it).gt.al) vv(i,it) = 0.0
            if (ee(i,it).eq.al) vv(i,it) = vtz 
         enddo
         ala(it) = al
      endif
c
c
c     lambda-iteration
c----------------------
       if(is.eq.3) then
         tzz = npr(it)
         al  = ala(it)
         de  = del(it)
         call lambcs(nt,tzz,al,de,sp,pwi,ee(1,it),mu,
     &               vv(1,it),vv1(1,it),ex,mx,lpr)
         ala(it) = al
         spk(it) = sp
         tz(it)  = tzz
       endif
c
c
c     temperature   
c----------------
      if (is.eq.4) then
        tzz = npr(it)
        al  = ala(it)
c        stop ' in OCCUP: lamtem not initialized '
        call lamtem(nt,tzz,al,ee(1,it),mu,vv(1,it),ex,mx,lpr)
        ala(it) = al
        tz(it)  = tzz
      endif
   10 continue
c
      if (lpr)
     &write(l6,*) ' ****** END OCCUP **********************************'
      return
c-end-OCCUP
      end
c======================================================================c

      subroutine lambcs(n,tz,alam,delta,spk,pwind,ee,mu,vv,
     &                 vv1,ex,mx,lpr)

c======================================================================c
c
c    solves the BCS-equations for fixed Gap delta
c    n     dimension of fields ee, vv
c    tz    wanted particle number
c    alam  chemical potential
c    delta gap parameter 
c    spk   trace of kappa
c    pwind pairing-window
c    ee    single particle energies
c    vv    BCS occupation numbers
c    mu    multiplicities of each shell
c    ex    auxiliary field
c    mx    auxiliary field
C
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      dimension ee(n),vv(n),vv1(n),ex(n),mu(n),mx(n)
c
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo
c
      data maxl/50/,epsl/1.d-9/
c
      spk = 0.0
c
c     numerical determination of lambda for delta > 0
c----------------------------------------------------
      if (lpr) write(l6,*) 'Delta = ',delta,'  Window =',pwind
      if (abs(delta).gt.0.0001) then
c
         del2 = delta**2
         alama = alam + 50.d0
         alami = alam - 50.d0
c
         do 10 lit = 1,maxl
c
c           calculation of particle number
            sn = 0.0
            do 20 i = 1,n 
               el = ee(i) - alam
               if (abs(el).le.pwind) then
                  ek = sqrt(el**2+del2)
                  sn = sn + mu(i)*(1-el/ek)
               else
                  if (el.lt.zero) sn = sn + 2*mu(i)
               endif
   20       continue
            sn = sn/2
            al = alam
            dn  = tz - sn
            if (abs(dn).lt.epsl) goto 30
c
            if (dn.gt.0.0) then
               alami = alam
            else
               alama = alam
            endif
c
c           determination of a new lambda-value
            if (lit.eq.1) then
               if (dn.gt.0) then
                  alax = alam + 0.01
               else
                  alax = alam - 0.01
               endif
            else
               ds = sn - sn0
               if (abs(ds).gt.1.d-8) then
                  alax = alam + dn*(al-al0)/ds
               else
                  if (dn.gt.0) then
                     alax = half*(alam+alama)
                  else
                     alax = half*(alam+alami)
                  endif
               endif
            endif
            if (alax.gt.alama) alax = half*(alam+alama)
            if (alax.lt.alami) alax = half*(alam+alami)
            if (lpr) write(l6,'(i4,a,3f15.8)') 
     &                     lit,'. Lambda-Iteration:',al,sn,alax    
            al0  = al
            sn0  = sn
            alam = alax
c
c        end of the lambda-loop
   10    continue
         write(l6,'(a,i4,a)') 
     &        ' Lambda-Iteration interupted after',lit,' steps'
         goto 40
   30    if (lpr) write(l6,'(i4,a,2f15.8)')
     &        lit,'. Lambda-Iteration successful:    ',alam,sn
c
c        calculation of occupation factors for fixed lambda             
   40    do 50 i = 1,n
            el    = ee(i) - alam
            if (abs(el).le.pwind) then
               eki   = 1/sqrt(el**2+del2)
               vv(i) = mu(i)*half*(1-el*eki)
               vv1(i) = half*(1-el*eki)
               spk   = spk + mu(i)*eki
            else
               if (el.gt.zero) then
                  vv(i) = zero
                  vv1(i) = zero
               else
                  vv(i) = mu(i)
                  vv1(i) = 1.0
               endif
            endif
   50    continue
         spk = 0.25d0*delta*spk
c
c
c        for delta = 0: filling from the bottom of the well
c----------------------------------------------------------
      else
         do 60 i = 1,n
            mx(i) = mu(i)
   60       ex(i) = ee(i)
         call ordi(n,ex,mx)
         ntz  = tz + 0.001
         ns   = 0
         do 61 i = 1,n
            ns = ns + mx(i)
            if (ns.ge.ntz) goto 62
   61    continue
         stop ' in LAMBCS: particle number too large'             
   62    alam  = ex(i)
         vtz = ntz - (ns-mx(i))
         do 63 i = 1,n
            if (ee(i).lt.alam) vv(i) = mu(i)
            if (ee(i).lt.alam) vv1(i) = 1.0
            if (ee(i).gt.alam) vv(i) = 0.0
            if (ee(i).gt.alam) vv1(i) = 0.0
            if (ee(i).eq.alam) vv(i) = vtz 
            if (ee(i).eq.alam) vv1(i) = vtz/mu(i) 
   63    continue
      endif
c
c
c     printout
c-------------
      if (lpr) then
         write(l6,'(/,a)') '   k         e(k)         vv(k)'
         sn = 0.0
         do 80 i = 1,n
            sn = sn + vv(i)
            write(l6,'(i4,i5,2f15.8)') i,mu(i),ee(i),vv(i)
   80    continue
         write(l6,'(/,a,f15.8)') '   trace of kappa    =',spk 
         write(l6,'(/,a,f15.8)') '   chemical potenial =',alam
         write(l6,'(  a,f15.8,//)') '   particle number   =',sn
      endif
c
      if (lpr)
     &write(l6,*) ' ****** END LAMBCS *********************************'
      return
c-end-LAMBCS
      end
c======================================================================c

      subroutine lamtem(n,tz,alam,ee,mu,vv,ex,mx,lpr)

c======================================================================c
c
c    calculates occupation numbers for fixed temperature temp
c    n     dimension of fields ee, vv
c    tz    wanted particle number
c    alam  chemical potential
c    temp  temperature
c    ee    single particle energies
c    vv    BCS occupation numbers
c    mu    multiplicities of each shell
c    ex    auxiliary field
c    mx    auxiliary field
C
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      dimension ee(n),vv(n),ex(n),mu(n),mx(n)
c
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /temper/ temp
c
      data maxl/50/,epsl/1.d-9/
c
c
c     numerical determination of lambda 
c--------------------------------------
      if (lpr) write(l6,*) 'Temp   =',temp
c
      if (temp.ne.0.0) then
c
         alama = alam + 50.d0
         alami = alam - 50.d0
c
         do 10 lit = 1,maxl
c
c           calculation of particle number
            sn = 0.0
            do 20 i = 1,n 
               ek = (ee(i) - alam)/temp
	       if (ek.lt.-15.0) sx = mu(i)
	       if (ek.gt.+15.0) sx = 0.0
	       if (ek.gt.-15.0.and.ek.lt.+15.0) sx = mu(i)/(exp(ek)+1)
               sn = sn + sx
   20       continue
            al = alam
            dn  = tz - sn
            if (abs(dn).lt.epsl) goto 30
c
            if (dn.gt.0.0) then
               alami = alam
            else
               alama = alam
            endif
c
c           determination of a new lambda-value
            if (lit.eq.1) then
               if (dn.gt.0) then
                  alax = alam + 0.01
               else
                  alax = alam - 0.01
               endif
            else
               ds = sn - sn0
               if (abs(ds).gt.1.d-8) then
                  alax = alam + dn*(al-al0)/ds
               else
                  if (dn.gt.0) then
                     alax = half*(alam+alama)
                  else
                     alax = half*(alam+alami)
                  endif
               endif
            endif
            if (alax.gt.alama) alax = half*(alam+alama)
            if (alax.lt.alami) alax = half*(alam+alami)
            if (lpr) write(l6,'(i4,a,3f15.8)') 
     &                     lit,'. Lambda-Iteration:',al,sn,alax    
            al0  = al
            sn0  = sn
            alam = alax
c
c        end of the lambda-loop
   10    continue
         write(l6,'(a,i4,a)') 
     &        ' Lambda-Iteration interupted after',lit,' steps'
         goto 40
   30    if (lpr) write(l6,'(i4,a,2f15.8)')
     &        lit,'. Lambda-Iteration successful:    ',alam,sn
c
c        calculation of occupation factors for fixed lambda             
   40    do 50 i = 1,n
            ek = (ee(i) - alam)/temp
	    if (ek.lt.-15.0) sx = mu(i)
	    if (ek.gt.+15.0) sx = 0.0
	    if (ek.gt.-15.0.and.ek.lt.+15.0) sx = mu(i)/(exp(ek)+1)
	    vv(i) = sx
   50    continue
c
c
c        for temperature = 0: filling from the bottom of the well
c----------------------------------------------------------------
      else
         do 60 i = 1,n
            mx(i) = mu(i)
   60       ex(i) = ee(i)
         call ordi(n,ex,mx)
         ntz  = tz + 0.001
         ns   = 0
         do 61 i = 1,n
            ns = ns + mx(i)
            if (ns.ge.ntz) goto 62
   61    continue
         stop ' in LAMTEM: particle number too large'             
   62    alam  = ex(i)
         vtz = ntz - (ns-mx(i))
         do 63 i = 1,n
            if (ee(i).lt.alam) vv(i) = mu(i)
            if (ee(i).gt.alam) vv(i) = zero
            if (ee(i).eq.alam) vv(i) = vtz 
   63    continue
      endif
c
c
c     printout
c-------------
      if (lpr) then
         write(l6,'(/,a)') '   k         e(k)         vv(k)'
         sn = 0.0
         do 80 i = 1,n
            sn = sn + vv(i)
            write(l6,'(i4,i5,2f15.8)') i,mu(i),ee(i),vv(i)
   80    continue
         write(l6,'(/,a,f15.8)') '   chemical potenial =',alam
         write(l6,'(  a,f15.8,//)') '   particle number   =',sn
      endif
c
      if (lpr)
     &write(l6,*) ' ****** END LAMTEM *********************************'
      return
c-end-LAMTEM
      end
