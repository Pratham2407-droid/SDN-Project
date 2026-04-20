from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class StarTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        for i in range(1, 6):
            host = self.addHost(
                f'h{i}',
                ip=f'10.0.0.{i}/24',
                mac=f'00:00:00:00:00:0{i}'
            )
            self.addLink(host, switch, bw=10, delay='5ms')


def run():
    topo = StarTopo()

    net = Mininet(
        topo=topo,
        switch=OVSSwitch,
        controller=RemoteController('c0', ip='127.0.0.1', port=6633),
        link=TCLink
    )

    net.start()
    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel('info')
    run()
