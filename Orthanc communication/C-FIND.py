from pynetdicom import AE ,evt, build_role, debug_logger
from pydicom.dataset import Dataset
from pynetdicom.sop_class import (Verification,PatientRootQueryRetrieveInformationModelFind)

debug_logger()
# Initialise the Application Entity
ae = AE()
ae.ae_title = 'SCU_PACS'


# Add a requested presentation context
ae.add_requested_context(Verification)
ae.add_requested_context(PatientRootQueryRetrieveInformationModelFind)

ds = Dataset()
ds.SOPClassesInStudy = '1.2.840.10008.5.1.4.1.1.2'
ds.PatientID = 'fbec5c3e-3361-4e95-9d68-75d82c64c836'
ds.QueryRetrieveLevel = 'STUDY'
# Associate with peer AE at IP 127.0.0.1 and port 11112
assoc = ae.associate("10.53.47.41", 4242)

# Check if association is established
if assoc.is_established:
    # Create a C-MOVE request dataset
    assoc.send_c_echo()
    
    # Send C-MOVE request
    findresponses = assoc.send_c_find(ds,PatientRootQueryRetrieveInformationModelFind)
    for (status, identifier) in findresponses:
        if status:
            print('C-FIND query status: 0x{0:04X}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

    # Release the association
    assoc.release()
else:
    print("Association not established")
