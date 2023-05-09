#---------------------------------------------------CASO 1---------------------------------------------------------------------------------------
# Carla S. Centeleghe
# Teleinformatica 2023

#Importo librerias
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import OVSKernelSwitch
from mininet.node import  Host, Node


def myNetwork():
    net = Mininet(topo=None, build=False, ipBase='192.168.100.0/24') # ipbase

    #Espesifico los Switches
    info('*** Add switches\n')
    s1, s2, s3 , s4= [
        net.addSwitch(s, cls=OVSKernelSwitch, failMode='standalone')
        for s in ('s1', 's2', 's3', 's4')
    ]

    #Especifico los routers
    info('*** Add router\n')
    r0 = net.addHost('r0', cls=Node, ip='192.168.100.6')  #Routher central
    r1 = net.addHost('r1', cls=Node, ip='192.168.100.1')  #Routher sucursal 1
    r2 = net.addHost('r2', cls=Node, ip='192.168.100.9')  #Routher sucursal 2

    r0.cmd('sysctl net.ipv4.ip_forward=1')
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    r2.cmd('sysctl net.ipv4.ip_forward=1')
 
    #Espesifico los Host
    info('*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.254/24') # defaultRoute = via 192.168.100.9
    h2 = net.addHost('h2', cls=Host, ip='10.0.2.254/24') # defaultRoute = via 192.168.100.17

    #---------------------------------------LINKS---------------------
    info('*** Add router links\n')
    #links con router central a switch central
    net.addLink(r0, s1, intfName1='r0s1-eth0',params1={'ip':'192.168.100.6/29'})
    net.addLink(r0, s2, intfName1='r0s2-eth0',params1={'ip':'192.168.100.14/29'})

    #links con router periferico a switch central
    net.addLink(r1, s1,intfName1='r1s1-eth0',params1={'ip':'192.168.100.1/29'})
    net.addLink(r2, s2,intfName1='r2s2-eth0',params1={'ip':'192.168.100.9/29'})

    #links con router periferico a switch periferico
    net.addLink(r1, s3,intfName1='r1s3-eth0',params1={'ip':'10.0.1.1/24'})
    net.addLink(r2, s4,intfName1='r2s4-eth0',params1={'ip':'10.0.2.1/24'})

    #Host a switch periferico
    info('*** Add hosts links\n')
    net.addLink(h1, s3, intfName1='h1s3-eth0',params1={'ip':'10.0.1.254/24'})
    net.addLink(h2, s4, intfName1='h2s4-eth0',params1={'ip':'10.0.2.254/24'})

    #------------------------------TABLA DE DIRECCIONES
    info('*** Starting network\n')
    net.build()
    #------------------------------------ROUTHER----------------------  
    #-----------------routher central
    info(r0.cmd('ip r add 10.0.1.0/24 via 192.168.100.1 dev r0s1-eth0')) #r0 a h1
    info(r0.cmd('ip r add 10.0.2.0/24 via 192.168.100.9 dev r0s2-eth0')) #r0 a h2

    #-----------------routher 1 
    info(r1.cmd('ip r add 192.168.100.8/29 via 192.168.100.6 dev r1s1-eth0')) #r1 a r2
    info(r1.cmd('ip r add 10.0.2.0/24 via 192.168.100.6 dev r1s1-eth0'))      #r1 a h2

    #-----------------routher 2 
    info(r2.cmd('ip r add 192.168.100.0/29 via 192.168.100.14 dev r2s2-eth0')) #r2 a r1
    info(r2.cmd('ip r add 10.0.1.0/24 via 192.168.100.14 dev r2s2-eth0'))      #r2 a h1

    #-------------------------------------HOSTS-------------------------
    #------------------host 1
    info(h1.cmd('ip r add 192.168.100.0/29 via 10.0.1.1 dev h1s3-eth0')) #h1 a r1

    info(h1.cmd('ip r add 192.168.100.8/29 via 10.0.1.1 dev h1s3-eth0')) #h1 a r2
    info(h1.cmd('ip r add 10.0.2.0/24 via 10.0.1.1 dev h1s3-eth0'))      #h1 a h2

    #-------------------host 2
    info(h2.cmd('ip r add 192.168.100.8/29 via 10.0.2.1 dev h2s4-eth0')) #h2 a r2
    
    info(h2.cmd('ip r add 192.168.100.0/29 via 10.0.2.1 dev h2s4-eth0')) #h2 a r1
    info(h2.cmd('ip r add 10.0.1.0/24 via 10.0.2.1 dev h2s4-eth0'))      #h2 a h1


    info('*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info('*** Starting switches\n')
    for s in (s1, s2, s3, s4):
        s.start([])

    info('*** Post configure switches and hosts\n')
    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    myNetwork()