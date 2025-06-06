from fillet_alg import execute_fillet
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(legacy='1.25')


##############################################      SPEC DATA
def Polyline(Thickness_decrement_var):
    my_thickness_decrement=(Thickness_decrement_var)
    print("*** MY CODE *** thickness decrement is "+str(np.ceil(Thickness_decrement_var)))
    
    #Mesh size for Abaqus
    mesh_size_BSC=30.0
    mesh_size_BM=30.0
    
    #Loads
    my_SF_kN=787
    my_BM_kNm=2047
    #Adjusting for Abaqus N-mm consistent units
    My_Loads=(my_SF_kN*1000.0,my_BM_kNm*1000000.0)
    

    BSC_dim=[
    [48,1075.25,1111.25,1321,1116.4,1235],
    [46,1025.25,1061.25,1271,1066.4,1200],
    [44,975.25,1011.25,1221,1016.4,1165],
    [42,925.25,961.25,1171,966.4,1130],
    [40,875.25,911.25,1121,916.4,1095],
    [32,675.25,711.25,921,716.4,955]
    ]
    
    my_dim=44
    
    index_dim=0
    for dim in BSC_dim:
        if dim[0]==my_dim:
            my_index_dim=index_dim
        index_dim += 1
    
    #print(my_index_dim)
    ##############################################      INPUTS
    
    n_points_straight=2
    n_points_arc=8
    
    #BSN900C or BSN900E
    BSC_TYPE="BSN900E"

    #PIPE inputs
    pipe_nominal_OD=281.0
    pipe_tol=8.0
    pipe_OD=pipe_nominal_OD+pipe_tol
    
    #Flared liner inputs
    radial_clearence_pipe_flared=1.0
    FLARED_MIN_THICK=18.0
    FLARED_MARGIN=0.0
    BUILT_IN_ANGLE=7
    FLARED_RADIUS=11000
    ADJUST_TO_FORGING=0
    FLARED_IR=(pipe_OD/2.0)+radial_clearence_pipe_flared+ADJUST_TO_FORGING
    Lista_Flared_Liner_D=[]
    Lista_Flared_Liner_H=[]
    
    
    IR_FL = FLARED_IR+FLARED_MARGIN+FLARED_MIN_THICK
    OR_FL = 725.0
    FL_HEIGHT=130.0
    BCD = 964
    RCD= BCD/2.0
    BCD_hole=51
    
    
    #Hydratight tool check - HM09 or HM07 - diamter, nearest obstruction
    tension_tool="HM09"
    
    #Inferior Ellipse
    semi_axis_hor_inf=65
    semi_axis_vert_inf=180
    
    #straight_mid_segment
    mid_length=0
    
    #Superior Ellipse
    semi_axis_hor_sup=65
    semi_axis_vert_sup=180
    
    #Dovetail
    Delta_P3y_P2y=150.0
    
    th_spec=27.44
    Theta_1=22.0
    Theta_3=35.2
    #Theta_2=90.0-(Theta_1+Theta_3)
    
    l2 = Delta_P3y_P2y/np.cos(np.deg2rad(Theta_3))
    l1_hor=(np.sin(np.deg2rad(Theta_3))*l2)+th_spec
    l1_vert=np.tan(np.deg2rad(Theta_1))*l1_hor
    
    P1 = ((BSC_dim[my_index_dim][2]/2.0)-th_spec, FL_HEIGHT+(semi_axis_vert_sup+semi_axis_vert_inf+mid_length))
    P2 = (P1[0]+l1_hor, P1[1]-l1_vert)
    P3 = (BSC_dim[my_index_dim][2]/2.0, P2[1]+150)

    
    #The neck_thick is a consequence of the flange internal radius, the horizontal semi axis and the BCD and the tool.
    #If the neck thickness needs to be intentionally reduced, use the variable my_neck_reduction
    #NECK THICK calculation

    my_neck_reduction=0
    
    #outer cylinder thickness at the top
    OC_THICK=50.0
    #thickness of the top plate
    TP_THICK=55
    
    #cavity - "V" or "straight"
    Cavity_type="straight"
    if BSC_TYPE=="BSN900E":
        corr_BSN_type=BSC_dim[my_index_dim][2]/2.0-BSC_dim[my_index_dim][1]/2.0
    elif BSC_TYPE=="BSN900C":
        corr_BSN_type=0
    
    retaU_dx=(170-((48-my_dim)/2.0)*25)-my_thickness_decrement-(corr_BSN_type)+40
    #retaU_dy=10.7048
    #retaU_dx=232.5-49
    retaU_dy=30
    U_RADIUS_EXT=25
    U_RADIUS_INT=25
    
    #outer cylinder radius
    top_radius=550.0
    top_vert_y=70.0
    fillet_top_radius=10.0
    
    #INNER CYLINDER
    IC_top_thick=50.5
    IC_int_fillet=2.0
    IC_out_fillet=10.0
    
    #INTERNAL CYLINDER TYPE, 6 OR 9 STEPS
    #you need to choose between ratios or mathcad
    flared_design_option="ratios"
    STEPS_INNER_CYL=6
    
    if STEPS_INNER_CYL==9:
        if flared_design_option=="mathcad":
            L7=286
            L6=585
            L5=774
            L4=1074
            L3=1315
            
            L7+=1
            L6+=1
            L5+=1
            L4+=1
            L3+=1
            #L2=vert_span-L3 Vert span só é calculado depois. Precisou ficar embaixo
            
            D7=490
            D5=432
            D4=392
            D3=374
            D2=346
            D1=316
            
            D7+=2
            D5+=2
            D4+=2
            D3+=2
            D2+=2
            D1+=2
            
            
            Di1=300
            FLARED_IR=Di1/2
        
            
            #If "mathcad" is chosen, the Internal radius of the flange becomes D1/2
            IR_FL=D1/2
            
        if flared_design_option=="ratios":
            retraction_0=IC_top_thick-my_thickness_decrement
            retraction_ratio_1=0.2
            retraction_ratio_2=0.2
            retraction_ratio_3=0.2
            retraction_ratio_4=0.25
            retraction_ratio_5=0.15
            
            Vertical_segment_ratio_0=0.1
            Vertical_segment_ratio_1=0.2
            Vertical_segment_ratio_2=0.2
            Vertical_segment_ratio_3=0.15
            Vertical_segment_ratio_4=0.15
            Vertical_segment_ratio_5=0.2

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
            
            Vertical_segment_ratio_0=0.25
            Vertical_segment_ratio_1=0.2
            Vertical_segment_ratio_2=0.3
            Vertical_segment_ratio_3=0.25

    
    #CAVITY INPUTS
    #from the P3[1]+150 the decrement
    delta_y_for_external_arc=100
    #first segment from internal side of cavity
    Rise1=130
    # second segment from internal side of cavity
    Rise2=295
    run_Rise2=40
    
       
    #TOP STRUCTURE
    TS_HEIGHT=265
    TS_bottom_plate_thick=50
    TS_inner_thickness=44
    TS_top_pate_thick=15
    TS_OR_base_bottom=(BSC_dim[my_index_dim][1]/2.0)-15
    TS_OR_base_top=TS_OR_base_bottom-30
    TS_OR_top_bottom=TS_OR_base_top-50
    TS_OR_top_top=TS_OR_top_bottom+20
    # TS_IR_bottom. The internal radius at bottom is assigned below according to retraction 0
    # TS_IR_top. Assigned right after the TS_IR_bottom
    TS_IR_top=TS_OR_top_top-150+my_thickness_decrement
    
    
    ##############################################      BSC DRAWING
    
    #execute_fillet(P1, P2, P3, 10.0)
    
    inf_line_dove, fillet_circle_dove, sup_line_dove = execute_fillet(P1, P2, P3, 10.0)
    
    
    Polyline1=[]
    Polyline2=[]
    Polyline3=[]
    Polyline4=[]
    Polyline5=[]
    #Polyline 6 is for the bell mouth
    Polyline6=[]
    
    
    #pipe drawing
    
    x = np.linspace(pipe_OD/2.0,pipe_OD/2.0, n_points_straight)
    y = np.linspace(-200, 2000, n_points_straight)
    plt.plot(x,y,c="darkorange")
    

    if tension_tool == "HM07":
        HM=[127,280]
    elif tension_tool == "HM09":
        HM=[144.5,288]
        #Design do Patrick considera uma ferramenta otimizada
        HM=[(144.5-11),288]
    
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
    
    sup_ellipse_end_x= (IR_FL+my_thickness_decrement)+NECK_THICK+semi_axis_hor_inf


    
    if my_neck_reduction>0:
        print("My neck thickness is "+str(round(NECK_THICK,4))+", which was manually reduced by "+str(my_neck_reduction)+" mm using my_neck_reduction var")
        if (sup_ellipse_end_x-P1[0])>0:
            NECK_THICK-=(sup_ellipse_end_x-P1[0])
            print("Due to the superior ellipse horizontal length, the neck thickness was reduced by "+str(round((sup_ellipse_end_x-P1[0]),3))+" mm")
        print("My final neck thickness is "+str(round(NECK_THICK,4)))
    else:
        if (sup_ellipse_end_x-P1[0])>0:
            NECK_THICK-=(sup_ellipse_end_x-P1[0])
            print("Due to the superior ellipse horizontal length, the neck thickness was reduced by "+str(round((sup_ellipse_end_x-P1[0]),3))+" mm")
        print("My final neck thickness is "+str(round(NECK_THICK,4)))
    
    
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
    t=np.linspace(3*np.pi/2, np.pi, n_points_arc)
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
    
    
    
    #segmento6: encaixe elipse rac1
    xx = np.linspace(x[-1], P1[0], n_points_straight*2)
    yy = np.linspace(y[-1], P1[1], n_points_straight*2)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    
    #Adding the dovetail to the Polyline1
    Polyline1.extend(inf_line_dove)
    #print(inf_line_dove)
    Polyline1.extend(fillet_circle_dove)
    Polyline1.extend(sup_line_dove)
    
    
    #segmento7: reta vertical pos rac3
    if BSC_TYPE == "BSN900E":
        x = np.linspace(P3[0], P3[0], n_points_straight)
        y = np.linspace(P3[1], P3[1]+150, n_points_straight)
        plt.plot(x,y)
        Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    elif BSC_TYPE == "BSN900C":
        x = np.linspace(P3[0], P3[0], n_points_straight)
        y = np.linspace(P3[1], P3[1]+150, n_points_straight)
        plt.plot(x,y)
        Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
        
    
    #segmento8: reta inclinada de 200mm de cateto adjacente
    if BSC_TYPE == "BSN900E":
        xx = np.linspace(x[-1], BSC_dim[my_index_dim][1]/2.0, n_points_straight)
        yy = np.linspace(y[-1], P3[1]+150+200, n_points_straight)
        plt.plot(xx,yy)
        Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    elif BSC_TYPE == "BSN900C":
        xx = np.linspace(x[-1], x[-1], n_points_straight)
        yy = np.linspace(y[-1], P3[1]+150+200, n_points_straight)
        plt.plot(xx,yy)
        Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
    
    #segmento9: reta ate a circunferencia de 550mm
    x = np.linspace(xx[-1], xx[-1], n_points_straight)
    y = np.linspace(yy[-1], yy[-1]+(BSC_dim[my_index_dim][5]-150-150-200-70), n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    #segmento10: circunferencia
    angle_start = 0
    angle_end = np.arcsin((top_vert_y-fillet_top_radius)/ top_radius)
    # Generate angles for the arc between start and end angle
    angles = np.linspace(angle_start, angle_end, n_points_arc)
    # Calculate the arc points
    arc_x = (top_radius * np.cos(angles))-(top_radius-x[-1])
    arc_y = y[-1] + top_radius * np.sin(angles)
    plt.plot(arc_x,arc_y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    #FILLET BETWEEN SEGMENTS 10 AND 11
    angle_start = np.deg2rad(0)  # Start angle in radians (e.g., 0 for the positive x-axis)
    angle_end = np.pi / 2
    f_center_x=arc_x[-1]-fillet_top_radius
    f_center_y=arc_y[-1]
    angles = np.linspace(angle_start, angle_end, n_points_arc)
    # Parametric equations for the arc
    x_values = fillet_top_radius * np.cos(angles) + f_center_x
    y_values = fillet_top_radius * np.sin(angles) + f_center_y
    plt.plot(x_values, y_values, label="Arc", color='b')
    Polyline1.extend([(xi, yi) for xi, yi in zip(x_values, y_values)])
    
    
    #segmento11: ate a superficie interna do cilindro externo, usa a espessura do seg9
    corrected_OC_thick=OC_THICK-(arc_x[0]-arc_x[-1])
    x = np.linspace(arc_x[-1]-fillet_top_radius, arc_x[-1]-corrected_OC_thick, n_points_straight*2)
    y = np.linspace(arc_y[-1]+fillet_top_radius, arc_y[-1]+fillet_top_radius, n_points_straight*2)
    plt.plot(x,y)
    x_ext_top_plate_for_TS=(arc_x[-1]-fillet_top_radius)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    #Assigning the variables for surface definition in Abaqus
    Surface_kit=[]
    Surface_kit.append(inf_line_dove[-1][1]-1)
    Surface_kit.append(P3[1]+1)
    Surface_kit.append(P1[1]+1)
    Surface_kit.append(inf_line_dove[-1][0]+1)
    Surface_kit.append(P3[1]-1)
    Surface_kit.append(x_values[-1]+1)
    
    #########END OF POLYLINE1
    
    
    #This is the tiny dent for top plate support
    support_triangle_cat_op=7.5
    support_triangle_cat_adj=30.0
    xx = np.linspace(x[-1]-support_triangle_cat_op, x[-1], n_points_straight*2)
    yy = np.linspace(y[-1]-TP_THICK, y[-1]-TP_THICK-support_triangle_cat_adj, n_points_straight*2)
    plt.plot(xx,yy)
    top_plate_P1=(x[-1]-fillet_top_radius, y[-1]-TP_THICK)
    Polyline2.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #Esse segmento e o dentinho /\
    
    
    #segmento 12: ate a curva inferior do outer cylinder
    xx = np.linspace(x[-1], x[-1], n_points_straight)
    yy = np.linspace(y[-1]-TP_THICK-support_triangle_cat_adj, P3[1]+150-delta_y_for_external_arc, n_points_straight)
    plt.plot(xx,yy)
    top_plate_P1=(x[-1]-10, y[-1]-TP_THICK)
    Polyline2.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    
    #segmento 13:arco externo do U
    angles = np.linspace(0, -np.pi/2.0, n_points_arc)
    angles = np.linspace(0, -np.deg2rad(94), n_points_arc)
        # Calculate the arc points
    arc_x = (U_RADIUS_EXT * np.cos(angles))+xx[-1]-U_RADIUS_EXT
    arc_y =  (U_RADIUS_EXT * np.sin(angles))+yy[-1]
    plt.plot(arc_x,arc_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    #segmento 14: reta do U inclinada
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
        

    #segmento 15: arco do U interno
    angle_start = -np.arcsin(retaU_dy/retaU_dx)-np.pi/2
    angle_end = -np.pi
        # Generate angles for the arc between start and end angle
    angles = np.linspace(angle_start, angle_end, n_points_arc)
        # Calculate the arc points
    arc_x = (U_RADIUS_INT * np.cos(angles))-(U_RADIUS_INT*np.cos(angle_start))+x[-1]
    arc_y = U_RADIUS_INT * np.sin(angles)-U_RADIUS_INT*np.sin(angle_start)+y[-1]
    plt.plot(arc_x,arc_y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    
    #segmento 16: porcao reta acima do U interno
    x = np.linspace(arc_x[-1], arc_x[-1], n_points_straight)
    y = np.linspace(arc_y[-1], arc_y[-1]+Rise1, n_points_straight)
    plt.plot(x,y)
    Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    Internal_cavity_radius_x=arc_x[-1]
    Internal_cavity_radius_y=arc_y[-1]
    
    
    #Second segment from inner side of cavity
    xx = np.linspace(x[-1], x[-1]+run_Rise2, n_points_straight)
    yy = np.linspace(y[-1], y[-1]+Rise2, n_points_straight)
    plt.plot(xx,yy)
    x_run_Rise2=x[-1]+run_Rise2 #this will be used for abaqus set construction
    Polyline2.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    #segmento 18: porcao reta ate o topo
    x = np.linspace(xx[-1], xx[-1], n_points_straight)
    y = np.linspace(yy[-1], BSC_dim[my_index_dim][5]+P2[1]-TP_THICK, n_points_straight)
    plt.plot(x,y)
    top_plate_P2=(xx[-1],BSC_dim[my_index_dim][5]+P2[1]-TP_THICK)
    Polyline2.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    #############END OF POLYLINE 2
    
    #Internal side of BSC
    hor_span=x[-1]-IR_FL-my_thickness_decrement
    vert_span=y[-1]+TP_THICK
    
    print("My vertical span is " + str(round(vert_span,4)))
    print("My horizontal span - ic_thick is " + str(round(hor_span-IC_top_thick,4)))
    
    if STEPS_INNER_CYL ==6:
        if flared_design_option == "ratios":
            retraction_0=IC_top_thick#my_thickness_decrement
            retraction_1=((hor_span-retraction_0))*retraction_ratio_1
            retraction_2=((hor_span-retraction_0))*retraction_ratio_2
            retraction_3=((hor_span-retraction_0))*retraction_ratio_3
            
    
        #segmento 19: espessura do inner cylinder at top
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1], D6/2, n_points_straight)
        else:
            xx = np.linspace(x[-1], x[-1]-retraction_0, n_points_straight)
        yy = np.linspace(y[-1]+TP_THICK, y[-1]+TP_THICK, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        x_int_top_plate_for_TS=xx[-1]
        Lista_Flared_Liner_D.append((xx[-1]))
        Lista_Flared_Liner_H.append((y[-1]+TP_THICK))
        
        #segmento 20: 0/5 segmento inclinado de cima pra baixo
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1], D3/2, n_points_straight)
            y = np.linspace(yy[-1], vert_span-L5, n_points_straight)
        else:
            x = np.linspace(xx[-1], xx[-1]-retraction_1, n_points_straight)
            y = np.linspace(yy[-1], yy[-1]-vert_span*Vertical_segment_ratio_0, n_points_straight)
        plt.plot(x,y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        Lista_Flared_Liner_D.append(round(x[-1],6))
        Lista_Flared_Liner_H.append(round(y[-1],6))
        
        #segmento 21: 1/5 segmento de cima pra baixo
        xx = np.linspace(x[-1], x[-1], n_points_straight)
        if flared_design_option == "mathcad":
            yy = np.linspace(y[-1], vert_span-L4, n_points_straight)
        else:
            yy = np.linspace(y[-1], y[-1]-(vert_span*Vertical_segment_ratio_1)+IC_int_fillet, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
    
        #segmento 22: 2/5 segmento horizontal
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight*6)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, D2/2+IC_out_fillet, n_points_straight*6)
            Lista_Flared_Liner_D.append(round(D2/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_2+IC_out_fillet, n_points_straight*6)
            Lista_Flared_Liner_D.append(round(xx[-1]-retraction_2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        plt.plot(x,y)
        
        #FILLET_RADIUS 1-int
        angles = np.linspace(0,-np.pi/2, n_points_arc)
        arc_x = (IC_int_fillet * np.cos(angles))+x[0]
        arc_y = IC_int_fillet * np.sin(angles)+y[0]+IC_int_fillet
        plt.plot(arc_x,arc_y)
        
        #A ordem do polyline3.extend precisa ser diferente da ordem de plotar o BSC drawing  para esse degrau com fillet
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        
        #FILLET_RADIUS 1-ext
        angles = np.linspace(np.pi/2, np.pi, n_points_arc)
        arc_x = (IC_out_fillet * np.cos(angles))+x[-1]
        arc_y = IC_out_fillet * np.sin(angles)+y[-1]-IC_out_fillet
        plt.plot(arc_x,arc_y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        
        
        #segmento 23: 3/5 segmento de cima pra baixo
        
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1]-IC_out_fillet, D2/2, n_points_straight)
            yy = np.linspace(y[-1]-IC_out_fillet, vert_span-L3 , n_points_straight)
        else:
            xx = np.linspace(x[-1]-IC_out_fillet, x[-1]-IC_out_fillet, n_points_straight)
            yy = np.linspace(y[-1]-IC_out_fillet, y[-1]-vert_span*Vertical_segment_ratio_2, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
        
        #segmento 24: 4/5 segmento horizontal
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight*6)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, D1/2+IC_out_fillet, n_points_straight*6)
            Lista_Flared_Liner_D.append(round(D1/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_3+IC_out_fillet, n_points_straight*6)
            Lista_Flared_Liner_D.append(round(xx[-1]-retraction_3,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        plt.plot(x,y)
        
        #FILLET_RADIUS 2-int
        angles = np.linspace(0,-np.pi/2, n_points_arc)
        arc_x = (IC_int_fillet * np.cos(angles))+x[0]
        arc_y = IC_int_fillet * np.sin(angles)+y[0]+IC_int_fillet
        plt.plot(arc_x,arc_y)
        
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        #FILLET_RADIUS 2-ext
        angles = np.linspace(np.pi/2, np.pi, n_points_arc)
        arc_x = (IC_out_fillet * np.cos(angles))+x[-1]
        arc_y = IC_out_fillet * np.sin(angles)+y[-1]-IC_out_fillet
        plt.plot(arc_x,arc_y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        
        
        #segmento 25: 5/5 segmento de cima pra baixo
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1]-IC_out_fillet, D1/2, n_points_straight)
            yy = np.linspace(y[-1]-IC_out_fillet, 0, n_points_straight)
        else:
            xx = np.linspace(x[-1]-IC_out_fillet, x[-1]-IC_out_fillet, n_points_straight)
            yy = np.linspace(y[-1]-IC_out_fillet, y[-1]-vert_span*Vertical_segment_ratio_3+IC_int_fillet, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        #END OF POLYLINE3
        
        
    if STEPS_INNER_CYL ==9:
        
        if flared_design_option == "ratios":
            retraction_0=IC_top_thick#-my_thickness_decrement
            retraction_1=((hor_span-retraction_0))*retraction_ratio_1
            retraction_2=((hor_span-retraction_0))*retraction_ratio_2
            retraction_3=((hor_span-retraction_0))*retraction_ratio_3
            retraction_4=((hor_span-retraction_0))*retraction_ratio_4
            retraction_5=((hor_span-retraction_0))*retraction_ratio_5

            
        #segmento 19: espessura do inner cylinder at top
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1], (D7/2),n_points_straight*2)
        else:
            xx = np.linspace(x[-1], x[-1]-retraction_0,n_points_straight*2)
        yy = np.linspace(y[-1]+TP_THICK, y[-1]+TP_THICK, n_points_straight*2)
        plt.plot(xx,yy)
        x_int_top_plate_for_TS=xx[-1]
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        Lista_Flared_Liner_D.append(round(xx[-1],6))
        Lista_Flared_Liner_H.append(round(yy[-1],6))
        
        #segmento 20: 0/6 segmento inclinado de cima pra baixo

        if flared_design_option == "mathcad":
            x =  np.linspace(xx[-1], (D5/2),n_points_straight)
            y = np.linspace(yy[-1], vert_span-L7, n_points_straight)
        else:
            x = np.linspace(xx[-1], xx[-1]-retraction_1,n_points_straight)
            y = np.linspace(yy[-1], yy[-1]-vert_span*Vertical_segment_ratio_0, n_points_straight)
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        plt.plot(x,y)
        Lista_Flared_Liner_D.append(round(x[-1],6))
        #Lista_Flared_Liner_H.append(round(yy[-1]-vert_span*Vertical_segment_ratio_0,6))
        Lista_Flared_Liner_H.append(round(y[-1],6))
        
        #segmento 21: 1/6 segmento de cima pra baixo
        xx = np.linspace(x[-1], x[-1],n_points_straight)
        if flared_design_option == "mathcad":
            yy = np.linspace(y[-1], vert_span-L6+IC_int_fillet, n_points_straight)
        else:
            yy = np.linspace(y[-1], y[-1]-vert_span*Vertical_segment_ratio_1+IC_int_fillet, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
        #segmento 22: 2/6 segmento horizontal
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight*4)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, (D4/2),n_points_straight*4)
            Lista_Flared_Liner_D.append(round(D4/2,6))
            Lista_Flared_Liner_H.append(round(y[-1],6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_2+IC_out_fillet,n_points_straight*4)
            Lista_Flared_Liner_D.append(round(xx[-1]-retraction_2,6))
            Lista_Flared_Liner_H.append(round(y[-1],6))
        plt.plot(x,y)
        
        #FILLET_RADIUS 1-int
        angles = np.linspace(0,-np.pi/2, n_points_arc)
        arc_x = (IC_int_fillet * np.cos(angles))+x[0]
        arc_y = IC_int_fillet * np.sin(angles)+y[0]+IC_int_fillet
        plt.plot(arc_x,arc_y)
        
        #A ordem do polyline3.extend precisa ser diferente da ordem de plotar o BSC drawing  para esse degrau com fillet
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        #FILLET_RADIUS 1-ext
        angles = np.linspace(np.pi/2, np.pi, n_points_arc)
        arc_x = (IC_out_fillet * np.cos(angles))+x[-1]
        arc_y = IC_out_fillet * np.sin(angles)+y[-1]-IC_out_fillet
        plt.plot(arc_x,arc_y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        
        #segmento 23: 3/6 segmento de cima pra baixo
        xx = np.linspace(x[-1]-IC_out_fillet, x[-1]-IC_out_fillet,n_points_straight)
        if flared_design_option == "mathcad":
            yy = np.linspace(vert_span-L6-IC_out_fillet, vert_span-L5, n_points_straight)
        else:
            yy = np.linspace(y[-1]-IC_out_fillet, y[-1]-vert_span*Vertical_segment_ratio_2+IC_int_fillet, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
        
        #segmento 24: 3/6 segmento horizontal
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight*4)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, (D3/2),n_points_straight*4)
            Lista_Flared_Liner_D.append(round(D3/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_3+IC_out_fillet,n_points_straight*4)
            Lista_Flared_Liner_D.append(round(xx[-1]-retraction_3,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        plt.plot(x,y)
        
        #FILLET_RADIUS 2-int
        angles = np.linspace(0,-np.pi/2, n_points_arc)
        arc_x = (IC_int_fillet * np.cos(angles))+x[0]
        arc_y = IC_int_fillet * np.sin(angles)+y[0]+IC_int_fillet
        plt.plot(arc_x,arc_y)
        
        #A ordem do polyline3.extend precisa ser diferente da ordem de plotar o BSC drawing  para esse degrau com fillet
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        #FILLET_RADIUS 2-ext
        angles = np.linspace(np.pi/2, np.pi, n_points_arc)
        arc_x = (IC_out_fillet * np.cos(angles))+x[-1]
        arc_y = IC_out_fillet * np.sin(angles)+y[-1]-IC_out_fillet
        plt.plot(arc_x,arc_y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        
        #segmento 25: 4/6 segmento de cima pra baixo
        xx = np.linspace(x[-1]-IC_out_fillet, x[-1]-IC_out_fillet,n_points_straight)
        if flared_design_option == "mathcad":
            yy = np.linspace(vert_span-L5-IC_out_fillet-IC_int_fillet, vert_span-L4, n_points_straight)
        else:
            yy = np.linspace(y[-1]-IC_out_fillet, y[-1]-vert_span*Vertical_segment_ratio_3+IC_int_fillet, n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
        #segmento 26: 4/6 segmento horizontal
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight*4)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, (D2/2),n_points_straight*4)
            Lista_Flared_Liner_D.append(round(D2/2,6))
            Lista_Flared_Liner_H.append(yy[-1]-IC_int_fillet)
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_4+IC_out_fillet,n_points_straight*4)
            Lista_Flared_Liner_D.append(xx[-1]-retraction_4)
            Lista_Flared_Liner_H.append(yy[-1]-IC_int_fillet)
        plt.plot(x,y)

        
        #FILLET_RADIUS 3-int
        angles = np.linspace(0,-np.pi/2, n_points_arc)
        arc_x = (IC_int_fillet * np.cos(angles))+x[0]
        arc_y = IC_int_fillet * np.sin(angles)+y[0]+IC_int_fillet
        plt.plot(arc_x,arc_y)
        
        #A ordem do polyline3.extend precisa ser diferente da ordem de plotar o BSC drawing  para esse degrau com fillet
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        #FILLET_RADIUS 3-ext
        angles = np.linspace(np.pi/2, np.pi, n_points_arc)
        arc_x = (IC_out_fillet * np.cos(angles))+x[-1]
        arc_y = IC_out_fillet * np.sin(angles)+y[-1]-IC_out_fillet
        plt.plot(arc_x,arc_y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
        
        #segmento 27: 5/6 segmento inclinado de cima pra baixo
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1]-IC_out_fillet, (D1/2),n_points_straight)
            yy = np.linspace(vert_span-L4-IC_out_fillet-IC_int_fillet, vert_span-L3, n_points_straight)
            Lista_Flared_Liner_D.append(round(D1/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1],6))
        else:
            xx = np.linspace(x[-1]-IC_out_fillet, x[-1]-IC_out_fillet-retraction_5,n_points_straight)
            yy = np.linspace(y[-1]-IC_out_fillet, y[-1]-vert_span*Vertical_segment_ratio_4, n_points_straight)
            Lista_Flared_Liner_D.append(round(xx[-1],6))
            Lista_Flared_Liner_H.append(round(yy[-1],6))
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])

        
        #segmento 27: 6/6 segmento de cima pra baixo
        x = np.linspace(xx[-1], xx[-1],n_points_straight)
        if flared_design_option == "mathcad":
            y = np.linspace(vert_span-L3, 0, n_points_straight)
        else:
            y = np.linspace(yy[-1], yy[-1]-(vert_span*Vertical_segment_ratio_5), n_points_straight)
        plt.plot(x,y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        Lista_Flared_Liner_D.append(round(x[-1],6))
        Lista_Flared_Liner_H.append(round(y[-1],6))
        
    
    top_plate_horizontal_length = round(x_ext_top_plate_for_TS-x_int_top_plate_for_TS,2)
    ######## END OF POLYLINE 3
    
    #drawing top plate inferior and superior edges
    x = np.linspace(top_plate_P1[0]+fillet_top_radius-support_triangle_cat_op, top_plate_P2[0],n_points_straight*6)
    y = np.linspace(top_plate_P1[1], top_plate_P2[1], n_points_straight*6)
    plt.plot(x,y)
    Polyline4.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    ######## END OF POLYLINE 4
    

    xx = np.linspace(top_plate_P1[0]+fillet_top_radius, top_plate_P2[0],n_points_straight*6)
    yy = np.linspace(top_plate_P1[1]+TP_THICK, top_plate_P2[1]+TP_THICK, n_points_straight*6)
    plt.plot(xx,yy)
    Polyline5.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    ######## END OF POLYLINE 5
    
    ####################### TOP STRUCTURE ##############################
    '''Lista_Flared_Liner_H.append(vert_span)
    Lista_Flared_Liner_D.append(TS_IR_top)
    
    Lista_Flared_Liner_H.append(vert_span+TS_HEIGHT)
    Lista_Flared_Liner_D.append(TS_IR_top)'''
    
    
    
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
        

    
    ##################### BELL MOUTH
    
    # the internal diameter dimensions come from the finished drawing, while the heights come from the welded BM drawging
    #pol, smallID, largeID, outerD, BottomD, G, H, K, J, hub diameter , Radius, flange thickness

    BM_dim=[
        [48, 1079.1, 1115.1, 1219.2, 1673.8, 1784.4, 805.9, 600, 300, 1343.2, 23.88, 233.43],
        [46, 1029.1, 1065.1, 1168.4, 1623.8, 1733.5, 814.0, 610, 290, 1292.4, 22.35, 225.55],
        [44, 979.1, 1015.1, 1117.6,1573.8, 1647.9, 834.3, 620, 280, 1235.0, 22.35, 214.38],
        [42, 929.1, 965.1, 1066.8, 1523.8, 1562.1, 853.6, 630, 270, 1176.3, 20.57, 206.25],
        [40, 879.1, 915.1, 1016.0, 1473.8, 1511.3, 861.5, 640, 260, 1127.3, 20.57, 196.85],
        [38, 829.1, 865.1, 963.2, 1423.8, 1460.5, 872.4, 650, 250, 1073.2, 19.05, 190.50], #1460.5 repeats on the ref table. It seems wrong
        [36, 779.1, 815.1, 914.4, 1373.8, 1460.5, 863.0, 660, 240, 1063.8, 14.22, 171.45],
        [34, 729.1, 765.1, 863.6, 1323.8, 1397.0, 875.7, 660, 240, 1006.4, 14.22, 165.10],
        [32, 679.1, 715.1, 812.8, 1273.8, 1314.5, 894.8, 670, 230, 946.15, 12.70, 158.75],
        [30, 629.1, 665.1, 762.0, 1223.8, 1231.9, 913.8, 680, 220, 889.0, 12.70, 149.35],
        [28, 579.1, 615.1, 711.2, 1173.8, 1168.4, 926.5, 690, 210, 831.85, 12.70, 142.75],
        [26, 529.1, 565.1, 660.4, 1123.7, 1085.9, 939.2, 700, 200, 774.7, 11.18, 139.70],
        ]
    
    BM_thick=47.7
    BM_angle=35.75
    BM_length=1525.0
    web_height=300.0
    large_radius= BM_dim[my_index_dim][2]/2.0
    transition_length = BM_dim[my_index_dim][8]
    small_radius = BM_dim[my_index_dim][1]/2.0
    small_radius_length = BM_dim[my_index_dim][7]
    bottom_radius = BM_dim[my_index_dim][3]/2.0
    height_minus_flange = BM_dim[my_index_dim][6]
    BM_flange_thick = BM_dim[my_index_dim][11]
    BM_hub_radius = BM_dim[my_index_dim][9]/2.0
    BM_flange_radius = BM_dim[my_index_dim][5]/2.0
    
    if BSC_TYPE == "BSN900C":
        small_radius=large_radius
        
    
    x = np.linspace(small_radius, small_radius,n_points_straight)
    y = np.linspace(BM_length+P3[1]-web_height, BM_length+P3[1]-web_height-small_radius_length, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(small_radius, large_radius,n_points_straight)
    y = np.linspace(BM_length+P3[1]-web_height-small_radius_length, BM_length+P3[1]-web_height-small_radius_length-transition_length, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius, large_radius,n_points_straight)
    y = np.linspace(BM_length+P3[1]-web_height-small_radius_length-transition_length, P3[1], n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius, large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height) ,n_points_straight)
    y = np.linspace(P3[1], P3[1]-web_height, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height) ,large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height)+ BM_thick*np.cos(np.deg2rad(BM_angle)), n_points_straight*2)
    y = np.linspace(P3[1]-web_height, P3[1]-web_height+ BM_thick*np.sin(np.deg2rad(BM_angle)), n_points_straight*2)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height)+ BM_thick*np.cos(np.deg2rad(BM_angle)) , bottom_radius, n_points_straight)
    y = np.linspace(P3[1]-web_height+ BM_thick*np.sin(np.deg2rad(BM_angle)), P3[1], n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(bottom_radius , bottom_radius, n_points_straight)
    y = np.linspace(P3[1],P3[1]+height_minus_flange, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(bottom_radius , BM_hub_radius, n_points_straight)
    y = np.linspace(P3[1]+height_minus_flange, (P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick) , n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_hub_radius , BM_flange_radius, n_points_straight)
    y = np.linspace((P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick), (P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick) , n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_flange_radius , BM_flange_radius, n_points_straight)
    y = np.linspace((P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick) , (P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick) + BM_flange_thick, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_flange_radius , small_radius, n_points_straight)
    y = np.linspace((P3[1]+height_minus_flange) + (BM_length-web_height-height_minus_flange-BM_flange_thick) + BM_flange_thick , BM_length+P3[1]-web_height, n_points_straight)
    plt.plot(x,y,c='blueviolet')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    ##################### CREO ##############################
    display_CREO=0
    
    if display_CREO>0:
        print(vert_span)
        # Define your variables
        var1 = 1674 + 1
        var2 = 1235
        var3 = OR_FL*2
        var4 = FL_HEIGHT
        var5 = IR_FL*2
        var6 = P3[1]+150
        var7 = P3[1]+100
        var8 = semi_axis_hor_inf
        var9 = semi_axis_vert_inf
        var10 = (IR_FL+NECK_THICK)*2
        var11 = U_RADIUS_INT
        var12 = U_RADIUS_EXT
        var13 = BSC_dim[my_index_dim][2]
        
        var14= 40 #pq e 40 no txt do Patrick? qual a referencia?
        var15= 555
        var16= (top_plate_P2[0]-IC_top_thick)*2
    
        
        var17= vert_span - (P2[1]+150+150-50)# o 50 vai ser sempre 50?
        var18= BSC_dim[my_index_dim][1]
        var19= BSC_dim[my_index_dim][1]-(2*OC_THICK) 
        var20= vert_span - (P2[1]+150+150+200)
        var21= vert_span - (P2[1]+150+150)
        
        var22= TP_THICK
        
        # Use f-strings to embed the variables in the string
        My_txt = f"""
        /*---FLANGE
        /*---The total and davetail length need to be reajust to match the length from BSC flange to TS lock plus +1.
        F_TOTAL_L={var1}
        F__DAVETAIL_L={var2}
        F_OD_FLANGE={var3}
        F_T_FLANGE={var4}
        F_ID_FLANGE={var5}
        F_H_INNER={var6}
        F_H_OUTER={var7}
        F_X_ELIPSE={var8}
        F_Y_ELIPSE={var9}
        F_OD_NECK={var10}
        F_TOOTH_R_INNER={var11}
        F_TOOTH_R_OUTER={var12}
        F_OD_OUTERTUBE={var13}
        
        /*---INNER TUBE
        I_H_UNDERCUT={var14}
        I_H_UPPERCUT={var15}
        I_OD_INNERTUBE={var16}
        
        /*---OUTER TUBE
        O_H_OUTERTUBE={var17}
        O_OD_OUTERTUBE={var18}
        O_ID_OUTERTUBE={var19}
        O_H2_OUTERTUBE={var20}
        O_H3_OUTERTUBE={var21}
        
        /*TOP PLATE
        TP_T={var22}
        
        """
        
        print(My_txt)
    
    
    ##################### FORGINGS
    
    display_forgings=1
    
    if display_forgings>0:
    
        #inner tube
        #580/320/950
        #645/385/950
        
        #outer tube
        
        My_forging="Custom"
        
        if My_forging == "Custom":
            
            IFOR_H = 885
            IFOR_ID=320
            IFOR_OD=690
            IFOR_thick=(IFOR_OD-IFOR_ID)/2.0
            
            OFOR_H=935
            OFOR_ID=850
            OFOR_OD=1035
            OFOR_thick=(OFOR_OD-OFOR_ID)/2.0
            
            foot_margin=10
            FOOT_ID= 290
            FOOT_OD_FL= 1500
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
    
    Sets_from_Edges=[[],[],[]]
    
    
    Set_name='My_set_DoveTail_side1'
    Set_initial_tuple=(P1[0]-5,P2[1],-1)
    Set_final_tuple=(P2[0],P3[1]+5,1)
    Sets_from_Edges[0].append(Set_name)
    Sets_from_Edges[0].append(Set_initial_tuple)
    Sets_from_Edges[0].append(Set_final_tuple)
    
    Set_name='My_set_Cavity_side1'
    Set_initial_tuple=(Internal_cavity_radius_x-5,P3[1],-1)
    Set_final_tuple=(P3[0]-OC_THICK,Internal_cavity_radius_y+5,1)
    Sets_from_Edges[1].append(Set_name)
    Sets_from_Edges[1].append(Set_initial_tuple)
    Sets_from_Edges[1].append(Set_final_tuple)
    
    Set_name='My_set_Cavity_side2'
    Set_initial_tuple=((P3[0]-OC_THICK)*-1,P3[1],-1)
    Set_final_tuple=((Internal_cavity_radius_x-5)*-1,Internal_cavity_radius_y+5,1)
    Sets_from_Edges[2].append(Set_name)
    Sets_from_Edges[2].append(Set_initial_tuple)
    Sets_from_Edges[2].append(Set_final_tuple)
       

    #print(Sets_from_Edges)
    
    Sets_from_Nodes=[[],[],[],[],[],[],[],[],[],[]]
    
    Set_name='My_set_Flange'
    Set_initial_tuple=(-800,(FL_HEIGHT/2.0)-20,-1)
    Set_final_tuple=(800,(FL_HEIGHT/2.0)+20,1)
    Sets_from_Nodes[0].append(Set_name)
    Sets_from_Nodes[0].append(Set_initial_tuple)
    Sets_from_Nodes[0].append(Set_final_tuple)
    
    Set_name='My_set_Neck_thickness'
    Set_initial_tuple=(-800,FL_HEIGHT+semi_axis_vert_inf+(mid_length/2.0)-20,-1)
    Set_final_tuple=(800,FL_HEIGHT+semi_axis_vert_inf+(mid_length/2.0)+20,1)
    Sets_from_Nodes[1].append(Set_name)
    Sets_from_Nodes[1].append(Set_initial_tuple)
    Sets_from_Nodes[1].append(Set_final_tuple)
    
    Set_name='My_set_Outer_tube_side1'
    Set_initial_tuple=(P3[0]-100,P3[1]+150-delta_y_for_external_arc,-1)
    Set_final_tuple=(800,P3[1]+150-delta_y_for_external_arc+40,1)
    Sets_from_Nodes[2].append(Set_name)
    Sets_from_Nodes[2].append(Set_initial_tuple)
    Sets_from_Nodes[2].append(Set_final_tuple)
    
    Set_name='My_set_Outer_tube-side2'
    Set_initial_tuple=(-800,P3[1]+150-delta_y_for_external_arc,-1)
    Set_final_tuple=(-P3[0]+100,P3[1]+150-delta_y_for_external_arc+50,1)
    Sets_from_Nodes[3].append(Set_name)
    Sets_from_Nodes[3].append(Set_initial_tuple)
    Sets_from_Nodes[3].append(Set_final_tuple)
    
    Set_name='My_set_Inner_tube'
    Set_initial_tuple=(-Internal_cavity_radius_x-5,Internal_cavity_radius_y,-1)
    Set_final_tuple=(Internal_cavity_radius_x+5,Internal_cavity_radius_y+50,1)
    Sets_from_Nodes[4].append(Set_name)
    Sets_from_Nodes[4].append(Set_initial_tuple)
    Sets_from_Nodes[4].append(Set_final_tuple)
    
    Set_name='My_set_Top_plate'
    Set_initial_tuple=(-800,top_plate_P2[1]+(TP_THICK/2.0)-10,-1)
    Set_final_tuple=(800,top_plate_P2[1]+(TP_THICK/2.0)+10,1)
    Sets_from_Nodes[5].append(Set_name)
    Sets_from_Nodes[5].append(Set_initial_tuple)
    Sets_from_Nodes[5].append(Set_final_tuple)
    
    Set_name='My_set_top-plate-for-thick-calc'
    Set_initial_tuple=(top_plate_P2[0]+10,top_plate_P2[1]+(TP_THICK/2.0)-100,-1)
    Set_final_tuple=(top_plate_P1[0]-10,top_plate_P2[1]+(TP_THICK/2.0)+100,1)
    Sets_from_Nodes[6].append(Set_name)
    Sets_from_Nodes[6].append(Set_initial_tuple)
    Sets_from_Nodes[6].append(Set_final_tuple)
    
    Set_name='My_set_Ellipse_side1_node'
    Set_initial_tuple=(ellipse_center_x-semi_axis_hor_inf-5,FL_HEIGHT-5,-1)
    Set_final_tuple=(ellipse_center_x,P1[1]+5,1)
    Sets_from_Nodes[7].append(Set_name)
    Sets_from_Nodes[7].append(Set_initial_tuple)
    Sets_from_Nodes[7].append(Set_final_tuple)

    Set_name='My_set_Ellipse_side2_node'
    Set_initial_tuple=(ellipse_center_x*-1,FL_HEIGHT-5,-1)
    Set_final_tuple=((ellipse_center_x-semi_axis_hor_inf-5)*-1,P1[1]+5,1)
    Sets_from_Nodes[8].append(Set_name)
    Sets_from_Nodes[8].append(Set_initial_tuple)
    Sets_from_Nodes[8].append(Set_final_tuple)
    
    Set_name='My_set_DoveTail_side1_node'
    Set_initial_tuple=(P1[0]-5,P2[1],-1)
    Set_final_tuple=(P2[0],P3[1]+5,1)
    Sets_from_Nodes[9].append(Set_name)
    Sets_from_Nodes[9].append(Set_initial_tuple)
    Sets_from_Nodes[9].append(Set_final_tuple)
    
    
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
        counter-=1
    


############################### TEXT BOXES

    if flared_design_option=="ratios":
        my_font_size=8
    
    
        # Adding top textbox for BSC type
        left_text = "BSC type: "+ str(BSC_TYPE) +" - "+str(my_dim)+"in"
        plt.gcf().text(0.4, 0.95, left_text, va='center', ha='left', fontsize=my_font_size+2,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgrey", edgecolor="black"))
    
        # Adding left textbox for ellipse
        
        left_text = "P3x - P1x: "+str(th_spec)+"\n"
        plt.gcf().text(0.1, 0.9, left_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightblue", edgecolor="blue"))
        
        left_text = "Lower hor semi axis: "+str(semi_axis_hor_inf)+"\n"+\
        "Lower vert semi axis: "+str(semi_axis_vert_inf)+"\n"+\
        "Mid length: "+str(mid_length)+"\n"+ \
        "Upper hor semi axis: "+str(semi_axis_hor_sup)+"\n"+\
        "Upper vert semi axis: "+str(semi_axis_vert_sup)+"\n"
        plt.gcf().text(0.1, 0.80, left_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightblue", edgecolor="blue"))
        
        # Adding left textbox for flange information
        left_text = "BCD: "+str(BCD)+"\n"+"Bolt: M"+str(BCD_hole-3)+"\n"+\
        "Tool: "+str(tension_tool)+"\n"+\
        "Flange Internal diameter: "+str(round((IR_FL+my_thickness_decrement)*2,2))+"\n"+\
        "Flange External diameter: "+str(OR_FL*2)+"\n"+\
        "Flange thickness: "+str(FL_HEIGHT)+"\n"
        plt.gcf().text(0.1, 0.65, left_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightblue", edgecolor="blue"))
        
        # Adding left textbox for cavity information
        left_text = "Cavity depth: "+str(delta_y_for_external_arc)+"\n" + "Rise 1: "+str(Rise1)+"\n" +\
        "Rise2: "+str(Rise2)+"\n" + "Run: "+str(run_Rise2)+"\n" +\
        "Ext radius: "+str(U_RADIUS_EXT)+"\n" + "Int radius: "+str(U_RADIUS_INT)+"\n"+\
        "Hor distance: " + str(round(retaU_dx,2)) + "\n" + "Vert distance: " + str(round(retaU_dy,2))
        plt.gcf().text(0.1, 0.50, left_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightblue", edgecolor="blue"))
        
        # Adding left textbox for thickness information
        left_text = "IC top thickness: "+str(IC_top_thick)+"\n" + "OC top thickness: "+str(OC_THICK)+"\n" +\
        "Top plate thickness: "+str(TP_THICK)+"\n"
        plt.gcf().text(0.1, 0.35, left_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightblue", edgecolor="blue"))
        
        ##############################################  RIGHT SIDE
        
        # Adding right textbox for pipe information
        right_text = "Pipe OD + tol: " + str(pipe_OD)
        plt.gcf().text(0.7, 0.90, right_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
        
        right_text = "BM: "+str(my_BM_kNm)+" KNm\n" + "SF: " + str(my_SF_kN) + " kN\n" +\
        "Mesh size BSC: " + str(mesh_size_BSC) + "\n" + "Mesh size Bell mouth: " +str(mesh_size_BM)
        plt.gcf().text(0.7, 0.825, right_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
        
        right_text = "Top hor length: "+str(top_plate_horizontal_length)
        plt.gcf().text(0.7, 0.75, right_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
        
        right_text = "Neck thickness: "+str(round(NECK_THICK,2)) + "\n" +\
        "Neck reduction: "+str(my_neck_reduction)
        plt.gcf().text(0.7, 0.70, right_text, va='center', ha='left', fontsize=my_font_size,
        bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
        
        
        if STEPS_INNER_CYL==6:
            # Adding left textbox for flared liner information
            right_text = "Flared liner type: "+str(STEPS_INNER_CYL)+" steps\n" +\
            "Flared liner radius: "+str(FLARED_RADIUS)+"\n" + "Built-in angle: "+str(BUILT_IN_ANGLE)+"+(2)°\n" + \
            "Total height: "+str(round(available_length,2))+"\n" + "Straight height: "+str(round(straight_length,2))+"\n" +\
            "Curve height: "+str(round(available_length-straight_length,2))+"\n" + "Top structure height: "+str(TS_HEIGHT)
            plt.gcf().text(0.7, 0.6, right_text, va='center', ha='left', fontsize=my_font_size,
            bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
            
            right_text = "Flared liner type: "+str(STEPS_INNER_CYL)+" steps\n" +\
            "Inner surface points bottom to top (Diameter, Height):\n" +\
            "First point: ("+str(round(Lista_Flared_Liner_D[3],2)) +", "+str(0.0)+")\n" +\
            "Second point: ("+str(round(Lista_Flared_Liner_D[3],2)) +", "+str(round(Lista_Flared_Liner_H[3],2))+")\n" +\
            "Third point: ("+str(round(Lista_Flared_Liner_D[2],2)) +", "+str(round(Lista_Flared_Liner_H[3],2))+")\n" +\
            "Fourth point: ("+str(round(Lista_Flared_Liner_D[2],2)) +", "+str(round(Lista_Flared_Liner_H[2],2))+")\n" +\
            "Fifth point: ("+str(round(Lista_Flared_Liner_D[1],2)) +", "+str(round(Lista_Flared_Liner_H[2],2))+")\n" +\
            "Sixth point: ("+str(round(Lista_Flared_Liner_D[1],2)) +", "+str(round(Lista_Flared_Liner_H[1],2))+")\n" +\
            "Seventh point: ("+str(round(Lista_Flared_Liner_D[0],2)) +", "+str(round(Lista_Flared_Liner_H[0],2))+")\n"
            plt.gcf().text(0.7, 0.43, right_text, va='center', ha='left', fontsize=my_font_size,
            bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
                
            right_text = "Flared liner type: "+str(STEPS_INNER_CYL)+" steps\n" +\
            "L0: "+str(round(vert_span*Vertical_segment_ratio_0,2))+"\n" +\
            "L1: "+str(round(vert_span*Vertical_segment_ratio_1,2))+"\n" +\
            "L2: "+str(round(vert_span*Vertical_segment_ratio_2,2))+"\n" +\
            "L3: "+str(round(vert_span*Vertical_segment_ratio_3,2))+"\n" +\
            "Retraction 1: "+str(round(retraction_1,2))+"\n" +\
            "Retraction 2: "+str(round(retraction_2,2))+"\n" +\
            "Retraction 3: "+str(round(retraction_3,2))+"\n"
            plt.gcf().text(0.7, 0.25, right_text, va='center', ha='left', fontsize=my_font_size,
            bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))

    
        elif STEPS_INNER_CYL==9:
            right_text = "Flared liner type: "+str(STEPS_INNER_CYL)+" steps\n" +\
            "Flared liner radius: "+str(FLARED_RADIUS)+"\n" + "Built-in angle: "+str(BUILT_IN_ANGLE)+"(+2)°\n" + \
            "Total height: "+str(round(available_length,2))+"\n" + "Straight height: "+str(round(straight_length,2))+"\n" +\
            "Curve height: "+str(round(available_length-straight_length,2))+"\n" + "Top structure height: "+str(TS_HEIGHT)+"\n"+ +\
            "L0: "+str(round(vert_span*Vertical_segment_ratio_0,2))+"\n" +\
            "L1: "+str(round(vert_span*Vertical_segment_ratio_1,2))+"\n" +\
            "L2: "+str(round(vert_span*Vertical_segment_ratio_2,2))+"\n" +\
            "L3: "+str(round(vert_span*Vertical_segment_ratio_3,2))+"\n" +\
            "L4: "+str(round(vert_span*Vertical_segment_ratio_4,2))+"\n" +\
            "L5: "+str(round(vert_span*Vertical_segment_ratio_5,2))+"\n" +\
            "Retraction 1: "+str(round(retraction_1,2))+"\n" +\
            "Retraction 2: "+str(round(retraction_2,2))+"\n" +\
            "Retraction 3: "+str(round(retraction_3,2))+"\n" +\
            "Retraction 4: "+str(round(retraction_4,2))+"\n" +\
            "Retraction 5: "+str(round(retraction_5,2))+"\n"
            plt.gcf().text(0.7, 0.5, right_text, va='center', ha='left', fontsize=my_font_size,
            bbox=dict(boxstyle="square,pad=0.3", facecolor="lightgreen", edgecolor="green"))
    

    
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
plt.xlim([-10, 1300])
plt.ylim([-100, 2000])
plt.grid(True)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')

# Show the plot
plt.show()






