c======================================================================c

      subroutine delta(it,lpr)

c======================================================================c
c
c     calculats the Pairing field in the HFB-equation
c     from precalculated matrixelements in VPP
c
c     IT = 1:  neutrons
c          2:  protons
c 
c----------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
c
      logical  lpr
      character*8 tb,tbb(nhx)
      character*25 txb
c
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /initia/ vin,rin,ain,inin,inink
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /hfbhfb/ hh(nhqx,nb2x),de(nhqx,nb2x)
      common /kappa / aka(nqx,nb2x)
      common /kappag/ akag(nqx,nb2x)
      common /mathco/ zero,one,two,half,third,pi
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /vvvppp/ vpp(mvx,mvx),ipos(nbx),ivpair
      common /parfac/ vfac
c
      ik(i,k,n) = i + (k-1)*(2*n-k)/2
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN DELTAV *******************************'
c
c
c
c
c---- loop over the different j-blocks
      decc = dec(it)
      do ib12 = 1,nb
         l1    = ilb(ib12,1)
         if (l1.gt.n0f) goto 10
c         write(6,*) ' Block ib12 = ',ib12
         j1    = ijb(ib12)
         l2    = l1
         ibg12 = ib12 - 1 + 2*mod(ib12,2)
         nf12  = id(ib12,1)
         ng12  = id(ib12,2)
         nh12  = nf12 + ng12
         mf12  = ib12 + (it-1)*nbx
	 mg12  = ibg12 + (it-1)*nbx
c
c
c------- large components
         ipb12 = ipos(ib12)
	 ipbg12 = ipos(ibg12)
         do n2 = 1,nf12
         do n1 = n2,nf12
            i12 = ik(n1,n2,nf12)  
            d12 = zero 
            do ib34 = 1,nb
               j3    = ijb(ib34)
               l3    = ilb(ib34,1)
               l4    = l3
               nf34  = id(ib34,1)
               mf34  = ib34 + (it-1)*nbx
               ipb34 = ipos(ib34)
               n34   = nf34*(nf34+1)/2
c
               s = zero
               do i34 = 1,n34
                  s   = s + vpp(ipb12+i12,ipb34+i34)*aka(i34,mf34)
               enddo
               d12 = d12 + s
            enddo
            d12 = half*d12
            if (n1.eq.n2) d12 = d12 + decc
c
            de(n1+(n2-1)*nh12,mf12) = d12
            de(n2+(n1-1)*nh12,mf12) = d12
         enddo
         enddo
c
c------- small components
         do n2 = 1,ng12
         do n1 = 1,ng12
            de(nf12+n1+(nf12+n2-1)*nh12,mf12) = zero
            de(nf12+n2+(nf12+n1-1)*nh12,mf12) = zero
         enddo
         enddo
c
c------- delta has no mixing between large and small components
         do n1 = 1,ng12
         do n2 = 1,nf12
            de(nf12+n1+(n2-1)*nh12,mf12) = zero
            de(n2+(nf12+n1-1)*nh12,mf12) = zero
         enddo
         enddo 
c
c------- Printout
   20    if (lpr) then
            imf = ia(ib12,1)
            img = ia(ib12,2)
            do i = 1,nf12
               tbb(i) = tb(imf+i)
            enddo
            do i = 1,ng12
               tbb(nf12+i) = tb(img+i)
            enddo
            write(l6,'(/,a)') txb(ib12)
            call aprint(1,2,6,nh12,nh12,nh12,de(1,mf12),tbb,' ','DE') 
         endif
c
c	 do i1=1,nh12
c	 do i2=1,nh12
c	   if(i1.ne.i2) then
c	     de(i1+(i2-1)*nh12,mf12) = 0.0
c	   endif
c         enddo
c         enddo

   10 enddo
c
      if (lpr)
     &write(l6,*) ' ****** END DELTAV *********************************'
      return
C-end-DELTAV
      end
