SDN Dynamic Firewall using POX
📌 Overview

This project implements a Dynamic Firewall using Software Defined Networking (SDN).
It uses the POX controller with Mininet to monitor network traffic in real time and automatically block hosts that exceed a defined bandwidth threshold.

🎯 Features
Real-time traffic monitoring
Automatic host blocking based on bandwidth
Auto-unblocking after timeout
Centralized SDN control (POX)
Live bandwidth table output
🧰 Tech Stack
POX Controller
Mininet
Open vSwitch (OVS)
Python
🏗️ Topology
1 Switch (s1)
5 Hosts (h1–h5)
Controller at 127.0.0.1:6633
⚙️ Setup & Execution
Clean Environment
pkill -f pox
sudo mn -c
Start Controller
cd ~/pox
./pox.py log.level --INFO openflow.of_01 ext.smart_firewall
Run Topology
sudo python3 topology.py
🧪 Testing
Connectivity Test
pingall
Start Server
h1 iperf -s &
Normal Traffic
h2 iperf -c 10.0.0.1 -t 5
Attack Traffic
h4 iperf -c 10.0.0.1 -t 10 -b 5M
Check Blocking
h1 ping -c 4 10.0.0.4

Expected: 100% packet loss

Check Allowed Host
h1 ping -c 4 10.0.0.2

Expected: 0% packet loss

View Flow Rules
sh ovs-ofctl dump-flows s1
