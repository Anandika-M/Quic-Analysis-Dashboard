import asyncio
import threading
import time
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP
import pandas as pd
from datetime import datetime, timedelta
import queue
import psutil
import numpy as np

class RealTimePacketCapture:
    def __init__(self):
        self.quic_packets = []
        self.tcp_tls_packets = []
        self.https_packets = []
        self.capture_active = False
        self.capture_thread = None
        self.packet_queue = queue.Queue()
        self.start_time = None
        self.interface = None
        
        # QUIC specific parameters
        self.quic_versions = {
            0x00000001: "QUIC v1",
            0x6b3343cf: "Google QUIC", 
            0xff00001d: "QUIC v2 Draft"
        }
        
    def quic_packet_parser(self, packet):
        """Parse QUIC packet headers and frames"""
        try:
            if UDP in packet and packet[UDP].dport in [443, 80, 8080]:
                udp_payload = bytes(packet[UDP].payload)
                
                # Basic QUIC detection (simplified)
                if len(udp_payload) > 4:
                    first_byte = udp_payload[0]
                    
                    # QUIC header type detection
                    header_type = (first_byte & 0x80) >> 7  # Long header if bit 7 is 1
                    
                    quic_info = {
                        'timestamp': datetime.now(),
                        'src_ip': packet[IP].src,
                        'dst_ip': packet[IP].dst,
                        'src_port': packet[UDP].sport,
                        'dst_port': packet[UDP].dport,
                        'protocol': 'QUIC',
                        'length': len(packet),
                        'header_type': 'Long' if header_type else 'Short',
                        'packet_number': None,
                        'version': None,
                        'frames': []
                    }
                    
                    if header_type:  # Long header
                        if len(udp_payload) >= 6:
                            version = int.from_bytes(udp_payload[1:5], byteorder='big')
                            quic_info['version'] = self.quic_versions.get(version, f"Unknown: {hex(version)}")
                    
                    return quic_info
        except Exception as e:
            print(f"QUIC parsing error: {e}")
        return None

    def tls_packet_parser(self, packet):
        """Parse TLS handshake and application data"""
        try:
            if TCP in packet and packet[TCP].dport in [443, 8443]:
                # Check if there's a TCP payload
                if not packet[TCP].payload:
                    return None
                    
                tcp_payload = bytes(packet[TCP].payload)
                
                if len(tcp_payload) > 0:
                    tls_info = {
                        'timestamp': datetime.now(),
                        'src_ip': packet[IP].src,
                        'dst_ip': packet[IP].dst,
                        'src_port': packet[TCP].sport,
                        'dst_port': packet[TCP].dport,
                        'protocol': 'TLS',
                        'length': len(packet),
                        'tls_content_type': None,
                        'tls_version': None,
                        'handshake_type': None
                    }
                    
                    # Basic TLS content type detection
                    if tcp_payload[0] in [20, 21, 22, 23]:  # TLS content types
                        tls_info['tls_content_type'] = {
                            20: 'ChangeCipherSpec',
                            21: 'Alert', 
                            22: 'Handshake',
                            23: 'ApplicationData'
                        }.get(tcp_payload[0])
                    
                    return tls_info
        except Exception as e:
            print(f"TLS parsing error: {e}")
        return None

    def https_packet_parser(self, packet):
        """Parse HTTPS traffic (TLS on port 443)"""
        tls_info = self.tls_packet_parser(packet)
        if tls_info:
            tls_info['protocol'] = 'HTTPS'
            return tls_info
        return None

    def packet_handler(self, packet):
        """Handle incoming packets and classify them"""
        try:
            if not IP in packet:
                return
                
            packet_time = datetime.now()
            
            # QUIC detection (UDP on typical QUIC ports)
            if UDP in packet and packet[UDP].dport in [443, 80, 8080]:
                quic_info = self.quic_packet_parser(packet)
                if quic_info:
                    self.quic_packets.append(quic_info)
                    self.packet_queue.put(('QUIC', quic_info))
            
            # TLS/HTTPS detection (TCP on port 443)
            elif TCP in packet and packet[TCP].dport == 443:
                https_info = self.https_packet_parser(packet)
                if https_info:
                    self.https_packets.append(https_info)
                    self.packet_queue.put(('HTTPS', https_info))
                
                tls_info = self.tls_packet_parser(packet)
                if tls_info:
                    self.tcp_tls_packets.append(tls_info)
                    self.packet_queue.put(('TLS', tls_info))
        except Exception as e:
            print(f"Packet handling error: {e}")

    def start_capture(self, interface=None, timeout=30):
        """Start real-time packet capture"""
        self.interface = interface or self.get_default_interface()
        self.capture_active = True
        self.start_time = datetime.now()
        
        def capture_loop():
            print(f"Starting capture on interface {self.interface}")
            try:
                sniff(
                    iface=self.interface,
                    prn=self.packet_handler,
                    timeout=timeout,
                    store=False
                )
            except Exception as e:
                print(f"Capture error: {e}")
            finally:
                self.capture_active = False
        
        self.capture_thread = threading.Thread(target=capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()

    def stop_capture(self):
        """Stop packet capture"""
        self.capture_active = False
        if self.capture_thread:
            self.capture_thread.join(timeout=5)

    def get_default_interface(self):
        """Get default network interface"""
        try:
            return list(psutil.net_if_addrs().keys())[0]
        except:
            return "eth0"

    def get_realtime_metrics(self):
        """Get real-time metrics for dashboard"""
        current_time = datetime.now()
        time_window = timedelta(seconds=10)  # 10-second window
        
        # Filter recent packets
        recent_quic = [p for p in self.quic_packets 
                      if current_time - p['timestamp'] <= time_window]
        recent_tls = [p for p in self.tcp_tls_packets 
                     if current_time - p['timestamp'] <= time_window]
        recent_https = [p for p in self.https_packets 
                       if current_time - p['timestamp'] <= time_window]
        
        metrics = {
            'quic': {
                'packet_count': len(recent_quic),
                'throughput_bps': sum(p['length'] for p in recent_quic) * 8 / 10,
                'avg_packet_size': np.mean([p['length'] for p in recent_quic]) if recent_quic else 0
            },
            'tls': {
                'packet_count': len(recent_tls),
                'throughput_bps': sum(p['length'] for p in recent_tls) * 8 / 10,
                'avg_packet_size': np.mean([p['length'] for p in recent_tls]) if recent_tls else 0
            },
            'https': {
                'packet_count': len(recent_https),
                'throughput_bps': sum(p['length'] for p in recent_https) * 8 / 10,
                'avg_packet_size': np.mean([p['length'] for p in recent_https]) if recent_https else 0
            }
        }
        
        return metrics

    def get_capture_stats(self):
        """Get comprehensive capture statistics"""
        return {
            'total_quic_packets': len(self.quic_packets),
            'total_tls_packets': len(self.tcp_tls_packets),
            'total_https_packets': len(self.https_packets),
            'capture_duration': (datetime.now() - self.start_time).total_seconds() if self.start_time else 0,
            'capture_active': self.capture_active
        }