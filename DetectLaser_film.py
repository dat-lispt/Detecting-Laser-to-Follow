import cv2 as cv
import numpy as np

def nothing(value):
    return

video = cv.VideoCapture("Senior_Project_Laser_detect/test_light.mp4")

hue_value =255
sat_value = 255
V_value = 255

# img_test = cv.imread("Senior_Project_Laser_detect/test_light.mp4")# NEED TO FILM A POINTER

window_name = "Spotting Laser"
title_hue = "Hue slides"
title_saturation = "Saturation slides"
title_value = "Value slides"

cv.namedWindow(window_name, cv.WINDOW_AUTOSIZE)
# cv.createTrackbar(title_hue, window_name, 0, 255, nothing)
# cv.createTrackbar(title_value, window_name, 0, 255,nothing)
# cv.createTrackbar(title_saturation, window_name, 0, 255,nothing)
screen_width = 1080
screen_heigh = 1920

kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5,5))

# if img_test is None:
#     print("Error: no image is loaded")
# else:
#     if img_test.shape[1] > screen_width  or img_test.shape[0] > screen_heigh:
#         print("resizing image")
#         scale_factor = min(screen_width / img_test.shape[1], screen_heigh/ img_test.shape[0])
#         img = cv.resize(img_test, (0,0), fx = scale_factor, fy = scale_factor)
#         # cv.imshow("Image",img)
#     else:
#         img = img_test

# cv.imshow("window",img_test)
while(video.isOpened()):   
    ret, frame = video.read()
    
    if not ret:
        print("Can't find frame")
        break 
    
    HSV_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    h, s ,v = cv.split(HSV_frame)

    # hue_value, sat_value, V_value = cv.getTrackbarPos(title_hue,window_name), cv.getTrackbarPos(title_saturation,window_name), cv.getTrackbarPos(title_value,window_name)
    hue_value, sat_value, V_value = 240, 240, 220

    ret_hue, thresh_hue = cv.threshold(h, hue_value, 255, cv.THRESH_BINARY)
    ret_sat, thresh_sat = cv.threshold(s, sat_value, 255, cv.THRESH_BINARY)
    ret_val, thresh_val = cv.threshold(v, V_value, 255, cv.THRESH_BINARY)

    laser = cv.bitwise_and(thresh_hue, thresh_val)
    laser = cv.bitwise_and(thresh_sat, laser)
    result = cv.merge([thresh_hue,thresh_sat,thresh_val])
    cv.imshow("resutl",result)
    
    mask_clean = cv.morphologyEx(result, cv.MORPH_OPEN, kernel)
    mask_clean = cv.morphologyEx(mask_clean, cv.MORPH_CLOSE, kernel)
    cv.imshow(window_name, mask_clean)
    
    # gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)
    # detected_circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,
    #                                     1, 20, param1 = 22,
    #                                     param2 = 22, minRadius= 1, maxRadius= 50)
    
    # if detected_circles is not None:
    #     frame_copy = gray.copy()
    #     detected_circles = np.uint16(np.around(detected_circles))        

    #     for pt in detected_circles[0,:]:
    #         a, b, r = pt[0], pt[1], pt[2]
    #         cv.circle(frame_copy, (a,b), r, (0,255,0), 2)
    #         cv.imshow("detected Circle", frame_copy)

    if cv.waitKey(100) & 0xFF == ord('q'):
        break

# while(1):

    # _, frame = video.read()
    
    # # frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
    # HSV_frame = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
    # h, s ,v = HSV_frame[:,:,0], HSV_frame[:,:,1], HSV_frame[:,:,2]

    # ret_hue, thresh_hue = cv.threshold(h, 127, hue_value, cv.THRESH_BINARY)
    # ret_sat, thresh_sat = cv.threshold(s, 110, sat_value, cv.THRESH_BINARY)
    # ret_val, thresh_val = cv.threshold(v, 110, V_value, cv.THRESH_BINARY)

# cv.waitKey()

# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# gray = cv.blur(gray,(3,3))
# cv.imshow("gray", gray)

# cv.createTrackbar("param1", window_name, 0, 60, nothing)
# cv.createTrackbar("Param2", window_name, 0, 60, nothing)

# while(1):
#     param1_value  , param2_value = cv.getTrackbarPos("param1", window_name) + 20, cv.getTrackbarPos("Param2", window_name) + 10
#     detected_circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT,
#                                             1, 5, param1= param1_value,
#                                             param2= param2_value , minRadius= 1, maxRadius= 100)

#     if detected_circles is not None:
#         image_copy = img.copy()
#         print("detect")
#         detected_circles = np.uint16(np.around(detected_circles))        
#         for pt in detected_circles[0,:]:
#             a, b, r = pt[0], pt[1], pt[2]
#             cv.circle(image_copy, (a,b), r, (0,255,0), 2)
#             cv.imshow("detected Circle", image_copy)
#     else:
#         print("didn't dectect :(")
#     if cv.waitKey(200) & 0xFF == ord('q'):
#         break
video.release()
cv.destroyAllWindows()