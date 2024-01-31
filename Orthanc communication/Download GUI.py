from pynetdicom import AE, evt, StoragePresentationContexts
from pydicom.dataset import Dataset
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelMove
import tkinter as tk
from tkinter import ttk


def handle_store(event):
    """Handle a C-STORE service request"""
    # Nothing fancy, just write to DICOM File Format
    ds = event.dataset
    ds.file_meta = event.file_meta
    ds.save_as(ds.SOPInstanceUID, write_like_original=False)

    return 0x0000


def start_server(ip, port):
    # Bind our C-STORE handler
    handlers = [(evt.EVT_C_STORE, handle_store)]

    # Initialise the Application Entity
    ae = AE()

    # Add the requested presentation context (Storage SCP)
    ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

    # Add the Storage SCP's supported presentation contexts
    ae.supported_contexts = StoragePresentationContexts

    # Try binding to the specified port
    for attempt in range(5):  # Try up to 5 times to find an available port
        try:
            # Start our Storage SCP in non-blocking mode, listening on the specified IP and port
            ae.ae_title = 'OUR_AE'
            scp = ae.start_server((ip, port + attempt), block=False, evt_handlers=handlers)
            return ae, scp
        except PermissionError as e:
            # Port is likely in use, try the next one
            print(f"Port {port + attempt} is in use. Trying an alternative port.")
            continue
    else:
        # Unable to find an available port after 5 attempts
        raise RuntimeError("Unable to find an available port for the server.")


def move_and_release_association(ae, move_dataset, dest_ip, dest_port):
    # Associate with peer AE at the specified IP and port
    assoc = ae.associate(dest_ip, dest_port)

    # Check if association is established
    if assoc.is_established:
        # Use the C-MOVE service to send the identifier
        responses = assoc.send_c_move(move_dataset, 'OUR_AE', PatientRootQueryRetrieveInformationModelMove)
        for (status, identifier) in responses:
            if status:
                print('C-MOVE query status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

        # Release the association
        assoc.release()
    else:
        print("Association not established")


def on_button_click():
    # Get values from entry widgets
    ip_address = ip_entry.get()
    port = int(port_entry.get())

    # Create a C-MOVE request dataset
    move_dataset = Dataset()
    move_dataset.QueryRetrieveLevel = 'SERIES'
    move_dataset.PatientID = 'LCTSC-Test-S1-104'
    move_dataset.StudyInstanceUID = '1.3.6.1.4.1.14519.5.2.1.7014.4598.829677454205016768063779242553'
    move_dataset.SeriesInstanceUID = '1.2.276.0.7230010.3.1.3.213603947.20628.1706035091.225'

    # Start the server and move data
    ae, scp = start_server(ip_address, port)
    move_and_release_association(ae, move_dataset, "10.53.47.41", 4242)


# Create tkinter window
window = tk.Tk()
window.title("DICOM Configuration")

# IP Address Entry
ip_label = ttk.Label(window, text="Enter IP Address:")
ip_label.grid(row=0, column=0, padx=5, pady=5)
ip_entry = ttk.Entry(window)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

# Port Entry
port_label = ttk.Label(window, text="Enter Port:")
port_label.grid(row=1, column=0, padx=5, pady=5)
port_entry = ttk.Entry(window)
port_entry.grid(row=1, column=1, padx=5, pady=5)

# Button to start the operation
start_button = ttk.Button(window, text="Start Operation", command=on_button_click)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

# Run the tkinter event loop
window.mainloop()
