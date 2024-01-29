from pynetdicom import AE, debug_logger
from pynetdicom.sop_class import Verification
debug_logger()
# Initialise the Application Entity
ae = AE()

# Add requested presentation context for Verification and C-GET
ae.add_requested_context(Verification)

# Associate with peer AE at IP 192.168.1.203 and port 4242
assoc = ae.associate("192.168.1.165", 4242)

# Check if the association was accepted
if assoc.is_established:
    # Perform DICOM services here (e.g., C-ECHO, C-GET)

    # Release the association when done
    assoc.release()
else:
    print('Association rejected or unable to establish.')
