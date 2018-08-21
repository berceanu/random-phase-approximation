c======================================================================c
  
      subroutine canon(it,npr)

c======================================================================c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      parameter (ndwork = nwork - 5*nhx-3*nhqx)
c
      character tp*1,tl*1,tis*1,nucnam*2,tb*8,tit*8,txtfor*10,txb*25
      character*8 tbb(nhfbx)
c
      dimension eb(nhx)
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /canonw/ dd(nhqx,nb2x)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /fermi / ala(2),tz(2)      
      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
      common /kappa / aka(nqx,nb2x) 
      common /mathco/ zero,one,two,half,third,pi
      common /rhoshe/ rrf(nqx,nb2x),rrg(nqx,nb2x)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp
      common /texblo/ tb(ntx),txb(nbx)
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /wavefg/ fg(2*nhq2x,nb2x)
      common /work  / vv(nhx),uv(nhx),h(nhx),d(nhx),z(nhx),zz(nhqx),
     &                aa(nhqx),bb(nhqx),cc(nhqx),dwork(ndwork)
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /baspar/ hom,hb0,b0
      common /wcan2/  h11(nhqx,nb2x),hcan(nhqx,nb2x),dcan(nhqx,nb2x),
     &                v11(nhx),u11(nhx) 
      common /wqrpa/   vvqrpa(nhx,nb2x),eeqrpa(nhx,nb2x),iqpa(2),iqap(2)
      common /wqrpa2/ deqrpa(nhx,nb2x)      
c
      data ash/4.d0/
      
      elower = -two*amu

c
c     write(6,*) ' Shift in CANON',ash
c
      if(npr.gt.0)
     &write(l6,*) ' ****** BEGIN CANON ********************************'
c
c
c---- BCS structure in the canonical basis:
c
      open(19,file='spenergyN.txt',status='unknown')
      open(20,file='spenergyP.txt',status='unknown')
      if (npr.ge.2) write(l6,'(//,a)') tit(it)
      if (npr.eq.1) write(l6,100) tit(it)
  100    format(' single-particle energies and gaps ',
     &          'in the canonical basis: ',a,/,1x,66(1h-))
c
c---- loop of the j-blocks
      ibl = nbl(it)
      kbl = nrbl(it)
      iqpa(it) = 0
      iqap(it) = 0
      do ib = 1,nb
         lf = ilb(ib,1)
         if (lf.gt.n0f) goto 10
         if (npr.ge.2) write(l6,'(/,a)') txb(ib)
         nf  = id(ib,1)
         ng  = id(ib,2)
         lg  = ilb(ib,2)
         nh  = nf + ng
         nhfb= nh + nh
         imf = ia(ib,1)
         img = ia(ib,2)
	 mul = 2*ijb(ib)
         ip  = ipb(ib)
         mf  = ib + (it-1)*nbx

	 write(l6,1111) ib,lf,nf,ng,nh,imf,img,n0f,ibg
 1111 format("  ib=",i5,"  lf=",i5,"  nf=",i5, "  ng=",i5,"  nh=",i5," 
     & imf=",i5,"  img=",i5,"  n0f=",i5,"  ibg=",i5)
c
c------- printout of wavefunctions and densities in oscillator basis 
         if (npr.eq.3) then
            do i = 1,nf
               tbb(i)    = tb(imf+i)
            enddo
            do i = 1,ng
               tbb(nf+i) = tb(img+i)
            enddo
            do i = 1,nh
               tbb(nh+i) = tbb(i)
            enddo 
            nfu = 1 
            ngu = nf+1 
            nfv = nh+1 
            ngv = nh+nf+1 
            call aprint(1,2,5,nhfb,nf,nf,fg(nfu,mf),tbb,' ','FUU')
            call aprint(1,2,5,nhfb,ng,nf,fg(ngu,mf),tb(img+1),' ','GUU')
            call aprint(1,2,5,nhfb,nf,nf,fg(nfv,mf),tbb,' ','FVV')
            call aprint(1,2,5,nhfb,ng,nf,fg(ngv,mf),tb(img+1),' ','GVV')
         endif
c------- end printout of wafefunctions
c
c
c------- transformation to the canonical basis
c
c------- calculation of the generalized density V*VT          
         do n2 = 1,nh
            do n1 = 1,nh
               s = zero
               do k = 1,nf
                  s = s+fg(nh+n1+(k-1)*nhfb,mf)*fg(nh+n2+(k-1)*nhfb,mf)
               enddo
c
c              blocking
              if (ib.eq.ibl) then
                 s1 = - fg(nh+n1+(kbl-1)*nhfb,mf)*
     &                   fg(nh+n2+(kbl-1)*nhfb,mf)
     &                 + fg(   n1+(kbl-1)*nhfb,mf)*
     &                   fg(   n2+(kbl-1)*nhfb,mf)
                 s = s + s1/mul
              endif
c
c              the anti-particle contributions are shifted by ash
c              ash = 1:    full antiparticle contributions
c              ash = >> 1: no antiparticle contributions
c              ash = 0:    is numercally unstable
               s1 = zero
               do k = 1,ng
                  s1 = s1 + fg(nh+n1+(nf+k-1)*nhfb,mf)*
     &                      fg(nh+n2+(nf+k-1)*nhfb,mf)
               enddo
               aa(n1+(n2-1)*nh) = s + ash*s1
            enddo
         enddo
c
         if (npr.eq.3) call aprint(1,3,1,nh,nh,nh,aa,tbb,tbb,'RRR')
         call sdiag(nh,nh,aa,vv,cc,z,1)
         eps=1.0e-6 
         call degen(nh,nh,vv,cc,hh(1,mf),eb,eps,zz,z)

         if (npr.ge.2) call aprint(1,1,1,1,1,nh,vv,' ',' ','vv')
         do i = 1,nh
            v = vv(i)
            if (v.lt.-0.00001) stop ' in CANON: vv negativ'
            if (v.lt.zero) vv(i) = zero
         enddo 
         if (npr.eq.3) call aprint(1,2,1,nh,nh,nf,cc,tbb,' ',
     &                'Transformation to the canonical basis: DD')
c 
c------- transformation of HH and DE to the canonical basis
         if (npr.eq.1) then
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + hh(i+(l-1)*nh,mf)*cc(l+(k-1)*nh)
               enddo
               aa(i+(k-1)*nh) = s
            enddo 
            enddo
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + cc(l+(i-1)*nh)*aa(l+(k-1)*nh)
               enddo
               bb(i+(k-1)*nh) = s
	       hcan(i+(k-1)*nh,mf) = s
            enddo
            enddo 
c            call aprint(1,1,6,nh,nh,nf,bb,' ',' ','HH-can')
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + de(i+(l-1)*nh,mf)*cc(l+(k-1)*nh)
               enddo
               aa(i+(k-1)*nh) = s
            enddo 
            enddo
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + cc(l+(i-1)*nh)*aa(l+(k-1)*nh)
               enddo
               bb(i+(k-1)*nh) = s
	       dcan(i+(k-1)*nh,mf) = s
            enddo
            enddo 
c            call aprint(1,1,5,nh,nh,nf,bb,' ',' ','DE-can')
         endif
	 do k = 1,nh
            hk = zero
            dk = zero
            do n2 = 1,nh
               h2 = zero
               d2 = zero
               do n1 = 1,nh
                  h2 = h2 + cc(n1+(k-1)*nh)*hh(n1+(n2-1)*nh,mf)
                  d2 = d2 + cc(n1+(k-1)*nh)*de(n1+(n2-1)*nh,mf)
               enddo
               hk = hk + h2*cc(n2+(k-1)*nh) 
               dk = dk + d2*cc(n2+(k-1)*nh) 
            enddo
            h(k) = hk
            d(k) = dk
         enddo
c-----     major component of dd is positive
         do k = 1,nh
            if (vv(k).le.1.005) then
               iqpa(it) = iqpa(it) + 1
            else
               iqap(it) = iqap(it) + 1
            endif
            ddmaj = cc(1+(k-1)*nh)
            do i = 1,nh
              dd(i+(k-1)*nh,mf) = cc(i+(k-1)*nh)
	      if(abs(dd(i+(k-1)*nh,mf)).gt.abs(ddmaj)) then
                   ddmaj = dd(i+(k-1)*nh,mf)
	      endif
            enddo
	    if (ddmaj.lt.0.0) then
 	       do i = 1,nh
		  dd(i+(k-1)*nh,mf) = -dd(i+(k-1)*nh,mf)
	       enddo
	    endif
         enddo	 
	 
c ------ diagonal elements of h,de and occupation probabilities for QRPA
         do k=1,nh
            vvqrpa(k,mf) = vv(k)
            eeqrpa(k,mf) = h(k)
	    deqrpa(k,mf) = d(k)
            if (vv(k).le.1.0005) then    !particles
	       if (vv(k) .gt. 1.0) vv(k) = 1.0
               v11(k) = sqrt(vv(k))
               u11(k) = sqrt(abs(1.0-vv(k)))
            else         !antiparticles
               v11(k) = 0.0
               u11(k) = 1.0
            endif
         enddo	 

c------ add for print out single particle energy
       if(it .eq. 1) then
         write(19,*)mf
         do k=1,nh
         write(19,*)eeqrpa(k,mf)
         enddo
       else 
        write(20,*)mf
        do k=1,nh
           write(20,*) eeqrpa(k,mf)
        enddo
      endif
	
c------- calculation of the generalized kappa U*VT
         do n2 = 1,nh
            do n1 = 1,nh
               s = zero
               do k = 1,nh
                  s = s+fg(n1+(k-1)*nhfb,mf)*fg(nh+n2+(k-1)*nhfb,mf)
     &                 +fg(n2+(k-1)*nhfb,mf)*fg(nh+n1+(k-1)*nhfb,mf)
               enddo
               aa(n1+(n2-1)*nh) = s
            enddo
         enddo
         if (npr.eq.3) then
c           call aprint(1,3,5,nh,nh,nh,aa,tbb,tbb,'AKK')
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + aa(i+(l-1)*nh)*dd(l+(k-1)*nh,mf)
               enddo
               bb(i+(k-1)*nh) = s
            enddo 
            enddo
            do k = 1,nh
            do i = 1,nh
               s = zero
               do l = 1,nh
                  s = s + dd(l+(i-1)*nh,mf)*bb(l+(k-1)*nh)
               enddo
               cc(i+(k-1)*nh) = s
            enddo
            enddo 
            call aprint(1,1,5,nh,nh,nf,cc,' ',' ','AK-can')
         endif
c
c------- transformation of the wavefunctions to the canonical basis
         do k = 1,nf
            ak = zero
            do n2 = 1,nh
               s2 = zero
               do n1 = 1,nh
                  s2 = s2 + dd(n1+(k-1)*nh,mf)*aa(n1+(n2-1)*nh)
               enddo
               ak = ak + s2*dd(n2+(k-1)*nh,mf) 
            enddo
            v = sqrt(vv(k))
            u = sqrt(one-vv(k))
            if (ak.gt.zero) v = -v
            uv(k) = u*v
	    v11(k) = v
	    u11(k) = u
	    vvqrpa(k,mf) = v ! particles only, not antiparticles
            do i = 1,nh
               fg(   i+(k-1)*nhfb,mf) = dd(i+(k-1)*nh,mf)*u
               fg(nh+i+(k-1)*nhfb,mf) = dd(i+(k-1)*nh,mf)*v
            enddo 
         enddo
         if (npr.ge.3) then
            call aprint(1,1,6,1,1,nh,uv,' ',' ','uv')
            call aprint(1,1,6,1,1,nh,vv,' ',' ','vv')
         endif
         if (npr.eq.3) then   
            nfu = 1 
            ngu = nf+1 
            nfv = nh+1 
            ngv = nh+nf+1 
            call aprint(1,2,5,nhfb,nf,nf,fg(nfu,mf),tbb,' ','FUU')
            call aprint(1,2,5,nhfb,ng,nf,fg(ngu,mf),tb(img+1),' ','GUU')
            call aprint(1,2,5,nhfb,nf,nf,fg(nfv,mf),tbb,' ','FVV')
            call aprint(1,2,5,nhfb,ng,nf,fg(ngv,mf),tb(img+1),' ','GVV')
         endif
         do i = 1,nh
            do k = 1,nh
              if(i.eq.k) then   !diagonal elements
                 h11(i+(k-1)*nh,mf) = (hcan(i+(k-1)*nh,mf)-ala(it))*
     &                           (u11(i)*u11(k)-v11(i)*v11(k))
     &            -dcan(i+(k-1)*nh,mf)*(u11(i)*v11(k)+v11(i)*u11(k))
              else          !offdiagonal elements
                 h11(i+(k-1)*nh,mf) = (hcan(i+(k-1)*nh,mf))*
     &                           (u11(i)*u11(k)-v11(i)*v11(k))
     &            -dcan(i+(k-1)*nh,mf)*(u11(i)*v11(k)+v11(i)*u11(k))  
             endif
           enddo
         enddo	 
        
c 
c------- calculation of the generalized density V*VT for test   
         if (npr.eq.3) then      
            do n2 = 1,nh
            do n1 = 1,nh
               s = zero
               do k = 1,nf
                  s = s+fg(nh+n1+(k-1)*nhfb,mf)*fg(nh+n2+(k-1)*nhfb,mf)
               enddo
               s1 = zero
               do k = 1,ng
                  s1 = s1 + fg(nh+n1+(nf+k-1)*nhfb,mf)*
     &                      fg(nh+n2+(nf+k-1)*nhfb,mf)
               enddo
               aa(n1+(n2-1)*nh) = s + ash*s1
            enddo
            enddo
            call aprint(1,3,1,nh,nh,nh,aa,tbb,tbb,'RRR-neu')
            call sdiag(nh,nh,aa,vv,bb,z,1)
            call aprint(1,2,1,1,1,nf,vv,' ',' ','vv')
         endif
c
        call aprint(1,2,1,nh,nh,nf,dd(1,mf),' ',' ','FG_DD')

          
c---- end loop over j-blocks
   10 enddo
c
c
       close(19)
       close(20)
  102 if (npr.gt.0)
     &write(l6,*) ' ****** END CANON **********************************'
c
      return
c-end-CANON
      end
