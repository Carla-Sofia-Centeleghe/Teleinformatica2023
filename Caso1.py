#------------- Prueba 50% 42/84 paqurtes---------------------------
# Carla S. Centeleghe
# Teleinformatica 2023

#Importo librerias
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch


def myNetwork():
    net = Mininet(topo=None, build=False, ipBase='192.168.100.0/24') # ipbase

    #Espesifico los Switches
    info('*** Add switches\n')
    sA1, sA2, sA3, sA4, sA5, sA6 = [
        net.addSwitch(sA, cls=OVSKernelSwitch, failMode='standalone')
        for sA in ('sA1', 'sA2', 'sA3','sA4', 'sA5', 'sA6')
    ]
    sB1, sB2, sB3, sB4, sB5, sB6 = [
        net.addSwitch(sB, cls=OVSKernelSwitch, failMode='standalone')
        for sB in ('sB1', 'sB2', 'sB3','sB4', 'sB5', 'sB6')
    ]

    #Especifico los routers
    info('*** Add router\n')
    router = net.addHost('r0', ip='192.168.100.1/29')  #Routher central
    router1 = net.addHost('r1', ip='192.168.100.1/29') #Routher sucursal 1
    router2 = net.addHost('r2', ip='192.168.100.9/29') #Routher sucursal 2
    router3 = net.addHost('r3', ip='192.168.100.17/29') #Routher sucursal 3
    router4 = net.addHost('r4', ip='192.168.100.25/29') #Routher sucursal 4
    router5 = net.addHost('r5', ip='192.168.100.33/29') #Routher sucursal 5
    router6 = net.addHost('r6', ip='192.168.100.41/29') #Routher sucursal 6
    
    router.cmd('sysctl net.ipv4.ip_forward=1')
    router1.cmd('sysctl net.ipv4.ip_forward=1')
    router2.cmd('sysctl net.ipv4.ip_forward=1')
    router3.cmd('sysctl net.ipv4.ip_forward=1')
    router4.cmd('sysctl net.ipv4.ip_forward=1')
    router5.cmd('sysctl net.ipv4.ip_forward=1')
    router6.cmd('sysctl net.ipv4.ip_forward=1')

    #Espesifico los Host
    info('*** Add hosts\n')
    h1 = net.addHost('h1', ip='10.0.1.254/24') #, defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.2.254/24') #, defaultRoute='via 10.0.2.1')
    h3 = net.addHost('h3', ip='10.0.3.254/24') #, defaultRoute='via 10.0.3.1')
    h4 = net.addHost('h4', ip='10.0.4.254/24') #, defaultRoute='via 10.0.4.1')
    h5 = net.addHost('h5', ip='10.0.5.254/24') #, defaultRoute='via 10.0.5.1')
    h6 = net.addHost('h6', ip='10.0.6.254/24') #, defaultRoute='via 10.0.6.1')

    #Espesifico links switch con router
    info('*** Add router links\n')
    #links con A
    net.addLink(sA1, router, intfName2='r0-eth1', params2={'ip': '192.168.100.1/29'})
    net.addLink(sA2, router, intfName2='r0-eth2', params2={'ip': '192.168.100.9/29'})
    net.addLink(sA3, router, intfName2='r0-eth3', params2={'ip': '192.168.100.17/29'})
    net.addLink(sA4, router, intfName2='r0-eth4', params2={'ip': '192.168.100.25/29'})
    net.addLink(sA5, router, intfName2='r0-eth5', params2={'ip': '192.168.100.33/29'})
    net.addLink(sA6, router, intfName2='r0-eth6', params2={'ip': '192.168.100.41/29'})

    #links con B
    net.addLink(sB1, router, intfName2='r1-eth1', params2={'ip': '10.0.1.1/24'})
    net.addLink(sB2, router, intfName2='r2-eth1', params2={'ip': '10.0.2.1/24'})
    net.addLink(sB3, router, intfName2='r3-eth1', params2={'ip': '10.0.3.1/24'})
    net.addLink(sB4, router, intfName2='r4-eth1', params2={'ip': '10.0.4.1/24'})
    net.addLink(sB5, router, intfName2='r5-eth1', params2={'ip': '10.0.5.1/24'})
    net.addLink(sB6, router, intfName2='r6-eth1', params2={'ip': '10.0.6.1/24'})
    

    #HOST A SWITCH "B"
    info('*** Add hosts links\n')
    for h, sB in [(h1, sB1), (h2, sB2), (h3, sB3), (h4, sB4), (h5, sB5), (h6, sB6)]:
        net.addLink(h, sB)

    #TABLA DE ROUTHEO
    info('*** Starting network\n')
    net.build()

    #host interno
    info(h1.cmd('ip r add 10.0.0.0/21 via 10.0.1.1'))
    info(h2.cmd('ip r add 10.0.0.0/21 via 10.0.2.1'))
    info(h3.cmd('ip r add 10.0.0.0/21 via 10.0.3.1'))
    info(h4.cmd('ip r add 10.0.0.0/21 via 10.0.4.1'))
    info(h5.cmd('ip r add 10.0.0.0/21 via 10.0.5.1'))
    info(h6.cmd('ip r add 10.0.0.0/21 via 10.0.6.1'))

    #host externo
    info(h1.cmd('ip r add 192.168.100.0/24 via 10.0.1.1'))
    info(h2.cmd('ip r add 192.168.100.0/24 via 10.0.2.1'))
    info(h3.cmd('ip r add 192.168.100.0/24 via 10.0.3.1'))
    info(h4.cmd('ip r add 192.168.100.0/24 via 10.0.4.1'))
    info(h5.cmd('ip r add 192.168.100.0/24 via 10.0.5.1'))
    info(h6.cmd('ip r add 192.168.100.0/24 via 10.0.6.1'))

    #routher externo
    info(router1.cmd('ip r add 192.168.100.0/24 via 192.168.100.6'))
    info(router2.cmd('ip r add 192.168.100.0/24 via 192.168.100.14'))
    info(router3.cmd('ip r add 192.168.100.0/24 via 192.168.100.22'))
    info(router4.cmd('ip r add 192.168.100.0/24 via 192.168.100.30'))
    info(router5.cmd('ip r add 192.168.100.0/24 via 192.168.100.38'))
    info(router6.cmd('ip r add 192.168.100.0/24 via 192.168.100.46'))

    #routher interno
    info(router1.cmd('ip r add 10.0.0.0/21 via 192.168.100.6'))
    info(router2.cmd('ip r add 10.0.0.0/21 via 192.168.100.14'))
    info(router3.cmd('ip r add 10.0.0.0/21 via 192.168.100.22'))
    info(router4.cmd('ip r add 10.0.0.0/21 via 192.168.100.30'))
    info(router5.cmd('ip r add 10.0.0.0/21 via 192.168.100.38'))
    info(router6.cmd('ip r add 10.0.0.0/21 via 192.168.100.46'))

    #routher central
    info(router.cmd('ip r add 10.0.0.0/21 via 192.168.100.0/24'))

    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for sA in (sA1, sA2, sA3, sA4, sA5, sA6):
        sA.start([])
    info('*** Post configure switches and hosts\n')
    net.start()

    info('*** Starting switches\n')
    for sB in (sB1, sB2, sB3, sB4, sB5, sB6):
        sB.start([])
    info('*** Post configure switches and hosts\n')
    net.start()

    info(router.cmd('ip r'))
    CLI(net)
    net.stop()

    info(router1.cmd('ip r'))
    CLI(net)
    net.stop()
    info(router2.cmd('ip r'))
    CLI(net)
    net.stop()
    info(router3.cmd('ip r'))
    CLI(net)
    net.stop()
    info(router4.cmd('ip r'))
    CLI(net)
    net.stop()
    info(router5.cmd('ip r'))
    CLI(net)
    net.stop()
    info(router6.cmd('ip r'))
    CLI(net)
    net.stop()



if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()