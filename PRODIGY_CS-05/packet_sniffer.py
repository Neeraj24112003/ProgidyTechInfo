from flask import Flask, render_template, jsonify
from scapy.all import sniff, IP, TCP, UDP
import threading

app = Flask(__name__)
packets = []

# Function to process each captured packet
def packet_callback(packet):
    if IP in packet:
        ip_layer = packet[IP]
        proto = ip_layer.proto
        payload = packet[IP].payload

        if proto == 6:
            protocol = "TCP"
        elif proto == 17:
            protocol = "UDP"
        else:
            protocol = "Other"

        packet_info = {
            "src_ip": ip_layer.src,
            "dst_ip": ip_layer.dst,
            "protocol": protocol,
            "payload": str(payload)
        }
        packets.append(packet_info)

# Function to start packet sniffing
def start_sniffing():
    sniff(prn=packet_callback, store=0)

# Start sniffing in a separate thread
sniff_thread = threading.Thread(target=start_sniffing)
sniff_thread.daemon = True
sniff_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/packets')
def get_packets():
    return jsonify(packets)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
