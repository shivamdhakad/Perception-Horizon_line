
# import library
import cv2
import matplotlib.pyplot as plt
import numpy as np
import math

# plt.imshow(image)
import cv2
from matplotlib import pyplot as plt


def Horizon_line(image):
    lower_threshold = 245
    upper_threshold = 255
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #  thresholding
    thresholded_image = cv2.threshold(gray, lower_threshold, upper_threshold, cv2.THRESH_BINARY)[1]
    plt.imshow(thresholded_image)
    # edge detection
    edges = cv2.Canny(thresholded_image, 50, 150, apertureSize=3)
    #Line Detection using Hough Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, threshold=70, minLineLength=90, maxLineGap= 20)

    #Filter out parallel lines
    filtered_lines = []
    for i in range(len(lines)-1):
        x1, y1, x2, y2 = lines[i][0]
        angle1 = np.rad2deg(np.arctan2(y2 - y1, x2 - x1))
        # print(angle1)
        parallel_count = 0
        # if -10<=angle1<=10 or 85<=angle1<=95 or -90<=angle1<=-85:
        #     continue
        if -5<=angle1<=5 or 85<=angle1<=95 or -90<=angle1<=-85:
            continue

        filtered_lines.append(lines[i])

    image2 = image.copy()
    for line in filtered_lines:
        x1 , y1, x2 , y2 = line[0]
        cv2.line(image2, (x1,y1), (x2,y2), (250,0,0),2)
    plt.imshow(image2)


    parallel_line_list = []

    for i in range(len(filtered_lines)):
        x1, y1, x2, y2 = filtered_lines[i][0]
        l = (x1, y1, x2, y2)
        print(x1, y1, x2, y2)
        
        parallel_line_list.append(l)
    print(parallel_line_list)


    line1= parallel_line_list[0]
    line2= parallel_line_list[1]

    def plot_and_find_intersection(image, line1, line2):

        # Extract line coordinates
        line1 = tuple(int(x) for x in line1)
        line2 = tuple(int(x) for x in line2)
        x1_1, y1_1, x1_2, y1_2  = line1  # changed order of points
        x2_1, y2_1, x2_2, y2_2 = line2

        pt1_l1 = (int(x1_1),int(y1_1)) 
        pt1_l2 =  (int(x2_1),int(y2_1)) 
        pt2_l1 = (int(x1_2),int(y1_2)) 
        pt2_l2= (int(x2_2),int(y2_2))


        # # Draw lines on the image 
        cv2.line(image, pt1_l1,pt2_l1, (255, 0, 0), 4)  # Blue line
        cv2.line(image, pt1_l2,pt2_l2,  (0, 0, 255), 4) # red line 

        # slope of line1
        start_point= list(pt2_l1)
        end_point = list(pt1_l1)
        l1_slope = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
        print("l1_slope:",l1_slope)

        l2_start_point = list(pt2_l2)
        l2_end_point = list(pt1_l2)
        l2_slope = (l2_end_point[1] - l2_start_point[1]) / (l2_end_point[0] - l2_start_point[0])
        print("l2_slope:",l2_slope)

        # Check for parallel lines (avoid division by zero)
        if l1_slope == l2_slope:
            return None

        # Calculate the x-coordinate of the intersection point
        x_intersect = (l2_start_point[1] - start_point[1] + l1_slope * start_point[0] - l2_slope * l2_start_point[0]) / (l1_slope - l2_slope)

        # Calculate the y-coordinate of the intersection point using the equation of either line
        y_intersect = l1_slope * (x_intersect - start_point[0]) + start_point[1]
        print("intersection_points(x,y):", x_intersect , y_intersect)
        x_intersect = int(x_intersect)
        y_intersect = int(y_intersect)
        hl_start_point = (0, y_intersect)
        hl_end_point = (image.shape[1], y_intersect)
        # Draw the line parallel to x-axis
        cv2.line(image, hl_start_point, hl_end_point, (0, 155, 255), 6)  # Blue line with thickness 2  # horizon  line 

        cv2.circle(image, (x_intersect,y_intersect), 5, (255, 0, 0), -1)  # vanishing point # Green circle at intersection #random pt test
        print("y_intesecpt:", y_intersect)
        return (x_intersect, y_intersect) , image

    ipt_img = image.copy()
    print("img_shape", ipt_img.shape)
    intersection_point ,image = plot_and_find_intersection(ipt_img, line1, line2)

    if intersection_point:
        # print("Intersection point:", intersection_point)
        # cv2.imshow("Image with Lines and Intersection", image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        plt.imshow(image)
        plt.show()
    else:
        print("Lines don't intersect!")

    return image

# image_path = 'path/to/your/image.jpg'  # add path to the image

image = cv2.imread(image_path)
Horizon_line(image)
