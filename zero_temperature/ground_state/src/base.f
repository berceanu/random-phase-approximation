c======================================================================c

      subroutine base(lpr)

c======================================================================c
c
c     determines the basis in spherical oscillators for Dirac solution 
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
      dimension iag0(nbx),idg0(nbx)
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /bloosc/ ia(nbx,2),id(nbx,2)
      common /bloqua/ ijb(nbx),ilb(nbx,2),ipb(nbx),ikb(nbx)
      common /gfviv / iv(0:igfv)
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /oscqua/ nr(ntx),nl(ntx),nj(ntx)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /texblo/ tb(ntx),txb(nbx)
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2)
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN BASE *********************************'
c
c      write(6,*) 'n0f,n0fx',n0f,n0fx
      if (n0f.gt.n0fx) stop ' in BASE: n0f too large'
c
c----------------------------------------------------------------------c
c     construction of the different kappa-blocks
c----------------------------------------------------------------------c
      nrm = 1 + (n0f+1)/2
      nlm = n0f+1
      if (nrm.gt.ndx) stop ' in BASE: ndx too small'
      if (nrm.gt.nrx) stop ' in BASE: nrx too small '
      if (nlm.gt.nlx) stop ' in BASE: nlx too small '
      nbl(1) = 0
      nbl(2) = 0
c
c---- loop over j-quantum number
      il = 0
      do j = 1,n0f+1
	 ilj = il
c
c------- loop over parity
         do 10 ip = 1,2
	    ib = 2*(j-1) + ip
	    id(ib,1) = 0
c
	    if (mod(j,2).eq.ip-1) then
	       ik = +j
	       l  =  j
	       la =  j - 1
	    else
	       ik = -j
	       l  =  j - 1
	       la =  j
            endif
c    if (l.gt.n0f) goto 10
            if (ib.gt.nbx) stop ' in BASE: nbx too small'
	    ipa     = 3 - ip
	    ijb(ib) = j
	    ilb(ib,1) = l
	    ilb(ib,2) = la 
	    ipb(ib) = ip
	    ikb(ib) = ik
            ne  = 1 + (n0f-l)/2 
	    if (l.gt.n0f) ne = 0 
            ne1 = 1 + (n0f+1-l)/2 
	    nea = 1 + (n0f-la)/2
	    if (la.gt.n0f) nea = 0 
	    nea1= 1 + (n0f+1-la)/2
	    idg0(ib) = nea1-nea
c
	    id(ib,1) = ne
	    id(ib,2) = nea1
	    ia(ib,1) = il 
	    if (ip.eq.1) then
	       ia(ib,2) = il + ne1 
            else
	       ia(ib,2) = il - nea1 
	    endif
	    idg0(ib) = nea1-nea
	    iag0(ib) = ia(ib,2)+nea
c           write(l6,'(/,a,i3,a,a1)') ' j = ',j+j-1,'/2',tp(ip)
            write(txb(ib),'(i3,a,i2,a,a1)') 
     &            ib,'.block:  j = ',j+j-1,'/2',tp(ip)
c
c---------- loop over radial quantum number
            do ir = 1,ne1
	       il   = il + 1
               if (il .gt.ntx) stop ' in BASE: ntx too small'
               nr(il) = ir
               nl(il) = l
               nj(il) = j
               write(tb(il),'(i2,a1,i3,2h/2)') ir,tl(l),j+j-1
               nn        = 2*(ir-1)+l
c              write(l6,'(i4,a,i2,a,i2,a,i2)') 
c    &               il,'  N = ',nn,'   n = ',ir,'   l = ',l
            enddo    
c          
c           determination of blocked level
            do it = 1,2
               if ( itbl(it).eq.1  .and. jbl(it).eq.j .and. 
     &              ipbl(it).eq.ip ) nbl(it)=ib
            enddo
c
   10    enddo    
      enddo
      nb  = ib 
      nt  = il
c
c----------------------------------------------------------------------c
c     Printout
c----------------------------------------------------------------------c
      if (lpr) then
	 do i = 1,nt
	    write(l6,'(i3,1x,a)') i,tb(i)
         enddo
         do 20 ib = 1,nb
	    if (id(ib,1).eq.0) goto 20
	    j = ijb(ib)
            write(l6,'(/,a,6i4)') txb(ib),id(ib,1),id(ib,2),idg0(ib) 
     &                                   ,ia(ib,1),ia(ib,2),iag0(ib)
            do i = ia(ib,1)+1,ia(ib,1)+id(ib,1)
               nn     =  2*(nr(i)-1) + nl(i)
               write(l6,102) i,'   NN = ',nn,
     &         '   nr = ',nr(i),'   l =',nl(i),'   j =',j+j-1,tb(i)
  102          format(i4,a,i2,a,i2,a,i2,a,i2,3h/2 ,a) 
            enddo       
            write(l6,'(3x,61(1h-))')
            do i = ia(ib,2)+1,ia(ib,2)+id(ib,2)-idg0(ib)
               nn     = 2*(nr(i)-1) + nl(i)
               write(l6,102) i,'   NN = ',nn,
     &         '   nr = ',nr(i),'   l =',nl(i),'   j =',j+j-1,tb(i)
            enddo
            write(l6,'(3x,61(1h.))')
            do i = iag0(ib)+1,iag0(ib)+idg0(ib)
               nn     =  2*(nr(i)-1) + nl(i)
               write(l6,102) i,'   NN = ',nn,
     &         '   nr = ',nr(i),'   l =',nl(i),'   j =',j+j-1,tb(i)
            enddo
   20    enddo
c
         write(l6,'(/,a,2i4)') ' Number of blocks: nb  = ',nb,nbx
         write(l6,100) ' Number of levels  nt  = ',nt,ntx 
         write(l6,100) ' Maximal n:        nrm = ',nrm,nrx
         write(l6,100) ' Maximal l:        nlm = ',nlm,nlx
         write(l6,100) ' Blocked levels:   nrbl= ',nrbl
  100    format(a,2i4)
      endif
c    
      if (lpr)
     &write(l6,*) ' ****** END BASE ***********************************'
      return
c-end-BASE
      end
