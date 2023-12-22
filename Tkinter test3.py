import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
import numpy as np

# Load the DICOM image
dicom_path = 'path_to_dicom_file.dcm'
dicom_dataset = pydicom.dcmread(dicom_path)

# Get pixel array and apply VOI LUT (if present)
image = apply_voi_lut(dicom_dataset.pixel_array, dicom_dataset)

# Reduce brightness by subtracting a constant (e.g., 50)
adjusted_image = np.clip(image.astype(np.int16) - 50, 0, 32767).astype(np.uint16)

# Update pixel data in DICOM dataset
dicom_dataset.PixelData = adjusted_image.tobytes()

# Save the adjusted DICOM image
output_path = 'adjusted_dicom_file.dcm'
dicom_dataset.save_as(output_path)