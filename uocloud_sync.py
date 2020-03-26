from uocloud_sync.uocloud_sync_cli import UOCloudSyncCli
from uocloud_sync.uocloud_sync_config import UOCloudSyncConfig
from uocloud_sync.uocloud_transfer_client import UOCloudTransferClient

cli = UOCloudSyncCli()

transfer_client = UOCloudTransferClient(UOCloudSyncConfig())

transfer_client.transfer_data(cli.get_src_endpoint(), cli.get_src_path(), cli.get_dest_endpoint(), cli.get_dest_path())
