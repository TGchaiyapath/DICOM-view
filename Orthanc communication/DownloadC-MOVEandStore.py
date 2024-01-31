from pynetdicom import AE ,evt, StoragePresentationContexts, debug_logger
from pydicom.dataset import Dataset
from pynetdicom.sop_class import (PatientRootQueryRetrieveInformationModelMove)
import os

debug_logger()
def handle_store(event):
        """Handle a C-STORE service request"""
        # Nothing fancy, just write to DICOM File Format
        ds = event.dataset
        ds.file_meta = event.file_meta
        ds.save_as(ds.SOPInstanceUID, write_like_original=False)
        

        return 0x0000



# Bind our C-STORE handler
handlers = [(evt.EVT_C_STORE, handle_store)]


# Initialise the Application Entity
ae = AE()


# Add the requested presentation context (Storage SCP)
ae.add_requested_context(PatientRootQueryRetrieveInformationModelMove)

# Add the Storage SCP's supported presentation contexts
ae.supported_contexts = StoragePresentationContexts

# Start our Storage SCP in non-blocking mode, listening on port 11120
ae.ae_title = 'OUR_AE'
scp = ae.start_server(("10.53.47.41", 11112), block=False, evt_handlers=handlers)


# Associate with peer AE at IP 127.0.0.1 and port 11112

#custommovedata set
move_dataset = Dataset()
move_dataset.QueryRetrieveLevel = 'SERIES'
move_dataset.PatientID = 'LCTSC-Test-S1-104'
move_dataset.StudyInstanceUID = '1.3.6.1.4.1.14519.5.2.1.7014.4598.829677454205016768063779242553'
move_dataset.SeriesInstanceUID = '1.2.276.0.7230010.3.1.3.213603947.20628.1706035091.225'

assoc = ae.associate("10.53.47.41", 4242)
# Check if association is established
if assoc.is_established:
    # Create a C-MOVE request dataset
   
    
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
