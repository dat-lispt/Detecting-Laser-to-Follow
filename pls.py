import cv2
import numpy as np

# image = cv2.imread("Senior_Project_Laser_detect/ultrahard_test.jpg")
# img = image.astype(np.float32) / 255.0
# hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

# hls[:,:,1] = np.power(hls[:,:,1], 3)
# hls[:,:,2] = (1.0+ 100 /float(100)) * hls[:,:,2]
# hls[:,:,2][hls[:,:,2] > 1] = 1

# cv2.imshow("image", img)

# print(img.ndim)

# cv2.waitKey()
# cv2.destroyAllWindows()

# Example of a Lightness channel (normalized to [0, 1])
lightness = np.array([[0.2, 0.5, 1.2], [0.8, 1.5, 0.9]])

# Apply the condition and clipping
lightness[lightness > 1] = 1

print(lightness)
