import cv2 as cv
import numpy as np

class Detector:

    def __init__(self, classifier_param, network_param_pth, range_filter, grad_thresh, args_in_CDPBS,
                 output_is_circle, structure_size):
        self.range_of_filter = range_filter
        self.grad_thresh = grad_thresh
        self.minVar =  args_in_CDPBS['minVar']
        self.minRadius = args_in_CDPBS['minRadius']
        self.maxRadius = args_in_CDPBS['maxRadius']
        self.output_is_circle = output_is_circle
        self.structure_size = (structure_size,structure_size)
    
    def adjust(self, raw_image):
        img = raw_image.astype(np.float32) /255.0      #transform image array into float for easy division + divide by 255 -> turning into only 1 and 0, easy for machine learning?
        hls_img = cv.cvtColor(img, cv.COLOR_BGR2HLS)    #Hue, lightness, and saturation
        gamma = 3
        s = 100
        MAX_VALUE = 100
        hls_img[:,:,1] = np.power(hls_img[:,:,1], 3)
        hls_img[:,:,2] = (1.0+ 100 /float(100)) * hls_img[:,:,2]
        hls_img[:,:,2][hls_img[:,:,2] > 1] = 1
        adjusted_img =  cv.cvtColor(hls_img,cv.COLOR_HLS2BGR) * 255
        return adjusted_img.astype(np.uint8)
    
    def Sobel_process(self, img):
        dx = cv.Sobel(img, cv.CV_32F, 1, 0)
        dy = cv.Sobel(img, cv.CV_32F, 0, 1)
        mag = cv.magnitude(dx,dy)
        mag = cv.convertScaleAbs(mag)
        return mag
   
    def combine_Gradient_with_SpecificColor(self, raw_img, grad):
        hsv = cv.cvtColor(raw_img, cv.COLOR_BGR2HSV)
        thresh = np.zeros(hsv.shape[:2], dtype=np.uint8)
        for i in self.range_of_filter:
            low_bound = np.array(i['low'])
            upper_bound = np.array(i['up'])
            thresh = thresh | cv.inRange(hsv,low_bound,upper_bound)
        img = grad.copy()
        thresh = cv.morphologyEx(thresh, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_ELLIPSE, self.structure_size))
        img[thresh == 0] = 0
        img = cv.threshold(img, self.grad_thresh, 255, cv.THRESH_BINARY)[1]
        return img
    
    def Variance(self, center, contours): #unsure of the usage
        points = contours.reshape((-1,2))
        distance = np.linmalg.norm(points - center, axis = 1) #find the distance between every point with the center
        variance = np.var(distance)
        return variance
    
    def Circle_detect(self, img, minVar, minRadius, maxRadius):
        result = []
        contour, hiearchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        for i in range(len(contour)):
            center, radius = cv.minEnclosingCircle(contour[i])
            variance = Detector.Variance(center, contour[i])
            if variance < minVar and minRadius< radius < maxRadius:
                result.append(contour[i])
        return result
    
    