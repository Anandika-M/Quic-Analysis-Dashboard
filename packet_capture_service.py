# #!/usr/bin/env python3
# import socket
# import json
# import time
# import sys
# from scapy.all import *
# from datetime import datetime
# import struct

# class RootPacketCapture:
#     def __init__(self, interface="en0"):
#         self.quic_packets = []
#         self.tcp_packets = []
#         self.interface = interface
#         self.packet_count = 0
        
#     def detect_quic(self, payload):
#         """Detect QUIC protocol based on packet characteristics"""
#         if len(payload) < 6:
#             return False
            
#         first_byte = payload[0]
        
#         # QUIC long header: bit 7 is 1
#         if first_byte & 0x80:
#             return True
            
#         # QUIC short header: bit 7 is 0, bit 6 is 1 (key phase)
#         if (first_byte & 0x80) == 0 and (first_byte & 0x40):
#             return True
            
#         # Check for common QUIC versions in long header
#         if len(payload) >= 5:
#             version = struct.unpack('>I', payload[1:5])[0]
#             quic_versions = [0x00000001, 0x6b3343cf, 0xff00001d]
#             if version in quic_versions:
#                 return True
                
#         return False

#     def packet_handler(self, packet):
#         """Handle incoming packets"""
#         self.packet_count += 1
        
#         packet_info = {
#             'timestamp': datetime.now().isoformat(),
#             'protocol': 'UNKNOWN',
#             'length': len(packet),
#             'packet_id': self.packet_count
#         }
        
#         try:
#             if IP in packet:
#                 packet_info['src_ip'] = packet[IP].src
#                 packet_info['dst_ip'] = packet[IP].dst
                
#                 # UDP packets (potential QUIC)
#                 if UDP in packet:
#                     udp = packet[UDP]
#                     packet_info['src_port'] = udp.sport
#                     packet_info['dst_port'] = udp.dport
                    
#                     # Check for QUIC on common ports
#                     if udp.dport in [443, 80, 8080, 8443]:
#                         payload = bytes(udp.payload)
#                         if self.detect_quic(payload):
#                             packet_info['protocol'] = 'QUIC'
#                             self.quic_packets.append(packet_info.copy())
#                         else:
#                             packet_info['protocol'] = 'UDP'
                    
#                 # TCP packets (TLS/HTTPS)
#                 elif TCP in packet:
#                     tcp = packet[TCP]
#                     packet_info['src_port'] = tcp.sport
#                     packet_info['dst_port'] = tcp.dport
                    
#                     # TLS/HTTPS on common ports
#                     if tcp.dport in [443, 8443]:
#                         packet_info['protocol'] = 'TLS'
#                         self.tcp_packets.append(packet_info.copy())
#                     elif tcp.dport in [80, 8080]:
#                         packet_info['protocol'] = 'HTTP'
                        
#         except Exception as e:
#             print(f"Error processing packet: {e}", file=sys.stderr)
    
#     def start_capture(self, duration=30):
#         """Start packet capture"""
#         print(f"Starting capture on {self.interface} for {duration} seconds...", file=sys.stderr)
        
#         try:
#             # Start sniffing with filter for common web ports
#             sniff(
#                 iface=self.interface,
#                 prn=self.packet_handler,
#                 timeout=duration,
#                 store=0,
#                 filter="port 443 or port 80 or port 8080 or port 8443"
#             )
            
#         except Exception as e:
#             print(f"Capture error: {e}", file=sys.stderr)
#             return None
        
#         # Return results as JSON
#         result = {
#             'quic_packets': self.quic_packets[-1000:],  # Limit to last 1000 packets
#             'tcp_packets': self.tcp_packets[-1000:],
#             'total_packets': self.packet_count,
#             'capture_duration': duration,
#             'timestamp': datetime.now().isoformat(),
#             'interface': self.interface
#         }
        
#         return result

# def main():
#     # Parse command line arguments
#     duration = 30
#     interface = "en0"
    
#     if len(sys.argv) > 1:
#         try:
#             duration = int(sys.argv[1])
#         except ValueError:
#             print("Invalid duration, using default 30 seconds", file=sys.stderr)
    
#     if len(sys.argv) > 2:
#         interface = sys.argv[2]
    
#     # Start capture
#     capture = RootPacketCapture(interface)
#     result = capture.start_capture(duration)
    
#     if result:
#         print(json.dumps(result))
#     else:
#         print(json.dumps({"error": "Capture failed"}))

# if __name__ == "__main__":
#     main()

#!/usr/bin/env python3
import socket
import json
import time
import sys
from scapy.all import *
from datetime import datetime
import struct

class RootPacketCapture:
    def __init__(self, interface="en0"):
        self.quic_packets = []
        self.tcp_tls_packets = []
        self.https_packets = []
        self.interface = interface
        self.packet_count = 0
        
    def detect_quic(self, payload):
        """Detect QUIC protocol based on packet characteristics"""
        if len(payload) < 6:
            return False
            
        first_byte = payload[0]
        
        # QUIC long header: bit 7 is 1
        if first_byte & 0x80:
            return True
            
        # QUIC short header: bit 7 is 0, bit 6 is 1 (key phase)
        if (first_byte & 0x80) == 0 and (first_byte & 0x40):
            return True
            
        # Check for common QUIC versions in long header
        if len(payload) >= 5:
            version = struct.unpack('>I', payload[1:5])[0]
            quic_versions = [0x00000001, 0x6b3343cf, 0xff00001d]
            if version in quic_versions:
                return True
                
        return False

    def detect_tls_handshake(self, payload):
        """Detect TLS handshake packets"""
        if len(payload) < 6:
            return False
            
        # TLS handshake content type is 22
        if payload[0] == 22:  # Handshake
            # TLS version check (03 03 for TLS 1.2, 03 04 for TLS 1.3)
            if len(payload) >= 3 and payload[1:3] in [b'\x03\x03', b'\x03\x04']:
                return True
        return False

    def detect_https_traffic(self, payload, src_port, dst_port):
        """Detect HTTPS traffic patterns"""
        # HTTPS typically uses TLS on port 443
        if dst_port == 443 or src_port == 443:
            if len(payload) > 0:
                # Check for TLS handshake or application data
                if payload[0] in [22, 23]:  # Handshake or Application Data
                    return True
        return False

    def packet_handler(self, packet):
        """Handle incoming packets"""
        self.packet_count += 1
        
        packet_info = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'UNKNOWN',
            'length': len(packet),
            'packet_id': self.packet_count
        }
        
        try:
            if IP in packet:
                packet_info['src_ip'] = packet[IP].src
                packet_info['dst_ip'] = packet[IP].dst
                
                # UDP packets (potential QUIC)
                if UDP in packet:
                    udp = packet[UDP]
                    packet_info['src_port'] = udp.sport
                    packet_info['dst_port'] = udp.dport
                    
                    # Check for QUIC on common ports
                    if udp.dport in [443, 80, 8080, 8443]:
                        payload = bytes(udp.payload)
                        if self.detect_quic(payload):
                            packet_info['protocol'] = 'QUIC'
                            self.quic_packets.append(packet_info.copy())
                        else:
                            packet_info['protocol'] = 'UDP'
                    
                # TCP packets (TLS/HTTPS)
                elif TCP in packet:
                    tcp = packet[TCP]
                    packet_info['src_port'] = tcp.sport
                    packet_info['dst_port'] = tcp.dport
                    
                    # Get TCP payload
                    payload = bytes(tcp.payload) if tcp.payload else b''
                    
                    # HTTPS detection (TLS on port 443)
                    if self.detect_https_traffic(payload, tcp.sport, tcp.dport):
                        packet_info['protocol'] = 'HTTPS'
                        self.https_packets.append(packet_info.copy())
                    
                    # TLS detection (any TLS handshake)
                    elif len(payload) > 0 and self.detect_tls_handshake(payload):
                        packet_info['protocol'] = 'TLS'
                        self.tcp_tls_packets.append(packet_info.copy())
                    
                    # Regular TCP on web ports
                    elif tcp.dport in [80, 443, 8080, 8443]:
                        packet_info['protocol'] = 'TCP'
                        self.tcp_tls_packets.append(packet_info.copy())
                        
        except Exception as e:
            print(f"Error processing packet: {e}", file=sys.stderr)
    
    def start_capture(self, duration=30):
        """Start packet capture"""
        print(f"Starting capture on {self.interface} for {duration} seconds...", file=sys.stderr)
        
        try:
            # Start sniffing with filter for common web ports
            sniff(
                iface=self.interface,
                prn=self.packet_handler,
                timeout=duration,
                store=0,
                filter="port 443 or port 80 or port 8080 or port 8443"
            )
            
        except Exception as e:
            print(f"Capture error: {e}", file=sys.stderr)
            return None
        
        # Return results as JSON
        result = {
            'quic_packets': self.quic_packets[-1000:],  # Limit to last 1000 packets
            'tcp_tls_packets': self.tcp_tls_packets[-1000:],
            'https_packets': self.https_packets[-1000:],
            'total_packets': self.packet_count,
            'capture_duration': duration,
            'timestamp': datetime.now().isoformat(),
            'interface': self.interface
        }
        
        return result

def main():
    # Parse command line arguments
    duration = 30
    interface = "en0"
    
    if len(sys.argv) > 1:
        try:
            duration = int(sys.argv[1])
        except ValueError:
            print("Invalid duration, using default 30 seconds", file=sys.stderr)
    
    if len(sys.argv) > 2:
        interface = sys.argv[2]
    
    # Start capture
    capture = RootPacketCapture(interface)
    result = capture.start_capture(duration)
    
    if result:
        print(json.dumps(result))
    else:
        print(json.dumps({"error": "Capture failed"}))

if __name__ == "__main__":
    main()