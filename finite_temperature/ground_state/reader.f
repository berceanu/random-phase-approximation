c======================================================================c

      subroutine reader

c======================================================================c
c
      include 'paramet'
c
      implicit real*8 (a-h,o-z)
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
      character*40 filename
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm
      common /initia/ vin,rin,ain,inin
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /para/ ipara
      common /temper/ temp
c
      common /file/ filename
c
c
      if (l6.ne.6) open(l6,file='dis.out',status='unknown')
      if (lin.eq.0) return
      open(lin,file='dis.dat',status='old')
c
c
c---- Output-File:            
      read(lin,'(10x,i5)') l6
      write(l6,*) ' ****** BEGIN READER *******************************'
      write(l6,'(a,i5)') ' Output file                 : ',l6 
c
c---- Basisparameters:            
      read(lin,'(10x,2i5)') n0f,n0b
      write(l6,'(a,2i5)') ' Number of oscillator shells : ',n0f,n0b
      read(lin,'(10x,f10.3)') b0
      write(l6,'(a,f9.3)') ' Oscillator length b0 (fm)   : ',b0
c
c---- Parameter for the iteration:
      read(lin,'(10x,i5)') maxi
      write(l6,'(a,i5)') ' Maximal number of iterations: ',maxi
      read(lin,'(10x,f10.3)') xmix
      write(l6,'(a,f9.3)') ' Mixing parameter            : ',xmix
      xmix0 = xmix
c
c---- Initialization of wavefunctions:
c     read(lin,'(10x,i5)') inin
      write(l6,'(a,i5)') ' Initial wavefunctions       :  ',inin
c
c---- Nucleus under consideration
      read(lin,'(a2,i4)') nucnam,nama
      write(l6,'(a,20x,a2,i4)') ' Nucleus:      ',nucnam,nama
c
c---- Gap-Parameters
      read(lin,'(10x,2f10.3)') dec
      write(l6,'(a,2f10.3)') ' Gap Parameters             : ',dec
c
c---- Density dependence type  
      read(lin,'(10x,i5)') ipara
      write(l6,'(a,i5)') ' Ipara                : ',ipara
c
c---- Temperature
      read(lin,'(10x,f10.3)') temp
      write(l6,'(a,f9.3)') ' Temperature                 :', temp
c
c-----filename
      read(lin, '(12x,a)')filename
c 
      close(lin)
c
      write(l6,*) ' ****** END READER *********************************'
c-end-reader 
      end
