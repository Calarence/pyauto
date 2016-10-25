import socket
import psutil

af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC'
}

duplex_map = {
    psutil.NIC_DUPLEX_FULL: 'full',
    psutil.NIC_DUPLEX_HALF: 'half',
    psutil.NIC_DUPLEX_UNKNOWN: '?',

}


def main():
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    for nic, addrs in psutil.net_if_addrs().items():
        print("%s: " % (nic))
        if nic in stats:
            st = stats[nic]
            print("   stats    :" + "   speed=%sMB,duplex=%s,mtu=%s,up=%s" % (
                st.speed, duplex_map[st.duplex], st.mtu, "yes" if st.isup else "no"))
        if nic in io_counters:
            io = io_counters[nic]
            print("   incoming   :" + "   bytes=%s,pkts=%s,errs=%s,drops=%s" %
                  (io.bytes_recv, io.packets_recv, io.errin, io.dropin))
            print("   outgoing   :" + "   ytes=%s,pkts=%s,errs=%s,drops=%s" %
                  (io.bytes_sent, io.packets_sent, io.errout, io.dropout))
        for addr in addrs:
            print("   %-4s" % af_map.get(addr.family, addr.family) +
                  "   address   : %s" % addr.address)
            if addr.broadcast:
                print("   broadcast : %s" % addr.broadcast)
            if addr.netmask:
                print("   netmask   : %s" % addr.netmask)
            if addr.ptp:
                print("      p2p       : %s" % addr.ptp)
        print("")

if __name__ == '__main__':
    main()
