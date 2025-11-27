from scapy.all import *
from scapy.layers.http import HTTP, HTTPRequest, HTTPResponse
import pandas as pd
from datetime import datetime

class HTTPSCapture:
    def __init__(self):
        self.https_sessions = []
        self.http_packets = []
        
    def analyze_https_handshake(self, packets):
        """Analyze TLS handshake for HTTPS connections"""
        handshake_packets = []
        
        for packet in packets:
            if TCP in packet and packet[TCP].dport == 443:
                # Look for TLS handshake patterns
                if packet[TCP].payload:
                    payload = bytes(packet[TCP].payload)
                    
                    if len(payload) > 0:
                        # TLS handshake content type is 22
                        if payload[0] == 22:
                            handshake_info = {
                                'timestamp': datetime.now(),
                                'src_ip': packet[IP].src,
                                'dst_ip': packet[IP].dst,
                                'src_port': packet[TCP].sport,
                                'dst_port': packet[TCP].dport,
                                'handshake_type': self._get_handshake_type(payload),
                                'length': len(packet),
                                'protocol': 'HTTPS'
                            }
                            handshake_packets.append(handshake_info)
        
        return handshake_packets
    
    def _get_handshake_type(self, payload):
        """Determine TLS handshake type"""
        if len(payload) > 5:
            handshake_type = payload[5]  # TLS handshake type byte
            types = {
                1: 'ClientHello',
                2: 'ServerHello',
                11: 'Certificate',
                16: 'ClientKeyExchange',
                14: 'ServerHelloDone',
                20: 'Finished'
            }
            return types.get(handshake_type, f'Unknown: {handshake_type}')
        return 'Unknown'