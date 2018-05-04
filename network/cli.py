import argparse
from network.vlan import VlanManager
from network.csvio import CsvIo


def parse_cli_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument(
        'files', type=str, nargs='*', help='test files to use: "test_vlans.csv​ test_requests.csv"'
    )
    parser.add_argument(
        '-v', '--v', action='store_true', help='verbose: shows all the logging'
    )

    args = parser.parse_args()
    if args.files is not None and len(args.files) not in (0, 2):
        parser.error(
            'Either give no values, or "{expect}", not {given}.'.format(
                expect='test_vlans.csv​ test_requests.csv',
                given=' '.join(i.strip() for i in args.files)
            )
        )
    if args.files:
        return (['test_vlans.csv', 'test_requests.csv'], 'test_output.csv')
    else:
        return (['vlans.csv', 'requests.csv'], 'output.csv')


def cli_run(files=None, output_file=None):
    if files is None or output_file is None:
        files, output_file = parse_cli_args()

    vmgr = VlanManager(files[0])
    vmgr.run_requests(files[1], output_file)


if __name__ == '__main__':
    cli_run()
