import cv2

# Placeholder script: reads an image and prints its shape
img = cv2.imread('input.jpg')
if img is None:
    print('Place an image named input.jpg in the folder to run this demo')
else:
    print('Image shape:', img.shape)
