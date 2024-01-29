import tkinter as tk
from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import Verification

class DICOMClientApp:
    def __init__(self, master):
        # Initialize the Application Entity
        self.ae = AE()
        self.master = master
        master.title("DICOM Client")

        self.label_ip = tk.Label(master, text="Server IP:")
        self.label_ip.pack()

        self.entry_ip = tk.Entry(master)
        self.entry_ip.pack()

        self.label_port = tk.Label(master, text="Server Port:")
        self.label_port.pack()

        self.entry_port = tk.Entry(master)
        self.entry_port.pack()

        self.btn_connect = tk.Button(master, text="Connect and Send C-ECHO", command=self.connect_and_send_echo)
        self.btn_connect.pack()
       

    def connect_and_send_echo(self):
        server_ip = self.entry_ip.get()
        server_port = int(self.entry_port.get())

        # Initialize the Application Entity
        ae = AE()
        ae.ae_title = 'SCU_AE_TITLE'


        # Add a requested presentation context
        ae.add_requested_context(Verification)

        # Associate with peer AE at the specified IP and port
        assoc = ae.associate(server_ip, server_port)

        # Send C-ECHO request
        if assoc.is_established:
            status = assoc.send_c_echo()

            # Check the status of the verification request
            if status:
                # If the verification request succeeded, this will be 0x0000
                print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
            else:
                print('Connection timed out, was aborted or received invalid response')

            # Release the association
            assoc.release()
        else:
            print('Association not established. Check IP and port.')


if __name__ == "__main__":
    root = tk.Tk()
    app = DICOMClientApp(root)
    root.mainloop()
