import os

import pytest


@pytest.mark.vlan
@pytest.mark.unit
@pytest.mark.parametrize('filename', [
    'vlans.csv',
    'test_vlans.csv'
])
def test_init_vlan(filename):
    from network.vlan import VlanManager
    vmgr = VlanManager(filename)

    pcount, scount = 0, 0
    for i in vmgr.primaries:
        assert i['primary_port'] == '1'
        pcount += 1
    for i in vmgr.secondaries:
        assert i['primary_port'] == '0'
        scount += 1

    assert len(vmgr.data) == (pcount + scount)


@pytest.mark.vlan
@pytest.mark.unit
@pytest.mark.parametrize('request_id,redundant', [
    ('0', '1'),
    ('1', '0'),
])
def test_request(request_id, redundant):
    from network.vlan import VlanManager
    vmgr = VlanManager('test_vlans.csv')
    req = {
        'request_id': request_id,
        'redundant': redundant
    }

    resp = vmgr.request(req)
    assert tuple(resp.values()) == ('1', '1', '1')
