import threading
import time
import queue
from datetime import datetime
import streamlit as st
from packet_capture import RealTimePacketCapture
from analysis import AdvancedProtocolAnalyzer

class RealTimeMonitor:
    def __init__(self):
        self.capture = RealTimePacketCapture()
        self.analyzer = AdvancedProtocolAnalyzer()
        self.monitor_active = False
        self.monitor_thread = None
        
    def start_monitoring(self, interface=None, duration=300):
        """Start real-time monitoring"""
        self.monitor_active = True
        self.capture.start_capture(interface, duration)
        
        def monitor_loop():
            while self.monitor_active and self.capture.capture_active:
                try:
                    # Process any queued packets
                    while not self.capture.packet_queue.empty():
                        protocol, packet = self.capture.packet_queue.get_nowait()
                        # Could add real-time processing here
                        
                    time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                    
                except Exception as e:
                    print(f"Monitor error: {e}")
                    break
                    
        self.monitor_thread = threading.Thread(target=monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitor_active = False
        self.capture.stop_capture()
        
    def get_current_data(self):
        """Get current data for visualization"""
        analysis_results = self.analyzer.calculate_comprehensive_metrics(
            self.capture.quic_packets,
            self.capture.tcp_tls_packets,
            self.capture.https_packets
        )
        
        realtime_metrics = self.capture.get_realtime_metrics()
        capture_stats = self.capture.get_capture_stats()
        
        return analysis_results, realtime_metrics, capture_stats