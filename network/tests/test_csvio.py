import os

import pytest


@pytest.mark.io
@pytest.mark.unit
@pytest.mark.parametrize('filename, fields', [
    ('requests.csv', ('request_id', 'redundant')),
    ('vlans.csv', ('device_id', 'primary_port', 'vlan_id'))
])
def test_read_file(filename, fields):
    from network.csvio import CsvIo
    handler = CsvIo(filename).read()
    for f in fields:
        assert f in handler.headers

    # just check if it's iterable
    for i in handler:
        break


@pytest.mark.io
@pytest.mark.unit
@pytest.mark.parametrize('filename, fields', [
    ('requests.csv', ('request_id', 'redundant')),
    ('vlans.csv', ('device_id', 'primary_port', 'vlan_id'))
])
def test_write_file(filename, fields):
    from network.csvio import CsvIo
    handler = CsvIo(filename).read()

    # writes a copy (t)
    handler.write(filename=os.path.join('/tmp/', filename))

    check_out = CsvIo(os.path.join('/tmp/', filename)).read()
    for f in fields:
        assert f in check_out.headers


@pytest.mark.io
@pytest.mark.unit
@pytest.mark.parametrize('filename', [
    'extra_test_requests.csv', 'extra_test_vlans.csv'
])
def test_create_empty_file(filename):
    from network.csvio import CsvIo
    check_out = CsvIo(os.path.join('/tmp/', filename)).create_file().read()

    assert len(list(check_out)) == 0


@pytest.mark.io
@pytest.mark.unit
@pytest.mark.parametrize('filename, fields', [
    ('test_requests.csv', ('request_id', 'redundant')),
    ('test_vlans.csv', ('device_id', 'primary_port', 'vlan_id'))
])
def test_sort_file(filename, fields):
    from network.csvio import CsvIo
    handler = CsvIo(filename).read()

    for column in fields:
        handler.sort(headers=[column])

        data = list(handler)
        for i, line in enumerate(data[1:]):
            assert int(data[i][column]) <= int(line[column])
