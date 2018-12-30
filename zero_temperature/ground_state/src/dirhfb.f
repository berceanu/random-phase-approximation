c======================================================================c

      subroutine dirhfb(it,lprh,lprl)

c======================================================================c
c
c     solves the Dirac-HFB-Equation in spherical oscillator basis
c     IT  = 1 neutrons
c           2 protons
c 
c     units:    fields and Hamiltonian in MeV
c               eigenvalues in MeV
c 
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical  lprh,lprl
      character*8 tb,tbb(nhfbx)
      character*25 txb
      character*1 bbb
c
      dimension e(nhfbx),ez(nhfbx)
      dimension hfb(nhfbqx)
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /fermi / ala(2),tz(2)
      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /wavefg/ fg(2*nhq2x,nb2x)
c
      data maxl/150/,epsl/1.d-8/,bbb/1h /
c
      if (lprh.or.lprl)
     &write(l6,*) ' ****** BEGIN DIRHFB *******************************'
c
      ibl = nbl(it)
      kbl = nrbl(it)
c
c---- loop over lambda-iteration
      sn    = zero
      dl    = 100.d0
      xh    = ala(it) + dl
      xl    = ala(it) - dl
      al    = ala(it)
      do lit = 1,maxl
c
c------- loop over the different j-blocks
         snold = sn
         sn = zero
         sp = zero
         do ib = 1,nb
            mul = ijb(ib)
            lf  = ilb(ib,1)
            if (lf.gt.n0f) then
               eqp(ia(ib,1)+1,it) = 1.d+8
               goto 10
            endif
            nf  = id(ib,1)
            ng  = id(ib,2)
            nh  = nf + ng
            nhfb= nh + nh
            imf = ia(ib,1)
            img = ia(ib,2)
            m   = ib + (it-1)*nbx
c
c---------- calculation of the Dirac-HFB-Matrix:
            do i2 = 1,nh
               do i1 = i2,nh
                  hla = hh(i1+(i2-1)*nh,m) 
                  dla = de(i1+(i2-1)*nh,m)
                  hfb(i1+(i2-1)*nhfb)       =  hla 
                  hfb(nh+i1+(nh+i2-1)*nhfb) = -hla
                  hfb(nh+i1+(i2-1)*nhfb)    =  dla
                  hfb(nh+i2+(i1-1)*nhfb)    =  dla
               enddo
               hfb(i2+(i2-1)*nhfb)       = hfb(i2+(i2-1)*nhfb) - al
               hfb(nh+i2+(nh+i2-1)*nhfb) = hfb(nh+i2+(nh+i2-1)*nhfb)+al
            enddo
c
c---------- Diagonalization:
            if (lprh.and.lit.eq.1) then
               do i = 1,nf
                  tbb(i)    = tb(imf+i)
               enddo
               do i = 1,ng
                  tbb(nf+i) = tb(img+i)
               enddo
               do i = 1,nh
                  tbb(nh+i) = tbb(i)
               enddo
               write(l6,'(/,a)') txb(ib)
               call aprint(2,2,6,nhfb,nhfb,nhfb,hfb,tbb,' ','HFB')
            endif
            call sdiag(nhfb,nhfb,hfb,e,hfb,ez,+1)
            if (lprh.and.lit.eq.1) then
               call aprint(1,1,6,1,1,nhfb,e,' ',' ','E')
               call aprint(1,2,6,nhfb,nhfb,nhfb,hfb,tbb,' ','XX')
            endif
c
c---------- particles
             do k = 1,nf
                eqp(imf+k,it) = e(nh+k)
                do i = 1,nhfb
                   fg(i+(k-1)*nhfb,m) = hfb(i+(nh+k-1)*nhfb)
                enddo
             enddo
c
c---------- antiparticles
            do k = 1,ng
               do i = 1,nhfb
                  fg(i+(nf+k-1)*nhfb,m) = hfb(i+(nh+nf+k-1)*nhfb)
               enddo
            enddo
c
c---------- particle number and trace of kappa
            sn1 = zero
            sp1 = zero
            do k = 1,nf
               do i = 1,nh
                  sn1 = sn1 + fg(nh+i+(k-1)*nhfb,m)**2
               enddo
	       do i=1,nf
	          sp1 = sp1 + fg(i+(k-1)*nhfb,m)*fg(nh+i+(k-1)*nhfb,m)
	       enddo
            enddo
            sn = sn + 2*mul*sn1
            sp = sp +   mul*sp1
c
c---------- blocking
	    if (ib.eq.ibl) then
	       sn1 = zero
	       sp1 = zero
               do i = 1,nh
                  sn1 = sn1 + fg(nh+i+(kbl-1)*nhfb,m)**2
                  sp1 = sp1 + fg(i+(k-1)*nhfb,m)*fg(nh+i+(k-1)*nhfb,m)
               enddo
	       sn = sn - 2*sn1 + one
	       sp = sp - sp1
	    endif
c
c---------- Printout
            if (lprh.and.lit.eq.1) then
               call aprint(1,1,1,1,1,nf,eqp(imf+1,it),' ',' ','EQP')
               call aprint(1,2,1,nhfb,nhfb,nf,fg(1,m),tbb,' ','FG')
               call aprint(1,2,1,nhfb,nhfb,ng,fg(nhfb*nf+1,m),tbb,' ',
     &                     'FG-a')
            endif
   10    enddo
         if (lit.gt.1) dd = (sn - snold)/(al - alold)
c
c------- calculation of a new lambda-value
         alold = al
         dn    = sn - tz(it)
         if (dn.lt.zero) then
            xl = al
         else
            xh = al
         endif
         if (lit.eq.1) then
            if(dabs(dn).le.0.1d0) then
               al = al - dn
            else
               al = al - 0.1d0*sign(one,dn)
            endif
         else
c
c           secant method
            if (dd.eq.zero) dd = 1.d-20
            al    = al - dn/dd
            if (al.lt.xl.or.al.gt.xh) then
c
c              bisection
               al = half*(xl+xh)
               bbb = 'B'
            endif
         endif
         if (abs(al-alold).lt.epsl) goto 30
c
         if (lprl.or.lit.gt.10) then
            write(l6,100) lit,'. L-Iteration: ',bbb,alold,dn,al    
c            write(6,100)  lit,'. L-Iteration: ',bbb,alold,dn,al    
  100       format(i4,a,a1,3f13.8)
            bbb = ' ' 
         endif
c
c---- end of lambda-loop
      enddo
      write(l6,'(a,i4,a)') 
     &     ' Lambda-Iteration interupted after',lit-1,' steps'
      stop 
   30 if (lprl) then
         write(l6,101) lit,'. Lambda-Iteration successful:',it,al,dn,sn
c        write(6,101) lit,'. Lambda-Iteration successful:',it,al,dn,sn
  101    format(i4,a,i4,3f13.8)
      endif
      ala(it) = al
      spk(it) = sp
c
c
      if (lprh.or.lprl)
     &write(l6,*) ' ****** END DIRHFB *********************************'
      return
C-end-DIRHFB
      end
