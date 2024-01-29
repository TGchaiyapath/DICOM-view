from pynetdicom import AE ,debug_logger
from pynetdicom.sop_class import Verification

debug_logger()
# Initialise the Application Entity
ae = AE()

# Add a requested presentation context
ae.add_requested_context(Verification)

# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate("192.168.1.165", 4242)
assoc.send_c_echo()
status = assoc.send_c_echo()

    # Check the status of the verification request
if status:
        # If the verification request succeeded this will be 0x0000
        print('C-ECHO request status: 0x{0:04x}'.format(status.Status))
else:
        print('Connection timed out, was aborted or received invalid response')





assoc.release()
