c===============================================================================

      subroutine reinhard

c===============================================================================
c      calculates diffraction radius and surface thickness
c      ref. Z. Phys. A 323, 13 (1986)
c-------------------------------------------------------------------------------
      include 'paramet'
      implicit real*8(a-h,o-z)


      logical fc_rise,fc_zero,fc_max
      dimension ap(1:4),an(1:4),bp(1:4),bn(1:4)

      common /baspar/ hom,hb0,b0
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,npr(2),jmax 
      common /physco/ amu,hqc,alphi,r0
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /erwar / ea,rms,qp,diffr,surface
      common /cenmas/ ecm,p2

      data maxr/256/,rstep/0.05/,maxi/4000/,qstep/0.001/
      data ap /0.312, 1.312, -0.709, 0.085/
      data bp /0.16667,0.06658,0.02269,0.006485/
      data an /1.,-1.,0.,0./
      data bn /0.04833,0.05833,0.0,0.0/

      am = amas*amu/hqc
      fc_rise = .false.
      fc_zero = .false.
      fc_max = .false.
      do i=1,maxi
         q=i*qstep
      
c----- radial integrals (2.15)
         fnq=zero
         fpq=zero
         do ih=1,ngh
            r=rb(ih)
            wx=b0*wh(ih)
            rintn=r*sin(q*r)*rv(ih,1)
            rintp=r*sin(q*r)*rv(ih,2)
            fnq=fnq+wx*rintn
            fpq=fpq+wx*rintp
         enddo
         fnq=4.*pi*fnq/q
         fpq=4.*pi*fpq/q

c----- factors 2.16
         ffnq=zero
	 ffpq=zero
	 do j=1,4
	    ffnq=ffnq+an(j)/(1+bn(j)*q**2)
	    ffpq=ffpq+ap(j)/(1+bp(j)*q**2)
	 enddo   

c----- F_c
         fcq=(fpq*ffpq+fnq*ffnq)*exp((0.51*q)**2/amas**(2./3.))
c        fcq=(fpq*ffpq+fnq*ffnq)*exp(q**2/(8.0*p2)) ! true CM correction
        write(31,*) q,fcq
c----- search fort F_c=0.0 and for max. F_c
         if (i .eq. 1) then
            fcq_old = fcq
            fcq_norm = fcq
         else
            if (fc_zero) then
               goto 15
            else
               if ( (fcq*fcq_old) .lt. zero) then
                  q_zero = q - qstep/2.
                  fc_zero = .true.
               endif
            endif
15          continue
            if (fc_max) then
               goto 17
            else
               if (fc_rise) then
                  if (fcq .lt. fcq_old) then
                     q_max = q - qstep
                     fc_m = fcq_old
                     fc_max = .true.
                  endif
               endif
               if (fcq_old .lt. fcq) fc_rise = .true.
            endif
         endif
17       continue
         if (fc_zero .and. fc_max) goto 10
         fcq_old = fcq
      enddo
10    continue

c----- diffraction radius (2.17)
      diffr = 4.493/q_zero   
       
c----- form factor normalization F_c(0) = 1
      fc_m = fc_m/fcq_norm 
      
c----- surface thickness (2.18)
      x = q_max*diffr
      t1 = 1/x*(-cos(x)+sin(x)/x)
      t2 = 3.d0*t1/(x*fc_m)
      surface = sqrt(two*log(t2)/q_max**2)
      write(*,*) diffr,surface

      return
      end
                           
