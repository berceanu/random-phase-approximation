c======================================================================c
  
      subroutine canon(it,npr,delta)

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
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
      common /canonw/ dd(nhqx,nb2x)
      common /dimens/ n0f,n0b,nrm,nlm
      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
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
      common /wavec/  f(ndg,nb2x),df(ndg,nb2x)
      common /radosc/ rnl(1:nrx,0:nlx,ngh),rnl1(1:nrx,0:nlx,ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /baspar/ hom,hb0,b0
c
      data ash/0.d+2/
      xsum=0.0
      dsum=0.0
      nggh = 2*ngh
c
c     write(6,*) ' Shift in CANON',ash
c
      if(npr.gt.0)
     &write(l6,*) ' ****** BEGIN CANON ********************************'
c
c
c---- BCS structure in the canonical basis:
c
      if (npr.ge.2) write(l6,'(//,a)') tit(it)
      if (npr.eq.1) write(l6,100) tit(it)
  100    format(' single-particle energies and gaps '
     &          'in the canonical basis: ',a,/,1x,66(1h-))
c
c---- loop of the j-blocks
      ibl = nbl(it)
      kbl = nrbl(it)
      do ib = 1,nb
         lf = ilb(ib)
         if (lf.gt.n0f) goto 10
         if (npr.ge.2) write(l6,'(/,a)') txb(ib)
         ibg = ib - 1 +2*mod(ib,2)
         nf  = id(ib)
         ng  = id(ibg)
         lg  = ilb(ibg)
         nh  = nf + ng
         nhfb= nh + nh
         imf = ia(ib)
         img = ia(ibg)
	 mul = 2*ijb(ib)
         ip  = 1 + mod(ilb(ib),2)
         mf  = ib + (it-1)*nbx

c	 write(l6,1111) ib,lf,nf,ng,nh,imf,img,n0f,ibg
c 1111 format("  ib=",i5,"  lf=",i5,"  nf=",i5, "  ng=",i5,"  nh=",i5," 
c     & imf=",i5,"  img=",i5,"  n0f=",i5,"  ibg=",i5)
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
         eps=1.0e-8 
         call degen(nh,nh,vv,cc,hh(1,mf),eb,eps,zz,z)

         if (npr.ge.2) call aprint(1,1,1,1,1,nh,vv,' ',' ','vv')
         do i = 1,nh
            v = vv(i)
            if (v.lt.-0.00001) stop ' in CANON: vv negativ'
            if (v.lt.zero) vv(i) = zero
            if (v.gt.+1.00001) stop ' in CANON: vv larger 1'
            if (v.gt.one) vv(i) = one
         enddo 
         if (npr.eq.3) call aprint(1,2,1,nh,nh,nf,cc,tbb,' ',
     &                'Transformation to the canonical basis: DD')
c 
c------- transformation of HH and DE to the canonical basis
         if (npr.eq.3) then
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
            enddo
            enddo 
            call aprint(1,1,6,nh,nh,nf,bb,' ',' ','HH-can')
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
            enddo
            enddo 
            call aprint(1,1,5,nh,nh,nf,bb,' ',' ','DE-can')
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
         if (npr.ge.2) then
            call aprint(1,1,6,1,1,nf,h,' ',' ','Hkk')
            call aprint(1,1,5,1,1,nf,d,' ',' ','Dkk')
         endif
c
c------- reordering according to the energy h(k) 
         call ordx(nh,h,d,vv,cc)
c
c------- reordering such that particles come first
         do k = 1,nf
            ee(imf+k,it) = h(ng+k)
            v2(imf+k,it) = vv(ng+k)
            z(k)         = d(ng+k)
            do i = 1,nh
               dd(i+(k-1)*nh,mf) = cc(i+(ng+k-1)*nh)
            enddo
         enddo
         do k = 1,ng
            vv(nh-k+1) = vv(ng-k+1)
            h(nh-k+1)  = h(ng-k+1)
            d(nh-k+1)  = d(ng-k+1)
            do i = 1,nh
               dd(i+(nf+k-1)*nh,mf) = cc(i+(k-1)*nh)
            enddo
         enddo
         do k = 1,nf
            vv(k) = v2(imf+k,it)
            h(k)  = ee(imf+k,it)
            d(k)  = z(k)
         enddo
         if (npr.eq.3) call aprint(1,2,1,nh,nh,nf,dd(1,mf),tbb,' ',
     &                'reordered: DD')
         if (npr.ge.2) then
            call aprint(1,1,6,1,1,nh,h,' ',' ','reordered: Hkk')
            call aprint(1,1,5,1,1,nh,d,' ',' ','reordered: Dkk')
            call aprint(1,1,6,1,1,nh,vv,' ',' ','reordered: vv')
         endif
               
c
c------- printout
         if (ib.eq.1) e0 = ee(imf+1,it)
         if (npr.ge.2) write(l6,100) tit(it)
         do 20 k = 1,nf
            k0 = imf+k
            e1 = ee(k0,it)
            v1 = v2(k0,it)
            xsum=xsum+v1*(2.0*(2*ijb(ib)-1)*0.5+1.0)
            dsum = dsum + v1
     &                *abs(d(k))*(2.0*(2*ijb(ib)-1)*0.5+1.0)
            if (e1.gt.5000.d0) goto 20
c           if (v1.lt.0.0001) goto 20
c
c           search for the main oscillator component
            smax = zero
            do i = 1,nh
               s = abs(dd(i+(k-1)*nh,mf))
               if (s.gt.smax) then
                  smax = s
                  imax = i
               endif
            enddo
            dx = dd(imax+(k-1)*nh,mf)
            if (npr.ge.1) write(l6,101) k0,2*ijb(ib)-1,tp(ip),
     &                    tb(imf+imax),dx,e1,e1-e0,v1,d(k)!,xsum
  101       format(i3,' j =',i2,'/2',a1,'  (',a8,')',f6.2,4f10.3)!,f7.4)
   20    enddo 
         delta = dsum/xsum
         
c
c
c------- calculation of the generalized kappa U*VT
         do n2 = 1,nh
            do n1 = 1,nh
               s = zero
               do k = 1,nf
                  s = s+fg(n1+(k-1)*nhfb,mf)*fg(nh+n2+(k-1)*nhfb,mf)
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
            if (ak.lt.zero) v = -v
            uv(k) = u*v
c            do i = 1,nh
c               fg(   i+(k-1)*nhfb,mf) = dd(i+(k-1)*nh,mf)*u
c               fg(nh+i+(k-1)*nhfb,mf) = dd(i+(k-1)*nh,mf)*v
c            enddo 
c------- wave functions in coordinate space
            do ih = 1,ngh
               wx = xh(ih)*sqrt(wh(ih))*b0**(3./2.)*sqrt(4*pi)
               wxd= wx*b0
               s = 0.0
               sd = 0.0
               do j = 1, nf    !loop over oscilator states
                  s = s + dd(j+(k-1)*nh,mf)*rnl(j,lf,ih)
                  sd = sd + dd(j+(k-1)*nh,mf)*rnl1(j,lf,ih)
               enddo                                     
               f(ih+(k-1)*nggh,mf) = s/wx
               df(ih + (k-1)*nggh,mf) = sd/wxd
               s = 0.0
               sd = 0.0
               do j = 1, ng
                  s = s + dd(nf+j+(k-1)*nh,mf)*rnl(j,lg,ih)
                  sd = sd + dd(nf+j+(k-1)*nh,mf)*rnl1(j,lg,ih)
               enddo
               f(ngh+ih+(k-1)*nggh,mf) = s/wx
               df(ngh+ih + (k-1)*nggh,mf) = sd/wxd 
            enddo  
            suml=zero
            sums=zero
            do ih=1,ngh
               wx = wdcor(ih)
               suml=suml+f(ih+(k-1)*nggh,mf)**2*wx
               sums=sums+f(ngh+ih+(k-1)*nggh,mf)**2*wx 
            enddo
            snorm = one/(suml+sums)
            snorm = sqrt(snorm)
            do ih=1,ngh
               f(ih+(k-1)*nggh,mf)= f(ih+(k-1)*nggh,mf)*snorm
             f(ngh+ih+(k-1)*nggh,mf)= f(ngh+ih+(k-1)*nggh,mf)*snorm 
               df(ih+(k-1)*nggh,mf)= df(ih+(k-1)*nggh,mf)*snorm
             df(ngh+ih+(k-1)*nggh,mf)= df(ngh+ih+(k-1)*nggh,mf)*snorm 
            enddo         
         enddo
         if (npr.ge.2) then
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
c---- end loop over j-blocks
   10 enddo
c
c
  102 if (npr.gt.0)
     &write(l6,*) ' ****** END CANON **********************************'
c
      return
c-end-CANON
      end
