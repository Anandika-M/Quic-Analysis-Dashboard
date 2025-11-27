import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import statistics
from collections import defaultdict

class AdvancedProtocolAnalyzer:
    def __init__(self):
        self.metrics_history = defaultdict(list)
        
    def calculate_comprehensive_metrics(self, quic_packets, tls_packets, https_packets):
        """Calculate comprehensive performance metrics for all protocols"""
        quic_df = pd.DataFrame(quic_packets)
        tls_df = pd.DataFrame(tls_packets)
        https_df = pd.DataFrame(https_packets)
        
        results = {}
        
        if not quic_df.empty:
            results['QUIC'] = self._analyze_protocol(quic_df, 'QUIC')
        
        if not tls_df.empty:
            results['TLS'] = self._analyze_protocol(tls_df, 'TLS')
            
        if not https_df.empty:
            results['HTTPS'] = self._analyze_protocol(https_df, 'HTTPS')
        
        return results
    
    def _analyze_protocol(self, df, protocol):
        """Analyze specific protocol metrics"""
        if df.empty:
            return {}
            
        df = df.sort_values('timestamp')
        
        # Basic timing metrics
        time_diffs = self._calculate_time_differences(df)
        packet_intervals = self._calculate_packet_intervals(df)
        
        # Throughput calculations
        throughput_1s = self._calculate_throughput(df, window_seconds=1)
        throughput_5s = self._calculate_throughput(df, window_seconds=5)
        
        # Advanced metrics
        metrics = {
            # Basic counts
            'total_packets': len(df),
            'total_bytes': df['length'].sum(),
            
            # Timing metrics
            'avg_latency_ms': np.mean(time_diffs) * 1000 if time_diffs else 0,
            'min_latency_ms': np.min(time_diffs) * 1000 if time_diffs else 0,
            'max_latency_ms': np.max(time_diffs) * 1000 if time_diffs else 0,
            'latency_std_ms': np.std(time_diffs) * 1000 if time_diffs else 0,
            'jitter_ms': self._calculate_jitter(time_diffs),
            
            # Throughput metrics
            'avg_throughput_mbps': np.mean(throughput_5s) / 1e6 if throughput_5s else 0,
            'peak_throughput_mbps': np.max(throughput_1s) / 1e6 if throughput_1s else 0,
            'throughput_stability': self._calculate_throughput_stability(throughput_5s),
            
            # Packet metrics
            'avg_packet_size': df['length'].mean(),
            'packet_size_std': df['length'].std(),
            'packet_loss_estimate': self._estimate_packet_loss(packet_intervals),
            
            # Efficiency metrics
            'protocol_efficiency': self._calculate_protocol_efficiency(df, protocol),
            'connection_setup_time': self._estimate_connection_setup(df, protocol),
            
            # Statistical metrics
            'goodput_ratio': self._calculate_goodput_ratio(df),
            'retransmission_estimate': self._estimate_retransmissions(df),
        }
        
        # Store in history for trend analysis
        self.metrics_history[protocol].append({
            'timestamp': datetime.now(),
            'metrics': metrics
        })
        
        return metrics
    
    def _calculate_time_differences(self, df):
        """Calculate time differences between consecutive packets"""
        if len(df) < 2:
            return []
        
        time_diffs = []
        timestamps = pd.to_datetime(df['timestamp']).sort_values()
        
        for i in range(1, len(timestamps)):
            diff = (timestamps.iloc[i] - timestamps.iloc[i-1]).total_seconds()
            time_diffs.append(diff)
            
        return time_diffs
    
    def _calculate_packet_intervals(self, df):
        """Calculate packet arrival intervals"""
        if len(df) < 2:
            return []
        
        intervals = []
        timestamps = pd.to_datetime(df['timestamp']).sort_values()
        
        for i in range(1, len(timestamps)):
            interval = (timestamps.iloc[i] - timestamps.iloc[i-1]).total_seconds()
            intervals.append(interval)
            
        return intervals
    
    def _calculate_throughput(self, df, window_seconds=5):
        """Calculate throughput over specified time windows"""
        if df.empty:
            return []
            
        df_sorted = df.sort_values('timestamp').copy()
        df_sorted['time_bin'] = df_sorted['timestamp'].dt.floor(f'{window_seconds}S')
        
        throughput = df_sorted.groupby('time_bin')['length'].sum() * 8 / window_seconds
        return throughput.tolist()
    
    def _calculate_jitter(self, time_diffs):
        """Calculate packet delay variation (jitter)"""
        if len(time_diffs) < 2:
            return 0
            
        jitter = 0
        for i in range(1, len(time_diffs)):
            jitter += abs(time_diffs[i] - time_diffs[i-1])
            
        return jitter * 1000 / len(time_diffs)  # Convert to ms
    
    def _estimate_packet_loss(self, intervals):
        """Estimate packet loss using statistical methods"""
        if len(intervals) < 10:
            return 0
            
        avg_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        
        # Consider intervals > 3 std deviations as potential loss
        threshold = avg_interval + 3 * std_interval
        loss_events = sum(1 for interval in intervals if interval > threshold)
        
        return (loss_events / len(intervals)) * 100
    
    def _calculate_protocol_efficiency(self, df, protocol):
        """Calculate protocol efficiency (payload/overhead ratio)"""
        if df.empty:
            return 0
            
        # Simplified efficiency calculation
        avg_packet_size = df['length'].mean()
        
        if protocol == 'QUIC':
            # QUIC has more overhead but better efficiency in some cases
            estimated_overhead = 50  # bytes for QUIC header
        else:
            # TCP/TLS has more overhead due to multiple layers
            estimated_overhead = 80  # bytes for TCP + TLS headers
            
        if avg_packet_size > estimated_overhead:
            efficiency = (avg_packet_size - estimated_overhead) / avg_packet_size
            return efficiency * 100
        return 0
    
    def _estimate_connection_setup(self, df, protocol):
        """Estimate connection setup time"""
        if len(df) < 3:
            return 0
            
        # Simplified: time from first to third packet (handshake simulation)
        timestamps = pd.to_datetime(df['timestamp']).sort_values()
        
        if len(timestamps) >= 3:
            setup_time = (timestamps.iloc[2] - timestamps.iloc[0]).total_seconds() * 1000
            return setup_time
        return 0
    
    def _calculate_goodput_ratio(self, df):
        """Calculate goodput ratio (application layer efficiency)"""
        if df.empty:
            return 0
            
        # Simplified: ratio of larger packets (assuming they carry more data)
        large_packets = len(df[df['length'] > 100])  # Packets > 100 bytes
        return (large_packets / len(df)) * 100 if len(df) > 0 else 0
    
    def _estimate_retransmissions(self, df):
        """Estimate retransmissions based on packet patterns"""
        if len(df) < 10:
            return 0
            
        # Simplified: look for similar sized packets close in time
        df_sorted = df.sort_values('timestamp')
        retrans_count = 0
        
        for i in range(1, len(df_sorted)):
            current = df_sorted.iloc[i]
            previous = df_sorted.iloc[i-1]
            
            time_diff = (current['timestamp'] - previous['timestamp']).total_seconds()
            size_diff = abs(current['length'] - previous['length'])
            
            # Potential retransmission if similar size and close timing
            if size_diff < 10 and time_diff < 0.1:  # 100ms threshold
                retrans_count += 1
                
        return (retrans_count / len(df_sorted)) * 100
    
    def _calculate_throughput_stability(self, throughput_values):
        """Calculate throughput stability (coefficient of variation)"""
        if not throughput_values or len(throughput_values) < 2:
            return 0
            
        cv = np.std(throughput_values) / np.mean(throughput_values) if np.mean(throughput_values) > 0 else 0
        stability = max(0, 100 - (cv * 100))  # Convert to percentage stability
        return stability
    
    def get_metrics_trends(self, protocol, window_minutes=5):
        """Get metrics trends over time"""
        if protocol not in self.metrics_history:
            return {}
            
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_metrics = [
            m for m in self.metrics_history[protocol] 
            if m['timestamp'] > cutoff_time
        ]
        
        trends = {}
        if recent_metrics:
            for metric_name in recent_metrics[0]['metrics'].keys():
                values = [m['metrics'][metric_name] for m in recent_metrics]
                trends[metric_name] = {
                    'current': values[-1] if values else 0,
                    'trend': 'up' if len(values) > 1 and values[-1] > values[0] else 'down',
                    'change_percent': ((values[-1] - values[0]) / values[0] * 100) if values[0] != 0 else 0
                }
                
        return trends