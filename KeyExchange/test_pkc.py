""" Tester file for Key Exchange with Public-Key Cryptography
"""

__author__ = "Goksel Kabadayi"
__contact__ = "gokselkabadayi@gmail.com"
__copyright__ = "Copyright 2022, WINSLAB"
__credits__ = ["Goksel Kabadayi"]
__date__ = "2022-01-15"
__deprecated__ = False
__email__ = "gokselkabadayi@gmail.com"
__license__ = "GPLv3"
__maintainer__ = "developer"
__status__ = "Production"
__version__ = "0.0.1"

from ahc.Ahc import ConnectorTypes, Topology
from ahc.Channels.Channels import Channel
from ahc.KeyExchange.PublicKeyCryptography import KDC, Alice, Bob

import networkx as nx

from time import sleep


def main():
    # Initialize nodes

    kdc = KDC("KDC", 0)
    alice = Alice("Alice", 1)
    bob = Bob("Bob", 2)

    # Set KDC public key for Alice

    kdc_public_key = kdc.get_public_key()
    alice.set_kdc_public_key(kdc_public_key)

    # Register Bob's session key to KDC
    kdc.register_public_key("Bob", bob.get_public_key())

    # Initialize channels

    # KDC-Alice channel using DOWN connectors

    kdc_alice = Channel("KDC-Alice", 3)
    kdc.connect_me_to_channel(ConnectorTypes.DOWN, kdc_alice)
    alice.connect_me_to_channel(ConnectorTypes.DOWN, kdc_alice)

    # Alice-Bob channel using UP connectors
    # Cannot use DOWN connector because Alice uses it to communicate with KDC

    alice_bob = Channel("Alice-Bob", 4)
    alice.connect_me_to_channel(ConnectorTypes.UP, alice_bob)
    bob.connect_me_to_channel(ConnectorTypes.UP, alice_bob)

    # Construct graph for topology

    G = nx.Graph()
    G.add_node("KDC")
    G.add_node("Alice")
    G.add_node("Bob")

    G.add_edge("KDC", "Alice")
    G.add_edge("Alice", "Bob")

    # Construct topology

    topo = Topology()

    topo.G = G

    topo.nodes["KDC"] = kdc
    topo.nodes["Alice"] = alice
    topo.nodes["Bob"] = bob

    topo.channels["KDC-Alice"] = kdc_alice
    topo.channels["Alice-Bob"] = alice_bob

    # Start topology
    topo.start()

    # Wait for Bob to receive a session key to finalize the protocol
    while bob.session_key is None:
        sleep(0.1)

    # Bob received a session key
    if alice.session_key == bob.session_key:
        # Bob's session key is the same as Alice's
        print("Session keys match!")
        print("[4] Both of them can encrypt their communications using the same key.")
    else:
        # Bob's session key is different from Alice's
        print("Session keys do not match")


if __name__ == '__main__':
    main()
