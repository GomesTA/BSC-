
'''

  ____   _____  _____               _                        _   _             
 |  _ \ / ____|/ ____|             | |                      | | (_)            
 | |_) | (___ | |        __ _ _   _| |_ ___  _ __ ___   __ _| |_ _  ___  _ __  
 |  _ < \___ \| |       / _` | | | | __/ _ \| '_ ` _ \ / _` | __| |/ _ \| '_ \ 
 | |_) |____) | |____  | (_| | |_| | || (_) | | | | | | (_| | |_| | (_) | | | |
 |____/|_____/ \_____|_ \__,_|\__,_|\__\___/|_| |_| |_|\__,_|\__|_|\___/|_| |_|
 
                     (_)             /_ | / _ \                                
  __   _____ _ __ ___ _  ___  _ __    | || | | |                               
  \ \ / / _ \ '__/ __| |/ _ \| '_ \   | || | | |                               
   \ V /  __/ |  \__ \ | (_) | | | |  | || |_| |                               
    \_/ \___|_|  |___/_|\___/|_| |_|  |_(_)___/                                
                                                                               
                                                                               

'''


import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(legacy='1.25')

import math

def line_circle_intersection(center, radius, point1, point2):
    x0, y0 = center
    r = radius
    x1, y1 = point1
    x2, y2 = point2

    # Line equation in the form y = mx + b
    if x1 == x2:  # Vertical line case
        x_intercept = x1
        delta = r**2 - (x_intercept - x0)**2
        if delta < 0:
            return None  # No intersection
        y_intercept1 = y0 + math.sqrt(delta)
        y_intercept2 = y0 - math.sqrt(delta)
        return [(x_intercept, y_intercept1), (x_intercept, y_intercept2)]
    
    # Slope and intercept
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1

    # Quadratic coefficients for intersection points
    A = 1 + m**2
    B = 2 * (m * b - m * y0 - x0)
    C = x0**2 + y0**2 + b**2 - 2 * y0 * b - r**2

    # Discriminant
    D = B**2 - 4 * A * C
    if D < 0:
        return None  # No intersection

    # Intersection points
    sqrt_D = math.sqrt(D)
    x_intercept1 = (-B + sqrt_D) / (2 * A)
    x_intercept2 = (-B - sqrt_D) / (2 * A)
    y_intercept1 = m * x_intercept1 + b
    y_intercept2 = m * x_intercept2 + b

    #return [(x_intercept1, y_intercept1), (x_intercept2, y_intercept2)]
    return (x_intercept1, y_intercept1)


##############################################      SPEC DATA
def Polyline(Thickness_decrement_var):
    my_thickness_decrement=(Thickness_decrement_var)
    print("*** MY CODE *** thickness decrement is "+str(np.ceil(Thickness_decrement_var)))
    
    #PPC-300 or PPC-350
    BSC_TYPE="PPC-350"
    
    #Bell mouth size [in]
    my_dim=48
   
    #Mesh size for Abaqus
    mesh_size_BSC=30.0
    mesh_size_BM=30.0
    
    #Loads
    my_SF_kN=676
    my_BM_kNm=1573
    #Adjusting for Abaqus N-mm consistent units
    My_Loads=(my_SF_kN*1000.0,my_BM_kNm*1000000.0)
    
    #inch, A, B, C, diamD, diamE, diamF, diamG, diamH, diamJ, diamK, R
    #Dimension I does not exist on the spec
    
    if BSC_TYPE == "PPC-300":
        BSC_dim=[
        [48,1729,290,199,1074.5,1149,1192,1244.5,936,950,872,537.25],
        [46,1729,290,199,1022.5,1098,1141.2,1193.5,867.2,899.2,821.2,511.25],
        [32, 1309, 310, 139, 672.5, 747, 790, 842.5, 569, 573, 495, 336.25]
        ]
        
        index_dim=0
        for dim in BSC_dim:
            if dim[0]==my_dim:
                my_index_dim=index_dim
                break
            elif dim[0]!= my_dim:
                index_dim+=1
        
        print("My index is \/")
        print(index_dim)

        height_A=BSC_dim[index_dim][1]
        height_B=BSC_dim[index_dim][2]
        height_C=BSC_dim[index_dim][3]
        radius_D=BSC_dim[index_dim][4]/2.0
        radius_E=BSC_dim[index_dim][5]/2.0
        radius_F=BSC_dim[index_dim][6]/2.0
        radius_G=BSC_dim[index_dim][7]/2.0
        radius_H=BSC_dim[index_dim][8]/2.0
        radius_J=BSC_dim[index_dim][9]/2.0
        radius_K=BSC_dim[index_dim][10]/2.0
        Radius_R=BSC_dim[index_dim][11]
        
        #inch, A, B, C, diamD, diamE, diamF, diamG, diamH, diamI, diamJ, diamK, R
    elif BSC_TYPE == "PPC-350":
        BSC_dim=[
        [48, 1729, 290, 199, 1073.5, 1175, 1218.0, 1270.5, 936.0, 1109.5, 950.0, 872.0, 537.25],
        [46, 1729, 290, 199, 1023.5, 1124, 1167.2, 1219.5, 867.2, 1059.5, 899.2, 821.2, 511.25],
        [32, 1309, 310, 139, 672.5, 747, 790, 842.5, 569, 573, 495, 336.25]
        ]
        
        index_dim=0
        for dim in BSC_dim:
            if dim[0]==my_dim:
                my_index_dim=index_dim
                break
            elif dim[0]!= my_dim:
                index_dim+=1
        
        print("My index is \/")
        print(index_dim)
        
        height_A=BSC_dim[index_dim][1]
        height_B=BSC_dim[index_dim][2]
        height_C=BSC_dim[index_dim][3]
        radius_D=BSC_dim[index_dim][4]/2.0
        radius_E=BSC_dim[index_dim][5]/2.0
        radius_F=BSC_dim[index_dim][6]/2.0
        radius_G=BSC_dim[index_dim][7]/2.0
        radius_H=BSC_dim[index_dim][8]/2.0
        radius_I=BSC_dim[index_dim][9]/2.0
        radius_J=BSC_dim[index_dim][10]/2.0
        radius_K=BSC_dim[index_dim][11]/2.0
        Radius_R=BSC_dim[index_dim][12]
    
    
    ##############################################      INPUTS
    
    n_points_straight=2
    n_points_arc=8

    #PIPE inputs
    pipe_nominal_OD=300
    pipe_tol=8
    pipe_OD=pipe_nominal_OD+pipe_tol
    
    #Flared liner inputs
    radial_clearence_pipe_flared=5
    FLARED_MIN_THICK=18.0
    FLARED_MARGIN=1.0
    BUILT_IN_ANGLE=7
    FLARED_RADIUS=7500
    ADJUST_TO_FORGING=0
    FLARED_IR=(pipe_OD/2.0)+radial_clearence_pipe_flared+ADJUST_TO_FORGING
    Lista_Flared_Liner_D=[]
    Lista_Flared_Liner_H=[]
    
    
    
    IR_FL = FLARED_IR+FLARED_MARGIN+FLARED_MIN_THICK
    OR_FL = 620.0
    FL_HEIGHT=130.0
    BCD = 864
    RCD= BCD/2.0
    BCD_hole=51
    
    
    #Hydratight tool check - HM09 or HM07 - diamter, nearest obstruction
    tension_tool="HM09"
    
    #Inferior Ellipse
    semi_axis_hor_inf=70
    semi_axis_vert_inf=160.5
    
    #straight_mid_segment
    mid_length=0
    
    #Superior Ellipse
    semi_axis_hor_sup=70
    semi_axis_vert_sup=160.5
    
    #The neck_thick is a consequence of the flange internal radius, the horizontal semi axis and the BCD and the tool.
    #If the neck thickness needs to be intentionally reduced, use the variable my_neck_reduction
    #NECK THICK calculation
    my_neck_reduction=0

    #outer cylinder thickness at middle of BSLM
    OC_THICK=32.1
    #thickness of the top plate
    TP_THICK=55
    
    #Outer cylinder internal radius
    int_R_large=35
    int_R_small=10
    
    #cavity - "V" or "straight"
    Cavity_type="V"
    Cavity_deep=80

    
    #retaU_dx=(231.27-((48-my_dim)/2.0)*25)-my_thickness_decrement-(corr_BSN_type)
    #retaU_dy=10.7048
    U_RADIUS_EXT=30
    U_RADIUS_INT=30
    retaU_dx=(252.5-U_RADIUS_EXT-U_RADIUS_INT)-my_thickness_decrement-((48-my_dim)*25)-70
    retaU_dy=10
    

    
    #INNER CYLINDER
    IC_top_thick=55.0
    IC_int_fillet=2.0
    IC_out_fillet=10.0
    
    #INTERNAL CYLINDER TYPE, 6 OR 9 STEPS
    #you need to choose between ratios or mathcad
    flared_design_option="ratios"
    STEPS_INNER_CYL=6
    
    if STEPS_INNER_CYL==6:
        if flared_design_option=="mathcad":
            L5=300
            L4=629
            L3=1065
            #L8=0
            
            L5+=1
            L4+=1
            L3+=1
            
            D6=517
            D3=405
            D2=345
            D1=300
            
            D3+=2
            D6+=2
            D2+=2
            D1+=2
            
            Di1=226
            FLARED_IR=Di1/2
    
            #If "mathcad" is chosen, the Internal radius of the flange becomes D1/2
            IR_FL=D1/2
            
        if flared_design_option=="ratios":
            retraction_0=IC_top_thick-my_thickness_decrement
            retraction_ratio_1=0.5
            retraction_ratio_2=0.25
            retraction_ratio_3=0.25
            
            Vertical_segment_ratio_0=0.2
            Vertical_segment_ratio_1=0.25
            Vertical_segment_ratio_2=0.25
            Vertical_segment_ratio_3=0.3

    
  
    #TOP STRUCTURE
    TS_HEIGHT=265
    TS_bottom_plate_thick=50
    TS_inner_thickness=44
    TS_top_pate_thick=15
    TS_OR_base_bottom=radius_H
    TS_OR_base_top=TS_OR_base_bottom-30
    TS_OR_top_bottom=TS_OR_base_top-50
    TS_OR_top_top=TS_OR_top_bottom+20
    # TS_IR_bottom. The internal radius at bottom is assigned below according to retraction 0
    # TS_IR_top. Assigned right after the TS_IR_bottom
    TS_IR_top=TS_OR_top_top-150+my_thickness_decrement
    

    ##############################################      BSC DRAWING

        
    
    Polyline1=[]
    Polyline2=[]
    Polyline3=[]
    Polyline4=[]
    Polyline5=[]
    #Polyline 6 is for the bell mouth
    Polyline6=[]
    
    
    #pipe drawing
    
    x = np.linspace(pipe_OD/2.0,pipe_OD/2.0, n_points_straight)
    y = np.linspace(-200, 3000, n_points_straight)
    plt.figure()
    plt.plot(x,y,c="darkorange")
    
    

    if tension_tool == "HM07":
        HM=[127,280]
    elif tension_tool == "HM09":
        HM=[144.5,288]
        #Design do Patrick considera uma ferramenta otimizada
        #HM=[(144.5-11),288]
    
    x = np.linspace(RCD-HM[0]/2,RCD+HM[0]/2, n_points_straight)
    y = np.linspace(FL_HEIGHT, FL_HEIGHT, n_points_straight)
    plt.plot(x,y,c="red")
    
    x = np.linspace(RCD+HM[0]/2,RCD+HM[0]/2, n_points_straight)
    y = np.linspace(FL_HEIGHT, FL_HEIGHT+HM[1], n_points_straight)
    plt.plot(x,y,c="red")
    
    x = np.linspace(RCD+HM[0]/2,RCD-HM[0]/2, n_points_straight)
    y = np.linspace(FL_HEIGHT+HM[1], FL_HEIGHT+HM[1], n_points_straight)
    plt.plot(x,y,c="red")
    
    x = np.linspace(RCD-HM[0]/2,RCD-HM[0]/2, n_points_straight)
    y = np.linspace(FL_HEIGHT+HM[1], FL_HEIGHT, n_points_straight)
    plt.plot(x,y,c="red")
    

    NECK_THICK=RCD-(HM[0]/2)-semi_axis_hor_inf-(IR_FL+my_thickness_decrement)-my_neck_reduction
    NECK_THICK=np.floor(NECK_THICK)
    if my_neck_reduction>0:
        print("My neck thickness is "+str(round(NECK_THICK,4))+", which was manually reduced by "+str(my_neck_reduction)+" mm using my_neck_reduction var")
    else:
        print("My neck thickness is "+str(round(NECK_THICK,4)))
    
    
    BSLM_height=height_A+(semi_axis_vert_inf+semi_axis_vert_sup+FL_HEIGHT+mid_length)
    print("The BSLM height is "+str(BSLM_height))
    #segmento1:base
    
    x = np.linspace(IR_FL+my_thickness_decrement, RCD-BCD_hole/2.0, n_points_straight)
    y = np.linspace(0, 0, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(RCD-BCD_hole/2.0, RCD-BCD_hole/2.0, n_points_straight)
    y = np.linspace(0, -5, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(RCD-BCD_hole/2.0, RCD+BCD_hole/2.0, n_points_straight*2)
    y = np.linspace(-5, -5, n_points_straight*2)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(RCD+BCD_hole/2.0, RCD+BCD_hole/2.0, n_points_straight)
    y = np.linspace(-5, 0, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(RCD+BCD_hole/2.0, OR_FL, n_points_straight)
    y = np.linspace(0, 0, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    #segmento2:altura do flange
    x = np.linspace(OR_FL, OR_FL, n_points_straight*3)
    y = np.linspace(0, FL_HEIGHT, n_points_straight*3)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    ellipse_center_x= (IR_FL+my_thickness_decrement)+NECK_THICK+semi_axis_hor_inf
    ellipse_center_y=FL_HEIGHT+semi_axis_vert_inf
    
    #segmento3:pre-elipse
    x = np.linspace(OR_FL, ellipse_center_x, n_points_straight)
    y = np.linspace(FL_HEIGHT, FL_HEIGHT, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    #segmento4:elipse inferior
    t=np.linspace(3*np.pi/2, np.pi, n_points_arc*2)
    x=ellipse_center_x+semi_axis_hor_inf*np.cos(t)
    y=ellipse_center_y+semi_axis_vert_inf*np.sin(t)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    if mid_length >0:
        mx = np.linspace(x[-1], x[-1], n_points_straight*2)
        my = np.linspace(y[-1], y[-1]+mid_length, n_points_straight*2)
        plt.plot(mx,my)
        Polyline1.extend([(xi, yi) for xi, yi in zip(mx, my)])
        
    
    #segmento5:elipse superior
    t=np.linspace(np.pi, np.pi/2, n_points_arc*2)
    x=ellipse_center_x+semi_axis_hor_sup*np.cos(t)-(semi_axis_hor_inf-semi_axis_hor_sup)
    y=ellipse_center_y+semi_axis_vert_sup*np.sin(t)+mid_length
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
      
    #segmento
    xx = np.linspace(x[-1], radius_D , n_points_straight)
    yy = np.linspace(y[-1], y[-1], n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #segmento
    x = np.linspace(radius_D , radius_D , n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+40, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    #segmento
    xx = np.linspace(radius_D , radius_E , n_points_straight)
    yy = np.linspace(y[-1], y[-1], n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #segmento
    incr_height_1=np.tan(np.deg2rad(37.5))*(radius_F-radius_E)
    x = np.linspace(radius_E , radius_F , n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+incr_height_1, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    #segmento
    incr_height_2=np.tan(np.deg2rad(39.5))*(radius_G-radius_F)
    xx = np.linspace(radius_F , radius_G , n_points_straight)
    yy = np.linspace(y[-1], y[-1]+incr_height_2, n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    surf_kit_height_0=(y[-1]+incr_height_2)-30

    
    ###################segmento (if PPC-350, the diameter is I, not D)
    if BSC_TYPE=="PPC-300":
        radius_D_or_I=radius_D
    elif BSC_TYPE=="PPC-350":
        radius_D_or_I=radius_I
    incr_height_3=180-(incr_height_1+incr_height_2) #180 is the same value for PPC300 and PPC350, comes from the dummy cap drawing
    x = np.linspace(radius_G , radius_D_or_I , n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+incr_height_3, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    surf_kit_height_1=(yy[-1]+incr_height_3)+1
    surf_kit_height_2=surf_kit_height_1
    surf_kit_radius_3=radius_D-1
    vertical_adjust= yy[-1]+incr_height_3
    print("The vertical adjust is: "+str(vertical_adjust))
    
    #segmento
    xx = np.linspace(radius_D_or_I , radius_D_or_I , n_points_straight)
    yy = np.linspace(y[-1], y[-1]+height_B, n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #segmento
    incr_height_4=(radius_D_or_I-radius_J)/np.tan(np.deg2rad(15))
    x = np.linspace(radius_D_or_I , radius_J , n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+incr_height_4, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    #segmento
    incr_height_5=height_A+(semi_axis_vert_inf+semi_axis_vert_sup+FL_HEIGHT+mid_length)-y[-1]- \
    height_C-(radius_D-radius_J)/np.tan(np.deg2rad(15))
    xx = np.linspace(radius_J , radius_J , n_points_straight)
    yy = np.linspace(y[-1], y[-1]+incr_height_5, n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #segmento
    incr_height_6=(radius_D-radius_J)/np.tan(np.deg2rad(15))
    x = np.linspace(radius_J , radius_D , n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+incr_height_6, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    ####### calculation of the intersection points between circumference and 45deg line #############
    center = (0, BSLM_height-height_C)
    radius = Radius_R
    point1 = (radius_H, BSLM_height)
    point2 = (radius_H+200, BSLM_height-200) #200 is an arbitrary value of delta to make a line
    
    intersections = line_circle_intersection(center, radius, point1, point2)
    print("Intersection points:", intersections)
    ##################### the points are used to connect the circumference and the arc
    
    #segmento: circunferencia
    angle_start = 0
    angle_end = np.deg2rad(20)
    # Generate angles for the arc between start and end angle
    angles = np.linspace(angle_start, angle_end, 20)
    # Calculate the arc points
    pre_arc_x = (Radius_R * np.cos(angles))-(Radius_R-x[-1])
    pre_arc_y = y[-1] + Radius_R * np.sin(angles)
    arc_x=[]
    arc_y=[]
    #print(list(zip(arc_x, arc_y)))
    for element in list(zip(pre_arc_x, pre_arc_y)):
        if element[1]<=intersections[1]:
            arc_x.append(element[0])
            arc_y.append(element[1])
    arc_x.append(intersections[0])
    arc_y.append(intersections[1])
    plt.plot(arc_x,arc_y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])

    #segmento
    line_x = np.linspace(arc_x[-1], radius_H, n_points_straight)
    line_y = np.linspace(arc_y[-1],height_A+(semi_axis_vert_inf+semi_axis_vert_sup+FL_HEIGHT+mid_length) ,n_points_straight)
    plt.plot(line_x,line_y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(line_x, line_y)])
    
    
    #segmento 
    xx = np.linspace(line_x[-1], radius_J-OC_THICK, n_points_straight)
    yy = np.linspace(line_y[-1], line_y[-1] ,n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    ext_x_for_top_plate=radius_J-OC_THICK
    #############################################END OF POLYLINE1
    
    #segmento cavidade 
    Cavity_right_side=FL_HEIGHT+semi_axis_vert_inf+semi_axis_vert_sup+mid_length+40+180-Cavity_deep
    x = np.linspace(xx[-1], xx[-1], n_points_straight)
    y = np.linspace(yy[-1]-TP_THICK, Cavity_right_side,n_points_straight)
    plt.plot(x,y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    

    
    #segmento: arco do U interno
    angle_start = 0
    angle_end = np.arcsin(retaU_dy/retaU_dx)-np.pi/2
    print(angle_end)
    print(np.rad2deg(angle_end))
        # Generate angles for the arc between start and end angle
    angles = np.linspace(angle_start, angle_end, n_points_arc*2)
        # Calculate the arc points
    arc_x = (U_RADIUS_EXT * np.cos(angles))-(U_RADIUS_EXT*np.cos(angle_start))+x[-1]
    arc_y = U_RADIUS_EXT * np.sin(angles)-U_RADIUS_EXT*np.sin(angle_start)+y[-1]
    plt.plot(arc_x,arc_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    
    #segmento: reta do U inclinada
    if Cavity_type == "straight":
        x = np.linspace(arc_x[-1], arc_x[-1]-retaU_dx, n_points_straight*2)
        y = np.linspace(arc_y[-1], arc_y[-1]+retaU_dy, n_points_straight*2)
        plt.plot(x,y)
        
        Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    elif Cavity_type == "V":
        x_ = np.linspace(arc_x[-1], arc_x[-1]-(retaU_dx/(2)), n_points_straight*2)
        y_ = np.linspace(arc_y[-1], arc_y[-1]-retaU_dy, n_points_straight*2)
        plt.plot(x_,y_)
        Polyline2.extend([(xi, yi) for xi, yi in zip(x_, y_)])
        
        x = np.linspace(arc_x[-1]-(retaU_dx/(2.0)), arc_x[-1]-(retaU_dx), n_points_straight*2)
        y = np.linspace(arc_y[-1]-retaU_dy, arc_y[-1], n_points_straight*2)
        plt.plot(x,y)
        Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
        
    #segmento: arco do U interno
    angle_start = -np.arcsin(retaU_dy/retaU_dx)-np.pi/2
    angle_end = -np.pi
    print(angle_start)
    print(np.rad2deg(angle_start))
        # Generate angles for the arc between start and end angle
    angles = np.linspace(angle_start, angle_end, n_points_arc*2)
        # Calculate the arc points
    arc_x = (U_RADIUS_INT * np.cos(angles))-(U_RADIUS_INT*np.cos(angle_start))+x[-1]
    arc_y = U_RADIUS_INT * np.sin(angles)-U_RADIUS_INT*np.sin(angle_start)+y[-1]
    plt.plot(arc_x,arc_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    
############################### STEPS NOT IN CONTACT WITH FLARED LINER
    print(arc_y[-1])
    int_vert_step=BSLM_height-arc_y[-1]
    print(int_vert_step)
    
    int_rise_1=int_vert_step/3
    int_rise_2=int_vert_step/3
    int_rise_3=int_vert_step/3

    
    #segmento 16: Rise1 
    x = np.linspace(arc_x[-1], arc_x[-1], n_points_straight)
    y = np.linspace(arc_y[-1], arc_y[-1]+int_rise_1-int_R_large, n_points_straight)
    plt.plot(x,y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    #FILLET_RADIUS_large
    angles = np.linspace(np.pi,np.pi/2, n_points_arc*2)
    fil_x = (int_R_large * np.cos(angles))+x[-1]+int_R_large
    fil_y = int_R_large * np.sin(angles)+y[-1]
    plt.plot(fil_x,fil_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(fil_x, fil_y)])
    
    #segmento 16: Rise2
    xx = np.linspace(fil_x[-1], arc_x[-1]+int_R_large, n_points_straight)
    yy = np.linspace(fil_y[-1], arc_y[-1]+int_rise_1+int_rise_2-int_R_small, n_points_straight)
    plt.plot(xx,yy)
    Polyline2.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    
    #FILLET_RADIUS_small
    angles = np.linspace(np.pi,np.pi/2, n_points_arc*2)
    fil_x = (int_R_small * np.cos(angles))+xx[-1]+int_R_small
    fil_y = int_R_small * np.sin(angles)+yy[-1]
    plt.plot(fil_x,fil_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(fil_x, fil_y)])

    
    #segmento 16: Rise3
    x = np.linspace(fil_x[-1], arc_x[-1]+int_R_large+int_R_small, n_points_straight)
    y = np.linspace(fil_y[-1], arc_y[-1]+int_rise_1+int_rise_2+int_rise_3-TP_THICK, n_points_straight)
    plt.plot(x,y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    int_x_for_top_plate=arc_x[-1]+int_R_large+int_R_small
    
#################################### END OF POLYLINE 2

    hor_span=x[-1]-IR_FL-my_thickness_decrement
    
    Drop1 = Vertical_segment_ratio_0*BSLM_height
    Drop2 = Vertical_segment_ratio_1*BSLM_height
    Drop3 = Vertical_segment_ratio_2*BSLM_height
    Drop4 = Vertical_segment_ratio_3*BSLM_height
    
    retraction_0=IC_top_thick#-my_thickness_decrement
    retraction_1=((hor_span-retraction_0))*retraction_ratio_1
    retraction_2=((hor_span-retraction_0))*retraction_ratio_2
    retraction_3=((hor_span-retraction_0))*retraction_ratio_3
    
    #segmento: IC top thick
    xx = np.linspace(x[-1], x[-1]-retraction_0 , n_points_straight)
    yy = np.linspace(BSLM_height,BSLM_height , n_points_straight)
    plt.plot(xx,yy)
    Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    Lista_Flared_Liner_D.append(round(xx[-1],3))
    Lista_Flared_Liner_H.append(round(yy[-1],3))
    
    #segmento: Drop1
    drop1_x = np.linspace(xx[-1], xx[-1] , n_points_straight)
    drop1_y = np.linspace(BSLM_height,BSLM_height-Drop1+IC_int_fillet , n_points_straight)
    plt.plot(drop1_x,drop1_y)
    Polyline3.extend([(xi, yi) for xi, yi in zip(drop1_x, drop1_y)])
    
    #########################################  fillets   1 ##############################
    #Fillet int drop1
    #FILLET_RADIUS 1-int
    angles = np.linspace(0,-np.pi/2, n_points_arc)
    i_arc_x = (IC_int_fillet * np.cos(angles))+drop1_x[1]-IC_int_fillet
    i_arc_y = IC_int_fillet * np.sin(angles)+drop1_y[-1]
    plt.plot(i_arc_x,i_arc_y)
    
    
    #The order is swapped because the Drop2 is needed for the fillet radius external
    #segmento: Drop2
    drop2_x = np.linspace(xx[-1]-retraction_1, xx[-1]-retraction_1 , n_points_straight)
    drop2_y = np.linspace(BSLM_height-Drop1-IC_out_fillet,BSLM_height-Drop1-Drop2+IC_int_fillet , n_points_straight)
    plt.plot(drop2_x,drop2_y)
    
    
    #Fillet ext drop1
    #FILLET_RADIUS 1-ext
    angles = np.linspace(np.pi,np.pi/2, n_points_arc)
    angles = np.linspace(np.pi/2,np.pi, n_points_arc)
    e_arc_x = (IC_out_fillet * np.cos(angles))+drop2_x[0]+IC_out_fillet
    e_arc_y = IC_out_fillet * np.sin(angles)+drop2_y[0]
    plt.plot(e_arc_x,e_arc_y)
    
    x = np.linspace(i_arc_x[-1], e_arc_x[0] , n_points_straight*2)
    y = np.linspace(i_arc_y[-1], e_arc_y[0] , n_points_straight*2)
    plt.plot(x,y)
    
    Polyline3.extend([(xi, yi) for xi, yi in zip(i_arc_x,i_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(e_arc_x,e_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(drop2_x,drop2_y)])
    
    Lista_Flared_Liner_D.append(round(e_arc_x[-1],3))
    Lista_Flared_Liner_H.append(round(e_arc_y[0],3))

    #########################################  fillets   2 ##############################

    #Fillet int drop2
    #FILLET_RADIUS 2-int
    angles = np.linspace(0,-np.pi/2, n_points_arc)
    i_arc_x = (IC_int_fillet * np.cos(angles))+drop2_x[1]-IC_int_fillet
    i_arc_y = IC_int_fillet * np.sin(angles)+drop2_y[-1]
    plt.plot(i_arc_x,i_arc_y)
    
    #segmento: Drop3
    drop3_x = np.linspace(xx[-1]-retraction_1-retraction_2, xx[-1]-retraction_1-retraction_2 , n_points_straight)
    drop3_y = np.linspace(BSLM_height-Drop1-Drop2-IC_out_fillet,BSLM_height-Drop1-Drop2-Drop3+IC_int_fillet , n_points_straight)
    plt.plot(drop3_x,drop3_y)
    
    #Fillet ext drop2
    #FILLET_RADIUS 2-ext
    angles = np.linspace(np.pi,np.pi/2, n_points_arc)
    angles = np.linspace(np.pi/2,np.pi, n_points_arc)
    e_arc_x = (IC_out_fillet * np.cos(angles))+drop3_x[0]+IC_out_fillet
    e_arc_y = IC_out_fillet * np.sin(angles)+drop3_y[0]
    plt.plot(e_arc_x,e_arc_y)
    
    x = np.linspace(i_arc_x[-1], e_arc_x[0] , n_points_straight*2)
    y = np.linspace(i_arc_y[-1], e_arc_y[0] , n_points_straight*2)
    plt.plot(x,y)
    
    Polyline3.extend([(xi, yi) for xi, yi in zip(i_arc_x,i_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(e_arc_x,e_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(drop3_x,drop3_y)])
    
    Lista_Flared_Liner_D.append(round(e_arc_x[-1],3))
    Lista_Flared_Liner_H.append(round(e_arc_y[0],3))
    
    #########################################  fillets   3 ##############################

    #Fillet int drop3
    #FILLET_RADIUS 3-int
    angles = np.linspace(0,-np.pi/2, n_points_arc)
    i_arc_x = (IC_int_fillet * np.cos(angles))+drop3_x[1]-IC_int_fillet
    i_arc_y = IC_int_fillet * np.sin(angles)+drop3_y[-1]
    plt.plot(i_arc_x,i_arc_y)

    #segmento: Drop4
    drop4_x = np.linspace(xx[-1]-retraction_1-retraction_2-retraction_3, xx[-1]-retraction_1-retraction_2-retraction_3 , n_points_straight)
    drop4_y = np.linspace(BSLM_height-Drop1-Drop2-Drop3-IC_out_fillet, 0 , n_points_straight)
    plt.plot(drop4_x,drop4_y)
    
    #Fillet ext drop3
    #FILLET_RADIUS 3-ext
    angles = np.linspace(np.pi,np.pi/2, n_points_arc)
    angles = np.linspace(np.pi/2,np.pi, n_points_arc)
    e_arc_x = (IC_out_fillet * np.cos(angles))+drop4_x[0]+IC_out_fillet
    e_arc_y = IC_out_fillet * np.sin(angles)+drop4_y[0]
    plt.plot(e_arc_x,e_arc_y)
    
    x = np.linspace(i_arc_x[-1], e_arc_x[0] , n_points_straight*2)
    y = np.linspace(i_arc_y[-1], e_arc_y[0] , n_points_straight*2)
    plt.plot(x,y)
    
    Polyline3.extend([(xi, yi) for xi, yi in zip(i_arc_x,i_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(e_arc_x,e_arc_y)])
    Polyline3.extend([(xi, yi) for xi, yi in zip(drop4_x,drop4_y)])
    
    Lista_Flared_Liner_D.append(round(e_arc_x[-1],3))
    Lista_Flared_Liner_H.append(round(e_arc_y[0],3))
    
    Lista_Flared_Liner_D.append(round(e_arc_x[-1],3))
    Lista_Flared_Liner_H.append(round(0,3))
    
#################################### END OF POLYLINE 3

    #segmento: superior top plate segement
    x = np.linspace(int_x_for_top_plate, ext_x_for_top_plate , n_points_straight)
    y = np.linspace(BSLM_height,BSLM_height, n_points_straight)
    plt.plot(x,y)
    Polyline4.extend([(xi, yi) for xi, yi in zip(x, y)])


#################################### END OF POLYLINE 4

    #segmento: inferior top plate segement
    
    #segmento: superior top plate segement
    x = np.linspace(int_x_for_top_plate, ext_x_for_top_plate , n_points_straight)
    y = np.linspace(BSLM_height-TP_THICK,BSLM_height-TP_THICK, n_points_straight)
    plt.plot(x,y)
    Polyline5.extend([(xi, yi) for xi, yi in zip(x, y)])



#################################### END OF POLYLINE 5


    ####################### TOP STRUCTURE ##############################
    '''Lista_Flared_Liner_H.append(vert_span)
    Lista_Flared_Liner_D.append(TS_IR_top)
    
    Lista_Flared_Liner_H.append(vert_span+TS_HEIGHT)
    Lista_Flared_Liner_D.append(TS_IR_top)'''
    
    
    vert_span=BSLM_height
    display_TS=0
    
    if display_TS>0:
        
        x = np.linspace( TS_OR_base_bottom,TS_OR_base_bottom , n_points_straight)
        y = np.linspace( vert_span , vert_span+TS_bottom_plate_thick  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_OR_base_bottom, TS_OR_base_top , n_points_straight)
        y = np.linspace( vert_span+TS_bottom_plate_thick, vert_span+TS_bottom_plate_thick , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_OR_base_top,TS_OR_top_bottom  , n_points_straight)
        y = np.linspace( vert_span+TS_bottom_plate_thick, vert_span+TS_HEIGHT-TS_top_pate_thick , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_OR_top_bottom, TS_OR_top_top , n_points_straight)
        y = np.linspace(vert_span+TS_HEIGHT-TS_top_pate_thick , vert_span+TS_HEIGHT-TS_top_pate_thick  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_OR_top_top, TS_OR_top_top  , n_points_straight)
        y = np.linspace( vert_span+TS_HEIGHT-TS_top_pate_thick, vert_span+TS_HEIGHT , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_OR_top_top, TS_IR_top  , n_points_straight)
        y = np.linspace( vert_span+TS_HEIGHT , vert_span+TS_HEIGHT , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_IR_top, TS_IR_top  , n_points_straight)
        y = np.linspace( vert_span+TS_HEIGHT , vert_span+TS_inner_thickness , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_IR_top, TS_IR_top, n_points_straight)
        y = np.linspace( vert_span+TS_inner_thickness , vert_span  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        

    #######################   FLARED LINER   #########################

    
    display_FlaredLiner=1
    
    if display_FlaredLiner>0:
        
        print("####FLARED LINER DIAMETER AND HEIGHT ###########")
        print(Lista_Flared_Liner_D)
        print(Lista_Flared_Liner_H)
        
        flared_liner_angle=BUILT_IN_ANGLE+2
        
        print("################  FLARED LINER  #############")###preciso achar a distancia vertical pra subtrair
        #flared_arc_length=2*np.pi*FLARED_RADIUS*(flared_liner_angle/360)
        needed_length=FLARED_RADIUS*np.sin(np.deg2rad(flared_liner_angle))
        available_length=vert_span+TS_HEIGHT
        print("needed length is "+str(round(needed_length,4))+" and available length is "+str(round(available_length,4)))
        straight_length=available_length-needed_length
        print("the straight segement is "+str(round(straight_length,4)))
        if needed_length>available_length:
            print("!!! Warning - The top structure must be increased from "+str(TS_HEIGHT)+" to "+str(straight_length*-1+TS_HEIGHT)+" !!!")
        
        count=0
        flared_thick_increase=0
        List_thick=[]
        for i in Lista_Flared_Liner_H:
            if i<straight_length:
                my_thick= Lista_Flared_Liner_D[count]-FLARED_IR
                print(FLARED_IR, Lista_Flared_Liner_D[count], Lista_Flared_Liner_H[count])
                List_thick.append(round(my_thick,4))
            else:
                pre_flared_x=((FLARED_RADIUS**2-(i-straight_length)**2)**0.5)
                flared_x=(pre_flared_x-FLARED_RADIUS-FLARED_IR)*-1
                my_thick=(flared_x-Lista_Flared_Liner_D[count])*-1
                List_thick.append(round(my_thick,4))
            count+=1
        print("The thicknesses are:")
        print(List_thick)
        print('the minimum thickness is '+str(min(List_thick)))
        if flared_design_option == "ratios":
            if min(List_thick)<FLARED_MIN_THICK:
                flared_thick_increase=FLARED_MIN_THICK-min(List_thick)+FLARED_MARGIN
            print('the thickness increase is '+str(flared_thick_increase))

        #STRAIGHT FLARED LINER
        xx = np.linspace(FLARED_IR, FLARED_IR,n_points_straight)
        yy = np.linspace(0, straight_length, n_points_straight)
        plt.plot(xx,yy,c="goldenrod")
        
        #FL ARC
        start_angle = 0
        end_angle = np.deg2rad(flared_liner_angle)
        angles = np.linspace(start_angle,end_angle, n_points_arc*3)
        arc_x = ((FLARED_RADIUS * np.cos(angles))-FLARED_RADIUS-FLARED_IR)*-1
        arc_y = (FLARED_RADIUS * np.sin(angles))+straight_length
        plt.plot(arc_x,arc_y,c="gold")
        
  
    #Assigning the variables for surface definition in Abaqus
    Surface_kit=[]
    Surface_kit.append(surf_kit_height_0)
    Surface_kit.append(surf_kit_height_1)
    Surface_kit.append(surf_kit_height_2)
    Surface_kit.append(surf_kit_radius_3)
    Surface_kit.append(surf_kit_height_0)
    Surface_kit.append(radius_H+1)
    

    ##################### BELL MOUTH
     
    #BM-inch, diamA, diamB, diamC, diamD, diamE, diamF, diamG,
    #H, J, K, L, M, N
    #diam P, diam S, 
    #U, flange thickness(TBC)
    
    if BSC_TYPE == "PPC-300":
        BM_dim=[
            [48, 1784.35, 1343.15, 1082.75, 1220.15, 1365.65, 1269.25, 1816, 2154, 419.10, 590, 345, 318.5, 40, 155.225, 1140.25, 607, 233.43],
            [46, 1733.55, 1292.35, 1030.75, 1168.15, 1313.65, 1217.25, 1769, 2156, 410.97, 600, 345, 318.5, 40, 155.225, 1090.25, 605, 225.55],
            [32, ]
            ]
        
        
        BM_radius_A= BM_dim[my_index_dim][1]/2.0
        BM_radius_B= BM_dim[my_index_dim][2]/2.0
        BM_radius_C= BM_dim[my_index_dim][3]/2.0
        BM_radius_D= BM_dim[my_index_dim][4]/2.0
        BM_radius_E= BM_dim[my_index_dim][5]/2.0
        BM_radius_F= BM_dim[my_index_dim][6]/2.0
        BM_radius_G= BM_dim[my_index_dim][7]/2.0
        BM_height_H= BM_dim[my_index_dim][8]
        BM_height_J= BM_dim[my_index_dim][9]
        BM_height_K= BM_dim[my_index_dim][10]
        BM_height_L= BM_dim[my_index_dim][11]
        BM_height_M= BM_dim[my_index_dim][12]
        BM_height_N= BM_dim[my_index_dim][13]
        BM_radius_P= BM_dim[my_index_dim][14]/2.0
        BM_radius_S= BM_dim[my_index_dim][15]/2.0
        BM_height_U= BM_dim[my_index_dim][16]
        #Flange thickness as per ASME 16.47 CLASS 900 SERIE A
        BM_flange_thickness= BM_dim[my_index_dim][17]
        
        vertical_adjust=0
        
    #BM-inch, diamA, diamB, diamC, diamD, diamE, diamF, diamG,
    #H, I, J, K, L, M,   (PPC-350 has dimension I)
    #diam P, diam S, 
    #U, flange thickness(TBC)
    #Dimension Q and is not needed, they are not hardcoded. They onli exist in PP-350
    elif BSC_TYPE == "PPC-350":
        BM_dim=[
            [48, 1748.35, 1343.15, 1080.75, 1220.4, 1387, 1294.85, 1816, 2171.1, 790, 419.10, 590, 345, 318.5, 40, 155.225, 300, 1140.25, 1116.75, 591.9, 233.43],
            [46, 1733.55, 1292.35, 1030.75, 1168.4, 1335, 1245.85, 1769, 2173.0, 780, 410.97, 600, 345, 318.5, 40, 155.225, 290, 1090.25, 1066.75, 610.5, 225.55],
            [32, ]
            ]
        
        
        BM_radius_A= BM_dim[my_index_dim][1]/2.0
        BM_radius_B= BM_dim[my_index_dim][2]/2.0
        BM_radius_C= BM_dim[my_index_dim][3]/2.0
        BM_radius_D= BM_dim[my_index_dim][4]/2.0
        BM_radius_E= BM_dim[my_index_dim][5]/2.0
        BM_radius_F= BM_dim[my_index_dim][6]/2.0
        BM_radius_G= BM_dim[my_index_dim][7]/2.0
        BM_height_H= BM_dim[my_index_dim][8]
        BM_height_I= BM_dim[my_index_dim][9]     ###### esse e diferente do ppc300
        BM_height_J= BM_dim[my_index_dim][10]
        BM_height_K= BM_dim[my_index_dim][11]
        BM_height_L= BM_dim[my_index_dim][12]
        BM_height_M= BM_dim[my_index_dim][13]
        BM_height_N= BM_dim[my_index_dim][14]
        BM_radius_P= BM_dim[my_index_dim][15]/2.0
        BM_height_R=BM_dim[my_index_dim][16]
        BM_radius_S= BM_dim[my_index_dim][17]/2.0
        BM_radius_T= BM_dim[my_index_dim][18]/2.0
        BM_height_U= BM_dim[my_index_dim][19]
        #Flange thickness as per ASME 16.47 CLASS 900 SERIE A
        BM_flange_thickness= BM_dim[my_index_dim][20]
    
        vertical_adjust=0 #this needs to be verified, the problem would be anode interference, not structural analysis
    
    x = np.linspace(BM_radius_C, BM_radius_A,n_points_straight)
    y = np.linspace(BSLM_height-30, BSLM_height-30, n_points_straight)

    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_radius_A, BM_radius_A,n_points_straight)
    y = np.linspace(y[-1], y[-1]-BM_flange_thickness, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_radius_A, BM_radius_B,n_points_straight)
    y = np.linspace(y[-1], y[-1], n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    BM_ellipse_hor_axis=BM_radius_B-BM_radius_D
    BM_ellipse_vert_axis=100
    
    t=np.linspace(np.pi/2, np.pi, n_points_arc*2)
    x=BM_radius_B+BM_ellipse_hor_axis*np.cos(t)
    y=y[-1]+BM_ellipse_vert_axis*np.sin(t)-BM_ellipse_vert_axis
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])

    x = np.linspace(x[-1], x[-1],n_points_straight)
    y = np.linspace(y[-1], BSLM_height-30+vertical_adjust-BM_height_J-BM_height_K-60, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    opp_cat=BM_radius_E-BM_radius_D
    angle_diam_E=30
    decr_y=opp_cat/np.tan(np.deg2rad(30))
    
    x = np.linspace(x[-1], BM_radius_E,n_points_straight)
    y = np.linspace(y[-1], y[-1]-decr_y, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(x[-1], x[-1],n_points_straight)
    y = np.linspace(y[-1], y[-1]-660, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    web_angle=35
    web_thick=BM_height_N
    height_web_extremity_ext=np.sin(np.deg2rad(web_angle))*web_thick
    adj_cat=300-height_web_extremity_ext
    opp_cat=np.tan(np.deg2rad(web_angle))*adj_cat
    
    x = np.linspace(x[-1], x[-1]+opp_cat,n_points_straight)
    y = np.linspace(y[-1], y[-1]-(300-height_web_extremity_ext), n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    decr_vert=web_thick*np.sin(np.deg2rad(web_angle))
    decr_hor=web_thick*np.cos(np.deg2rad(web_angle))
    
    x = np.linspace(x[-1], x[-1]-decr_hor,n_points_straight)
    y = np.linspace(y[-1], y[-1]-decr_vert, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    incr_vert=300
    
    #x = np.linspace(x[-1], x[-1]-decr_hor,n_points_straight)
    x = np.linspace(x[-1], BM_radius_F,n_points_straight)
    y = np.linspace(y[-1], y[-1]+incr_vert, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(x[-1], x[-1],n_points_straight)
    y = np.linspace(y[-1], y[-1]+BM_height_M, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    if BSC_TYPE == "PPC-300":
        decr_hor=x[-1]-BM_radius_C
        incr_vert=np.tan(np.deg2rad(55))*decr_hor
        
        x = np.linspace(x[-1], x[-1]-decr_hor,n_points_straight)
        y = np.linspace(y[-1], y[-1]+incr_vert, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        x = np.linspace(x[-1], x[-1],n_points_straight)
        y = np.linspace(y[-1], BSLM_height-30, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    elif BSC_TYPE== "PPC-350":
        decr_hor=x[-1]-BM_radius_T
        incr_vert=np.tan(np.deg2rad(55))*decr_hor
        
        x = np.linspace(x[-1], x[-1]-decr_hor,n_points_straight)
        y = np.linspace(y[-1], y[-1]+incr_vert, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        x = np.linspace(x[-1], x[-1],n_points_straight)
        y = np.linspace(y[-1], y[-1]+BM_height_L, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        
        x = np.linspace(x[-1], BM_radius_C,n_points_straight)
        y = np.linspace(y[-1], y[-1]+BM_height_R, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        x = np.linspace(x[-1], x[-1],n_points_straight)
        y = np.linspace(y[-1], BSLM_height-30, n_points_straight)
        plt.plot(x,y,c='blueviolet')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        

    ##################### FORGINGS
    
    display_forgings=0
    
    if display_forgings>0:
    
        #inner tube
        #580/320/950
        #645/385/950
        
        #outer tube
        
        My_forging="Custom"
        
        if My_forging == "Custom":
            
            IFOR_H = 885
            IFOR_ID=240
            IFOR_OD=590
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            OFOR_H=935
            OFOR_ID=850
            OFOR_OD=1035
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 214
            FOOT_OD_FL= 1420
            FOOT_L_FL= 150
            FOOT_OD_NE= 935
            FOOT_L_NE= 450
            FOOT_OD_BD= 1250
            FOOT_L= 770
        
        elif My_forging == "Atapu-4GL":
            
            IFOR_H = 950.0
            IFOR_ID=385.0
            IFOR_OD=645.0
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            OFOR_H=1000
            OFOR_ID=950.0
            OFOR_OD=1135.0
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 235
            FOOT_OD_FL= 1220
            FOOT_L_FL= 150
            FOOT_OD_NE= 760
            FOOT_L_NE= 457
            FOOT_OD_BD= 1310
            FOOT_L= 770
            
        elif My_forging == "Atapu-4GL":
            
            IFOR_H = 950.0
            IFOR_ID=320.0
            IFOR_OD=580.0
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            
            OFOR_H=1000
            OFOR_ID=950.0
            OFOR_OD=1135.0
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 280
            FOOT_OD_FL= 1410
            FOOT_L_FL= 150
            FOOT_OD_NE= 935
            FOOT_L_NE= 457
            FOOT_OD_BD= 1310
            FOOT_L= 770
            
        elif My_forging == "Atapu-6wi-Swapped":
            
            IFOR_H = 950.0
            IFOR_ID=385.0
            IFOR_OD=645.0
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            OFOR_H=1000
            OFOR_ID=950.0
            OFOR_OD=1135.0
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 280
            FOOT_OD_FL= 1410
            FOOT_L_FL= 150
            FOOT_OD_NE= 935
            FOOT_L_NE= 457
            FOOT_OD_BD= 1310
            FOOT_L= 770
            
        elif My_forging == "Atapu-4gl-Swapped":
            
            IFOR_H = 950.0
            IFOR_ID=320.0
            IFOR_OD=580.0
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            OFOR_H=1000
            OFOR_ID=950.0
            OFOR_OD=1135.0
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 235
            FOOT_OD_FL= 1220
            FOOT_L_FL= 150
            FOOT_OD_NE= 760
            FOOT_L_NE= 457
            FOOT_OD_BD= 1310
            FOOT_L= 770
        

        print(IFOR_thick)
        #### inner forging
        x = np.linspace(IFOR_OD/2.0, IFOR_OD/2.0,n_points_straight)
        y = np.linspace(vert_span+5, vert_span+5-IFOR_H , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(IFOR_OD/2.0, IFOR_OD/2.0-IFOR_thick,n_points_straight)
        y = np.linspace(vert_span+5-IFOR_H , vert_span+5-IFOR_H , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(IFOR_OD/2.0-IFOR_thick, IFOR_OD/2.0-IFOR_thick,n_points_straight)
        y = np.linspace(vert_span+5-IFOR_H , vert_span+5 , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(IFOR_OD/2.0-IFOR_thick, IFOR_OD/2.0,n_points_straight)
        y = np.linspace(vert_span+5 , vert_span+5 , n_points_straight)
        plt.plot(x,y,c="black")
        
        #### outer forging
        x = np.linspace((OFOR_OD/2.0)+5, (OFOR_OD/2.0)+5,n_points_straight)
        y = np.linspace(vert_span+5, vert_span+5-OFOR_H , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace((OFOR_OD/2.0)+5, (OFOR_OD/2.0)+5-OFOR_thick,n_points_straight)
        y = np.linspace(vert_span+5-OFOR_H , vert_span+5-OFOR_H , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace((OFOR_OD/2.0)+5-OFOR_thick, (OFOR_OD/2.0)+5-OFOR_thick,n_points_straight)
        y = np.linspace(vert_span+5-OFOR_H , vert_span+5 , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace((OFOR_OD/2.0)+5-OFOR_thick, (OFOR_OD/2.0)+5,n_points_straight)
        y = np.linspace(vert_span+5 , vert_span+5 , n_points_straight)
        plt.plot(x,y,c="black")
        
        #foot
        
        x = np.linspace(FOOT_ID/2.0, FOOT_OD_FL/2.0,n_points_straight)
        y = np.linspace(-foot_margin , -foot_margin , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_FL/2.0, FOOT_OD_FL/2.0,n_points_straight)
        y = np.linspace(-foot_margin , -foot_margin+FOOT_L_FL , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_FL/2.0, FOOT_OD_NE/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L_FL , -foot_margin+FOOT_L_FL , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_NE/2.0, FOOT_OD_NE/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L_FL ,-foot_margin+FOOT_L_NE , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_NE/2.0, FOOT_OD_BD/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L_NE , -foot_margin+FOOT_L_NE , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_BD/2.0, FOOT_OD_BD/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L_NE , -foot_margin+FOOT_L , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_OD_BD/2.0, FOOT_ID/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L , -foot_margin+FOOT_L , n_points_straight)
        plt.plot(x,y,c="black")
        
        x = np.linspace(FOOT_ID/2.0, FOOT_ID/2.0,n_points_straight)
        y = np.linspace(-foot_margin+FOOT_L , -foot_margin , n_points_straight)
        plt.plot(x,y,c="black")
    
            
    ################## SETS FOR POSTPROCESSING
    
    Sets_from_Edges=[[]]
    
    
    '''Set_name='My_set_DoveTail_side1'
    Set_initial_tuple=(P1[0]-5,P2[1],-1)
    Set_final_tuple=(P2[0],P3[1]+5,1)
    Sets_from_Edges[0].append(Set_name)
    Sets_from_Edges[0].append(Set_initial_tuple)
    Sets_from_Edges[0].append(Set_final_tuple)'''
      

    #print(Sets_from_Edges)
    
    Sets_from_Nodes=[[]]
    
    '''Set_name='My_set_Flange'
    Set_initial_tuple=(-800,(FL_HEIGHT/2.0)-20,-1)
    Set_final_tuple=(800,(FL_HEIGHT/2.0)+20,1)
    Sets_from_Nodes[0].append(Set_name)
    Sets_from_Nodes[0].append(Set_initial_tuple)
    Sets_from_Nodes[0].append(Set_final_tuple)
    

    
    
    #Lista_Flared_Liner_D_for_set=Lista_Flared_Liner_D[:-2 or None]
    #Lista_Flared_Liner_H_for_set=Lista_Flared_Liner_H[:-2 or None]
    
    Lista_Flared_Liner_D_for_set=Lista_Flared_Liner_D
    Lista_Flared_Liner_H_for_set=Lista_Flared_Liner_H
    
    counter=len(Lista_Flared_Liner_D_for_set)
    for i,j in zip(Lista_Flared_Liner_D_for_set,Lista_Flared_Liner_H_for_set):
        tol_incr=0
        if counter !=1:
            spacer = x_run_Rise2-i
        else:
            spacer = ellipse_center_x-i
            if counter ==3:
                tol_incr=20
        Sets_from_Nodes.append([])
        Set_name="My_set_Retraction_"+str(counter)
        Set_initial_tuple=(-i-(spacer)-10,j-20+tol_incr,-1)
        Set_final_tuple=(i+(spacer)+10,j+20+tol_incr,1)
        Sets_from_Nodes[-1].append(Set_name)
        Sets_from_Nodes[-1].append(Set_initial_tuple)
        Sets_from_Nodes[-1].append(Set_final_tuple)
        counter-=1'''
    


    # Customize the plot
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Plot of Coordinates from List of Tuples")
    plt.xlim([-10, 1000])
    plt.ylim([-100, 2500])
    plt.grid(True)
    plt.legend()
    plt.gca().set_aspect('equal', adjustable='box')

    # Show the plot
    #plt.show()


    
################################ RETURN 
    Polylist=[Polyline1,Polyline2,Polyline3,Polyline4,Polyline5,Polyline6,
              flared_thick_increase,My_Loads,Sets_from_Edges,Sets_from_Nodes,mid_length,
              Surface_kit,(mesh_size_BM,mesh_size_BSC)]
    return Polylist

import warnings
warnings.filterwarnings("ignore", message="No artists with labels found to put in legend")
################# EXECUTION ##############################


pre_coordinates= Polyline(0)
#coordinates= Polyline(pre_coordinates[6])

if pre_coordinates[6]>0:
    coordinates= Polyline(pre_coordinates[6])
    with open('output_abq.txt', 'w') as file:
        file.write(str(coordinates))
    
    coordinates_1 = coordinates[0]
    coordinates_2 = coordinates[1]
    coordinates_3 = coordinates[2]
    coordinates_4= coordinates[3]
    coordinates_5= coordinates[4]
    coordinates_6= coordinates[5]
    
elif pre_coordinates[6]==0:
    with open('output_abq.txt', 'w') as file:
        file.write(str(pre_coordinates))
    
    coordinates_1 = pre_coordinates[0]
    coordinates_2 = pre_coordinates[1]
    coordinates_3 = pre_coordinates[2]
    coordinates_4= pre_coordinates[3]
    coordinates_5= pre_coordinates[4]
    coordinates_6= pre_coordinates[5]



for my_index in range(0,len(coordinates_1)-1,2):
    point1=coordinates_1[my_index]
    point2=coordinates_1[my_index+1]
        

# Unpack the list of tuples into two separate lists: x and y
x_values_1, y_values_1 = zip(*coordinates_1)
x_values_2, y_values_2 = zip(*coordinates_2)
x_values_3, y_values_3 = zip(*coordinates_3)
x_values_4, y_values_4 = zip(*coordinates_4)
x_values_5, y_values_5 = zip(*coordinates_5)
x_values_6, y_values_6 = zip(*coordinates_6)

# Plot the points
plt.figure(figsize=(8, 8))  # Increased width for textboxes
plt.plot(x_values_1, y_values_1, marker='.', linestyle='-', label='Polyline 1')
plt.plot(x_values_2, y_values_2, marker='.', linestyle='-', label='Polyline 2')
plt.plot(x_values_3, y_values_3, marker='.', linestyle='-', label='Polyline 3')
plt.plot(x_values_4, y_values_4, marker='.', linestyle='-', label='Polyline 4')
plt.plot(x_values_5, y_values_5, marker='.', linestyle='-', label='Polyline 5')
plt.plot(x_values_6, y_values_6, marker='.', linestyle='-', label='Polyline 6')



# Customize the plot
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Plot of Coordinates from List of Tuples")
plt.xlim([-10, 1500])
plt.ylim([-100, 3500])
plt.grid(True)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()






