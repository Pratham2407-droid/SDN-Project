from pox.core import core
import pox.openflow.libopenflow_01 as of
import time
from collections import defaultdict

log = core.getLogger()

# ===== CONFIG =====
THRESHOLD_MBPS = 2.0     # Only high traffic gets blocked
POLL_INTERVAL = 5        # seconds
BLOCK_TIME = 20          # seconds

# ===== DATA =====
packet_count = defaultdict(int)
start_time = time.time()
blocked_hosts = {}   # mac -> time
mac_to_port = {}

# ===== PACKET HANDLER =====
def _handle_PacketIn(event):
    global start_time

    packet = event.parsed
    if not packet.parsed:
        return

    src = str(packet.src)
    dst = str(packet.dst)
    in_port = event.port

    mac_to_port[src] = in_port

    # Count packets
    packet_count[src] += 1

    now = time.time()
    duration = now - start_time

    # ===== UNBLOCK LOGIC =====
    for mac in list(blocked_hosts.keys()):
        if time.time() - blocked_hosts[mac] > BLOCK_TIME:
            del blocked_hosts[mac]
            log.info(f"UNBLOCKED HOST {mac}")

    # ===== BANDWIDTH CHECK =====
    if duration >= POLL_INTERVAL:
        print("\n" + "="*60)
        print(" MAC Address        Bandwidth (Mbps)     Status")
        print("="*60)

        for mac in list(packet_count.keys()):
            packets = packet_count[mac]
            mbps = (packets * 1500 * 8) / (duration * 1e6)

            status = "ALLOWED"

            if mbps > THRESHOLD_MBPS and mac not in blocked_hosts:
                blocked_hosts[mac] = time.time()
                status = "BLOCKED !!!"

                log.warning(f"BLOCKING HOST {mac} ({mbps:.2f} Mbps)")

                # DROP rule
                msg = of.ofp_flow_mod()
                msg.priority = 100
                msg.match.dl_src = packet.src
                msg.actions = []
                msg.idle_timeout = BLOCK_TIME
                msg.hard_timeout = BLOCK_TIME
                event.connection.send(msg)

            elif mac in blocked_hosts:
                status = "BLOCKED"

            print(f"{mac:20} {mbps:10.3f} Mbps     {status}")

        print("="*60)

        packet_count.clear()
        start_time = now

    # ===== DROP IF BLOCKED =====
    if src in blocked_hosts:
        return

    # ===== FORWARD (NO FLOW INSTALL) =====
    if dst in mac_to_port:
        out_port = mac_to_port[dst]
    else:
        out_port = of.OFPP_FLOOD

    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.actions.append(of.ofp_action_output(port=out_port))
    msg.in_port = in_port
    event.connection.send(msg)


def _handle_ConnectionUp(event):
    log.info("Switch connected")


def launch():
    log.info("PRO SDN Firewall Running")

    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
