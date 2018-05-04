from collections import OrderedDict
from network.csvio import CsvIo


class VlanManager:
    '''
    Class to manage the vlans.
    '''

    def __init__(self, vlans_file):
        self.data = CsvIo(vlans_file).read()
        self.sauce()

    def sauce(self):
        '''
        Separate the vlans into primaries and secondaries ordered
        by vlan_id and device_id.
        It makes simpler the assignment of requests to ports.
        '''

        self.primaries = list(i for i in filter(
            lambda v: v['primary_port'] == '1',
            self.data.sort(headers=('vlan_id', 'device_id')))
        )
        self.secondaries = (i for i in filter(
            lambda v: v['primary_port'] == '0',
            self.data.sort(headers=('vlan_id', 'device_id')))
        )

    def request(self, request):
        '''
        non redundant: use the lowest vlanid available for a primary port.
        redundant: use the lowest vlanid for both primary and secondary port
        on the same device. Also, the device has to be the lowest numbered
        one (in case of a tie, use the lower device_id).

        :returns the primary port found:
        '''

        # if redundant, runs the secondaries until finds
        # a match with the primaries
        # if the primary isn't available, just discards the
        # secondary (secondaries alone are useless here)
        # and tries the next one
        vlan = None
        if request['redundant'] == '1':
            for vlan in self.secondaries:
                # just to check if the eq port
                # is in the primary ones
                # return it if is
                vlan['primary_port'] = '1'
                if vlan in self.primaries:
                    self.primaries.remove(vlan)
                    vlan['request_id'] = request['request_id']
                    return vlan
            else:
                # if the forloop ends normaly, the secondaries are over
                # and we can't do any more for redundancy
                return None

        if vlan is None:
            try:
                vlan = self.primaries.pop(0)
                vlan['request_id'] = request['request_id']
            except IndexError:
                return None

        return vlan

    def _gen_responses(self, requests_io):
        for req in requests_io:
            vlan = self.request(req)
            if vlan is None:
                vlan = OrderedDict()
                vlan['request_id'] = req['request_id']
                vlan['primary_port'] = '1'
                vlan['vlan_id'] = '-1'
                vlan['device_id'] = '-1'
                yield vlan
                continue

            if req['redundant'] == '1':
                yield dict(vlan.items())
                vlan['primary_port'] = '0'
            yield vlan

    def run_requests(self, requests_file, output_file):
        reqs_io = CsvIo(requests_file).read()
        out_writer = CsvIo(output_file).create_file().read()

        headers = ('request_id', 'primary_port', 'vlan_id', 'device_id')
        out_data = sorted(
            self._gen_responses(reqs_io),
            key=lambda row: [int(row[h]) for h in headers],
            reverse=False
        )
        out_writer.write(
            data=out_data,
            headers=headers
        )
