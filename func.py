import io
import json
import logging
import oci

from fdk import response

def get_volumes(blockStorageClient, volume_group_backup_id):
    volume_group_backup = blockStorageClient.get_volume_group_backup(volume_group_backup_id).data
    backup_ids = volume_group_backup.volume_backup_ids
    for backup_id in backup_ids:
        copy_vol(blockStorageClient, backup_id)

def copy_vol(blockStorageClient, volume_backup_id):
    copy_volume_backup_details = oci.core.models.CopyVolumeBackupDetails(destination_region="us-phoenix-1")
    blockStorageClient.copy_volume_backup(volume_backup_id, copy_volume_backup_details)

def handler(ctx, data: io.BytesIO=None):
    delegation_token = open('/etc/oci/delegation_token', 'r').read()
    signer = oci.auth.signers.InstancePrincipalsDelegationTokenSigner(delegation_token=delegation_token)
    blockStorageClient = oci.core.BlockstorageClient(config={}, signer=signer)
    try:
        body = json.loads(data.getvalue())
        logging.info(body)
        volume_group_backup_id = body.get("id")
        # volume_group_backup_id = "ocid1.volumegroupbackup.oc1.iad.abuwcljryruljo27yv7kvgi6jmijojglh2ktuxgqurs6gituzo66z662npta"
        # logging.info(body)
    except (Exception, ValueError) as ex:
        logging.info('error parsing json payload: ' + str(ex))
    get_volumes(blockStorageClient, volume_group_backup_id)
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello"}),
        headers={"Content-Type": "application/json"}
    )
