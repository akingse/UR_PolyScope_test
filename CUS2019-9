# ----------------------------------------------------------------
# README
# version number:5
# creat time:2019/10/31
# editor: akingse
# design for:CUS2019-9
# procedure:take and put 1st,scan 1st,take n then scan n then pave n.
# keep the script order as below;
# initia()
# calcul()
# scandatum()# scanrevise()
# scantake()
# pavefetch()
# main()
# ----------------------------------------------------------------

# CUS2019-9
'''
initial
calculate
scandatum
takescan
--------
pave
takeback
main
'''
# ----------------------------------------------------------------------------------------------------------------------
def SubP_pave(): #pave 9 pieces
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
	if (i<2): #when pave 2 3;
		offset=p[0,-(i+1)*(width+gap),0,0,0,0]
    elif (i>=2 and i<5):  # when pave 4 5 6;
		offset=p[-(width+gap),-(i-2)*(width+gap),0,0,0,0]
	else: #(i>=5 and i<8), when pave 7 8 9;
        offset=p[-(width+gap),-(i-5)*(width+gap),0,0,0,0]
	end

	point_pave_above=pose_trans(point_centre,offset)
    point_pave = pose_trans(point_pave_above, delta_offset)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movel(pose_trans(point_pave,dropz),a=al,v=vl_erect) #pave,down
	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end

# ------------------------------------------------
def SubP_take_back(): #take back pave 9 pieces
	popup("Take_back_9", "message", False, False, blocking=True)
	while (i>5): #when take back 9 8 7; i=8,7,6
		global back_offset=p[-(width+gap),(6-i)*(width+gap),0,0,0,0]
		SubP_tack_back_action()
		i=i-1
	end
	set_standard_digital_out(6,True)
	set_standard_digital_out(5,True)
	sleep(9)
	if  get_standard_digital_in(0): #()== True
		while (i>=0):
			if (i>2):  #when take back 6 5 4;
				global back_offset=p[-(width+gap),(3-i)*(width+gap),0,0,0,0]
			else: #(i>0) #when take back 3 2 1;
				global back_offset=p[0,-i*(width+gap),0,0,0,0]
			end
			SubP_tack_back_action()
			i=i-1
		end
	end
end

def SubP_tack_back_action():
    point_take_back_above = pose_trans(point_centre, back_offset)
    movej(point_take_back_above, a=aj, v=vj_idle, r=r_nar)  # take,up
    offset = p[0, 0, dropz[2] + thickn/2, 0, 0, 0]
    movel(pose_trans(point_take_back_above, offset), a=al, v=vl_erect)  # take,down
    set_standard_digital_out(4, True)
    sleep(1)
    movel(point_take_back_above, a=al, v=vl_erect, r=r_wide)  # take,up
    movej(point_turn, a=aj, v=vj_load, r=r_wide)

    movej(point_take1, a=aj, v=vj_load, r=r_nar)  # back,up
    offset = p[0, 0, dropz[2] + i* thickn, 0, 0, 0]
    movel(pose_trans(point_take1, offset),a=al, v=vl_erect)  # back,down
    set_standard_digital_out(4, False)
    sleep(0.5)
    movel(point_take1, a=al, v=vl_erect)  # back,up
    movej(point_turn, a=aj, v=vj_idle)
end
# -------------------------------------------------------------------------------------
# main program; pave 9 pieces
global i = 0
SubP_initialize()
SubP_scan_datum()
calculate_datum(p_1, p_2, p_3, p_4)
while (i < 5): # 0,1,2,3,4,5
    SubP_scan_take()
    calculate_per(p_1, p_2, p_3, p_4)
    SubP_pave()
    i = i + 1
end

set_standard_digital_out(5,True)
sleep(9)
set_standard_digital_out(5,False)
while True:
    if (get_standard_digital_in(0)) and i==5:
        SubP_scan_datum()
        calculate_datum(p_1,p_2,p_3,p_4)
        while (i<8):
            SubP_scan_take()
            calculate_per(p_1,p_2,p_3,p_4)
            SubP_pave()
            i=i+1
        end
    end
    if i==8:
        break
    end
    sync()
end
SubP_take_back()
# ---------------------------------------------
'''# pave 12 pieces
set_standard_digital_out(5,True)
sleep(9)
set_standard_digital_out(5,False)
if get_standard_digital_in(0) and i==8:
	SubP_scan_datum()()
	calculate(p_1,p_2,p_3,p_4)
	while (i<11):
		SubP_take_scan()
		calculate(p_5,p_6,p_7,p_8)
		SubP_pave()
		i=i+1
	end
end

SubP_take_back()'''

'''
# old version, test error;
def SubP_pave_old(): #pave 6 pieces
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
	if (i<2): #when pave 2 3;
		offset=p[delta_offset[0],delta_offset[1]-(i+1)*(width+gap),0,0,0,delta_offset[5]]
	else: #(i<5)  when pave 4 5 6;
		offset=p[delta_offset[0]-(width+gap),delta_offset[1]-(i-2)*(width+gap),0.002,0,0,delta_offset[5]]
	end
    # offset=p[0,0,-(i+1)*thickn,0,0,0] #palletizing
    point_pave = pose_trans(point_centre, offset)
    movej(point_pave, a=aj,v=vj_idle,r=r_nar)  # pave,up
	movel(pose_trans(point_pave,dropz),a=al,v=vl_erect) #pave,down
	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end

'''
# ------------------------------------------------------------------------------------------------------------------

def SubP_scan_datum(): #without break version;
    if i==0: #put the first tile;
        movej(point_turn, a=aj, v=vj_idle, r=r_wide)
        movej(point_take1, a=aj, v=vj_idle, r=r_nar)  # take,up
        movel(pose_trans(point_take1, dropz), a=al, v=vl_erect)  # take,down
        set_standard_digital_out(4, True)
        sleep(1)
        movel(point_take1, a=al, v=vl_erect, r=r_nar)  # take,up
        movej(point_turn, a=aj, v=vj_idle, r=r_wide)  # --------------------
        movej(point_pave1, a=aj, v=vj_idle, r=r_nar)  # pave,up
        movel(pose_trans(point_pave1, dropz), a=al, v=vl_erect)  # pave,down
        set_standard_digital_out(4, False)
        sleep(0.5)
        movel(point_pave1, a=al, v=vl_erect)  # pave,up
    end


    global scanh1=0.063
    global point_scan=p[0.915, -0.130, scanh1, pi, 0, 0]  # p1
    movej(point_scan, a=aj, v=vj_idle)
    move_scan_max()
    global p_1=p_0
    point_scan = p[0.715, -0.130, scanh1, pi, 0, 0]  # p2
    movej(point_scan, a=aj, v=vj_idle)
    move_scan_max()
    global p_2=p_0
    point_scan = p[0.690, -0.100, scanh1, pi, 0, 0]  # p3
    movej(point_scan, a=aj, v=vj_idle)
    move_scan_max()
    global p_3=p_0
    point_scan = p[0.690, 0.100, scanh1, pi, 0, 0]  # p4
    movej(point_scan, a=aj, v=vj_idle)
    move_scan_max()
    global p_4=p_0
end

def move_scan_max():
    catching=run catch_point()
    if (point_scan[1] == -0.130):  # line1,p1 p2
        offset = p[0, 0.050, 0, 0, 0, 0]
    elif (point_scan[0] == 0.690):  # line2,p3 p4
        offset = p[-0.050, 0, 0, 0, 0, 0]
    end
    point_scan_max = pose_trans(point_scan, offset)
    movel(point_scan_max, a=al, v=vl_scan)
    kill catching
end

thread catch_point():
    while (True):
        if (get_standard_digital_in(1) == False):
            global p_0 = get_actual_tcp_pose()
            break
        end
        sync()
    end
end

# ------------------------------------------------------------------------------------------------------------------
def SubP_scan_take():
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
	movej(point_take1,a=aj,v=vj_idle,r=r_nar) #take,up
	offset=p[0,0,dropz[2]+(i+1)*thickn,0,0,0]
	point_take=pose_trans(point_take1,offset)
	movel(point_take,a=al,v=vl_erect)  #take,down
	set_standard_digital_out(4,True)
	sleep(1)  #wait the suker grip the tile;
	movel(point_take1,a=al,v=vl_erect)  #take,up

	global scanh2=0.360
	point_scan=p[0.350,0.080,scanh2,pi,0,0] #p1
	movej(point_scan,a=aj,v=vj_idle)
    move_scan_max2()
	global p_1=p_0
	point_scan=p[0.501,0.080,scanh2,pi,0,0] #p2
	movej(point_scan,a=aj,v=vj_idle)
    move_scan_max2()
    global p_2=p_0
	point_scan=p[0.500,0.081,scanh2,pi,0,0] #p3
	movej(point_scan,a=aj,v=vj_idle)
	move_scan_max2()
	global p_3=p_0
	point_scan=p[0.500,-0.110,scanh2,pi,0,0] #p4
	movej(point_scan,a=aj,v=vj_idle)
	move_scan_max2()
	global p_4=p_0
end


def move_scan_max2():
    catching2=run catch_point2()
    if (point_scan[1] == 0.080):  # line1,p1 p2
        offset = p[0, -0.050, 0, 0, 0, 0]
    elif (point_scan[0] == 0.500):  # line2,p3 p4
        offset = p[0.050, 0, 0, 0, 0, 0]
    end
    point_scan_max = pose_trans(point_scan, offset)
    movel(point_scan_max, a=al, v=vl_scan)
    kill catching2
end

thread catch_point2():
    while (True):
        if (get_standard_digital_in(2) == False):
            global p_0 = get_actual_tcp_pose()
            break
        end
        sync()
    end
end

