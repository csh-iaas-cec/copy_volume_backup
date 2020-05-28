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
    signer = oci.auth.signers.get_resource_principals_signer()
    blockStorageClient = oci.core.BlockstorageClient(config={}, signer=signer)
    try:
        body = json.loads(data.getvalue())
        volume_group_backup_id = body.get("id")
        logging.info(body)
    except (Exception, ValueError) as ex:
        logging.info('error parsing json payload: ' + str(ex))
    get_volumes(blockStorageClient, volume_group_backup_id)
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Hello"}),
        headers={"Content-Type": "application/json"}
    )
