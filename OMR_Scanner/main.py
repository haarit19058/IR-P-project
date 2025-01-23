import cv2

image = cv2.imread('./OMR_dataset/images/omr_aiml_dataset_page_6.png',cv2.IMREAD_GRAYSCALE)


blurred_image = cv2.GaussianBlur(image, (5, 5), 3)


edges = cv2.Canny(blurred_image, 50, 150)


cv2.imshow('Original Image', image)
cv2.imshow('Blurred Image', blurred_image)
cv2.imshow('canny without blurr',cv2.Canny(image,50,150))
cv2.imshow('Canny Edges', edges)

# Wait for a key press and close windows
cv2.waitKey(0)