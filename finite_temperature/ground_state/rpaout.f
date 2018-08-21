c=====================================================================c
   
      subroutine rpaout(lpr)  

c=====================================================================c
c
c   Writes out the single-particle energies, occupation probabilities
c        and wave functions for RPA
c
c---------------------------------------------------------------------
      include 'paramet' 
c
      implicit real*8 (a-h,o-z)
c      parameter (ndwork = nwork - 5*nd2x-3*nd4x)
      parameter (nmesh = 400)
      parameter (nhfbx=2*nd2x)
c
      character tp*1,tl*1,tis*1,nucnam*2,tb*8,tit*8,txtfor*10,txb*25
      character*8 tbb(nhfbx)
      logical lpr 
      dimension rnlr(nd2x),sn(nox),pn(nox)
      dimension wave(0:nmesh)      
      dimension sigr(0:nmesh),ffr(0:nmesh),ggr(0:nmesh)
      dimension gs(0:nmesh),gv(0:nmesh),gtv(0:nmesh)
      dimension dgs(0:nmesh),dgv(0:nmesh),dgtv(0:nmesh)
      dimension ddgs(0:nmesh),ddgv(0:nmesh),ddgtv(0:nmesh) 
      dimension dens0(0:nmesh)
c
      common /baspar/ hom,hb0,b0
c      common /bloosc/ ia(nbx,2),id(nbx,2)
c      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)

      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)

c      common /canonw/ dd(nhqx,nb2x)
c      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /dimens/ n0f,n0b,nrm,nlm
c      common /eeeeee/ eqp(ntx,2),ee(ntx,2),v2(ntx,2),mu(ntx)
      common /erwar / ea,rms,qp
      common /fermi / ala(2),tz(2)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
c      common /gogny / gw(2),gb(2),gh(2),gm(2),gr(2),gt3,gwls,txpair
c      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
c      common /kappa / aka(nqx,nb2x) 
      common /mathco/ zero,one,two,half,third,pi
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat      
      common /nucnuc/ amas,nmas,nneu,npro,jmax
      common /physco/ amu,hqc,alphi,r0
      common /radbos/ rnb(1:nox,ngh)
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh) 
c      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /texblo/ tb(ntx),txb(nbx)
c      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
c      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
c      common /wcan2/  h11(nhqx,nb2x),hcan(nhqx,nb2x),dcan(nhqx,nb2x),
c     &                v11(nhx),u11(nhx) 

      common /eerpa/ erpa(nd2x,nb2x),vvrpa(nd2x,nb2x),hhrpa(nq4x,nb2x)
     &,nrpa(2) 
      common /eeeeee/ ee(ntx,2),vv(ntx,2),vv1(ntx,2),mu(ntx)
c      common /wqrpa/   vvqrpa(nhx,nb2x),eeqrpa(nhx,nb2x),nqpa(2),nqap(2)
c      common /wqrpa2/ deqrpa(nhx,nb2x)
c      common /parfac/ vfac                
      common /para/ ipara
 
      if (lpr)
     &write(l6,*) ' ****** BEGIN CANOUT ******************************'
c
      lqrpa=14
      open(lqrpa,file='rpa.wel',status='unknown')
      write(lqrpa,100) nucnam,nmas,nneu,npro
  100 format(1x,a2,8i4)
      write(lqrpa,'(a10,5f10.4)') txtfor,amsig,amome,amrho,amu
      write(lqrpa,'(10x,3f10.4)') gsigs,gomes,grhos
      write(lqrpa,'(10x,4f10.4)') a_s,b_s,c_s,d_s
      write(lqrpa,'(10x,4f10.4)') a_v,b_v,c_v,d_v
      write(lqrpa,'(10x,f10.4)') a_tv
      write(lqrpa,'(10x,f10.4)') dsat         
c      write(lqrpa,'(a10)') 'D1S'
c      write(lqrpa,'(4f10.4)') gw(1),gw(2),gb(1),gb(2)
c      write(lqrpa,'(4f10.4)') gh(1),gh(2),gm(1),gm(2)
c      write(lqrpa,'(4f10.4)') gr(1),gr(2),gt3,gwls
c      write(lqrpa,'(f10.4)') vfac
 
c---- mesh in the coordinate space
      elower = -2.0*amu
      rstep = 0.05d0 
      rmax  = rstep*nmesh
      xstep = rstep/b0
      write(lqrpa,'(i4,2f20.10)') nmesh,rstep,rmax
      write(lqrpa,'(f20.10)') rms
      write(lqrpa,'(2f20.10)') ala
      write(lqrpa,'(3i5)') nd2x,nb2x,nb 

c      do it = 1,2
c	  write(*,*) 'in canon'      
c          call canon(it,1)
c      enddo
 
c      write(lqrpa,'(2i4)') nqpa(1)+nqap(1),nqpa(2)+nqap(2)
c       write(lqrpa,'(2i4)') nrpa(1),nrpa(2)
       write(lqrpa,'(2i5)') nrpa(1),nrpa(2)

c---- write denss,densv,denstv
      x = zero
      do ix = 0, nmesh
         rsn = rdens(1,rs(1,1),pn,x)   
         rsp = rdens(1,rs(1,2),pn,x)
         rvn = rdens(1,rv(1,1),pn,x)
         rvp = rdens(1,rv(1,2),pn,x)
         denss  =  rsn + rsp
         densv  =  rvn + rvp
         denstv = -rvn + rvp
         write(lqrpa,'(10x,3f10.4)') denss,densv,denstv
         rho1 = densv/dsat
         if (ipara .eq. 0) then
            gs(ix) = gsigs*dip1(rho1,a_s,b_s,c_s,d_s)
            gv(ix) = gomes*dip1(rho1,a_v,b_v,c_v,d_v)
           dgs(ix) = d_dip1(gsigs,dsat,rho1,a_s,b_s,c_s,d_s)
           dgv(ix) = d_dip1(gomes,dsat,rho1,a_v,b_v,c_v,d_v)
           ddgs(ix) = dddip1(gsigs,dsat,rho1,a_s,b_s,c_s,d_s)
           ddgv(ix) = dddip1(gomes,dsat,rho1,a_v,b_v,c_v,d_v) 
         elseif (ipara .eq. 1) then
            gs(ix) = gsigs*dip2(rho1,a_s,b_s,0.,0.)
            gv(ix) = gomes*dip2(rho1,a_v,b_v,0.,0.)
           dgs(ix) = d_dip2(gsigs,dsat,rho1,a_s,b_s,0.,0.)
           dgv(ix) = d_dip2(gomes,dsat,rho1,a_v,b_v,0.,0.) 
           ddgs(ix) = dddip2(gsigs,dsat,rho1,a_s,b_s,0.,0.)
           ddgv(ix) = dddip2(gomes,dsat,rho1,a_v,b_v,0.,0.) 	    
         else 
            gs(ix) = gsigs*dip3(rho1,a_s)
            gv(ix) = gomes*dip3(rho1,a_v)
           dgs(ix) = d_dip3(gsigs,dsat,rho1,a_s,0.,0.,0.)
           dgv(ix) = d_dip3(gomes,dsat,rho1,a_v,0.,0.,0.)
           ddgs(ix) = dddip3(gsigs,dsat,rho1,a_s,0.,0.,0.)
           ddgv(ix) = dddip3(gomes,dsat,rho1,a_v,0.,0.,0.)	   
         endif
            gtv(ix) = grhos*dip3(rho1,a_tv)
           dgtv(ix) = d_dip3(grhos,dsat,rho1,a_tv,0.,0.,0.)
           ddgtv(ix) = dddip3(grhos,dsat,rho1,a_tv,0.,0.,0.)   	   
         x = x + xstep
      enddo 
c
c---- write coupling constants
      x = zero
      do ix = 0,nmesh
         write(lqrpa,'(10x,3f10.4)') gs(ix),gv(ix),gtv(ix)
         x = x + xstep
      enddo
c---- write coupling constants derivatives
      x = zero
      do ix = 0,nmesh
         write(lqrpa,'(10x,3f10.4)') dgs(ix),dgv(ix),dgtv(ix)
         x = x + xstep
      enddo  
c---- write coupling constants second derivatives
      x = zero
      do ix = 0,nmesh
         write(lqrpa,'(10x,3f10.4)') ddgs(ix),ddgv(ix),ddgtv(ix)
         x = x + xstep
      enddo           

       dens0=0
      do it = 1,2
c   
c---- write out wave functions in the canonical basis
c---- first write H11 and j-block parameters
c       do ib = 1,nb
c      lf = ilb(ib,1)
c      lg = ilb(ib,2)
c	   lf = ilb(ib)
c	   ibq = ib - 1 + 2*mod(ib,2)
c	   lg = ilb(ibq)
c          nf = id(ib,1)
c          ng = id(ib,2)
c       nf = id(ib)
c       ng = idq(ib)
c	  nh = nf + ng
c	  nhfb = nh + nh
c          ip  = ipb(ib)	
c	  mf = ib + (it-1)*nbx
c          write(lqrpa,1023) mf,nh 
c1023      format(2i5)
c          do ii=1,nh
c             do kk =1,nh
c                write(lqrpa,1022) h11(ii+(kk-1)*nh,mf
c1022            format(f20.10)              
c             enddo
c          enddo
c             do k=1,ng
c                vvrpa(k,mf)=0
c             enddo
c             do k=ng+1,nh
c                vvrpa(k,mf)=vv(ia(ib)+k-ng,it)
c             enddo
c           do ii=1,nh
c              write(lqrpa,1022) erpa(ii,mf),vvrpa(ii,mf)
c1022          format(2f20.10)                
c           enddo
c        enddo


c-----  PARTICLE AND ANTIPARTICLE WAVE FUNCTIONS
          do ib = 1,nb
c	     lf = ilb(ib,1)
c	     lg = ilb(ib,2)
             lf = ilb(ib)
	     ibq = ib - 1 + 2*mod(ib,2)
	     lg = ilb(ibq)
c	     if (lf.gt.n0f) goto 10 
c             nf = id(ib,1)
c             ng = id(ib,2)
             nf = id(ib)
             ng = idq(ib)
             nh = nf + ng 
             nhfb = nh + nh
c             ip = ipb(ib)
             mf = ib + (it-1)*nbx
             
             do k=1,ng
                vvrpa(k,mf)=0
             enddo
             do k=ng+1,nh
                vvrpa(k,mf)=vv(ia(ib)+k-ng,it)/(2*ijb(ib))
             enddo
             
	     if (ijb(ib).eq.lf) then
		nqkappa = ijb(ib) 
             else
		nqkappa = -ijb(ib) 
             endif	
	     do k = 1,nh  
c                v1 = vvqrpa(k,mf) 
c                e1 = eeqrpa(k,mf)
              v1 = vvrpa(k,mf)
              e1 = erpa(k,mf)
c		d1 = deqrpa(k,mf) ???
	        write(lqrpa,102) nqkappa,e1,v1,k,mf
102             format(i5,2f20.10,2i4)
                 r = zero
                 s = zero 
                 do istep = 0,nmesh
                    call rqwave(it,ib,k,r,f,g,0)
                    ffr(istep) = f
                    ggr(istep) = g
103                 format(f10.4,2f20.10)
                    s = s + (f*f+g*g)*r*r
                    r = r + rstep
                    
c--- check for density
                 dens0(istep) = dens0(istep) + (ffr(istep)**2
     &            +ggr(istep)**2)*vvrpa(k,mf)*2.*ijb(ib)/(4.*pi)
                
                 enddo
                 write(lqrpa,104) ffr
                 write(lqrpa,104) ggr
104              format(4e20.12)  
c                 write(6,*) ' check norm of part. f and g',s*rstep
                 write(l6,*) ' check norm of part. f and g',s*rstep
             enddo !k
10        enddo !ib
      enddo !it
      close(lqrpa)

       open(28, file='density.out',status='unknown')
       do istep=0, nmesh
           write(28,*) istep*rstep, dens0(istep)
       enddo
       close(28)          
c---check for wavefunctions
      return
c-end-CANOUT
      end
c======================================================================c

      subroutine rqwave(it,ib,k,r,f,g,ipa)

c======================================================================c
c
c     calculation of the wavefunctions f(r) and g(r) at point x
c     in the canonical basis
c     x is given in units of the oscillator lenght: x = r/b0 
c     it = 1:  neutron,  it = 2: proton
c     j  = j+1/2
c     ip = 1:  positive  it = 2: negative parity
c     k  = number of the wavefunction in the j-parity block
c----------------------------------------------------------------------c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
c
      dimension rnlr(nd2x)
C
      common /baspar/ hom,hb0,b0
c      common /bloosc/ ia(nbx,2),id(nbx,2)
c      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /bloblo/ nb,ijb(nbx),ilb(nbx),
     &                id(nbx),idq(nbx),ia(nbx),iaq(nbx)
c      common /canonw/ dd(nhqx,nb2x)
      common /eerpa/ erpa(nd2x,nb2x),vvrpa(nd2x,nb2x),hhrpa(nq4x,nb2x)
     &,nrpa(2) 
c      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /dimens/ n0f,n0b,nrm,nlm
      common /gfvsq / sq(0:igfv)
      common /gfvsqi/ sqi(0:igfv)
      common /gfvsqh/ sqh(0:igfv)
      common /gfvshi/ shi(0:igfv)
      common /gfvwgi/ wgi(0:igfv)
      common /mathco/ zero,one,two,half,third,pi
c      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
          
c      nf  = id(ib,1)
c      ng  = id(ib,2)
       nf = id(ib)
       ng = idq(ib)
      nh  = nf + ng
      mf  = ib + (it-1)*nbx
c      lf  = ilb(ib,1)
c      lg  = ilb(ib,2)
       lf = ilb(ib)
	   ibq = ib - 1 + 2*mod(ib,2)
	   lg = ilb(ibq)
      x  = r/b0
      sf = zero
      call osc(nf,lf,x,rnlr)
      do n = 1,nf
c         sf = sf + dd(n+(k-1)*nh,mf)*rnlr(n)
          sf = sf + hhrpa(n+(k-1)*nh,mf)*rnlr(n)
      enddo
      f = sf*b0**(-1.5d0)
      call osc(ng,lg,x,rnlr)
      sg = zero
c      write(lqrpa,*)' --'
      do n = 1,ng
c         sg = sg + dd(nf+n+(k-1)*nh,mf)*rnlr(n)
          sg = sg + hhrpa(nf+n+(k-1)*nh,mf)*rnlr(n)
      enddo
      g = sg*b0**(-1.5d0)
c      write(lqrpa,7656)'g= ',g
      return
c-end-RQWAVE
      end
