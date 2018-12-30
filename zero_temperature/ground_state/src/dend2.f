      subroutine dend2(lpr,cc)
      
c     cc = 0 energy
c     cc = 1 potential

      implicit real*8(a-h,o-z)
      
      include 'dis.par'
      integer cc
      logical lpr
      
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos        
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat      
      common /rhorho/ rs(ngh,2),rv(ngh,2),dro(ngh)      
      common /gaucor/ rb(ngh),wdcor(ngh)
      common /rearen/ er,rear(ngh)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /tapes / l6,lin,lou,lwin,lwou,lplo      
      common /para/ ipara           
                  
      if (lpr)
     &   write(l6,*) '********** BEGIN DEND2 **********'
     
     
      er =0.d0
      if (cc .eq. 0) then
         do ih = 1,ngh
	    denss = rs(ih,1) + rs(ih,2)
	    densv = rv(ih,1) + rv(ih,2)
	    denstv = -rv(ih,1) + rv(ih,2)
	    x = densv/dsat
	    if (ipara.eq.0) then
	       facs = d_dip1(gsigs,dsat,x,a_s,b_s,c_s,d_s)
	       facv = d_dip1(gomes,dsat,x,a_v,b_v,c_v,d_v)
	    elseif(ipara.eq.1) then
	       facs = d_dip2(gsigs,dsat,x,a_s,b_s,0.,0.)
	       facv = d_dip2(gomes,dsat,x,a_v,b_v,0.,0.)
	    elseif(ipara.eq.2) then
	       facs = d_dip3(gsigs,dsat,x,a_s,0.,0.,0.)
	       facv = d_dip3(gomes,dsat,x,a_v,0.,0.,0.)
	    endif
	       factv = d_dip3(grhos,dsat,x,a_tv,0.,0.,0.)	    	       
	       ss = denss*sig(ih)*densv*facs +
     &              densv*ome(ih)*densv*facv +
     &              denstv*rho(ih)*densv*factv
            er = er + ss*wdcor(ih)
	 enddo
	 
      else
         do ih = 1,ngh
	    denss = rs(ih,1) + rs(ih,2)
	    densv = rv(ih,1) + rv(ih,2)
	    denstv = -rv(ih,1) + rv(ih,2)
	    x = densv/dsat 
	    if (ipara.eq.0) then
	       facs = d_dip1(gsigs,dsat,x,a_s,b_s,c_s,d_s)
	       facv = d_dip1(gomes,dsat,x,a_v,b_v,c_v,d_v)
	    elseif(ipara.eq.1) then
	       facs = d_dip2(gsigs,dsat,x,a_s,b_s,0.,0.)
	       facv = d_dip2(gomes,dsat,x,a_v,b_v,0.,0.)
	    elseif(ipara.eq.2) then
	       facs = d_dip3(gsigs,dsat,x,a_s,0.,0.,0.)
	       facv = d_dip3(gomes,dsat,x,a_v,0.,0.,0.)
	    endif
	       factv = d_dip3(grhos,dsat,x,a_tv,0.,0.,0.)	    	 
	    rear(ih) = facs*denss*sig(ih) +
     &                 facv*densv*ome(ih) +
     &                 factv*denstv*rho(ih)

         enddo
      endif
      
      if (lpr)
     &   write(l6,*) '********** END DEND2 **********'
     
      return
      end
            
         
