c======================================================================c
c
      subroutine degen(na,n,ea,dd,bb,eb,eps,zz,z)
c
c======================================================================c
c
c     EA    is a set of partially degenerate eigenvalues of some matrix 
c     DD    are the corresponding eigenvectors DD. 
c     BB    is a matrix, which is diagonalized in the subspaces of
c           degenerate eigenvales EA.
c     EB    contains the eigenvalues of BB in these subspaces.
c     EPS   determines, to which accuracy the eigenvalues EA are
c           considered to be degenerate
c     ZZ,Z  are auxiliary arrays
c
c----------------------------------------------------------------------c
      implicit real*8 (a-h,o-z) 
c
      dimension bb(na,n),dd(na,n),ea(n),eb(n)
      dimension zz(na,n),z(n)
c
      common /mathco/ zero,one,two,half,third,pi
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
c 
c---- check for degeneracies
      k1 = 0
      do i1 = 1,n
         k1 = k1 + 1
         if (k1.ge.n) goto 20
         do k2 = k1+1,n
            if (ea(k2)-ea(k1).gt.eps) goto 10
         enddo
   10    me = k2 - 1
         ma = k1
c
c----    diagonalize together with bb 
         if (me.gt.k1) then
            m0 = ma - 1
            mm = me - m0
c           write(6,'(3i3,a,/,(10f12.8))') mm,ma,me,
c     &      ' Eigenvalues degenerate:',(ea(i),i=ma,me)
c           write(l6,'(3i3,a,/,(10f12.8))') mm,ma,me,
c     &      ' Eigenvalues degenerate:',(ea(i),i=ma,me)

            do m1 = ma,me
               do k = 1,n
                  s = zero
                  do i = 1,n  
                     s = s + dd(i,m1) * bb(i,k)
                  enddo   ! i
                  z(k) = s
               enddo   ! k
               do m2 = ma,me
                  s = zero
                  do k = 1,n
                     s = s + z(k) * dd(k,m2)
                  enddo   ! k
                  zz(m1-m0,m2-m0) = s
               enddo   ! m2
            enddo   ! m1
            call sdiag(na,mm,zz,eb(ma),zz,z,+1)
c           call aprint(1,1,6,1,1,mm,eb,' ',' ','H_x')
c	    call aprint(1,1,6,1,1,mm,eb(ma),' ',' ','H_x')
c           call aprint(1,1,1,na,mm,mm,zz,' ',' ','DD_x')
            do i = 1,n
               do m = ma,me
                  s = zero
                  do l = ma,me 
                     s = s + dd(i,l) * zz(l-m0,m-m0)
                  enddo   ! l
                  z(m) = s
               enddo   ! m
               do m = ma,me
                  dd(i,m) = z(m)
               enddo   ! m
            enddo   ! i
            k1 = me 
         endif
      enddo   ! i1
c
   20 return
c-end-DEGEN
      end
