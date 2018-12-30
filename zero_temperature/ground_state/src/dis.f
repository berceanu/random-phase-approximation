c======================================================================c

c     PROGRAM DISHFB

c======================================================================c
c     Relativistic mean field theory mit HFB in a spherical basis
c     contains transformation to canonical basis; adjusted for RQRPA
c     Nov. 11, 2001
c----------------------------------------------------------------------c
      implicit real*8(a-h,o-z)
c
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
c---- initialization of kappa
      call kinout(1,.true.)
c
c---- wavefunctions at Gauss-Meshpoints
      call radgh(.false.)
c
c---- single-particle matix elements
      call singf(.false.)
c
c---- pairing matrix elements
      call vpair(.false.)
c
c---- iteration
      call iter(.true.)
c
c---- results
      call resu(.true.)
c
c---- punching of potentials to tape  dis.wel
      call inout(2,.false.)
c
c---- punching of the pairing tensor  dis.aka
      call kinout(2,.false.)
c
c---- plotting of densities in coordinate space
       call plotd(.true.)
c
c---- output for qrpa
      call canout(.true.)
c July 1998 
c---- plotting of wavefunctions in the canonical basis in coordinate space
      it = 1
      j  = 7
      ip = 2
      k  = 6
      call plotw(it,j,ip,k,.true.)
c      stop ' FINAL STOP'
c-end-DISHFB
      end

