subroutine arrraw(seedcsv,xs,xe,xm,ys,ye,ym,zs,ze,zm,focus,dupnum,phasereverse,&
        & patternsize,intnum,randomseed,intmax,spd,seedtxt,basetxt,plotcsv)
    implicit none
    integer :: i,j,k,rnum,n2
    integer :: cut,nextn,n,dx,dy,dz,dup_t,dup_arr_t
    real :: x,y,z,trans,phase,NA,r,wide,t_size
    integer, intent(in) :: xm,ym,zm,phasereverse,randomseed,spd
    real, intent(in) :: xs,xe,ys,ye,zs,ze,focus,dupnum,intnum,patternsize,intmax
    character(*), intent(in) :: seedcsv,seedtxt,plotcsv,basetxt
    real(4), dimension(xm,ym,zm) :: arr 
    integer(4), dimension(xm,ym) :: dup_arr
    integer :: seedsize
    integer, allocatable:: seed(:)
    character,parameter :: seedfmt*38='(a,2f11.6,2f6.2,f11.6,f9.3,f11.6,f9.5)'
    character(4) :: rect
    character,parameter :: csvfmt*25='(a,a,a,a,a,a,a,a,a,a,a,a)'
    !arr_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (16, file=seedtxt, status='replace') 
    open (18, file=basetxt, status='replace')
    call random_seed(size=seedsize)  ! シードの格納に必要なサイズを取得する
    allocate(seed(seedsize))         ! シード格納領域を確保
    seed=randomseed
    call random_seed(put=seed) 
    t_size = real(patternsize / 2)
    open (17, file=seedcsv, status='old') 
    n = 0

    read (17, '()')
    do 
        read ( 17, *, end =100)x,y,z,trans,wide
        n = n + 1
    enddo
100 continue
    rewind (17)
    read (17, '()')

    do i = 1, n
        read (17, *) x,y,z,trans,wide
        dx=digtxy(x,t_size,xs,xe,xm)
        dy=digtxy(y,t_size,ys,ye,ym)
        dz=digtz(z,zs,ze,zm)
        arr(dx,dy,dz) = 1
    enddo
    close(17)
    n2 = 0
    dup_arr = 0
    do k  = zm, 1, -1
        do i = 1, xm
            do j = 1, ym

                if (arr(i,j,k) /= 0) then
                    dup_t = dup_arr(i,j)
                    dup_arr(i,j) = dup_t + 1
                    n2 = n2 + 1
                    dup_arr_t = dup_arr(i,j)
                    if (mod(n2,spd) == 0 )then
                        x = xs + i*(xe-xs)/(xm-1)
                        y = ys + j*(ye-ys)/(ym-1)
                        z = (-1)*ze + (zm-k)*(ze-zs)/(zm-1)
                        trans = intfct(z,intnum,dupnum,dup_arr_t,intmax)
                        call random_number(r)
                        rnum = int(r*100)+1
                        phase = phasefct(z-focus,rnum,phasereverse)
                        NA = NAfct(z-focus,xe-xs)
                        write(16,seedfmt)"rect",x,y,patternsize,patternsize,trans,phase,z,NA

                    print *,n2  
                    end if
                end if    
            enddo
        enddo
    enddo
    close(16)

    call random_seed(put=seed) 

    dup_arr = 0
    do k  = zm, 1, -1
        do i = 1, xm
            do j = 1, ym

                if (arr(i,j,k) /= 0) then
                    dup_t = dup_arr(i,j)
                    dup_arr(i,j) = dup_t + 1
                    dup_arr_t = dup_arr(i,j)
                    x = xs + i*(xe-xs)/(xm-1)
                    y = ys + j*(ye-ys)/(ym-1)
                    z = (-1)*ze + (zm-k)*(ze-zs)/(zm-1)
                    trans = intfct(z,intnum,dupnum,dup_arr_t,intmax)
                    call random_number(r)
                    rnum = int(r*100)+1
                    phase = phasefct(z-focus,rnum,phasereverse)
                    NA = NAfct(z-focus,xe-xs)
                    write(18,seedfmt)"rect",x,y,patternsize,patternsize,trans,phase,z,NA
                end if    
            enddo
        enddo
    enddo
    close(18)




    open (15, file=seedtxt, status='old') 
    open (14, file=plotcsv, status='replace') 
    rewind (15)
    n = 0
    do 
        read ( 15, *, end =101)rect,x,y,wide,wide,trans,phase,z,NA
        n = n + 1
    enddo
101 continue
    cut = 1
    nextn = n
    do while (nextn >30000)
        nextn = nextn/2
        cut = cut + 1
    enddo
    rewind (15)
    write(14,csvfmt)"x",",","y",",","z",",","int",",","phase",",","size"
    do i = 1, n
        read (15, *) rect,x,y,wide,wide,trans,phase,z,NA
        if (mod(i,cut**2) == 0) then
            write(14,*)x,",",y,",",z,",",trans,",",phase,",",1
        end if
    enddo
    close(14)
    close(15)

    contains

    function digtxy(c1,size,xystart,xyfi, mult) result(digtnum)
        implicit none
        integer :: mult,digtnum
        real :: c1, xystart, xyfi
        real :: width, c2, size
        width = real(xyfi - xystart)/real(mult - 1) 
        c2 = c1 + size - xystart
        digtnum = int(c2 / width )+1
        return
    end function digtxy

    function digtz(cz,zstart,zfi, mult) result(digtnum)
        implicit none
        integer :: mult,digtnum
        real :: cz, zstart, zfi
        real :: width
        width = real(zfi - zstart)/real(mult - 1)
        digtnum = int((mult-1)- cz / (width) )+1 
        return
    end function digtz


    function phasefct(c1,num,reversenum) result(phase)
        implicit none
        integer :: num,reversenum,sho
        real :: c1, lamda
        real :: phase,phasea
        lamda = 0.365
        phasea = 360*c1/lamda
        if (mod(num,reversenum) /= 0) then
            phasea = phasea + 180
        end if
        sho = int(phasea/360)
        phase = phasea - 360*sho
        return
    end function phasefct

    function intfct(cz,intpara,duppara,doublenum,transmax) result(trans)
        implicit none
        real :: cz, intpara,duppara,transmax,trans
        integer :: doublenum
        trans = transmax - cz * intpara + duppara * doublenum
        return
    end function intfct

    function NAfct(cz,field) result(NA)
        implicit none
        real :: cz, NA,field
        if (cz == 0) then
            NA = 1
        end if
        if (cz /= 0) then
            NA = sin(field/(2*cz))
        end if
        return
    end function NAfct



    end subroutine arrraw


    subroutine output2improve(arr,firstseed,beforeseed,afterseed,xi,yi,zi,xs,xe,ys,ye,zs,ze,internum,zmp,minus_th,plus_th, &
        &                     f_plus,f_minus,impnum,focus,dupnum,patternsize,sp1,sp2,decnum,phasereverse,randomseed &
        &                     ,paralist,listlen,eva_csv,arr_csv,pointcut)
    implicit none
    integer :: i,j,k,p1,p2,p3,u,rnum
    integer :: n,dx,dy,dz,interx,intery,interz
    integer :: pn,dc1,dc2,dc3
    !integer :: sign
    real :: x,y,z,wide,trans,phase,NA,r,temp,tempf,temp_phase,t_size
    real, intent(in) :: xs,xe,ys,ye,zs,ze,minus_th,plus_th,f_plus,f_minus
    real, intent(in) :: focus,dupnum,patternsize,sp1,sp2,decnum
    real(4), dimension(listlen), intent(out) :: paralist
    real :: a,b,c,d,e,f,g,h
    real :: X1,X2,X3,X4,Y1,Y2,Z1
    real :: arrmax,arrmin
    integer, intent(in) :: xi,yi,zi,internum,zmp,impnum,phasereverse,randomseed,listlen,pointcut
    character(4):: rect
    real(4), dimension(xi,yi,zi), intent(in) :: arr 
    character(*), intent(in) :: firstseed
    character(*), intent(in) :: beforeseed
    character(*), intent(in) :: afterseed
    character(*), intent(in) :: eva_csv,arr_csv
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrinter 
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrinter_nor
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrfirst
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrbefore
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arreva
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arreee
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrimp
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrfirst_amp
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1) :: arrbefore_phase

    integer :: seedsize
    integer, allocatable:: seed(:)
    character,parameter :: seedfmt*38='(a,2f11.6,2f6.2,f11.6,f9.3,f11.6,f9.5)'
    character,parameter :: csvfmt*21='(a,a,a,a,a,a,a,a,a,a)'
    arrinter = 0
    arrinter_nor = 0
    arrfirst = 0
    arrbefore = 0
    arreva = 0
    arreee= 0
    arrimp = 0
    arrfirst_amp = 0
    arrbefore_phase = 0

    t_size = real(patternsize / 2)
    
    !interpolate
    interx=(xi-1)*internum+1
    intery=(yi-1)*internum+1
    interz=(zi-1)*zmp+1
    do i = 1,xi-1
        do j = 1,yi-1
            do k = 1,zi-1
                a = arr(i,j,k)
                b = arr(i+1,j,k)
                c = arr(i+1,j+1,k)
                d = arr(i,j+1,k)
                e = arr(i,j,k+1)
                f = arr(i+1,j,k+1)
                g = arr(i+1,j+1,k+1)
                h = arr(i,j+1,k+1)
                do p1 = 0,internum
                    X1=a+p1*(b-a)/internum
                    X2=d+p1*(c-d)/internum
                    X3=e+p1*(f-e)/internum
                    X4=h+p1*(g-h)/internum
                    do p2 = 0,internum
                            Y1=X1+p2*(X2-X1)/internum
                            Y2=X3+p2*(X4-X3)/internum
                            do p3 = 0,zmp
                                Z1=Y1+p3*(Y2-Y1)/zmp
                                arrinter(1+(i-1)*internum+p1,1+(j-1)*internum+p2,1+(k-1)*zmp+p3) = Z1
                            enddo
                        enddo
                    enddo 
            enddo
        enddo    
    enddo
    !normalization
    arrmax = maxval(arrinter)
    arrmin = minval(arrinter)
    

    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                arrinter_nor(i,j,k) = (arrinter(i,j,k)-arrmin) / (arrmax - arrmin)
            enddo
        enddo
    enddo

    !firstseed2arr
    open (18, file=firstseed, status='old') 
    n = 0
    read (18, '()')
    do 
        read ( 18, *, end =102)rect,x,y,wide,wide,trans,phase,z,NA
        n=n+1
    enddo
102 continue
    rewind (18)
    read (18, '()')
    do i = 1, n
        read (18, *)rect,x,y,wide,wide,trans,phase,z,NA
        dx=digtxy(x,t_size,xs,xe,interx)
        dy=digtxy(y,t_size,ys,ye,intery)
        dz=digtz(z,zs,ze,interz)
        arrfirst(dx,dy,dz) = 1
    enddo
    close(18)
    !beforeseed2arr
    open (19, file=beforeseed, status='old') 
    n = 0
    read (19, '()')
    do 
        read ( 19, *, end =103)rect,x,y,wide,wide,trans,phase,z,NA
        n=n+1
    enddo
103 continue
    rewind (19)
    read (19, '()')
    do i = 1, n
        read (19, *)rect,x,y,wide,wide,trans,phase,z,NA
        dx=digtxy(x,t_size,xs,xe,interx)
        dy=digtxy(y,t_size,ys,ye,intery)
        dz=digtz(z,zs,ze,interz)
        arrbefore(dx,dy,dz) = trans
        arrbefore_phase(dx,dy,dz) = phase
    enddo
    close(19)

    !arreva_crate
    arreva = -50
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arrfirst(i,j,k) < 0.1) then 
                    if (arreva(i,j,k) < -5)then
                        arreva(i,j,k) = -30
                    end if
                end if
                if (arrfirst(i,j,k) > 0.1) then 
                    do pn= 30,0,-1
                        ! sign = 1
                        ! if (pn>=5) then
                        !     sign=-1
                        ! end if
                        do p1 = (-1)*pn,pn,1
                            do p2 = (-1)*pn,pn,1
                                do p3 = (-1)*pn,pn,1
                                    dc1= dc(i+p1,interx)
                                    dc2= dc(j+p2,intery)
                                    dc3= dc(k+p3,interz)
                                    if (pn <= 1) then
                                        arrfirst_amp(dc1,dc2,dc3) = 1
                                    end if
                                    if (arreva(dc1,dc2,dc3) < 10 - pn  )then
                                        arreva(dc1,dc2,dc3)= 10 -pn
                                    end if
                                enddo
                            enddo
                        enddo
                    enddo



                end if
            enddo
        enddo
    enddo        
    !arreee_crate
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arrinter_nor(i,j,k)>minus_th) then
                    arreee(i,j,k)=arreva(i,j,k)
                end if
            enddo
        enddo
    enddo

    !arrimp_crate
    arrimp=arrbefore
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arrfirst_amp(i,j,k)>0.1) then

                    if (arrinter_nor(i,j,k) < minus_th) then 
                        arrimp(i,j,k) =arrbefore(i,j,k) +(1-arrinter_nor(i,j,k))*f_plus/real(impnum)
                    end if

                    ! if (arrimp(i,j,k) > plus_th) then
                    !     if (arrinter_nor(i,j,k) > plus_th) then 
                    !         arrimp(i,j,k) =arrbefore(i,j,k) +(-1)*arrinter_nor(i,j,k)*f_minus/real(impnum)
                    !     end if
                    ! end if

                    
                    ! if (arrfirst(i,j,k) > 0.1) then
                    !     if (arrinter_nor(i,j,k) > plus_th) then 
                    !         arrimp(i,j,k) =arrbefore(i,j,k) +(-1)*arrinter_nor(i,j,k)*f_minus/real(impnum)
                    !     end if
                    ! end if
                end if
                if (arrfirst_amp(i,j,k)<0.1) then
                    if (arrinter_nor(i,j,k) > minus_th) then 
                        arrimp(i,j,k) =arrbefore(i,j,k) +(-1)*arrinter_nor(i,j,k)*f_minus/real(impnum)
                    end if
                end if
            enddo
        enddo
    enddo        

    !improve_seed_crate

    open (29, file=afterseed, status='replace') 
    call random_seed(size=seedsize)  ! シードの格納に必要なサイズを取得する
    allocate(seed(seedsize))         ! シード格納領域を確保
    seed=randomseed
    call random_seed(put=seed) 
    do i = 1, interx
        do j = 1, intery
            u = -1
            do k  = interz, 1, -1
                temp = arrimp(i,j,k)
                temp_phase =  arrbefore_phase(i,j,k)
    !                tempf=arrfirst_amp(i,j,k)
                if (temp /= 0) then
                    u = u +1
                    x = xs + i*(xe-xs)/(interx-1)
                    y = ys + j*(ye-ys)/(intery-1)
                    z = (-1)*ze + (interz-k)*(ze-zs)/(interz-1)
                    trans = temp
    !                    trans = intfctimp(temp,tempf,dupnum,u,sp1,sp2,decnum)
                    if (temp_phase /= 0) then
                        phase = temp_phase
                    end if
                    if (temp_phase == 0) then
                        call random_number(r)
                        rnum = int(r*100)+1
                        phase = phasefct(z-focus,rnum,phasereverse)
                    end if
                    NA = NAfct(z-focus,xe-xs)
                    write(29,seedfmt)"rect",x,y,patternsize,patternsize,trans,phase,z,NA
                end if    
            enddo
        enddo
    enddo
    close(29)

    !paramaterget
    paralist = 0
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arrfirst_amp(i,j,k)>0.1) then
                    paralist(1)=paralist(1)+1
                    if (arrinter_nor(i,j,k)>minus_th)then
                        paralist(3)=paralist(3)+1
                    end if
                    if (paralist(5)<(arrfirst_amp(i,j,k)-arrinter_nor(i,j,k)))then
                        paralist(5)=arrfirst_amp(i,j,k)-arrinter_nor(i,j,k)
                    end if
                end if
                if (arrfirst_amp(i,j,k)<0.1) then
                    paralist(2)=paralist(2)+1
                    if (arrinter_nor(i,j,k)<minus_th)then
                        paralist(4)=paralist(4)+1
                    end if
                    if (paralist(6)>(arrfirst_amp(i,j,k)-arrinter_nor(i,j,k)))then
                        paralist(6)=arrfirst_amp(i,j,k)-arrinter_nor(i,j,k)
                    end if
                end if

            enddo
        enddo
    enddo     
    !siguma
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arreee(i,j,k)>0) then
                    paralist(7)=paralist(7)+arreee(i,j,k)
                end if
                if (arreee(i,j,k)<0) then
                    paralist(8)=paralist(8)+arreee(i,j,k)
                end if

            enddo
        enddo
    enddo         

    !arreee_graphic_arreee

    open (20, file=eva_csv, status='replace') 
    write(20,csvfmt)"x",",","y",",","z",",","int",",","size"
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arreee(i,j,k) /=0) then
                    x = xs + i*(xe-xs)/(interx-1)
                    y = ys + j*(ye-ys)/(intery-1)
                    z = (-1)*ze + (interz-k)*(ze-zs)/(interz-1)
                    trans = arreee(i,j,k)
                    write(20,*)x,",",y,",",z,",",trans,",",1
                end if    
            enddo
        enddo
    enddo
    close(20)

    open (13, file=arr_csv, status='replace') 
    write(13,csvfmt)"x",",","y",",","z",",","int",",","size"
    do i = 1,interx
        do j = 1,intery
            do k = 1,interz
                if (arrinter_nor(i,j,k) > real(1)/real(pointcut)) then
                    x = xs + i*(xe-xs)/(interx-1)
                    y = ys + j*(ye-ys)/(intery-1)
                    z = (-1)*ze + (interz-k)*(ze-zs)/(interz-1)
                    trans = arrinter_nor(i,j,k)
                    write(13,*)x,",",y,",",z,",",trans,",",1
                end if    
            enddo
        enddo
    enddo
    close(13)



    contains
    function phasefct(c1,num,reversenum) result(phase)
        implicit none
        integer :: num,reversenum,sho
        real :: c1, lamda
        real :: phase,phasea
        lamda = 0.365
        phasea = 360*c1/lamda
        if (mod(num,reversenum) /= 0) then
            phasea = phasea + 180
        end if
        sho = int(phasea/360)
        phase = phasea - 360*sho
        return
    end function phasefct

    ! function intfctimp(intensity,seedi,duppara,doublenum,stoptrans1,stoptrans2,decnum) result(trans)
    !     implicit none
    !     real :: intensity,seedi,duppara,trans,stoptrans1,stoptrans2,decnum
    !     integer :: doublenum
    !     trans = intensity + duppara * doublenum
    !     if (seedi == 0) then
    !         if (intensity<stoptrans1)then
    !             trans = intensity + duppara * doublenum * decnum
    !         end if
    !     end if
    !     if (seedi /= 0) then 
    !         if (intensity>stoptrans2)then
    !             if (trans<stoptrans1)then
    !                 trans = intensity + duppara * doublenum * decnum
    !             end if
    !         end if
    !     end if 
    !     return
    ! end function intfctimp

    function NAfct(cz,field) result(NA)
        implicit none
        real :: cz, NA,field
        if (cz == 0) then
            NA = 1
        end if
        if (cz /= 0) then
            NA = sin(field/(2*cz))
        end if
        return
    end function NAfct

    function digtxy(c1,size,xystart,xyfi, mult) result(digtnum)
        implicit none
        integer :: mult,digtnum
        real :: c1, xystart, xyfi
        real :: width, c2, size
        width = real(xyfi - xystart)/real(mult - 1) 
        c2 = c1 + size - xystart
        digtnum = int(c2 / width )+1
        return
    end function digtxy

    function digtz(cz,zstart,zfi, mult) result(digtnum)
        implicit none
        integer :: mult,digtnum
        real :: cz, zstart, zfi
        real :: width
        width = real(zfi - zstart)/real(mult - 1)
        digtnum = int((mult-1)- cz / (width) )+1 
        return
    end function digtz


    function dc(c1,c2) result(dd)
        implicit none
        integer :: c1,c2,dd
        dd = c1
        if (c1>=c2) then
            dd = c2
        end if 
        if (c1<=1) then
            dd = 1
        end if

        return
    end function dc


    end subroutine output2improve


    subroutine arr2normalization(arr,xi,yi,zi,arr_nor)
    implicit none
    integer, intent(in) :: xi,yi,zi
    real :: arrmax, arrmin
    real(4), dimension(xi,yi,zi), intent(in) :: arr 
    real(4), dimension(xi,yi,zi), intent(out) :: arr_nor

    arrmax = maxval(arr)
    arrmin = minval(arr)
    arr_nor = (arr-arrmin) / (arrmax - arrmin)

    end subroutine arr2normalization



    subroutine txt2csv_for_seed(seedtxt,seedcsv)
    implicit none
    integer :: i,cut,next,n
    real :: x,y,z,trans,phase,NA,size
    character(*), intent(in) :: seedtxt
    character(*), intent(in) :: seedcsv
    character(4) :: rect
    character,parameter :: fmt*25='(a,a,a,a,a,a,a,a,a,a,a,a)'
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (28, file=seedtxt, status='old') 
    open (27, file=seedcsv, status='replace') 
    n = 0
    do 
        read ( 28, *, end =110)rect,x,y,size,size,trans,phase,z,NA
        n = n + 1
    enddo
110 continue
    cut = 1
    next = n
    do while (next >30000)
        next = next/2
        cut = cut +1
    enddo
    rewind (28)
    write(27,fmt)"x",",","y",",","z",",","int",",","phase",",","size"
    do i = 1, n
        read (28, *) rect,x,y,size,size,trans,phase,z,NA
        if (mod(i,cut**2) == 0) then
            write(27,*)x,",",y,",",z,",",trans,",",phase,",",1
        end if
    enddo
    close(27)
    close(28)
    print *, n
    print *, cut
    print *, next

    end subroutine txt2csv_for_seed


    subroutine arr2csv(arr,xs,xe,xm,ys,ye,ym,zs,ze,zm,arrmax,g_csv,pointcut)
    implicit none
    integer :: i,j,k
    real :: x,y,z,trans
    integer, intent(in) :: xm,ym,zm
    real, intent(in) :: xs,xe,ys,ye,zs,ze,arrmax,pointcut
    character(*), intent(in) :: g_csv
    real(4), dimension(xm,ym,zm), intent(in) :: arr 
    character,parameter :: fmt*21='(a,a,a,a,a,a,a,a,a,a)'
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (26, file=g_csv, status='replace') 
    write(26,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1, xm
        do j = 1, ym
            do k  = 1, zm
                if (arr(i,j,k) > arrmax/pointcut) then
                    x = xs + i*(xe-xs)/(xm-1)
                    y = ys + j*(ye-ys)/(ym-1)
                    z = (-1)*ze + (zm-k)*(ze-zs)/(zm-1)
                    trans = arr(i,j,k)
                    write(26,*)x,",",y,",",z,",",trans,",",1
                end if    
            enddo
        enddo
    enddo
    close(26)

    end subroutine arr2csv



    subroutine csv2plot(g_csv,plotcsv)
    implicit none
    integer :: i,cut,next,n
    real :: x,y,z,trans,size
    character(*), intent(in) :: g_csv
    character(*), intent(in) :: plotcsv 
    character,parameter :: fmt*21='(a,a,a,a,a,a,a,a,a,a)'
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (12, file=g_csv, status='old') 
    open (11, file=plotcsv, status='replace') 
    n = 0
    read (12, '()')
    do 
        read ( 12, *, end =111)x,y,z,trans,size
        n = n + 1
    enddo
111 continue
    cut = 1
    next = 0
    next = n
    do while (next >30000)
        next = next/2
        cut = cut +1
    enddo
    rewind (12)
    read (12, '()')
    write(11,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1,n
        read (12, *) x,y,z,trans,size
        if (mod(i,cut**2) == 0) then
            write(11,*)x,",",y,",",z,",",trans,",",1
        end if
    enddo
    close(11)
    close(12)


    end subroutine csv2plot



    subroutine csv2plot_minus(g_csv,plotcsv)
    implicit none
    integer :: i,cut,nextn,n,p1
    real :: x,y,z,trans,size
    character(len=13) :: tempfile = "eva_minus.csv"
    character(*), intent(in) :: g_csv
    character(*), intent(in) :: plotcsv 
    character,parameter :: fmt*21='(a,a,a,a,a,a,a,a,a,a)'
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (21, file=g_csv, status='old') 
    open (22, file=plotcsv, status='replace') 
    open (30, file=tempfile, status='replace')    
    p1 = 0
    n = 0
    read (21, '()')
    do 
        read ( 21, *, end =105)x,y,z,trans,size
        n=n+1
    enddo
105 continue

    rewind (21)
    read (21, '()')
    write(30,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1, n
        read (21, *) x,y,z,trans,size
        if (trans<0)then
            write(30,*)x,",",y,",",z,",",trans,",",1
            p1 = p1 + 1
        end if
    enddo
    close(21)
    close(30)
    open (30, file=tempfile, status='old')   
    rewind (30)
    cut = 1
    nextn = n
    do while (nextn >30000)
        nextn = nextn/2
        cut = cut +1
    enddo
    rewind (30)
    read (30, '()')
    write(22,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1,p1
        read (30, *) x,y,z,trans,size
        if (mod(i,cut**2) == 0) then
            write(22,*)x,",",y,",",z,",",trans,",",1
        end if

    enddo
    close(22)
    close(30)

    end subroutine csv2plot_minus


    subroutine csv2plot_plus(g_csv,plotcsv)
    implicit none
    integer :: i,cut,nextn,n,p1
    real :: x,y,z,trans,size
    character(len=12) :: tempfile = "eva_plus.csv"
    character(*), intent(in) :: g_csv
    character(*), intent(in) :: plotcsv 
    character,parameter :: fmt*21='(a,a,a,a,a,a,a,a,a,a)'
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    open (23, file=g_csv, status='old') 
    open (24, file=plotcsv, status='replace') 
    open (31, file=tempfile, status='replace')    
    n = 0
    p1 = 0
    read (23, '()')
    do 
        read ( 23, *, end =106)x,y,z,trans,size
        n = n + 1
    enddo
106 continue
    rewind (23)
    read (23, '()')
    write(31,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1, n
        read (23, *) x,y,z,trans,size
        if (trans>=0)then
            write(31,*)x,",",y,",",z,",",trans,",",1
            p1 = p1 + 1
        end if
    enddo
    close(23)
    close(31)
    open (31, file=tempfile, status='old')  
    rewind (31)  
    cut = 1
    nextn = p1
    do while (nextn >30000)
        nextn = nextn/2
        cut = cut +1
    enddo
    read (31, '()')
    write(24,fmt)"x",",","y",",","z",",","int",",","size"
    do i = 1, p1
        read (31, *) x,y,z,trans,size
        if (mod(i,cut**2) == 0) then
            write(24,*)x,",",y,",",z,",",trans,",",1
        end if 
    enddo
    close(31)
    close(24)

    end subroutine csv2plot_plus

    subroutine interpolate(qq,xi,yi,zi,internum,zmp,qq_add)
    implicit none
    integer :: i,j,k,p1,p2,p3
    real :: a,b,c,d,e,f,g,h
    real :: X1,X2,X3,X4,Y1,Y2,Z
    integer, intent(in) :: xi,yi,zi,internum,zmp
    real(4), dimension(xi,yi,zi), intent(in) :: qq 
    real(4), dimension((xi-1)*internum+1,(yi-1)*internum+1,(zi-1)*zmp+1),intent(out) :: qq_add 
    !qq_add(::internum,::internum,::zmp) = qq(:,:,:)
    do i = 1,xi-1
        do j = 1,yi-1
            do k = 1,zi-1
                a = qq(i,j,k)
                b = qq(i+1,j,k)
                c = qq(i+1,j+1,k)
                d = qq(i,j+1,k)
                e = qq(i,j,k+1)
                f = qq(i+1,j,k+1)
                g = qq(i+1,j+1,k+1)
                h = qq(i,j+1,k+1)
                do p1 = 0,internum
                    X1=a+p1*(b-a)/internum
                    X2=d+p1*(c-d)/internum
                    X3=e+p1*(f-e)/internum
                    X4=h+p1*(g-h)/internum
                    do p2 = 0,internum
                        Y1=X1+p2*(X2-X1)/internum
                        Y2=X3+p2*(X4-X3)/internum
                        do p3 = 0,zmp
                            Z=Y1+p3*(Y2-Y1)/zmp
                            qq_add(1+(i-1)*internum+p1,1+(j-1)*internum+p2,1+(k-1)*zmp+p3) = Z
                        enddo
                    enddo
                enddo 
            enddo
        enddo    
    enddo

    return
end subroutine interpolate