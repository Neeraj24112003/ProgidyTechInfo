import os
import sys
import ctypes
import webbrowser
from scapy.all import sniff
from flask import Flask, render_template_string

# HTML template for displaying packet information
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Packet Sniffer</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <h2>Captured Packets</h2>
    <table>
        <tr>
            <th>Source IP</th>
            <th>Destination IP</th>
            <th>Protocol</th>
            <th>Payload</th>
        </tr>
        {% for packet in packets %}
        <tr>
            <td>{{ packet['src_ip'] }}</td>
            <td>{{ packet['dst_ip'] }}</td>
            <td>{{ packet['protocol'] }}</td>
            <td>{{ packet['payload'] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
'''

app = Flask(__name__)
captured_packets = []

def packet_callback(packet):
    try:
        src_ip = packet[0][1].src
        dst_ip = packet[0][1].dst
        protocol = packet[0][1].proto
        payload = bytes(packet[0][1].payload).hex()
        
        captured_packets.append({
            'src_ip': src_ip,
            'dst_ip': dst_ip,
            'protocol': protocol,
            'payload': payload
        })
    except Exception as e:
        print(f"Error processing packet: {e}")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, packets=captured_packets)

def require_admin():
    """Force the script to run as an administrator on Windows."""
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        os._exit(0)

if __name__ == '__main__':
    require_admin()
    sniff(prn=packet_callback, store=False, count=10)  # Capture 10 packets for demonstration
    webbrowser.open('http://localhost:5000')
    app.run(port=5000, debug=True)
