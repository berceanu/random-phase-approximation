c======================================================================c

      subroutine resu(lpr)

c======================================================================c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      logical lpr
      character*1 tp,tl,tis,tt
      character*2 nucnam
      character*8 tit
      character*10 txtfor

      dimension eeord(ntx,2), vvord(ntx,2), vvnor(ntx,2)
      dimension nrord(ntx,2), nlord(ntx,2), jord(ntx,2)
c
c
      common /oscqua/ nr(ntx),nl(ntx),nj(ntx)
      common /fermi / ala(2),tz(2)   
      common /wqrpa/   vvqrpa(nhx,nb2x),eeqrpa(nhx,nb2x),iqpa(2),iqap(2)     
     
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no      
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /texblo/ tb(ntx),txb(nbx)
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx) 
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /wavefg/ fg(2*nhq2x,nb2x)
c
      write(l6,*) ' ****** BEGIN RESU *********************************'
c
      if (.not.lpr) goto 102
c
c---- printing of densities
      call prigh(0,rs,b0,'x(fm) ')
      do it = 1,2
         call prigh(1,rs(1,it),one,'ROS '//tis(it))
         call prigh(1,rv(1,it),one,'ROV '//tis(it))
      enddo
      call prigh(1,dro,one,'DRO  ')
c
c---- printing of fields
      call prigh(0,sig,b0,'x(fm) ')
      call prigh(1,sig,one,'Sigma ')
      call prigh(1,ome,one,'Omega ')
      call prigh(1,rho,one,'Rho   ')
      call prigh(1,cou,one,'Coulom')
c
      call expect(.true.)
c---- Quasi-particle energies
      do it = it1,it2  !loop over neutrons and protons
         ibl = nbl(it)
         kbl = nrbl(it)      
         write(l6,100) tit(it)
         do ib = 1,nb   ! loop over blocks
            ip  = ipb(ib)	
	    nf  = id(ib,1)
	    ng  = id(ib,2)
	    nh = nf+ng
	    imf = ia(ib,1) 
	    mf  = ib + (it-1)*nbx
	    nhfb = nh + nh
	    
	    do k = 1,nf  !loop over states in block
	       eq = eqp(imf+k,it) 
	       k0 = imf+k 
c---------- search for main oscillator component
               sx = zero
	       su = zero
	       sv = zero
	       do n = 1,nh
	          u = fg(n+(k-1)*nhfb,mf)**2
		  v = fg(nh+n+(k-1)*nhfb,mf)**2
		  su = su + u
		  sv = sv + v
		  s  = u + v
		  if (s .gt. sx) then
		     sx = s
		     ix = n
	          endif
	       enddo
	       if ((eq.gt.20.0) .and. (su.gt.sv)) goto 10	       
	       if (su.gt.sv) then
	          tt = 'p'
	       else
	          tt = 'h'
	       endif
	       if((ibl.eq.ib). and. (kbl.eq.k)) tt = 'blocked'
	       write(l6,101) k0,2*ijb(ib)-1,tp(ip),
     &                    tb(imf+ix),sx,eq,su,sv,tt
10             continue
            enddo
	 enddo
      enddo	

c---- add for printing out ei and vi
c----print out occupation ni versus ei
c
      open(17,file='dish_' //'occup_n.txt',status='unknown')
      open(18,file='dish_' //'occup_p.txt',status='unknown')

      do it=1,2
       do i=1,nt
        vvnor(i,it)=v2(i,it)
        eeord(i,it)=eqp(i,it)
        vvord(i,it)=vvnor(i,it)

        nrord(i,it) = nr(i)
        nlord(i,it) = nl(i)
        jord(i,it) = nj(i)
       enddo

       call ordi2(nt, eeord(1,it), vvord(1,it),
     $ nrord(1,it),nlord(1,it),jord(1,it))
      enddo

      do 30 i=1,nt
        if (eeord(i,1).gt.20.0.and.eeord(i,2).gt.20.0) goto 30
        write(17,*)eeord(i,1), vvord(i,1),
     $   nrord(i,1), nlord(i,1),jord(i,1)
        write(18,*)eeord(i,2),vvord(i,2),
     $   nrord(i,2), nlord(i,2),jord(i,2)
  30  continue
       write(17,*)ala(1)
       write(18,*)ala(2)
      close(17)
      close(18)
c---add end

c
c
c---- BCS structure in the canonical basis:
c      do it = it1,it2
c         call canon(it,1)
c         write(l6,*) 'delta=',delta
c      enddo
c      call cmcd(.false.)
c      call cmcn(.false.)
      call expect(.true.)
c
c
c
  100    format(' Quasi-particle energies  ',a,/,1x,66(1h-))
  101    format (i3,' j =',i2,'/2',a1,'  (',a8,')',f6.2,3f10.3,' ',a8)
  102 write(l6,*) ' ****** END RESU ***********************************'

      return
c-end-RESU
      end


c=======================================================================

      subroutine ordi2(n,e,emu,nr,nl,nj)

c=======================================================================
c
C     orders a set of numbers according to their size
c

c
c-----------------------------------------------------------------------
      implicit double precision (a-h,o-z)
C     
      dimension e(n),emu(n)
      dimension nr(n), nl(n), nj(n)
c
      do 10 i = 1,n 
         k  = i
         p  = e(i)
         if (i.lt.n) then
            do 20 j = i+1,n
               if (e(j).lt.p) then
                  k = j 
                  p = e(j)
               endif
   20       continue
            if (k.ne.i) then
               e(k)  = e(i)
               e(i)  = p
               emk    = emu(k)
               emu(k) = emu(i)
               emu(i) = emk
               nrk = nr(k)
               nr(k) = nr(i)
               nr(i) = nrk
               nlk = nl(k)
               nl(k) = nl(i)
               nl(i) = nlk
               njk = nj(k)
               nj(k) = nj(i)
               nj(i) = njk
            endif
         endif
   10 continue
c
      return
c-end-ORDI
      end

 
