from pynetdicom import AE ,evt, build_role, debug_logger
from pydicom.dataset import Dataset
from pynetdicom.sop_class import (Verification,
  PatientRootQueryRetrieveInformationModelGet,
  PatientRootQueryRetrieveInformationModelMove,
    CTImageStorage)
debug_logger()
# Initialise the Application Entity
ae = AE()
ae.ae_title = 'SCU_PACS'


# Add a requested presentation context
ae.add_requested_context(Verification)

# Add the requested presentation context (Storage SCP)
ae.add_requested_context(CTImageStorage)
ae.add_requested_context(PatientRootQueryRetrieveInformationModelGet)
role = build_role(CTImageStorage, scp_role=True)


# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate("10.53.47.41", 4242)

# Check if association is established
if assoc.is_established:
    # Create a C-MOVE request dataset
    assoc.send_c_echo()
    get_dataset =Dataset()
    get_dataset.PatientID = 'LCTSC-Test-S1-104'

    
    # Send C-MOVE request
    getresponses = assoc.send_c_get(get_dataset,PatientRootQueryRetrieveInformationModelGet)
   


    for (status, dataset) in getresponses:
        if status.Status in (0xFF00, 0xFF01):  # Pending statuses
            print("C-MOVE operation is pending...")
        elif status.Status == 0x0000:  # Success
            print("C-GET operation completed successfully")
        else:
            print(f"Error: C-GET operation failed with status {status!r}")
 
    
    assoc.release()
else:
    print("Association not established")
