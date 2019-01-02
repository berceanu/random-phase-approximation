c======================================================================c

c     PROGRAM SKYS

c======================================================================c
c     Relativistic mean field theory in a spherical basis
c----------------------------------------------------------------------c
c
      program SKYS

      use chdir_mod

      implicit real*8 (a-h,o-z)
      common /temper/ temp
      
      integer iargc
      integer argc
      character*100 argv(10)
      character*100 :: workdir

      argc=iargc()
      write (*,*) 'Number of arguments:', argc
      do i=1,min(argc,10)
        call getarg(i,argv(i))
        write (*,*) 'Argument no',i,'=',argv(i)
      enddo

      call chdir("skys")

c---- reads in data     
      call reader
c
c---- preparations
      call prep
c
c---- initialization of the potentials
      call inout(1,.false .)
      call start(.true.)
c
c---- oscillator basis for single particle states
      call base(.true.)
c
c---- wavefunctions at Gauss-Meshpoints
      call radgh(.false.)
c
c---- single-particle matix elements
      call singf(.false.)
c
c      open(20, file='skys_' // 'ERSvT.txt')
c      do i=0,15
c      temp=i*0.2
c---- iteration
      call iter(.true.)
c
c---- results
      call resu(.true.)
      
c      enddo
c      close(20)
c
c---- punching of potentials
      call inout(2,.true.)
c
c---- plotting of densities in coordinate space
       call plotd(.true.)
c       call reinhard
c
c---- plotting of wavefunctions in coordinate space
      it = 1
      ib = 1
      k  = 1
      call plotw(it,ib,k,.false.)
c---- time-dependent code input
      call td_out
      
c---- rpa code input
      call rpaout(.true.)  
      
      stop ' FINAL STOP'
c-end-DIS
      end
