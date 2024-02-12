from pydicom import dcmread
from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import (MRImageStorage,CTImageStorage,UltrasoundImageStorage,XRayAngiographicImageStorage,
PositronEmissionTomographyImageStorage,ComputedRadiographyImageStorage,DigitalXRayImageStorageForPresentation,
DigitalXRayImageStorageForProcessing)
from tkinter import Tk, Label, Entry, Button, filedialog

debug_logger()
def send_files():
    # Read server IP, port, and selected DICOM files
    server_ip = ip_entry.get()
    server_port = int(port_entry.get())
    file_paths = filedialog.askopenfilenames(title='Select DICOM files', filetypes=[('DICOM Files', '*.dcm')])

    if not file_paths:
        status_label.config(text='No files selected.')
        return

    # Initialize the Application Entity
    ae = AE()
    ae.ae_title = 'OUR_AE'
    ae.add_requested_context(MRImageStorage)
    ae.add_requested_context(CTImageStorage)
    ae.add_requested_context(UltrasoundImageStorage)
    ae.add_requested_context(XRayAngiographicImageStorage)
    ae.add_requested_context(PositronEmissionTomographyImageStorage)
    ae.add_requested_context(ComputedRadiographyImageStorage)
    ae.add_requested_context(DigitalXRayImageStorageForPresentation)
    ae.add_requested_context(DigitalXRayImageStorageForProcessing)

    assoc = ae.associate(server_ip, server_port)
    for file_path in file_paths:
       

        # Associate 

        
        if assoc.is_established:
            # Use the C-STORE service to send the dataset
            # Read in the selected DICOM dataset
            ds = dcmread(file_path)
            status = assoc.send_c_store(ds)

            # Check the status of the storage request
            if status:
                # If the storage request succeeded, this will be 0x0000
                status_label.config(text='C-STORE request status for file {}: 0x{:04x}'.format(file_path, status.Status))
            else:
                status_label.config(text='Connection timed out, was aborted, or received an invalid response for file {}'.format(file_path))

            # Release the association
            assoc.release()
        else:
            status_label.config(text='Association rejected, aborted, or never connected for file {}'.format(file_path))

# Create a Tkinter root window
root = Tk()
root.title("DICOM Sender")

# Server IP Entry
ip_label = Label(root, text="Server IP:")
ip_label.grid(row=0, column=0, padx=5, pady=5)
ip_entry = Entry(root)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

# Server Port Entry
port_label = Label(root, text="Server Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = Entry(root)
port_entry.grid(row=1, column=1, padx=5, pady=5)

# Send Button
send_button = Button(root, text="Send Files", command=send_files)
send_button.grid(row=2, column=0, columnspan=2, pady=10)

# Status Label
status_label = Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2, pady=5)

# Start the GUI event loop
root.mainloop()