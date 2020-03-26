import argparse


class SplitAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(SplitAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            endpoint, path = values.split(':')
        except ValueError:
            raise argparse.ArgumentError(self, 'not in the required format of ENDPOINT:PATH')
        if not endpoint:
            raise argparse.ArgumentError(self, 'endpoint not specified')
        if not path:
            raise argparse.ArgumentError(self, 'path not specified')
        setattr(namespace, self.dest + '_endpoint', endpoint)
        setattr(namespace, self.dest + '_path', path)


class UOCloudSyncCli:
    def __init__(self):
        program_description = 'Sync files between UOCloud storage and Talapas'
        parser = argparse.ArgumentParser(description=program_description,
                                         add_help=False,
                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('--src', metavar='Source to copy', action=SplitAction, required=True,
                            help='ENDPOINT:SRC ENDPOINT is a Globus endpoint name, followed by colon character'
                                 ' \':\', followed by SRC the absolute path to the source directory to copy',
                            dest='src')

        parser.add_argument('--dest', metavar='Destination for copy', action=SplitAction, required=True,
                            help='ENDPOINT:DEST ENDPOINT is a Globus endpoint name, followed by colon character'
                                 ' \':\', followed by DEST the absolute path to the destination',
                            dest='dest')

        self._args = parser.parse_args()

    def get_src_endpoint(self):
        return self._args.src_endpoint

    def get_dest_endpoint(self):
        return self._args.dest_endpoint

    def get_src_path(self):
        return self._args.src_path

    def get_dest_path(self):
        return self._args.dest_path
