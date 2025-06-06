from fillet_alg import execute_fillet
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(legacy='1.25')


def Polyline(Thickness_decrement_var):
    my_thickness_decrement=Thickness_decrement_var
    print("*** MY CODE *** thickness decrement is "+str(Thickness_decrement_var))
    
    #Mesh size for Abaqus
    mesh_size_BSC=25
    mesh_size_BM=40
    
    #Loads
    my_SF_kN=849
    my_BM_kNm=1838
    #Adjusting for Abaqus N-mm consistent units
    My_Loads=(my_SF_kN*1000.0, my_BM_kNm*1000000.0)

    #BSN300, BSN900C or BSN900E
    BSC_TYPE= "BSN300"
    my_dim=22
    
    
    #Dovetail
    Delta_P3y_P2y=92.7
    th_spec=20.0
    Theta_1=17.25
    Theta_3=29.75
    fillet_dove_radius=5
    
    BSC_dim=[
    [18,000,416,000,000,450],
    [22,000,518,000,000,490],
    [24,000,569,000,000,510],
    [26,000,619,000,000,530],
    [28,000,670,000,000,555],
    [30,000,721,000,000,575],
    [32,000,772,000,000,600],
    [34,000,823,000,000,625],
    [36,000,873,000,000,650],
    [38,000,924,000,000,675]
    ]

    #Precisa desenhar o Outer cylinder do 900E ainda
    if BSC_TYPE== "BSN900E" or BSC_TYPE== "BSN900C":
        BSC_dim=[
            [26,525.25,561.25,850,000,850],
            [28,575.25,611.25,885,000,885],
            [30,625.25,661.25,920,000,920],
            [32,675.25,711.25,955,000,955],
            [34,725.25,761.25,990,000,990],
            [36,775.25,811.25,1025,000,1025],
            [38,825.25,861.25,1060,000,1060],
            [40,875.25,911.25,1121,000,1095],
            [42,925.25,961.25,1171,000,1130],
            [44,975.25,1011.25,1221,000,1165],
            [46,1025.25,1061.25,1271,000,1200],
            [48,1075.25,1111.25,1321,000,1235]
            ]
        Delta_P3y_P2y=150.0
        th_spec=25.0
        Theta_1=22.0
        Theta_3=35.2
        fillet_dove_radius=10.0
        
        
    index_dim=0
    for dim in BSC_dim:
        if dim[0]==my_dim:
            print(dim[0])
            my_index_dim=index_dim
        index_dim += 1
    
    print(my_index_dim)


    ##############################################      INPUTS
    
    n_points_straight=2
    n_points_arc=8
    
    #PIPE inputs
    pipe_nominal_OD=267.4
    pipe_tol=8
    pipe_OD=pipe_nominal_OD+pipe_tol
    
    #Flared liner inputs
    radial_clearence_pipe_flared=1.0
    FLARED_MIN_THICK=15.0
    FLARED_MARGIN=0
    BUILT_IN_ANGLE=7
    FLARED_RADIUS=4500
    ADJUST_TO_FORGING=0
    FLARED_IR=(pipe_OD/2.0)+radial_clearence_pipe_flared+ADJUST_TO_FORGING
    Lista_Flared_Liner_D=[]
    Lista_Flared_Liner_H=[]
    

    
    #plt.plot([P1[0],P2[0],P3[0]],[P1[1],P2[1],P3[1]])
    IR_FL = FLARED_IR+FLARED_MARGIN+FLARED_MIN_THICK
    FL_HEIGHT=130.0
    OR_FL = 700
    BCD = 776
    RCD= BCD/2.0
    BCD_hole=51
    
    
    NECK_THICK=0
    
    
    #you need to choose between ratios or mathcad
    flared_design_option="ratios"
    STEPS_INNER_CYL=4
    
    if STEPS_INNER_CYL==6:
        if flared_design_option=="mathcad":
            L5=199
            L4=464
            L3=694
            #L8=0
            
            L5+=1
            L4+=1
            L3+=1
            
            D6=400
            D3=320
            D2=295
            D1=250
            
            D3+=2
            D6+=2
            D2+=2
            D1+=2
            
            Di1=213
            FLARED_IR=Di1/2
    
            #If "mathcad" is chosen, the Internal radius of the flange becomes D1/2
            IR_FL=D1/2
            
        if flared_design_option=="ratios":
            retraction_ratio_1=0.4
            retraction_ratio_2=0.3
            retraction_ratio_3=0.3
            
            Vertical_segment_ratio_0=0.25
            Vertical_segment_ratio_1=0.25
            Vertical_segment_ratio_2=0.25
            Vertical_segment_ratio_3=0.25
        
    if STEPS_INNER_CYL==4:
        if flared_design_option=="mathcad":
            L5=299
            L4=664

            #L8=0
            
            L5+=1
            L4+=1
            
            D6=400
            D3=250
            D1=250
            
            D3+=2
            D6+=2
            D1+=2
            
            Di1=213
            FLARED_IR=Di1/2
    
            #If "mathcad" is chosen, the Internal radius of the flange becomes D1/2
            IR_FL=D1/2
            
        if flared_design_option=="ratios":
            retraction_ratio_1=1
            
            Vertical_segment_ratio_0=0.4
            Vertical_segment_ratio_1=0.2
            Vertical_segment_ratio_2=0.4
                    
    
    
    #Inferior Ellipse
    semi_axis_hor_inf=70
    semi_axis_vert_inf=70
    
    #straight_mid_segment
    mid_length=200
    
    #Superior Ellipse
    semi_axis_hor_sup=10
    semi_axis_vert_sup=20
    
    #ajust overall neck thickness by displacing the ellipse
    my_neck_reduction=0
    

    #Theta_2=90.0-(Theta_1+Theta_3)
    
    l2 = Delta_P3y_P2y/np.cos(np.deg2rad(Theta_3))
    l1_hor=(np.sin(np.deg2rad(Theta_3))*l2)+th_spec
    l1_vert=np.tan(np.deg2rad(Theta_1))*l1_hor
    
    P1 = ((BSC_dim[my_index_dim][2]/2.0)-th_spec, FL_HEIGHT+(semi_axis_vert_sup+semi_axis_vert_inf+mid_length))
    P2 = (P1[0]+l1_hor, P1[1]-l1_vert)
    P3 = (BSC_dim[my_index_dim][2]/2.0, P2[1]+Delta_P3y_P2y)
    
    #outer cylinder thickness at the top
    OC_THICK=100

   
    #INNER CCYLINDER FILLET RADIUS
    IC_int_fillet=2.0
    IC_out_fillet=6.0
    
    #TOP RIGHT CORNER FILLET
    trc_fillet=10.0
    
    
    #TOP structure
    TS_HEIGHT=265
    
    TS_bottom_plate_thick=50
    TS_inner_thickness=44
    TS_top_pate_thick=15
    TS_OR_base_bottom=(BSC_dim[my_index_dim][2]/2.0)-15
    TS_OR_base_top=TS_OR_base_bottom-10
    TS_OR_top_bottom=TS_OR_base_top-10
    TS_OR_top_top=TS_OR_top_bottom+20
    # TS_IR_bottom. The internal radius at bottom is assigned below according to retraction 0
    # TS_IR_top. Assigned right after the TS_IR_bottom
    TS_IR_top=0
    
    ##############################################      BSC DRAWING
    
    #execute_fillet(P1, P2, P3, 10.0)
    
    inf_line_dove, fillet_circle_dove, sup_line_dove = execute_fillet(P1, P2, P3, fillet_dove_radius)
    
    
    Polyline1=[]
    Polyline2=[]
    Polyline3=[]
    Polyline4=[]
    Polyline5=[]
    Polyline6=[]
    
    x = np.linspace(pipe_OD/2.0,pipe_OD/2.0, n_points_straight)
    y = np.linspace(-200, 2000, n_points_straight)
    plt.plot(x,y,c="black")
    
    #Hydratight tool check - HM09 or HM07 - diamter, nearest obstruction
    tension_tool="HM09"
    if tension_tool == "HM07":
        HM=[127,280]
    elif tension_tool == "HM09":
        HM=[144.5,288]
    
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
    
    #NECK THICK calculation
    NECK_THICK=RCD-(HM[0]/2)-semi_axis_hor_sup-(IR_FL+my_thickness_decrement)-my_neck_reduction
    
    
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
    x = np.linspace(OR_FL, OR_FL, n_points_straight)
    y = np.linspace(0, FL_HEIGHT, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    


    ellipse_center_x= (IR_FL+my_thickness_decrement)+NECK_THICK+semi_axis_hor_sup
    ellipse_center_y=FL_HEIGHT+semi_axis_vert_inf
    
    #HORIZONTAL OVERLAP CALCULATION FOR SUPERIOR ELLIPSE AND DOVETAIL
    t=np.linspace(np.pi, np.pi/2, n_points_arc*2)
    x=ellipse_center_x+semi_axis_hor_sup*np.cos(t)-(semi_axis_hor_inf-semi_axis_hor_sup)
    y=ellipse_center_y+semi_axis_vert_sup*np.sin(t)+mid_length

    
    horizontal_overlap=x[-1]-P1[0]
    
    if horizontal_overlap>0:
        print("HORIZONTAL OVERLAP IS: " + str(horizontal_overlap))

        ellipse_center_x=ellipse_center_x-horizontal_overlap
    else:
        print("No horizontal overlap")
        
    
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
    
    horizontal_overlap=x[-1]-P1[0]
    print("HORIZONTAL OVERLAP IS: " + str(horizontal_overlap))
    
    
    
    #segmento6: encaixe elipse rac1
    xx = np.linspace(x[-1], P1[0], n_points_straight)
    yy = np.linspace(y[-1], P1[1], n_points_straight)
    plt.plot(xx,yy)
    Polyline1.extend([(xi, yi) for xi, yi in zip(xx, yy)])
    
    
    #Adding the dovetail to the Polyline1
    Polyline1.extend(inf_line_dove)
    Polyline1.extend(fillet_circle_dove)
    Polyline1.extend(sup_line_dove)
    
    
    #segmento7: reta vertical pos rac3
    x = np.linspace(P3[0], P3[0], n_points_straight)
    y = np.linspace(P3[1], P3[1]+150, n_points_straight)
    plt.plot(x,y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    if BSC_TYPE == "BSN900E":
        diam_post_rac3=BSC_dim[my_index_dim][1]/2.0
        
        #segmento7: reta vertical pos rac3
        x = np.linspace(P3[0], diam_post_rac3, n_points_straight)
        y = np.linspace(P3[1]+150, P3[1]+150+200, n_points_straight)
        plt.plot(x,y)
        Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        #segmento7: reta vertical pos rac3
        x = np.linspace(diam_post_rac3, diam_post_rac3, n_points_straight)
        y = np.linspace(P3[1]+150+200, P2[1]+BSC_dim[my_index_dim][5]-trc_fillet, n_points_straight)
        plt.plot(x,y)
        Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    else:
        diam_post_rac3=P3[0]
    
        #segmento7: reta vertical pos rac3
        x = np.linspace(P3[0], diam_post_rac3, n_points_straight)
        y = np.linspace(P3[1]+150, P2[1]+BSC_dim[my_index_dim][5]-trc_fillet, n_points_straight)
        plt.plot(x,y,c='red')
        Polyline1.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    
    #FILLET_RADIUS top right corner
    angles = np.linspace(0, np.pi/2, n_points_arc)
    arc_x = (trc_fillet * np.cos(angles))+x[0]-trc_fillet
    arc_y = trc_fillet * np.sin(angles)+y[-1]
    plt.plot(arc_x,arc_y)
    Polyline1.extend([(xi, yi) for xi, yi in zip(arc_x, arc_y)])
    
    #Assigning the variables for surface definition in Abaqus
    Surface_kit=[]
    Surface_kit.append(inf_line_dove[-1][1]-1)
    Surface_kit.append(P3[1]+1)
    Surface_kit.append(P1[1]+1)
    Surface_kit.append(inf_line_dove[-1][0]+1)
    Surface_kit.append(P3[1]-1)
    Surface_kit.append(arc_x[-1]+1)

    

    #my_thickness_decrement
    #segmento11: ate a superficie interna do cilindro externo, usa a espessura do seg9
    if flared_design_option == "mathcad":
        x_ = np.linspace(x[-1]-trc_fillet, (D6/2), n_points_straight)
        y_ = np.linspace(y[-1]+trc_fillet, y[-1]+trc_fillet, n_points_straight)
    else:
        x_ = np.linspace(x[-1]-trc_fillet, (x[-1]-OC_THICK+my_thickness_decrement), n_points_straight)
        y_ = np.linspace(y[-1]+trc_fillet, y[-1]+trc_fillet, n_points_straight)
    plt.plot(x_,y_)
    Polyline1.extend([(xi, yi) for xi, yi in zip(x_, y_)])
    
    print("X_ is " + str(x_[-1]))

    ###################       END OF POLYLINE1
    
    hor_span=x_[-1]-IR_FL-my_thickness_decrement
    vert_span=y_[-1]
    
    print("My vertical span is "+str(round(vert_span,3)))
    print("My hor span is "+str(x_[-1])+"-"+str(IR_FL-my_thickness_decrement)+"="+str(hor_span))
    

    if STEPS_INNER_CYL ==6:
        #Internal side of BSC
        
        if flared_design_option == "ratios":
            retraction_1=(hor_span)*retraction_ratio_1
            retraction_2=(hor_span)*retraction_ratio_2
            retraction_3=(hor_span)*retraction_ratio_3
            
        
        #segmento 19: espessura do inner cylinder at top
        if flared_design_option == "mathcad":
            xx = np.linspace(x_[-1], D6/2, n_points_straight)
        else:
            xx = np.linspace(x_[-1], x_[-1], n_points_straight)
        yy = np.linspace(y_[-1], y_[-1], n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        Lista_Flared_Liner_D.append(xx[-1])
        Lista_Flared_Liner_H.append( yy[-1])
        
        TS_IR_bottom=xx[-1]-20
        TS_IR_top=TS_IR_bottom+15
        
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
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, D2/2+IC_out_fillet, n_points_straight)
            Lista_Flared_Liner_D.append(round(D2/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_2+IC_out_fillet, n_points_straight)
            Lista_Flared_Liner_D.append(xx[-1]-retraction_2)
            Lista_Flared_Liner_H.append(yy[-1]-IC_int_fillet)
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
        y = np.linspace(yy[-1]-IC_int_fillet, yy[-1]-IC_int_fillet, n_points_straight)
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1]-IC_int_fillet, D1/2+IC_out_fillet, n_points_straight)
            Lista_Flared_Liner_D.append(round(D1/2,6))
            Lista_Flared_Liner_H.append(round(yy[-1]-IC_int_fillet,6))
        else:
            x = np.linspace(xx[-1]-IC_int_fillet, xx[-1]-retraction_3+IC_out_fillet, n_points_straight)
            Lista_Flared_Liner_D.append(xx[-1]-retraction_3)
            Lista_Flared_Liner_H.append(yy[-1]-IC_int_fillet)
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
        
    elif STEPS_INNER_CYL ==4:
        
        if flared_design_option == "ratios":
            retraction_1=(hor_span)*retraction_ratio_1
            

        #segmento 19: espessura do inner cylinder at top
        if flared_design_option == "mathcad":
            xx = np.linspace(x_[-1], D6/2, n_points_straight)
        else:
            xx = np.linspace(x_[-1], x_[-1], n_points_straight)
        yy = np.linspace(y_[-1], y_[-1], n_points_straight)
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        Lista_Flared_Liner_D.append(xx[-1])
        Lista_Flared_Liner_H.append( yy[-1])
        
        TS_IR_bottom=xx[-1]-20
        TS_IR_top=TS_IR_bottom+15
        

        
        #segmento 20: 0/5 segmento de cima pra baixo
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1], D6/2, n_points_straight)
            y = np.linspace(yy[-1], vert_span-L5, n_points_straight)
            Lista_Flared_Liner_D.append(D3/2)
            Lista_Flared_Liner_H.append(vert_span-L5)
            print("+++++ vert_span-L5 vale "+str(vert_span-L5)+"  +++++")
        else:
            x = np.linspace(xx[-1], xx[-1], n_points_straight)
            y = np.linspace(yy[-1], yy[-1]-vert_span*Vertical_segment_ratio_0, n_points_straight)
            #Lista_Flared_Liner_D.append(x[-1]-retraction_1)
            Lista_Flared_Liner_D.append(x[-1])
            Lista_Flared_Liner_H.append(y[-1]-vert_span*Vertical_segment_ratio_0)
        plt.plot(x,y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])

        
        #segmento 21: 1/5 segmento inclinado de cima pra baixo
        if flared_design_option == "mathcad":
            xx = np.linspace(x[-1], D3/2, n_points_straight)
            yy = np.linspace(y[-1], vert_span-L4, n_points_straight)
        else:
            xx = np.linspace(x[-1], x[-1]-retraction_1, n_points_straight)
            yy = np.linspace(y[-1], y[-1]-(vert_span*Vertical_segment_ratio_1)+IC_int_fillet, n_points_straight)
        Lista_Flared_Liner_D.append(xx[-1])
        Lista_Flared_Liner_H.append(yy[-1])
        plt.plot(xx,yy)
        Polyline3.extend([(xi, yi) for xi, yi in zip(xx, yy)])
        
        
        
        #segmento 23: 3/5 segmento de cima pra baixo
        if flared_design_option == "mathcad":
            x = np.linspace(xx[-1], D1/2, n_points_straight)
            y = np.linspace(yy[-1], 0, n_points_straight)
        else:
            x = np.linspace(xx[-1], xx[-1], n_points_straight)
            y = np.linspace(yy[-1], 0, n_points_straight)
        plt.plot(x,y)
        Polyline3.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        
 
        

        
    ####################### TOP STRUCTURE ########################
    '''Lista_Flared_Liner_H.append(vert_span)
    Lista_Flared_Liner_D.append(TS_IR_bottom)
    
    Lista_Flared_Liner_H.append(vert_span+TS_bottom_plate_thick)
    Lista_Flared_Liner_D.append(TS_IR_bottom)
    
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
        
        x = np.linspace( TS_IR_top, TS_IR_bottom, n_points_straight)
        y = np.linspace( vert_span+TS_inner_thickness , vert_span+TS_inner_thickness  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_IR_bottom, TS_IR_bottom, n_points_straight)
        y = np.linspace( vert_span+TS_inner_thickness , vert_span  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        x = np.linspace( TS_IR_bottom, TS_OR_base_bottom, n_points_straight)
        y = np.linspace( vert_span , vert_span  , n_points_straight)
        plt.plot(x,y,c='deeppink')
        
        
    #######################   FLARED LINER   #################
    
    display_FlaredLiner=1
    
    if display_FlaredLiner>0:
        
        #print(Lista_Flared_Liner_D)
        #print(Lista_Flared_Liner_H)
        
        flared_liner_angle=BUILT_IN_ANGLE+2
        
        print("################  FLARED LINER  #############")###preciso achar a distancia vertical pra subtrair
        #flared_arc_length=2*np.pi*FLARED_RADIUS*(flared_liner_angle/360)
        needed_length=FLARED_RADIUS*np.sin(np.deg2rad(flared_liner_angle))
        available_length=vert_span+TS_HEIGHT
        print("needed length is "+str(round(needed_length,3))+" and available length is "+str(round(available_length,3)))
        straight_length=available_length-needed_length
        print("the straight segement is "+str(round(straight_length,3)))
        if needed_length>available_length:
            print("!!! Warning - The top structure must be increased from "+str(TS_HEIGHT)+" to "+str(straight_length*-1+TS_HEIGHT)+" !!!")
        
        count=0
        flared_thick_increase=0
        List_thick=[]
        #print(Lista_Flared_Liner_D)
        for i in Lista_Flared_Liner_H:
            if i<straight_length:
                my_thick= Lista_Flared_Liner_D[count]-FLARED_IR
                print(round(FLARED_IR,3), round(Lista_Flared_Liner_D[count],3), round(Lista_Flared_Liner_H[count],3))
                List_thick.append(round(my_thick,4))
            else:
                pre_flared_x=((FLARED_RADIUS**2-(i-straight_length)**2)**0.5)
                flared_x=(pre_flared_x-FLARED_RADIUS-FLARED_IR)*-1
                my_thick=(flared_x-Lista_Flared_Liner_D[count])*-1
                print(round(flared_x,3), round(Lista_Flared_Liner_D[count],3), round(Lista_Flared_Liner_H[count],3))
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
    #pol, diam menor, diam maior, cota K, cota J
    #a partir do elemento 5 da sublista, começa o flange: overall length, flange thickness, overall diameter, hub diameter

    if BSC_TYPE=="BSN300":
        BM_dim=[
            [18,419.35,'xxx', 800, 150, 157.2, 53.85, 711, 562.05],
            [22,521.35,'xxx', 800, 150, 165.10, 66.55, 838.2, 641.35],
            [24,572.35,'xxx', 800, 150, 174.625,72.9,904.875,681.1],#pq o indice [3] era 510, e nao 800? erro? deveria ser no dummy?
            [26,622.35,'xxx', 800, 150, 184.15 ,79.25 ,971.55 ,720.85 ],
            [28,673.35,'xxx', 800, 150, 196.85 ,85.85 ,1035.1 ,774.70 ],
            [30,724.35,'xxx', 800, 150, 209.55 ,91.95 ,1092.2 ,827.02 ],
            [32,775.35,'xxx', 800, 150, 222.25 ,98.55 ,1149.4 ,881.13 ],
            [34,826.35,'xxx', 800, 150, 231.65 ,101.60 ,1206.5 ,936.75 ],
            [36,876.35,'xxx', 800, 150, 241.30 ,104.65 ,1270.0 ,990.6 ],
            [38,927.35,'xxx', 800, 150, 180.85 ,107.95 ,1168.4 ,993.65 ]
            ]
        
        small_radius=BM_dim[my_index_dim][1]/2.0
        BM_angle=30.0
        BM_length=1013.0
        web_height=205.0
        #small_radius_length=BM_dim[my_index_dim][3]
        large_radius=BM_dim[my_index_dim][1]/2.0
        transition_length=BM_dim[my_index_dim][4]
        BM_thick=22.3 # 30 veio de uma spec da plataforma
        BM_flange_overall_length=BM_dim[my_index_dim][5]
        BM_flange_thick= BM_dim[my_index_dim][6]
        BM_flange_radius= BM_dim[my_index_dim][7]/2.0
        BM_hub_radius= BM_dim[my_index_dim][8]/2.0
        BM_hub_height = BM_flange_overall_length-BM_flange_thick
        
        last_x=BM_dim[my_index_dim][1]/2.0
    
    

    if BSC_TYPE == "BSN900E" or BSC_TYPE == "BSN900C" :
        # the internal diameter dimensions come from the finished drawing, while the heights come from the welded BM drawging
        #pol, smallID, largeID, outerD, BottomD, G, H, K, J, D, F, C, A
        BM_thick=47.7
        BM_dim=[
        [26, 529.1, 565.1, 660.4, 1123.7, 1085.9, 939.2, 700, 200, 285.75, 774.70, 139.7],
        [28, 579.1, 615.1, 711.2, 1173.8, 1168.4, 926.5, 690, 210, 298.45, 831.85, 142.75],
        [30, 629.1, 665.1, 762.0, 1223.8, 1231.9, 913.8, 680, 220, 311.15, 889.0, 149.35],
        [32, 679.1, 715.1, 812.8, 1273.8, 1314.5, 894.8, 670, 230, 330.20, 946.15, 158.75],
        [34, 729.1, 765.1, 863.6, 1323.8, 1397.0, 875.7, 660, 240, 349.25, 1006.4, 165.10],
        [36, 779.1, 815.1, 914.4, 1373.8, 1460.5, 863.0, 660, 240, 361.95, 1063.8, 171.45],
        [38, 829.1, 865.1, 963.2, 1423.8, 1460.5, 872.4, 650, 250, 352.55, 1073.2, 190.50], #1460.5 repeats on the ref table. It seems wrong
        [40, 879.1, 915.1, 1016.0, 1473.8, 1511.3, 861.5, 640, 260, 363.47, 1127.3, 196.85],
        [42, 929.1, 965.1, 1066.8, 1523.8, 1562.1, 853.6, 630, 270, 371.35, 1176.3, 206.25],
        [44, 979.1, 1015.1, 1117.6,1573.8, 1647.9, 834.3, 620, 280, 390.65, 1235, 214.38],
        [46, 1029.1, 1065.1, 1168.4, 1623.8, 1733.5, 814.0, 610, 290, 410.97, 1292.4, 225.55],
        [48, 1079.1, 1115.1, 1219.2, 1673.8, 1784.4, 805.9, 600, 300, 419.10, 1343.2, 233.43]
        ]
        
        BM_angle=35.75
        BM_length=1525.0
        web_height=300.0
        large_radius=BM_dim[my_index_dim][2]/2.0
        transition_length=BM_dim[my_index_dim][8] ### isso aqui e a cota J, precisa atualizar
        small_radius=BM_dim[my_index_dim][1]/2.0
        small_radius_length=BM_dim[my_index_dim][7] ### isso aqui e a cota K, precisa atualizar
        BM_flange_overall_length=BM_dim[my_index_dim][9]
        BM_hub_radius= BM_dim[my_index_dim][10]/2.0
        BM_flange_thick= BM_dim[my_index_dim][11]
        BM_flange_radius=BM_dim[my_index_dim][5]/2.0
        BM_hub_height = BM_flange_overall_length-BM_flange_thick
        
        last_x=BM_dim[my_index_dim][1]/2.0
        if BSC_TYPE == "BSN900C":
            small_radius=large_radius
            last_x=BM_dim[my_index_dim][2]/2.0
        
    if BSC_TYPE=="BSN300":
        x = np.linspace(large_radius, large_radius,n_points_straight)
        y = np.linspace(BM_length+P3[1]-web_height, P3[1], n_points_straight)
        plt.plot(x,y,c='darkslateblue')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    else:
        x = np.linspace(small_radius, small_radius,n_points_straight)
        y = np.linspace(BM_length+P3[1]-web_height, BM_length+P3[1]-web_height-small_radius_length, n_points_straight)
        plt.plot(x,y,c='darkslateblue')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        x = np.linspace(small_radius, large_radius,n_points_straight)
        y = np.linspace(BM_length+P3[1]-web_height-small_radius_length, BM_length+P3[1]-web_height-small_radius_length-transition_length, n_points_straight)
        plt.plot(x,y,c='darkslateblue')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
        
        x = np.linspace(large_radius, large_radius,n_points_straight)
        y = np.linspace(BM_length+P3[1]-web_height-small_radius_length-transition_length, P3[1], n_points_straight)
        plt.plot(x,y,c='darkslateblue')
        Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius, large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height) ,n_points_straight)
    y = np.linspace(P3[1], P3[1]-web_height, n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height) ,large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height)+ BM_thick*np.cos(np.deg2rad(BM_angle)), n_points_straight*2)
    y = np.linspace(P3[1]-web_height, P3[1]-web_height+ BM_thick*np.sin(np.deg2rad(BM_angle)), n_points_straight*2)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+((np.tan(np.deg2rad(BM_angle)))*web_height)+ BM_thick*np.cos(np.deg2rad(BM_angle)) , large_radius+BM_thick, n_points_straight)
    y = np.linspace(P3[1]-web_height+ BM_thick*np.sin(np.deg2rad(BM_angle)), P3[1], n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+BM_thick , large_radius+BM_thick, n_points_straight)
    y = np.linspace(P3[1], P3[1]+BM_length-web_height-BM_flange_overall_length, n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(large_radius+BM_thick , BM_hub_radius, n_points_straight)
    y = np.linspace(P3[1]+BM_length-web_height-BM_flange_overall_length, P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height, n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_hub_radius , BM_flange_radius, n_points_straight)
    y = np.linspace(P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height, P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height, n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_flange_radius , BM_flange_radius, n_points_straight)
    y = np.linspace(P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height, P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height+BM_flange_thick, n_points_straight)
    plt.plot(x,y,c='darkslateblue')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    
    x = np.linspace(BM_flange_radius , last_x, n_points_straight)
    y = np.linspace(P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height+BM_flange_thick, P3[1]+BM_length-web_height-BM_flange_overall_length+BM_hub_height+BM_flange_thick, n_points_straight)
    plt.plot(x,y,c='red')
    Polyline6.extend([(xi, yi) for xi, yi in zip(x, y)])
    


########################### SETS FOR POSTPROCESSING

    Sets_from_Nodes=[[],[],[],[],[],[]]
    
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
    
    Set_name='My_set_Ellipse_side1_node'
    Set_initial_tuple=(ellipse_center_x-semi_axis_hor_inf-5,FL_HEIGHT-5,-1)
    Set_final_tuple=(ellipse_center_x,P1[1]+5,1)
    Sets_from_Nodes[2].append(Set_name)
    Sets_from_Nodes[2].append(Set_initial_tuple)
    Sets_from_Nodes[2].append(Set_final_tuple)

    Set_name='My_set_Ellipse_side2_node'
    Set_initial_tuple=(ellipse_center_x*-1,FL_HEIGHT-5,-1)
    Set_final_tuple=((ellipse_center_x-semi_axis_hor_inf-5)*-1,P1[1]+5,1)
    Sets_from_Nodes[3].append(Set_name)
    Sets_from_Nodes[3].append(Set_initial_tuple)
    Sets_from_Nodes[3].append(Set_final_tuple)
    
    Set_name='My_set_DoveTail_side1_node'
    Set_initial_tuple=(P1[0]-5,P2[1],-1)
    Set_final_tuple=(P2[0],P3[1]+5,1)
    Sets_from_Nodes[4].append(Set_name)
    Sets_from_Nodes[4].append(Set_initial_tuple)
    Sets_from_Nodes[4].append(Set_final_tuple)
    
    Set_name='My_set_Top_plate'
    Set_initial_tuple=(-800,vert_span-30,-1)
    Set_final_tuple=(800,vert_span+20,1)
    Sets_from_Nodes[5].append(Set_name)
    Sets_from_Nodes[5].append(Set_initial_tuple)
    Sets_from_Nodes[5].append(Set_final_tuple)

    

    
################################ RETURN 
    Polylist=[Polyline1,Polyline2,Polyline3,Polyline4,Polyline5,Polyline6,
              flared_thick_increase,My_Loads,[],Sets_from_Nodes,mid_length,
              Surface_kit,(mesh_size_BM,mesh_size_BSC)]
    return Polylist


################# EXECUTION ##############################

pre_coordinates = Polyline(0)
#coordinates= Polyline(pre_coordinates[6])


if pre_coordinates[6]>0:
    coordinates= Polyline(pre_coordinates[6])
    with open('output_abq.txt', 'w') as file:
        file.write(str(coordinates))
    
    coordinates_1 = coordinates[0]
    coordinates_3 = coordinates[2]
    coordinates_6 = coordinates[5]
    
elif pre_coordinates[6]==0:
    with open('output_abq.txt', 'w') as file:
        file.write(str(pre_coordinates))
    
    coordinates_1 = pre_coordinates[0]
    coordinates_3 = pre_coordinates[2]
    coordinates_6= pre_coordinates[5]





for my_index in range(0,len(coordinates_1)-1,2):
    point1=coordinates_1[my_index]
    point2=coordinates_1[my_index+1]
        




# Unpack the list of tuples into two separate lists: x and y
x_values_1, y_values_1 = zip(*coordinates_1)
x_values_3, y_values_3 = zip(*coordinates_3)
x_values_6, y_values_6 = zip(*coordinates_6)

# Plot the points
plt.figure(figsize=(8, 8))
plt.plot(x_values_1, y_values_1, marker='.', linestyle='-', label='Polyline 1')
plt.plot(x_values_3, y_values_3, marker='.', linestyle='-', label='Polyline 3')
plt.plot(x_values_6, y_values_6, marker='.', linestyle='-', label='Polyline 6')


# Customize the plot
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.title("Plot of Coordinates from List of Tuples")
plt.xlim([0,1300])
plt.ylim([-100,2000])
plt.grid(True)
plt.legend()
plt.gca().set_aspect('equal', adjustable='box')  # To ensure equal scaling on both axes'''

# Show the plot
plt.show()



