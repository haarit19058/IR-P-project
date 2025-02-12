




import cv2
import numpy as np

def detect_bubbles(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # blurred = cv2.GaussianBlur(image, (5, 5), 0)
    # edged = cv2.Canny(image, 50, 150)
    
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    bubbles = []
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        bubbles.append((x, y, w, h))
        
    
    output = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    for (x, y, w, h) in bubbles:
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    # cv2.imshow("Edges",edged)
    cv2.imshow("Detected Bubbles", output)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return bubbles

# Example usage:
bubbles = detect_bubbles("./OMR_dataset/images/omr_aiml_dataset_page_6.png")