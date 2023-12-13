import numpy as np  
import matplotlib.pyplot as plt
import pydicom
import cv2 

dicom_image = pydicom.dcmread(r'img/HN001/case1_008.dcm').pixel_array

#ensure the image is in 8 bit format 
dicom_image=(dicom_image/np.max(dicom_image)*255).astype(np.unit8)

#display original
plt.figure(figsize=(6,6))
plt.imshow(dicom_image,cmap='gray')
plt.title('original')
plt.show()