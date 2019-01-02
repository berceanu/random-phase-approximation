c=====================================================================c

      subroutine plotd(lpr)

c=====================================================================c
C
C     prepares plot of densities in coordinate space
C
c---------------------------------------------------------------------c
      include 'dis.par'
c
      implicit real*8 (a-h,o-z)
      logical lpr
c
      dimension pn(nox), ppn(nox)
c
      common /baspar/ hom,hb0,b0
      common /gaussh/ xh(ngh),wh(ngh),ph(ngh)
      common /mathco/ zero,one,two,half,third,pi
      common /optopt/ icm,icou,it1,it2,ncut
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo,laka,lvpp,lqrpa
      common /potpot/ vps(ngh,1:2),vms(ngh,1:2)
      common /physco/ amu,hqc,alphi,r0
      common /plot1/ vps2(ngh,1:2)
      common /coupl/  gsig(ngh),gome(ngh),grho(ngh) 
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)  
      common /gaucor/ rb(ngh),wdcor(ngh)          
c
c
      if (lpr)
     &write(l6,*) ' ****** BEGIN PLOTD ********************************'
c
c
c-------------------------------------------------
c     test:
c     do ih=1,ngh
c        ro = rdens(1,rs(1,1),pn,xh(ih))
c        write(l6,*) 'rs neut',ih,xh(ih)*b0f,ro
c     enddo
c-------------------------------------------------
c     number of points for the plot
      mxpl  = 128 
c     plot step in (fm)
      stpl = 0.1

c----- plot for potentials
      inx=91
      ipx=92
      insx=93
      ipsx=94  
      open(inx,file='dish_' //'xncen.pot',status='unknown')
      open(ipx,file='dish_' //'xpcen.pot',status='unknown')
      open(insx,file='dish_' //'xnspin.pot',status='unknown')
      open(ipsx,file='dish_' //'xpspin.pot',status='unknown')
c      do 10 it = it1,it2
      write(inx,'(/,a,i3)') '# n central it =',1
      write(ipx,'(/,a,i3)') '# p central it =',2
      write(insx,'(/,a,i3)') '# n s-o pot it =',1
      write(ipsx,'(/,a,i3)') '# p s-o pot it =',2
      r=zero
      do ist = 0, mxpl
      x = r/b0
      xr1= rdens(1,vps(1,1),ppn,x)
            write(inx,100) r,xr1
      xr2= rdens(1,vps(1,2),ppn,x)
            write(ipx,100) r,xr2
      xr3= rdens(1,vms(1,1),ppn,x)
            xr3 = xr3*amu/(amu-0.5*xr3)
            write(insx,100) r,xr3
      xr4= rdens(1,vms(1,2),ppn,x)
            xr4 = xr4*amu/(amu-0.5*xr4)
            write(ipsx,100) r,xr4
      r = r + stpl
      enddo  
      close(inx)
      close(ipx)
      close(insx)
      close(ipsx)
c
c---- plot for densities:

      open(lplo,file='dish_' //'dis.plo',status='unknown')
      do it = it1,it2
         write(lplo,'(/,a,i3)') '# scalar density it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,rs(1,it),pn,x)
c           write(lplo,100) r,ro
  100       format(f10.3,f15.6) 
            r = r + stpl
         enddo
c
         write(lplo,'(/,a,i3)') '# vector density it =',it
         r = zero
         do ist = 0,mxpl
            x  = r/b0
            ro = rdens(1,rv(1,it),pn,x)
c           write(lplo,100) r,ro 
            r = r + stpl
         enddo
      enddo
c
      write(lplo,'(/,a)') '# neutron and proton densities'
      r = zero
      do ist = 0, mxpl
	  x  = r/b0
	  rn  = rdens(1,rv(1,1),pn,x)
	  rp  = rdens(1,rv(1,2),pn,x)
	  write(lplo,103) r,rn,rp
	  r   = r +stpl
      enddo
103          format(f10.3,2f15.6)
      close(lplo)
c
      if (lpr)
     &write(l6,*) ' ****** END PLOTD **********************************'
      return
C-end-PLOT
      end
