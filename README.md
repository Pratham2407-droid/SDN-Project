# 🚀 SDN Dynamic Firewall using POX

## 📌 Overview
This project implements a **Dynamic Firewall using Software Defined Networking (SDN)** using the **POX controller** and **Mininet**.

The firewall:
- Monitors real-time traffic
- Detects high bandwidth usage
- Blocks malicious hosts automatically
- Restores access after timeout

---

## 🎯 Objectives
- Demonstrate SDN-based network security
- Implement dynamic traffic monitoring
- Automatically block suspicious hosts
- Maintain normal traffic for safe hosts

---

## 🧰 Technologies Used
- POX Controller
- Mininet
- Open vSwitch (OVS)
- Python

---

## 🏗️ Network Topology
- 1 Switch: `s1`
- 5 Hosts: `h1, h2, h3, h4, h5`
- Controller: `127.0.0.1:6633`

---

## ⚙️ COMPLETE SETUP + EXECUTION + TESTING

### 🔹 STEP 1: Clean Everything
```bash
pkill -f pox
sudo mn -c
```

### 🔹STEP 2: Start POX Controller
```bash
cd ~/pox
./pox.py log.level --INFO openflow.of_01 ext.smart_firewall
```

### 🔹 STEP 3: Run Mininet Topology
```bash
cd ~/pox
sudo python3 topology.py
```

### Final Testing
```bash
pingall
h1 iperf -s &
h2 iperf -c 10.0.0.1 -t 5
h4 iperf -c 10.0.0.1 -t 10 -b 5M
h1 ping -c 4 10.0.0.4
h1 ping -c 4 10.0.0.2
sh ovs-ofctl dump-flows s1
```
