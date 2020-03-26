from .uocloud_sync_config import UOCloudSyncConfig
from globus_sdk import ConfidentialAppAuthClient, \
    ClientCredentialsAuthorizer, \
    TransferClient, \
    TransferData, \
    TransferAPIError
from typing import Union
from pathlib import Path
from os import PathLike
import sys


class UOCloudTransferClient:
    def __init__(self, config: UOCloudSyncConfig):
        confidential_client = ConfidentialAppAuthClient(
            client_id=config.get_client_id(), client_secret=config.get_client_secret())
        scopes = "urn:globus:auth:scope:transfer.api.globus.org:all"
        cc_authorizer = ClientCredentialsAuthorizer(confidential_client, scopes)
        # create a new client
        self._transfer_client = TransferClient(authorizer=cc_authorizer)
        self._src_endpoint = None
        self._dest_endpoint = None

    def get_endpoint_id(self, endpoint_name: str):
        kwargs = {}
        endpoints = self._transfer_client.endpoint_search(filter_fulltext=endpoint_name, **kwargs)
        # Just return the first result. Hope it is right!
        for ep in endpoints:
            return ep['id']

    def transfer_data(self, src_endpoint: str, src_path: Union[str, Path, PathLike],
                      dest_endpoint: str, dest_path: Union[str, Path, PathLike]):
        self._src_endpoint = src_endpoint
        self._dest_endpoint = dest_endpoint
        src_endpoint_id = self.get_endpoint_id(src_endpoint)
        if not src_endpoint_id:
            print(f'ERROR: Unable to find source endpoint id for: "{self._src_endpoint}"')
            return

        dest_endpoint_id = self.get_endpoint_id(dest_endpoint)
        if not dest_endpoint_id:
            print(f'ERROR: Unable to find destination endpoint id for: "{self._dest_endpoint}"')
            return

        transfer_data = TransferData(self._transfer_client,
                                     src_endpoint_id,
                                     dest_endpoint_id,
                                     encrypt_data=True)
        transfer_data.add_item(src_path, dest_path, recursive=True)
        try:
            print(
                f'Submitting a transfer task from {self._src_endpoint}:{src_path} to {self._dest_endpoint}:{dest_path}')
            task = self._transfer_client.submit_transfer(transfer_data)
        except TransferAPIError as e:
            print(str(e))
            sys.exit(1)
        print(f'\tWaiting for transfer to complete with task_id: {task["task_id"]}')
        self._transfer_client.task_wait(task_id=task['task_id'], timeout=60, polling_interval=60)
