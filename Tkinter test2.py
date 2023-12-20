import cv2
import numpy as np

# Read the DICOM image using OpenCV
image = cv2.imread(r'C:\Users\Admin\Desktop\TG\TEST\img\HN001\case1_008.dcm', cv2.IMREAD_UNCHANGED)

# Check if the image is read correctly
if image is None:
    print("Error: Could not read the DICOM image.")
    exit()

# Create an array of zeros of the same size as the DICOM image
zero_array = np.zeros_like(image)

# Set the brightness adjustment parameters
alpha = 1.5  # To increase brightness (you can adjust this value as per your requirement)
beta = 0
gamma = 0

# Adjust the brightness using addWeighted function
adjusted_image = cv2.addWeighted(image, alpha, zero_array, beta, gamma)

# Save or display the adjusted image
cv2.imwrite('adjusted_dicom_image.dcm', adjusted_image)
