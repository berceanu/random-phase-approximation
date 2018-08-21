c======================================================================c

      subroutine kinout(is,lpr)

c======================================================================c
c
c     IS = 1 : for ININK = 0  reads pairing tensor AKA from tape  
c                  ININK = 1  calculates pairing tensor AKA  
c     IS = 2 : writs pairing tensor AKA to tape                  
c
c
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*8 tb,tit
      character*25 txb
c
      common /baspar/ hom,hb0,b0
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /fermi / ala(2),tz(2)
      common /initia/ vin,rin,ain,inin,inink
      common /kappa / aka(nqx,nb2x)
      common /kappag/ akag(nqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
c
      ik(i,k,n) = i + (k-1)*(2*n-k)/2
c
c
      write(l6,*) ' ****** BEGIN KINOUT *******************************'
c
      if ((is.eq.1.and.inink.eq.0).or.is.eq.2) 
     &   open(laka,file='dis.aka',status='unknown')
c
c
c---- loop over neutron and proton
      do it = it1,it2
c
c------- loop over the j-blocks
         sp = zero
         do ib = 1,nb
            nf  = id(ib,1)
            ng  = id(ib,2)
            nff = nf*(nf+1)/2
            ngg = ng*(ng+1)/2
            imf = ia(ib,1)+1 
            img = ia(ib,2)+1 
            m   = ib  + (it-1)*nbx
            lf  = ilb(ib,1)
            lg  = ilb(ib,2)
c
c
            if (is.eq.1) then
c
c------------- calculation of the pairing tensor
               emc2 = 2*600.d0
               if (inink.ne.0) then
                  do i = 1,nff
                     aka(i,m) = zero
                  enddo
                  ntz = 0
                  do nn = 0,10
                     ntz = ntz + (nn+1)*(nn+2)
                     if (ntz.gt.tz(it)) goto 10
                  enddo
   10             al = hom*(nn+1.5d0)
c                  ne = nf
c                  if (2*(nf-1)+lf.gt.n0f) ne = nf-1
                  do n1 =  1,nf
                     el = hom*(2*(n1-1)+lf+1.5d0)-al 
                     uv = half*del(it)/sqrt(el**2 + del(it)**2)
                     aka(ik(n1,n1,nf),m) = 2*ijb(ib)*uv
                  enddo
                  do i = 1,ngg
                     akag(i,m) = zero
                  enddo
c                  ne = ng
c                  if (2*(ng-1)+lg.gt.n0f) ne = ng-1
                  do n1 =  1,ng
                     el = -emc2-hom*(2*(n1-1)+lf+1.5d0)-al 
                     uv = half*del(it)/sqrt(el**2 + del(it)**2)
                     akag(ik(n1,n1,ng),m) = 0.0!2*ijb(ibg)*uv 
                  enddo
c
c
c------------- reading of the pairing tensor
               else 
                  read(laka,'(4x,2i3)') i1,i2
                  if (i1.ne.it.or.i2.ne.nb) stop ' in KINOUT: AKA wrong'
                  read(laka,101) (aka(i,m),i=1,nff)
                  read(laka,101) (akag(i,m),i=1,nff)
  101             format(4e20.12)
                  s = zero
                  do n1 = 1,nf
                     s = s + aka(ik(n1,n1,nf),m)
                  enddo
                  sp = sp + half*s
c
               endif
c
c---------- writing of the pairing tensor aka:
            else
               write(laka,105) ' AKA',it,nb,ib,txb(ib)
  105          format(a,3i3,'  ',a)
               write(laka,101) (aka(i,m),i=1,nff)
               write(laka,101) (akag(i,m),i=1,nff)
            endif
c
c
c---------- printing
            if (lpr) then
               write(l6,'(/,a,1x,a)') txb(ib),tis(it)
               call aprint(3,2,1,nf,nf,nf,aka(1,m),tb(imf),' ','AKA ')
               call aprint(3,2,1,ng,ng,ng,akag(1,m),tb(img),' ','AKAG')
            endif
c
c------- end loop over blocks ib
         enddo
         spk(it) = sp
c
c---- end loop over neutrons and protons
      enddo
c
      if (is.eq.1.and.inink.eq.1) then
         write(l6,*) ' Pairing tensor AKA has been calculated'
      elseif (is.eq.1) then
         write(l6,*) ' Pairing tensor AKA has been read from dis.aka'
      else 
         write(l6,*) ' Pairing tensor AKA has been written to dis.aks'
      endif
      close(laka)
c
      write(l6,*) ' ****** END KINOUT *********************************'
      return
c-end-KINOUT
      end  
