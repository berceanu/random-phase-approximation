c======================================================================c

      subroutine reader

c======================================================================c
c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      character*1 tp,tl,tis
      character*2 nucnam
      character*8 tit
      character*10 txtfor
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm,nrbm,nb,nt,no
      common /initia/ vin,rin,ain,inin,inink
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /pair  / ga(2),gg(2),del(2),spk(2),spk0(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /textex/ nucnam,tp(2),tis(2),tit(2),tl(0:20),txtfor
      common /vvvppp/ vpp(mvx,mvx),ipos(nbx),ivpair
      common /parfac/ vfac        
      common /para/ ipara
      common /ugugug/ itbl(2),jbl(2),ipbl(2),nbl(2),nrbl(2) 
c
c
c
      if (l6.ne.6) open(l6,file='dis.out',status='unknown')
      if (lin.eq.0) return
      open(lin,file='dis.dat',status='old')

c
c
c---- Output-File:            
      read(lin,100) l6
  100 format(10x,2i5)
      write(l6,*) ' ****** BEGIN READER *******************************'
      write(l6,101) ' Output file                 : ',l6 
  101 format(a,2i5)
c
c---- Basisparameters:            
      read(lin,100) n0f,n0b
      write(l6,101) ' Number of oscillator shells : ',n0f,n0b
      read(lin,102) b0f
  102 format(10x,2f10.4) 
      write(l6,103) ' Oscillator length b0f (fm)  : ',b0f
  103 format(a,2f10.4) 
c
c---- Parameter for the iteration:
      read(lin,100) maxi
      write(l6,101) ' Maximal number of iterations: ',maxi
      read(lin,102) xmix
      write(l6,103) ' Mixing parameter            : ',xmix
      xmix0 = xmix
c
c---- Initialization of wavefunctions:
c     read(lin,100) inin,inink
      write(l6,101) ' Initial wavefunctions       :  ',inin,inink
c
c---- Nucleus under consideration
      read(lin,'(a2,i4)') nucnam,nama
      write(l6,'(a,20x,a2,i4)') ' Nucleus:      ',nucnam,nama
c
c---- Frozen Gap-Parameters
      read(lin,102) dec
      write(l6,103) ' Frozen Gap Parameters      : ',dec
c
c---- Pairing-Constants
      read(lin,102) ga
      write(l6,103) ' Pairing-Constants          : ',ga
c
c---- Initial Gap Parameters
      read(lin,102) del
      write(l6,103) ' Initial Gap Parameters     : ',del
c
c
c---- Pairing matrix elements    
      read(lin,100) ivpair
      write(l6,101) ' Pairing matrix elements    : ',ivpair

c---- vfac factor for vpair multiplication
      read(lin,102) vfac

c---- Parametrization type   
c     read(lin,100) ipara
      write(l6,101) ' Parametrization type       : ',ipara
c
c---- blocking
      read(lin,104) itbl(1),jbl(1),ipbl(1),nrbl(1)
      read(lin,104) itbl(2),jbl(2),ipbl(2),nrbl(2)
      write(l6,105) 'Blocking neutrons    : ',itbl(1),jbl(1),ipbl(1),
     &                                       nrbl(1)
      write(l6,105) 'Blocking protons     : ',itbl(2),jbl(2),ipbl(2),
     &                                       nrbl(2) 
104   format(10x,4i3)
105   format(a,4i3)
c      close(lin)
c
      write(l6,*) ' ****** END READER *********************************'
c-end-reader 
      end
