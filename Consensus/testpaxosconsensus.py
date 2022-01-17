
import sys
import time
import os

sys.path.insert(0, os.getcwd())

import networkx as nx

from ahc.Ahc import Topology
from ahc.Ahc import ComponentRegistry
from ahc.Channels.Channels import BasicLossyChannel
from ahc.Consensus.Paxos.paxos_component import PaxosConsensusComponentModel, Resolution
from itertools import combinations
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

logger = logging.getLogger(__name__)

registry = ComponentRegistry()

class Client:

    def send(self, message:Resolution):
        logger.info("For client Resolution message is received from component %s",
                    message.from_uid.componentinstancenumber)
        logger.info("Client received new set value %s", message.value)


def main():
    nodes = ['A', 'B', 'C', 'D', 'E']

    edges = combinations(nodes, 2)
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    topo = Topology()
    topo.construct_from_graph(G, PaxosConsensusComponentModel, BasicLossyChannel)
    client = Client()

    topo.start()
    time.sleep(2)
    a_node: PaxosConsensusComponentModel = topo.nodes.get('A')
    a_node.data_received_client(client, "Hello World!!!")
    #waitforit = input("hit something to exit...")
    cnt = 1
    while True:
        cnt = cnt +1 
        time.sleep(1)
        if cnt > 5:
            break

if __name__ == "__main__":
    main()
