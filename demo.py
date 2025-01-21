from detetector import Detector
import cv2

param = {"minVar":5,"minRadius":2,"maxRadius":15}

# at 3rd input, range of filter is an array for lower bound and upper bound 
filter_range = [{"low":[150,20,220], "up":[180,255,255]}]
grad_thresh = 50

detection = Detector(1,1, filter_range,grad_thresh,param,1,7)

img = cv2.imread("Senior_Project_Laser_detect/ultrahard_test.jpg")
img = cv2.resize(img,(3840//2, 2176//2))

adjusted_image = detection.adjust(img)
gray_img = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2GRAY)
sobel = detection.Sobel_process(gray_img)
contour = detection.combine_Gradient_with_SpecificColor(img, sobel)
potential_area = detection.Circle_detect(contour, param["minVar"], param["minRadius"], 
                                         param["maxRadius"])

cv2.drawContours(img, potential_area, -1, (0,255,0), 3)
cv2.imshow("sobel", sobel)
cv2.imshow("contour", contour)
cv2.imshow('original',img)
# cv2.imshow("name",adjusted_image)qqq

cv2.waitKey()
cv2.destroyAllWindows()
