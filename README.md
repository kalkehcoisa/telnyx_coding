## Telnyx challenge

This project is made to solve the problem of handling reservation requests of available VLANs on network devices.
These devices have a primary port and may have a secondary one as well and attend to two kinds of requests:
 - **Without redundancy:** use the lowest vlanid available for a primary port.
 - **With redundancy:** use the lowest vlanid for both primary and secondary port on the same device. Also, the device has to be the lowest numbered one (in case of a tie, use the lower device_id).
Once a port is reserved, it can't serve any other request anymore.

#### Solution done

We always have to use the lowest numbered data. So, to speed up and simplify the process, the data read from the `vlans.csv` is ordered by `vlan_id` and `device_id`.
Also, split into primary and secondary for reducing the length to search and simplifying the processing.

In case of a non redundant request, it just gets the first primary vlan available and remove it from the list. It reduces the memory usage with time and keep us safe from reusing this value another time.

In case of redundant request, we look for a secondary vlan until one is available with also the respective primary one. Removes all the secondaries not useful in the search, the chosen one and the primary associated.

When ran without parameters, it generates an **output.csv** (inside data directory) ordered ascending by request_id and primary_port.
When ran with **test_vlans.csv test_requests.csv** parameters, it will output a **test_output.csv** (inside data directory) when provided  as input.


## Usage

First, install it (better in an virtualenv):

    python3 setup.py install

To check the command line options:

	network -h

Testing:

    python3 setup.py test

Finally, to run it:

	network

To run the test files, do:

    network test_vlans.csv test_requests.csv
