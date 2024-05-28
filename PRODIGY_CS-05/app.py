import scapy.all as scapy

def sniff_packets(interface, count=100):
    print("Sniffing packets on interface", interface)
    packets = scapy.sniff(iface=interface, count=count)
    analyze_packets(packets)

def analyze_packets(packets):
    for packet in packets:
        print("Packet:", packet.summary())
        if packet.haslayer(scapy.IP):
            print("Source IP:", packet[scapy.IP].src)
            print("Destination IP:", packet[scapy.IP].dst)
            if packet.haslayer(scapy.TCP):
                print("Protocol:", "TCP")
            elif packet.haslayer(scapy.UDP):
                print("Protocol:", "UDP")
            elif packet.haslayer(scapy.ICMP):
                print("Protocol:", "ICMP")
            else:
                print("Protocol:", "Unknown")
        else:
            print("Protocol:", "Non-IP packet")
        print("Payload:", packet.payload)
        print()

def main():
    interface = input("Enter the interface to sniff (e.g. Wi-Fi): ")
    count = int(input("Enter the number of packets to capture (default=100): ") or 100)
    sniff_packets(interface, count)

if __name__ == "__main__":
    main()