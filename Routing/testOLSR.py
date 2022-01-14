import time, os, sys
sys.path.insert(0, os.getcwd())

from ahc.Ahc import Topology
from ahc.Channels.Channels import P2PFIFOPerfectChannel

from ahc.Routing.HOLSR.HOLSRComponent import OLSRComponent
from ahc.Routing.HOLSR.utils import random_directed_graph, Tracing, RepeatDeltaTimer

import networkx as nx
import matplotlib.pyplot as plt


def main():
    plt.figure(1)
    plt.clf()
    fig, ax = plt.subplots(3, 2, num=1)
    graph = random_directed_graph(25)

    topology = Topology()
    topology.construct_from_graph(graph, OLSRComponent, P2PFIFOPerfectChannel)
    topology.start()

    RepeatDeltaTimer().set_interval(0.25)
    RepeatDeltaTimer().start()

    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos=pos, ax=ax[0, 0])

    time.sleep(15)
    RepeatDeltaTimer().cancel()

    for i in range(4):
        nx.draw_networkx(Tracing().step_to_graph(i), pos=pos, ax=ax[int(int(i + 1) / 2), int(int(i + 1) % 2)])
    nx.draw_networkx(Tracing().to_graph(), pos=pos, ax=ax[2, 1])

    plt.setp(ax, xlim=ax[0, 0].get_xlim(), ylim=ax[0, 0].get_ylim())
    plt.draw()
    plt.show()

    print("done.")
    time.sleep(10000)


if __name__ == '__main__':
    main()
