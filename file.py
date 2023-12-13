import pydicom  as dicom

path="./img/case1_008.dcm"
x=dicom.dcmread(path)
print(dir(x))

import matplotlib.pyplot as plt
import pydicom as dicom


path ="./img/case1_008.dcm"
x=dicom.dcmread(path)
plt.imshow(x.pixel_array,cmap=plt.cm.gray)
plt.show()

