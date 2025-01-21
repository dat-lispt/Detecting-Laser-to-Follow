import cv2 as cv
import numpy as np

def nothing(value):
    return


hue_value =255
sat_value = 255
V_value = 255

img_test = cv.imread("Senior_Project_Laser_detect/Case_light_close.jpg")

window_name = "Spotting Laser"
title_hue = "Hue slides"
title_saturation = "Saturation slides"
title_value = "Value slides"

cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
cv.createTrackbar(title_hue, window_name, 0, 255, nothing)
cv.createTrackbar(title_value, window_name, 0, 255,nothing)
cv.createTrackbar(title_saturation, window_name, 0, 255,nothing)
screen_width = 1080
screen_heigh = 1920

if img_test is None:
    print("Error: no image is loaded")
else:
    if img_test.shape[1] > screen_width  or img_test.shape[0] > screen_heigh:
        print("resizing image")
        scale_factor = min(screen_width / img_test.shape[1], screen_heigh/ img_test.shape[0])
        img = cv.resize(img_test, (0,0), fx = scale_factor, fy = scale_factor)
        # cv.imshow("Image",img)
    else:
        img = img_test

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))

# PRE_SET Hough Param
# cv.createTrackbar("param1", window_name, 0, 60, nothing)
# cv.createTrackbar("Param2", window_name, 0, 60, nothing)
#  param1_value = 18
# param2_value = 18

# count = 0
if img_test is None:
        print("Error: no image is loaded")
else:
    while(True):
        HSV_frame = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        h, s ,v = cv.split(HSV_frame)

        # param1_value  , param2_value = cv.getTrackbarPos("param1", window_name) + 20, cv.getTrackbarPos("Param2", window_name) + 10
        hue_value, sat_value, V_value = cv.getTrackbarPos(title_hue,window_name), cv.getTrackbarPos(title_saturation,window_name), cv.getTrackbarPos(title_value,window_name)
        # hue_value, sat_value, V_value = 240, 200, 251

        ret_hue, thresh_hue = cv.threshold(h, 35, 85, cv.THRESH_BINARY)
        ret_sat, thresh_sat = cv.threshold(s, sat_value, 255, cv.THRESH_BINARY)
        ret_val, thresh_val = cv.threshold(v, V_value, 255, cv.THRESH_BINARY)
                
        laser = cv.bitwise_and(thresh_hue, thresh_val)
        laser = cv.bitwise_and(thresh_sat, laser)
        result = cv.merge([thresh_hue,thresh_sat,thresh_val])
        cv.imshow("resutl",result)
        color_result = cv.cvtColor(result, cv.COLOR_HSV2BGR)

        mask_clean = cv.morphologyEx(result, cv.MORPH_OPEN, kernel)
        mask_clean = cv.morphologyEx(mask_clean, cv.MORPH_CLOSE, kernel)
        cv.imshow("morph filter", mask_clean)
        
        #ADPATIVE THRESHOLDING
        # mask_blur = cv.GaussianBlur(mask_clean, (3,3), 2)
        # cv.imshow("blur", mask_blur)

        result = cv.cvtColor(color_result, cv.COLOR_BGR2GRAY)
        thresh = cv.adaptiveThreshold(result, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv.THRESH_BINARY, 11, 2)
        cv.imshow("threshold", thresh)

        # gray = cv.cvtColor(mask_clean, cv.COLOR_BGR2GRAY)
        # detected_circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,
        #                                     1.2, 30, param1 = param1_value,
        #                                     param2 = param2_value, minRadius= 1, maxRadius = 30)
        # if detected_circles is not None:
        #     detected_circles = np.uint16(np.around(detected_circles))     
        #     img_copy = img.copy()   

        #     for pt in detected_circles[0,:]:
        #         a, b, r = pt[0], pt[1], pt[2]
        #         cv.circle(img_copy, (a,b), r, (0,255,0), 2)
        #         cv.imshow(window_name, img_copy)
                
        # count += 1
        # if count >= 50:
        #     print("%d , %d" % (param1_value, param2_value) )
        #     count = 0

        if cv.waitKey(50) & 0xFF == ord('q'):
            break

cv.destroyAllWindows()