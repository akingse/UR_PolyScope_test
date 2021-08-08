# ----------------------------------------------------------------
# README
# version number:URtest5
# create time:2019/10/31
# editor: akingse
# design for:CUS2019-6
# procedure:take and put 1st,scan 1st,take n then scan n then pave n.
# keep the script order as below;
# initia()
# calcul()
# scandatum()
# scantake()
# pavefetch()
# main()
# ----------------------------------------------------------------

def SubP_initialize():
    set_standard_digital_out(4, False)  # close the vacuum valve;
    set_standard_digital_out(5, False)  # control the AGV;
    set_standard_digital_out(6, False)  # the flag of AGV direction;
    # get_standard_digital_in(1) # the laser1,place in TCP;(Tool Center Point)
    # get_standard_digital_in(2) # the laser2,place in AGV;(Automated Guided Vehicle)

    global pi = 3.141593  # the circumference radio;
    global width = 0.300  # the width of ceramic tile,unit is meter;
    global thickn = 0.0088  # the thickness of ceramic tile;
    global gap = 0.005  # the gap between two adjoining tiles;
    global dropz = p[0, 0, 0.050, 0, 0, 0]
    global x_laser1 = 0.178  # west(right) toward forward; depend on TCP pose;
    global y_laser1 = -0.009  # north toward forward;
    global x_laser2 = 0.0015 #same direction
    global y_laser2 = 0.0045
    # movel(m/sˆ2,m/s),movej(rad/sˆ2,rad/s),high speed version;
    global vl_scan = 0.05  # the scan velocity;
    global vl_erect = 0.20  # the up and down velocity;
    global vj_idle = 1.0  # the none load velocity;
    global vj_load = 0.6  # the tile load velocity;
    global al = 1.20  # the unified line acceleration;
    global aj = 1.40  # the joint radian acceleration;
    global r_wide = 0.050  # the blend radius when used in wide range;
    global r_nar = 0.010  # the blend radius when used in narrow range

    # the upper point when take first; point_take1_touch[2]==0.206;
    global point_take1 = p[0.077, 0.595, 0.258, pi, 0, 0] #point_above;
    # the upper point when pave first; point_pave1_touch[2]==-0.183;
    global point_pave1 = p[0.990, 0.0, -0.135, pi, 0, 0] #point_above;
    # the transition point that above 5th tile;
    global point_turn = p[0.690, 0.300, 0.250, pi, 0, 0]
    # the installation position of laser2;
    global point_laser2 = p[0.391, -0.034, 0.300, pi, 0, 0]
end
# ----------------------------------------------------------------------------------------------------------------------

def calculate_datum(a, b, c, d):
    if (p_3[0] == p_4[0]):  # when line_2 is perpendicular to x axis;
        popup("line_2 is perpendicular to X",title="error",warning=False,error=True)
        halt
    else:
        k_1 = (p_2[1] - p_1[1]) / (p_2[0] - p_1[0])
        k_2 = (p_4[1] - p_3[1]) / (p_4[0] - p_3[0])
        theta_1 = atan(k_1) #to be monitor;
        theta_2 = atan(k_2)
        global angle1 = r2d(theta_1)
        global angle2 = r2d(theta_2)
        if norm(norm(angle1 - angle2) - 90) > 1:
            popup("angle12_over_range",title="error",warning=False,error=True)#
            halt
        end
        x_0 = (k_1 * p_1[0] - k_2 * p_3[0] + p_3[1] - p_1[1]) / (k_1 - k_2)
        y_0 = k_1 * (x_0 - p_1[0]) + p_1[1]
        global cp_rz=0
        if (k_1 > 0) and (k_2 < 0):
            cp_rz = (theta_1 + theta_2 + pi / 2) / 2
        elif (k_1 < 0) and (k_2 > 0):
            cp_rz = (theta_1 + theta_2 - pi / 2) / 2
        else:
            cp_rz = 0
        end
    end
    point_lines_cross = p[x_0, y_0, scanh1, pi, 0, 0]
    offset = p[x_laser1, y_laser1, 0, 0, 0, -cp_rz]
    point_cross_tcp = pose_trans(point_lines_cross, offset)
    offset = p[width / 2, -width / 2, scanh1 - point_pave1[2], 0, 0, 0]  # 0.063+0.133=0.196
	global point_centre = pose_trans(point_cross_tcp, offset)

end

# ---------------------------
def calculate_per(a, b, c, d):
	if (p_3[0] == p_4[0]):  # when line_2 is perpendicular to x axis;
		popup("line_2 is perpendicular to x",title="error",warning=False,error=True)
        halt
    else:
        k_3=(p_2[1]-p_1[1])/(p_2[0]-p_1[0])  #determined by p_1 and p_2;
        k_4=(p_4[1]-p_3[1])/(p_4[0]-p_3[0])  #determined by p_3 and p_4;
        theta_3 = atan(k_3)
        theta_4 = atan(k_4)
        global angle3 = r2d(theta_3)
        global angle4 = r2d(theta_4)
        if (norm(norm(angle3 - angle4) - 90) > 1):
            popup("angle34_over_range", title="error", warning=False, error=True)
            halt
        end
        # distance formulation from point_laser2 to line3 and line4;
        d_x=norm((k_4*(point_laser2[0]-p_3[0])-point_laser2[1]+p_3[1])/sqrt(k_4*k_4+1))-width/2
        d_y=norm((k_3*(point_laser2[0]-p_1[0])-point_laser2[1]+p_1[1])/sqrt(k_3*k_3+1))-width/2

        global d_rz=0
        if (k_3>0 and k_4<0):
            d_rz=(theta_3+pi/2+theta_4)/2
        elif (k_3<0 and k_4>0):
            d_rz=(theta_3-pi/2+theta_4)/2
        else:
            d_rz=0
        end
    end
    #TCP direction and BASE direction depended on [pi,0,0];
    global delta_offset=p[d_x+x_laser2,-d_y+y_laser2,0,0,0,d_rz] #-d_y means y-direction;
end

# ----------------------------------------------------------------------------------------------------------------------

def SubP_scan_datum():
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
	global point_scan=p[0.915,-0.130,scanh1,pi,0,0] #p1
	movej(point_scan,a=aj,v=vj_idle)
    catch_point()
	global p_1=p_0
	point_scan=p[0.715,-0.130,scanh1,pi,0,0] #p2
	movej(point_scan,a=aj,v=vj_idle)
    catch_point()
	global p_2=p_0
	point_scan=p[0.690,-0.100,scanh1,pi,0,0] #p3
	movej(point_scan,a=aj,v=vj_idle)
    catch_point()
	global p_3=p_0
	point_scan=p[0.690,0.100,scanh1,pi,0,0] #p4
	movej(point_scan,a=aj,v=vj_idle)
    catch_point()
	global p_4=p_0
end

def catch_point():
    moving = run move_scan_max()
    while (True):
        if (get_standard_digital_in(1) == False):
            global p_0 = get_actual_tcp_pose()
            kill moving
            break
        end
        sync()
    end
end
# put the movel() into subthread,using if() kill subthread;
thread move_scan_max():
    if (point_scan[1] == -0.130):  # line1,p1 p2
        offset = p[0, 0.050, 0, 0, 0, 0]
    elif (point_scan[0] == 0.690):  # line2,p3 p4
        offset = p[-0.050, 0, 0, 0, 0, 0]
    end
    point_scan_max = pose_trans(point_scan, offset)
    movel(point_scan_max, a=al, v=vl_scan)
end

# ----------------------------------------------------------------------------------------------------------------------

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
    catch_point2()
	global p_1=p_0
	point_scan=p[0.501,0.080,scanh2,pi,0,0] #p2
	movej(point_scan,a=aj,v=vj_idle)
    catch_point2()
    global p_2=p_0
	point_scan=p[0.500,0.081,scanh2,pi,0,0] #p3
	movej(point_scan,a=aj,v=vj_idle)
	catch_point2()
	global p_3=p_0
	point_scan=p[0.500,-0.110,scanh2,pi,0,0] #p4
	movej(point_scan,a=aj,v=vj_idle)
	catch_point2()
	global p_4=p_0
end

def catch_point2(): #redefine the thread,using laser2;
	moving=run move_scan_max2()
	while (True):
		if (get_standard_digital_in(2)==False):
			global p_0 = get_actual_tcp_pose()
			kill moving
			break
		end
		sync()
	end
end

thread move_scan_max2():
	if (point_scan[1]==0.080): #line1,p1 p2
		offset=p[0,-0.080,0,0,0,0]
	elif (point_scan[0]==0.500): #line2,p3 p4
		offset=p[0.080,0,0,0,0,0]
	end
	point_scan_max=pose_trans(point_scan,offset)
	movel(point_scan_max,a=al,v=vl_scan)
end
# ----------------------------------------------------------------------------------------------------------------------
def SubP_pave(): #pave 6 pieces
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
	if (i<2): #when pave 2 3;
		offset=p[0,-(i+1)*(width+gap),0,0,0,0]
	else: #(i<5)  when pave 4 5 6;
		offset=p[-(width+gap),-(i-2)*(width+gap),0.002,0,0,0] #0.002 because robotarm unlevel;
	end
    # offset=p[0,0,-(i+1)*thickn,0,0,0] #palletizing

	point_pave_move=pose_trans(point_centre,offset) #posetrans tile first;
    point_pave = pose_trans(point_pave_move, delta_offset)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movel(pose_trans(point_pave,dropz),a=al,v=vl_erect) #pave,down
	set_standard_digital_out(4,False)
	sleep(0.5)
	movej(point_pave,a=aj,v=vj_idle,r=r_nar)  #pave,up
	movej(point_turn,a=aj,v=vj_idle,r=r_wide)
end

def SubP_take_back(): #take back pave 6 pieces
	popup("Take_back_6", "message", False, False, blocking=True)
    while (i>=0): #i=5--
        if (i>2):  #when take back 6 5 4;i=5,4,3
            global back_offset=p[-(width+gap),(3-i)*(width+gap),0,0,0,0]
        else: #(i>0) #when take back 3 2 1;
            global back_offset=p[0,-i*(width+gap),0,0,0,0]
        end
        SubP_tack_back_action()
        i=i-1
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
    movej(point_turn, a=aj, v=vj_load, r=r_wide) # transition point
    movej(point_take1, a=aj, v=vj_load, r=r_nar)  # back,up
    offset = p[0, 0, dropz[2] + i* thickn, 0, 0, 0]
    movel(pose_trans(point_take1, offset),a=al, v=vl_erect)  # back,down
    set_standard_digital_out(4, False)
    sleep(0.5)
    movel(point_take1, a=al, v=vl_erect)  # back,up
    movej(point_turn, a=aj, v=vj_idle)
end
# ----------------------------------------------------------------------------------------------------------------------
def test_first(): #put it in front main function;
    movel(point_centre,a=aj, v=vj_idle)
    movel(pose_trans(point_centre, dropz), a=al, v=vl_erect)
    halt
end

# main program; pave 6 pieces
global i = 0
SubP_initialize()
SubP_scan_datum()
calculate_datum(p_1, p_2, p_3, p_4)
# test_first()
while (i < 5): # 0,1,2,3,4
    SubP_scan_take()
    calculate_per(p_1, p_2, p_3, p_4)
    SubP_pave()
    i = i + 1  # 1,2,3,4,5
end
SubP_take_back()

