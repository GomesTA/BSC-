import numpy as np
import matplotlib.pyplot as plt
import math




# Points for test
#P1 = (80, 80)
#P2 = (50, 100)
#P3 = (65, 130)
#P4 = (0, 10)

#vector1=np.array([P2[0],P2[1],0])-([P1[0],P1[1],0])
#vector2=np.array([P3[0],P3[1],0])-([P1[0],P1[1],0])
#cross_prod=np.cross(vector1,vector2)
#print(vector1)
#print(vector2)
#print(cross_prod)
#print(cross_prod[2])
#print("*************")

# Function to calculate the coefficients of the line equation Ax + By + C = 0 from two points
def line_from_points(Pi, Pf):
    x1, y1 = Pi
    x2, y2 = Pf
    A = y2 - y1
    B = x1 - x2
    C = A * x1 + B * y1
    return A, B, -C

# Function to calculate the bisector line between two lines
def bisector_line(a1, b1, c1, a2, b2, c2):
    norm1 = math.sqrt(a1**2 + b1**2)
    norm2 = math.sqrt(a2**2 + b2**2)
    
    a_pos = a1 / norm1 + a2 / norm2
    b_pos = b1 / norm1 + b2 / norm2
    c_pos = c1 / norm1 + c2 / norm2
    
    a_neg = a1 / norm1 - a2 / norm2
    b_neg = b1 / norm1 - b2 / norm2
    c_neg = c1 / norm1 - c2 / norm2
    
    return (a_pos, b_pos, c_pos), (a_neg, b_neg, c_neg)

# Function to find the intersection point of two lines
def find_intersection(a1, b1, c1, a2, b2, c2):
    det = a1 * b2 - a2 * b1
    if det == 0:
        return None  # Lines are parallel or coincident
    else:
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        return (x, y)
    
# Function to calculate the distance between a point (x0, y0) and a line Ax + By + C = 0
def point_to_line_distance(A, B, C, x0, y0):
    return abs(A * x0 + B * y0 + C) / math.sqrt(A**2 + B**2)

# Function to find the center of the circle that is tangent to Line 1
def find_tangent_circle_center(A1, B1, C1, bisector_A, bisector_B, bisector_C, radius, start_point):
    # We move along the bisector line to find the center
    for x0 in np.linspace(start_point, start_point-4*radius, 1000000):  # Test different x0 values along the bisector
        if bisector_B != 0:
            y0 = (-bisector_A * x0 - bisector_C) / bisector_B
        else:
            y0 = 0
        
        # Calculate the distance from this center to Line 1
        distance_to_line1 = point_to_line_distance(A1, B1, C1, x0, y0)
        
        # If the distance equals the radius, we have found the center
        if abs(distance_to_line1 - radius) < 1e-3:  # Allowing a small tolerance
            #print(f"Tangent Circle Center: ({x0:.4f}, {y0:.4f})")
            #print(x0*-1,y0*-1)
            return x0, y0
    return None

# Function to find the interception of line and circle, so the beginning of the line plot is the interception
def circle_line_intersection(circle_center, radius, A, B, C):
    x0, y0 = circle_center
    
    # If the line is vertical (B=0), we handle it separately
    if B == 0:
        x_intersect = -C / A
        y_part = (radius+0.001)**2 - (x_intersect - x0)**2
        if y_part < 0:
            return None  # No intersection
        y1 = y0 + math.sqrt(y_part)
        y2 = y0 - math.sqrt(y_part)
        return (x_intersect, y1), (x_intersect, y2)
    
    # Convert the line to slope-intercept form y = mx + b
    m = -A / B
    b = -C / B

    # Substitute the line equation into the circle equation
    # (x - x0)^2 + (mx + b - y0)^2 = r^2
    a = 1 + m**2
    b_ = 2 * (m * (b - y0) - x0)
    c = (b - y0)**2 + x0**2 - (radius+0.001)**2

    # Solve the quadratic equation for x
    discriminant = b_**2 - 4 * a * c

    if discriminant < 0:
        return None  # No intersection

    x1 = (-b_ + math.sqrt(discriminant)) / (2 * a)
    x2 = (-b_ - math.sqrt(discriminant)) / (2 * a)

    y1 = m * x1 + b
    y2 = m * x2 + b

    return  (x1,y1)#,(x2, y2) I chose to use the first values only, they are virtually the same

# Function to convert the line equation to y = mx + b form
def line_to_slope_intercept(A, B, C):
    if B != 0:
        slope = -A / B
        intercept = -C / B
        return slope, intercept
    else:
        return None, None  # For vertical lines, return None
    
# Function to print the line equation in y = mx + b form
def print_line_equation(A, B, C, label):
    slope, intercept = line_to_slope_intercept(A, B, C)
    if slope is not None:
        print(f"{label}: y = {slope:.2f}x + {intercept:.2f}")
    else:
        print(f"{label}: The line is vertical and cannot be written as y = mx + b")

# Function to plot a line given its equation Ax + By + C = 0
def plot_line(A, B, C, x_range, label):
    x = np.linspace(x_range[1], x_range[0], 15)  # Generate  points in the given x range
    if B != 0:
        y = (-A * x - C) / B  # Calculate corresponding y values from the equation Ax + By + C = 0
    else:
        x = np.full_like(x, -C / A)  # If B is 0, line is vertical, set constant x
        y = np.linspace(x_range[1], x_range[0], 15)
    
    plt.plot(x, y)#, label=label)
    return([(xi, yi) for xi, yi in zip(x, y)])


# Function to calculate the angle of a point relative to the center of the circle
def angle_of_point_in_circle(center, point):
    x_c, y_c = center
    x = point[0]
    y=point[1]
    
    # Calculate the angle in radians using atan2
    #print("hello")
    #print((y - y_c, x - x_c))
    angle = math.atan2(y - y_c, x - x_c)
    
    # Convert to a positive angle in the range [0, 2*pi]
    if angle < 0:
        angle += 2 * math.pi
    print(round(angle,3))
    return angle


#INTERESSANTE MUDAR + PRA -. QUAL A RELACAO COM +3RADIUS OU -3RADIUS
# Function to plot a circle given center and radius
def plot_circle(x0, y0, radius, start, end, label):
    if start>end:
        end+=2*math.pi
    theta = np.linspace(start, end, 8)
    #theta = np.linspace(2.8079147454115656,5.046066888562858, 200)
    x = x0 + radius * np.cos(theta)
    y = y0 + radius * np.sin(theta)
    plt.plot(x, y)#, label=label)
    return([(xi, yi) for xi, yi in zip(x, y)])

# Function to calculate the center of the circle on the bisector line
def center_on_bisector(A, B, C, x0):
    if B != 0:
        y0 = (-A * x0 - C) / B  # Use the bisector equation to get the corresponding y
        return x0, y0
    else:
        return None  # For vertical lines, handle separately





def execute_fillet(P1,P2,P3,fillet_radius):
    # Calculate the equations of both lines from the points
    a1, b1, c1 = line_from_points(P1, P2)
    a2, b2, c2 = line_from_points(P3, P2)
    
    # Calculate the bisectors
    bisector1, bisector2 = bisector_line(a1, b1, c1, a2, b2, c2)
    
    # Find the intersection of the two original lines
    intersection = find_intersection(a1, b1, c1, a2, b2, c2)
    
    
    
    if intersection is None:
        print("The lines are parallel and do not intersect.")
    else:
        print(f"Intersection point: {intersection}")

        
        # Print the equations of the original lines
        print_line_equation(a1, b1, c1, label="Line 1")
        print_line_equation(a2, b2, c2, label="Line 2")
    
        # Print the equations of the bisectors
        print_line_equation(*bisector1, label="Bisector 1")
        print_line_equation(*bisector2, label="Bisector 2")
    
    
    
        '''# Plot a circle whose center moves along the bisector 1
        for x0 in np.linspace(intersection[0], intersection[0]+1, 2):  # Vary x0 along bisector 1
            center = center_on_bisector(*bisector1, x0)
            print(center)
            if center is not None:
                print(center[0])
                print(center[1])
                plot_circle(center[0], center[1], radius=0.5, label=f"Circle at x0={x0:.1f}")'''
                
    
        #how to use even and odd simetry?
        # Find and plot the circle tangent to Line 1
        my_radius = fillet_radius  # Example radius
        tangent_center = find_tangent_circle_center(a1, b1, c1, *bisector1, radius=my_radius, start_point=intersection[0])
        tangent_center_x=round(tangent_center[0],3)
        tangent_center_y=round(tangent_center[1],3)
        print('Tangent cricle center: ' + str(tangent_center_x) +", "+ str(tangent_center_y))
        
        #Find the insterction between line and circle, so can be use on x_range
        circle_center = (tangent_center_x, tangent_center_y)
        A, B, C = a1, b1, c1
        intersection_points_line1 = circle_line_intersection(circle_center, my_radius, A, B, C)
        A, B, C = a2, b2, c2
        intersection_points_line2 = circle_line_intersection(circle_center, my_radius, A, B, C)
        
        if intersection_points_line1 is None:
            print("No intersection between the circle and the line.")
        else:
            print(f"Intersection points - line 1: {intersection_points_line1}")
            
        '''if intersection_points_line2 is None:
            print("No intersection between the circle and the line.")
        else:
            print(f"Intersection points - line 2: {intersection_points_line2}")'''
            
        #Find the angles for plotting the circle sector
        start_angle=angle_of_point_in_circle(circle_center, intersection_points_line1)
        end_angle=angle_of_point_in_circle(circle_center, intersection_points_line2)
        
        
        #Aqui tem o segundo circulo\/
        #tangent_center2 = find_tangent_circle_center(a1, b1, c1, *bisector2, radius=my_radius, start_point=intersection[0])
        #Aqui o segundo termo serve para inverter a concavidade
        #tangent_center_x2=tangent_center2[0]-2*(tangent_center2[0]-intersection[0])
        #tangent_center_y2=tangent_center2[1]-2*(tangent_center2[1]-intersection[1])
        #print(tangent_center2[0]-intersection[0])
        #print(tangent_center2[1]-intersection[1])
        #print('Tangent cricle center2: ' + str(tangent_center2))
        #print(*bisector2)
        
        #Find the insterction between line and circle, so can be use on x_range
        #circle_center2 = (tangent_center_x2, tangent_center_y2)
        #A, B, C = a1, b1, c1
        #intersection_points_line1 = circle_line_intersection(circle_center2, my_radius, A, B, C)
        #A, B, C = a2, b2, c2
        #intersection_points_line2 = circle_line_intersection(circle_center2, my_radius, A, B, C)
        
        #if intersection_points_line1 is None:
        #    print("No intersection between the circle and the line.")
        #else:
        #    print(f"Intersection points - line 1: {intersection_points_line1}")
            
        #if intersection_points_line2 is None:
        #    print("No intersection between the circle and the line.")
        #else:
        #    print(f"Intersection points - line 2: {intersection_points_line2}")
            
        #Find the angles for plotting the circle sector
        #start_angle2=angle_of_point_in_circle(circle_center2, intersection_points_line1)
        #end_angle2=angle_of_point_in_circle(circle_center2, intersection_points_line2)
        
        #Aqui termina o segundo circulo
        
        
        # Plot the lines
        plt.figure(figsize=(8, 8))
    
        # Define x-range starting from the intersection between circle and lines
        x_range_line1 = [intersection_points_line1[0], 150]
        x_range_line2 = [intersection_points_line2[0], 150]
        
        x_range_line1 = [intersection_points_line1[0], P1[0]]
        x_range_line2 = [P3[0],intersection_points_line2[0]]
    

        
        
    
        # Plot the original lines
        plot_line(a1, b1, c1, x_range_line1, label="Line 1")
        
        #Plot the circle
        plot_circle(tangent_center_x, tangent_center_y, radius=my_radius, start=start_angle, end=end_angle, label="tangent circle")
        #plot_circle(tangent_center_x2, tangent_center_y2, radius=my_radius, start=start_angle2, end=end_angle2, label="tangent circle2")
    
        
        plot_line(a2, b2, c2, x_range_line2, label="Line 2")
        
        # Define x-range starting from the intersection between two lines
        #x_range_bis= [-50, 200]
    
        # Plot the bisectors
        #plot_line(*bisector1, x_range_bis, label="Bisector 1")
        #plot_line(*bisector2, x_range_bis, label="Bisector 2")'''
        
        
    
    
        # Add labels and show the plot
        #plt.axhline(0, color='black', linewidth=0.5)
        #plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True)
        plt.legend()
        plt.xlim([0,1000])
        plt.ylim([-100,2000])
        plt.gca().set_aspect('equal', adjustable='box')  # Equal scaling for x and y axes
        plt.title("BSC drawing")
        plt.show()
        
        return(plot_line(a1, b1, c1, x_range_line1, label="Line 1"),
               plot_circle(tangent_center_x, tangent_center_y, radius=my_radius, start=start_angle, end=end_angle, label="tangent circle"),
               plot_line(a2, b2, c2, x_range_line2, label="Line 2")
               )

