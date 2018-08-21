c======================================================================c

      blockdata default

c======================================================================c
c
c     Default for Relativistic Mean Field spherical
c
c----------------------------------------------------------------------c
c
      implicit real*8 (a-h,o-z)
      include 'paramet'
c
      character*1 tp,tl,tis
      character*2 nucnam
      character*10 txtfor
c
      common /baspar/ hom,hb0,b0
      common /dimens/ n0f,n0b,nrm,nlm
      common /fermi / ala(2),tz(2)
      common /fields/ sig(ngh),ome(ngh),rho(ngh),cou(ngh)
      common /fixocc/ ioc(nbx,2)
      common /initia/ vin,rin,ain,inin
      common /iterat/ si,siold,epsi,xmix,xmix0,xmax,maxi,ii,inxt,iaut
      common /mespar/ amsig,amome,amrho,gsigs,gomes,grhos
      common /cpara/ a_s,b_s,c_s,d_s,a_v,b_v,c_v,d_v,a_tv,dsat                 
      common /mathco/ zero,one,two,half,third,pi
      common /nucnuc/ amas,nama,nneu,npro,jmax
      common /optopt/ icm,icou,it1,it2,ncut
      common /pair  / ga(2),gg(2),del(2),spk(2),dec(2),pwi
      common /physco/ amu,hqc,alphi,r0
      common /tapes / l6,lin,lou,lwin,lwou,lplo
      common /temper/ temp
      common /textex/ nucnam,tp(2),tis(2),tl(0:20),txtfor
      common /woodsa/ v0,akv,vso(2),r0v(2),av(2),rso(2),aso(2)
c
c
c---- nucleus
      data nucnam/' O'/,nama/16/
      data jmax/8/
c
c---- options
c     center of mass:
      data icm/0/
c     protons or neutrons of both
      data it1/1/,it2/2/
c
c---- iteration
      data maxi/500/,si/1.0d0/,epsi/0.000001/
      data iaut/0/,inxt/3/
      data xmix0/0.1d0/,xmix/0.1d0/,xmax/0.8d0/
c---- force-parameters
c----------------------------------------------------------------
c       data txtfor/'ME-DD1'/
c       data amu/939.0/
c       data amsig/549.526/,amome/783.000/,amrho/763.0/
c       data gsigs/10.4434/,gomes/12.8939/,grhos/3.8053/
c       data b_s/0.9781/,c_s/1.5342/
c       data b_v/0.8525/,c_v/1.3566/
c       data a_tv/0.5008/
c       data dsat/0.152/
c---------------------------------------------------------------
      data txtfor/'DD-ME2'/
      data amu/939.0/
      data amsig/550.1238/,amome/783.000/,amrho/763.0/
      data gsigs/10.5396/,gomes/13.0189/,grhos/3.6836/
      data b_s/1.0943/,c_s/1.7057/
      data b_v/0.9240/,c_v/1.4620/
      data a_tv/0.5647/
      data dsat/0.152/
c---------------------------------------------------------------
c      data txtfor/'TW-99'/
c      data amu/939.0/
c      data amsig/550.0/,amome/783.000/,amrho/763.0/
c      data gsigs/10.72854/,gomes/13.29015/,grhos/3.66098/
c      data b_s/0.226061/,d_s/0.901995/
c      data b_v/0.172577/,d_v/0.983955/
c      data a_tv/0.515/
c      data dsat/0.153/
c---------------------------------------------------------------
c      data txtfor/'test'/
c      data amu/939.0/
c      data amsig/551.5867/,amome/783.000/,amrho/763.0/
c      data gsigs/10.4379/,gomes/12.8443/,grhos/3.8192/
c      data b_s/3.8933/,c_s/4.8405/
c      data b_v/0.8933/,c_v/0.9997/
c      data a_tv/0.5/
c      data dsat/0.152/
c---------------------------------------------------------------
c---- Coulomb-field: not at all (0), direct term (1), plus exchange (2)
      data icou/1/
c---------------------------------------------------------------
c
c
c---- pairing
c      data dec/5.0,5.0/
c      data del/5.0,5.0/
      data dec/0.0,0.0/
      data del/0.0,0.0/
      data ala/-7.0,-7.0/
      data ga/0.0,0.0/
c
c---- temperture
      data temp/0.0/
c
c---- parameters of the initial potentials
c     inin = 0: fields read, 1: default, 2: saxon-wood, 3:oscillator
      data inin/2/
c
c     Saxon-Woods parameter von Koepf und Ring, Z.Phys. (1991)
      data v0/-71.28/,akv/0.4616/
      data r0v/1.2334,1.2496/,av/0.615,0.6124/
      data vso/11.1175,8.9698/
      data rso/1.1443,1.1401/,aso/0.6476,0.6469/
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c          data v0/-71.28/,akv/0.4616/
c          data r0v/1.17,1.17/,av/0.75,0.75/
c	  data vso/14.5,14.5/
c       	  data rso/1.01,1.01/,aso/0.75,0.75/
ccccccccccccccccccccccccccccccccccccccccc
c---- Saxon-Woods parameter for test without Coulomb
c     data v0/-71.28/,akv/0.4616/
c     data r0v/1.2334,1.2334/,av/0.6150,0.6150/
c     data vso/11.1175,11.1175/
c     data rso/1.1443,1.1443/,aso/0.6476,0.6476/
c
c     data vin/-55.0/,rin/1.0/,qin/1.3/,ain/0.6/
c     Woods-Saxon Potential Dudek
c     data wsv0/-49.6/,wsv1/0.86/,wsr/1.347,1.275/,wsa/0.7/
c
c---- basis parameters:
c     number of major oscillator shells 
      data n0f/20/,n0b/20/
c     oscillator length b0 (is calcuated for b0 <= 0)
      data b0/-2.320/
c
c
c---- tapes
      data l6/10/,lin/3/,lou/6/,lwin/1/,lwou/2/,lplo/11/
c
c---- fixed texts
      data tp/'+','-'/,tis/'n','p'/
      data tl/'s','p','d','f','g','h','i','j','k','l','m',
     &            'n','o','P','q','r','S','t','u','v','w'/
c
c
c---- physical constants
      data hqc/197.328284d0/,r0/1.2/,alphi/137.03602/
c
c---- mathemathical constants
c     are determined in GFV
c      data zero/0.0d0/,one/1.d0/,two/2.d0/
c      data half/0.5d0/,third/0.333333333333333333d0/
c      data pi/3.141592653589793d0/
c
c
c---- fixed occupation patterns
c     O-16
c     data ioc/1,1,0,1,0,0,0,0,0,0, 32*0,
c    &         1,1,0,1,0,0,0,0,0,0, 32*0/
c
c     Pb-208
c     data ioc/3,3,2,3,2,2,1,2,1,1, 0,1,1,29*0,
c    &         3,2,2,2,2,1,1,1,1,0, 0,1,0,29*0/
c
c     GG-298
c      data ioc/4,3,3,3,3,2,2,2,2,1, 1,1,1,0,0,1,26*0,
c     &         3,2,2,3,2,2,1,2,1,0, 0,1,1,0,0,0,26*0/
c
c---- fields O-16 for NL1, ngh = 12
c      data sig/0.d0,
c     1 -.197896732795d+00, -.203336593050d+00, -.175178199706d+00,
c     2 -.110773903644d+00, -.492821497342d-01, -.155056088258d-01,
c     3 -.370467731601d-02, -.752571143561d-03, -.128392213020d-03,
c     4 -.178840524301d-04, -.123043868927d-06, -.138401023191d-05/
c      data ome/0.d0,
c     1  .122884775525d+00,  .128313360162d+00,  .111273919274d+00,
c     2  .678286964552d-01,  .271388311726d-01,  .717766421530d-02,
c     3  .140426026681d-02,  .243999373057d-03,  .378195438601d-04,
c     4  .312885710667d-05,  .507556868833d-06, -.331104601547d-06/
c      data rho/0.d0,
c     1 -.402717077863d-03, -.401598408644d-03, -.327222122144d-03,
c     2 -.134890782160d-03,  .226171401831d-04,  .537452482103d-04,
c     3  .302903348538d-04,  .103608532225d-04,  .228698677638d-05,
c     4  .197570927351d-06,  .514723017016d-07, -.380613801692d-07/
c      data cou/0.d0,
c     1  .280242732120d-01,  .268490299578d-01,  .243582917371d-01,
c     2  .209044213183d-01,  .173601945696d-01,  .143915626933d-01,
c     3  .121166187436d-01,  .103808124163d-01,  .901598395252d-02,
c     4  .790128300969d-02,  .694924512594d-02,  .607533630278d-02/
c
c-end-DEFAULT
      end






