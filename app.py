# # # import streamlit as st
# # # import pandas as pd
# # # import subprocess
# # # import json
# # # import os
# # # import tempfile
# # # from datetime import datetime, timedelta
# # # import plotly.graph_objects as go
# # # import plotly.express as px
# # # from plotly.subplots import make_subplots
# # # import numpy as np
# # # from typing import Dict, Any, Tuple, Optional
# # # import time

# # # class AdvancedPacketAnalyzer:
# # #     def __init__(self):
# # #         self.metrics_history = []
# # #         self.traffic_patterns = []
        
# # #     def calculate_comprehensive_metrics(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame) -> Dict[str, Any]:
# # #         """Calculate comprehensive metrics for both protocols"""
# # #         metrics = {}
        
# # #         # QUIC Metrics
# # #         if not quic_df.empty:
# # #             quic_df = quic_df.copy()
# # #             # Ensure timestamp conversion
# # #             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
# # #             quic_df = quic_df.sort_values('timestamp')
            
# # #             # Basic metrics
# # #             metrics['QUIC'] = {
# # #                 'packet_count': len(quic_df),
# # #                 'total_bytes': quic_df['length'].sum(),
# # #                 'avg_packet_size': quic_df['length'].mean(),
# # #                 'std_packet_size': quic_df['length'].std(),
# # #                 'throughput_mbps': (quic_df['length'].sum() * 8) / 1e6,
# # #                 'packets_per_second': len(quic_df) / max(1, (quic_df['timestamp'].max() - quic_df['timestamp'].min()).total_seconds()),
# # #                 'unique_sources': quic_df['src_ip'].nunique(),
# # #                 'unique_destinations': quic_df['dst_ip'].nunique(),
# # #                 'port_diversity': quic_df['dst_port'].nunique(),
# # #                 'common_ports': quic_df['dst_port'].value_counts().head(5).to_dict()
# # #             }
            
# # #             # Advanced timing metrics
# # #             if len(quic_df) > 1:
# # #                 time_diffs = quic_df['timestamp'].diff().dt.total_seconds().dropna()
# # #                 metrics['QUIC'].update({
# # #                     'avg_interval_ms': time_diffs.mean() * 1000,
# # #                     'jitter_ms': time_diffs.std() * 1000,
# # #                     'min_interval_ms': time_diffs.min() * 1000,
# # #                     'max_interval_ms': time_diffs.max() * 1000,
# # #                     'burstiness': self.calculate_burstiness(time_diffs),
# # #                     'traffic_volume_variation': quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
# # #                 })
            
# # #             # Efficiency metrics
# # #             metrics['QUIC'].update({
# # #                 'efficiency_ratio': metrics['QUIC']['total_bytes'] / max(1, metrics['QUIC']['packet_count']),
# # #                 'goodput_estimate': self.estimate_goodput(quic_df),
# # #                 'overhead_estimate': self.estimate_protocol_overhead(quic_df, 'QUIC'),
# # #                 'compression_efficiency': self.calculate_compression_efficiency(quic_df)
# # #             })
        
# # #         # TCP/TLS Metrics
# # #         if not tcp_df.empty:
# # #             tcp_df = tcp_df.copy()
# # #             # Ensure timestamp conversion
# # #             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
# # #             tcp_df = tcp_df.sort_values('timestamp')
            
# # #             # Basic metrics
# # #             metrics['TCP/TLS'] = {
# # #                 'packet_count': len(tcp_df),
# # #                 'total_bytes': tcp_df['length'].sum(),
# # #                 'avg_packet_size': tcp_df['length'].mean(),
# # #                 'std_packet_size': tcp_df['length'].std(),
# # #                 'throughput_mbps': (tcp_df['length'].sum() * 8) / 1e6,
# # #                 'packets_per_second': len(tcp_df) / max(1, (tcp_df['timestamp'].max() - tcp_df['timestamp'].min()).total_seconds()),
# # #                 'unique_sources': tcp_df['src_ip'].nunique(),
# # #                 'unique_destinations': tcp_df['dst_ip'].nunique(),
# # #                 'port_diversity': tcp_df['dst_port'].nunique(),
# # #                 'common_ports': tcp_df['dst_port'].value_counts().head(5).to_dict()
# # #             }
            
# # #             # Advanced timing metrics
# # #             if len(tcp_df) > 1:
# # #                 time_diffs = tcp_df['timestamp'].diff().dt.total_seconds().dropna()
# # #                 metrics['TCP/TLS'].update({
# # #                     'avg_interval_ms': time_diffs.mean() * 1000,
# # #                     'jitter_ms': time_diffs.std() * 1000,
# # #                     'min_interval_ms': time_diffs.min() * 1000,
# # #                     'max_interval_ms': time_diffs.max() * 1000,
# # #                     'burstiness': self.calculate_burstiness(time_diffs),
# # #                     'traffic_volume_variation': tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
# # #                 })
            
# # #             # Efficiency metrics
# # #             metrics['TCP/TLS'].update({
# # #                 'efficiency_ratio': metrics['TCP/TLS']['total_bytes'] / max(1, metrics['TCP/TLS']['packet_count']),
# # #                 'goodput_estimate': self.estimate_goodput(tcp_df),
# # #                 'overhead_estimate': self.estimate_protocol_overhead(tcp_df, 'TCP/TLS'),
# # #                 'compression_efficiency': self.calculate_compression_efficiency(tcp_df)
# # #             })
        
# # #         # Comparison metrics
# # #         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# # #             quic_tput = metrics['QUIC']['throughput_mbps']
# # #             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
            
# # #             metrics['comparison'] = {
# # #                 'throughput_ratio': quic_tput / tcp_tput if tcp_tput > 0 else float('inf'),
# # #                 'packet_size_ratio': metrics['QUIC']['avg_packet_size'] / metrics['TCP/TLS']['avg_packet_size'] if metrics['TCP/TLS']['avg_packet_size'] > 0 else float('inf'),
# # #                 'efficiency_ratio': metrics['QUIC']['efficiency_ratio'] / metrics['TCP/TLS']['efficiency_ratio'] if metrics['TCP/TLS']['efficiency_ratio'] > 0 else float('inf'),
# # #                 'jitter_ratio': metrics['QUIC']['jitter_ms'] / metrics['TCP/TLS']['jitter_ms'] if metrics['TCP/TLS']['jitter_ms'] > 0 else float('inf'),
# # #                 'performance_score': self.calculate_performance_score(metrics)
# # #             }
        
# # #         # Store for trend analysis
# # #         self.metrics_history.append({
# # #             'timestamp': datetime.now(),
# # #             'metrics': metrics
# # #         })
        
# # #         return metrics

# # #     def calculate_burstiness(self, intervals):
# # #         """Calculate traffic burstiness (Burstiness Parameter)"""
# # #         if len(intervals) < 2:
# # #             return 0
# # #         mean_interval = np.mean(intervals)
# # #         std_interval = np.std(intervals)
# # #         return (std_interval - mean_interval) / (std_interval + mean_interval) if (std_interval + mean_interval) > 0 else 0

# # #     def estimate_goodput(self, df):
# # #         """Estimate goodput (application layer throughput)"""
# # #         # Simplified: assume larger packets have more application data
# # #         large_packets = df[df['length'] > 100]  # Packets > 100 bytes
# # #         if len(df) > 0:
# # #             return (large_packets['length'].sum() * 8) / 1e6  # Mbps
# # #         return 0

# # #     def estimate_protocol_overhead(self, df, protocol):
# # #         """Estimate protocol overhead"""
# # #         avg_size = df['length'].mean()
# # #         if protocol == 'QUIC':
# # #             estimated_header = 50  # bytes for QUIC
# # #         else:
# # #             estimated_header = 80  # bytes for TCP+TLS
        
# # #         if avg_size > estimated_header:
# # #             return (estimated_header / avg_size) * 100
# # #         return 0

# # #     def calculate_compression_efficiency(self, df):
# # #         """Calculate compression efficiency estimate"""
# # #         # Simplified: ratio of large to small packets
# # #         large_packets = len(df[df['length'] > 500])
# # #         small_packets = len(df[df['length'] <= 100])
# # #         total_packets = len(df)
        
# # #         if total_packets > 0:
# # #             return (large_packets / total_packets) * 100
# # #         return 0

# # #     def calculate_performance_score(self, metrics):
# # #         """Calculate overall performance score (0-100)"""
# # #         score = 0
# # #         max_score = 0
        
# # #         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# # #             # Throughput contribution (30%)
# # #             quic_tput = metrics['QUIC']['throughput_mbps']
# # #             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
# # #             if tcp_tput > 0:
# # #                 throughput_score = min(100, (quic_tput / tcp_tput) * 50)
# # #                 score += throughput_score
# # #             max_score += 30
            
# # #             # Efficiency contribution (25%)
# # #             quic_eff = metrics['QUIC']['efficiency_ratio']
# # #             tcp_eff = metrics['TCP/TLS']['efficiency_ratio']
# # #             if tcp_eff > 0:
# # #                 efficiency_score = min(25, (quic_eff / tcp_eff) * 25)
# # #                 score += efficiency_score
# # #             max_score += 25
            
# # #             # Stability contribution (20%)
# # #             quic_jitter = metrics['QUIC']['jitter_ms']
# # #             tcp_jitter = metrics['TCP/TLS']['jitter_ms']
# # #             if tcp_jitter > 0:
# # #                 stability_score = min(20, (tcp_jitter / max(quic_jitter, 0.1)) * 10)
# # #                 score += stability_score
# # #             max_score += 20
            
# # #             # Connection diversity (15%)
# # #             quic_diversity = metrics['QUIC']['port_diversity']
# # #             tcp_diversity = metrics['TCP/TLS']['port_diversity']
# # #             if tcp_diversity > 0:
# # #                 diversity_score = min(15, (quic_diversity / tcp_diversity) * 15)
# # #                 score += diversity_score
# # #             max_score += 15
            
# # #             # Goodput efficiency (10%)
# # #             quic_goodput = metrics['QUIC']['goodput_estimate']
# # #             tcp_goodput = metrics['TCP/TLS']['goodput_estimate']
# # #             if tcp_goodput > 0:
# # #                 goodput_score = min(10, (quic_goodput / tcp_goodput) * 10)
# # #                 score += goodput_score
# # #             max_score += 10
        
# # #         return min(100, (score / max_score * 100)) if max_score > 0 else 0

# # #     def get_traffic_trends(self, window_minutes=5):
# # #         """Get traffic trends over time"""
# # #         if len(self.metrics_history) < 2:
# # #             return {}
        
# # #         cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
# # #         recent_data = [m for m in self.metrics_history if m['timestamp'] > cutoff_time]
        
# # #         trends = {}
# # #         if len(recent_data) >= 2:
# # #             for protocol in ['QUIC', 'TCP/TLS']:
# # #                 if protocol in recent_data[0]['metrics']:
# # #                     first = recent_data[0]['metrics'][protocol]
# # #                     last = recent_data[-1]['metrics'][protocol]
                    
# # #                     trends[protocol] = {
# # #                         'throughput_trend': '📈' if last['throughput_mbps'] > first['throughput_mbps'] else '📉',
# # #                         'throughput_change': ((last['throughput_mbps'] - first['throughput_mbps']) / first['throughput_mbps'] * 100) if first['throughput_mbps'] > 0 else 0,
# # #                         'packet_count_trend': '📈' if last['packet_count'] > first['packet_count'] else '📉',
# # #                         'efficiency_trend': '📈' if last['efficiency_ratio'] > first['efficiency_ratio'] else '📉'
# # #                     }
        
# # #         return trends

# # # class AdvancedVisualizer:
# # #     def __init__(self):
# # #         self.colors = {
# # #             'QUIC': '#1f77b4',
# # #             'TCP/TLS': '#ff7f0e',
# # #             'HTTPS': '#2ca02c'
# # #         }
# # #         self.light_colors = {
# # #             'QUIC': '#8fc1e3',
# # #             'TCP/TLS': '#ffb366',
# # #             'HTTPS': '#98df8a'
# # #         }
    
# # #     def create_comprehensive_dashboard(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame, analyzer: AdvancedPacketAnalyzer):
# # #         """Create comprehensive performance dashboard with advanced visualizations"""
        
# # #         # Performance Score Card
# # #         st.subheader("🏆 Overall Performance Score")
# # #         if 'comparison' in metrics:
# # #             score = metrics['comparison'].get('performance_score', 0)
# # #             col1, col2, col3 = st.columns([2, 1, 1])
            
# # #             with col1:
# # #                 # Create gauge chart for performance score
# # #                 fig = go.Figure(go.Indicator(
# # #                     mode = "gauge+number+delta",
# # #                     value = score,
# # #                     domain = {'x': [0, 1], 'y': [0, 1]},
# # #                     title = {'text': "QUIC Performance Score"},
# # #                     delta = {'reference': 50},
# # #                     gauge = {
# # #                         'axis': {'range': [None, 100]},
# # #                         'bar': {'color': self.colors['QUIC']},
# # #                         'steps': [
# # #                             {'range': [0, 50], 'color': "lightgray"},
# # #                             {'range': [50, 80], 'color': "lightyellow"},
# # #                             {'range': [80, 100], 'color': "lightgreen"}
# # #                         ],
# # #                         'threshold': {
# # #                             'line': {'color': "red", 'width': 4},
# # #                             'thickness': 0.75,
# # #                             'value': 90
# # #                         }
# # #                     }
# # #                 ))
# # #                 fig.update_layout(height=300)
# # #                 st.plotly_chart(fig, use_container_width=True)
            
# # #             with col2:
# # #                 throughput_ratio = metrics['comparison'].get('throughput_ratio', 1)
# # #                 st.metric("Throughput Ratio", f"{throughput_ratio:.2f}x", 
# # #                          "QUIC vs TCP/TLS")
            
# # #             with col3:
# # #                 efficiency_ratio = metrics['comparison'].get('efficiency_ratio', 1)
# # #                 st.metric("Efficiency Ratio", f"{efficiency_ratio:.2f}x",
# # #                          "QUIC vs TCP/TLS")
        
# # #         # Real-time Metrics Header
# # #         st.subheader("📊 Real-time Performance Metrics")
# # #         self._display_advanced_metrics_header(metrics)
        
# # #         # Advanced Comparison Charts
# # #         st.subheader("📈 Advanced Protocol Comparison")
# # #         tab1, tab2, tab3, tab4 = st.tabs(["Throughput Analysis", "Efficiency Metrics", "Traffic Patterns", "Connection Analysis"])
        
# # #         with tab1:
# # #             self._plot_advanced_throughput_analysis(metrics)
        
# # #         with tab2:
# # #             self._plot_efficiency_breakdown(metrics)
        
# # #         with tab3:
# # #             self._plot_traffic_pattern_analysis(quic_df, tcp_df)
        
# # #         with tab4:
# # #             self._plot_connection_analysis(metrics, quic_df, tcp_df)
        
# # #         # Statistical Analysis
# # #         st.subheader("📊 Statistical Analysis")
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             self._plot_packet_size_distribution(quic_df, tcp_df)
        
# # #         with col2:
# # #             self._plot_timing_analysis(metrics)
        
# # #         # Network Quality Indicators
# # #         st.subheader("🌐 Network Quality Indicators")
# # #         self._plot_network_quality_indicators(metrics)
        
# # #         # Traffic Composition
# # #         st.subheader("🔍 Traffic Composition Analysis")
# # #         self._plot_traffic_composition(quic_df, tcp_df)
        
# # #         # Detailed Metrics Table
# # #         st.subheader("📋 Comprehensive Metrics Table")
# # #         self._show_advanced_metrics_table(metrics)
        
# # #         # Trends (if available)
# # #         trends = analyzer.get_traffic_trends()
# # #         if trends:
# # #             st.subheader("📅 Performance Trends")
# # #             self._display_trend_indicators(trends)

# # #     def _display_advanced_metrics_header(self, metrics: Dict[str, Any]):
# # #         """Display advanced metrics header with more indicators"""
# # #         col1, col2, col3, col4, col5 = st.columns(5)
        
# # #         with col1:
# # #             if 'QUIC' in metrics:
# # #                 st.metric(
# # #                     "QUIC Throughput", 
# # #                     f"{metrics['QUIC']['throughput_mbps']:.2f} Mbps",
# # #                     f"{metrics['QUIC']['packet_count']} packets"
# # #                 )
        
# # #         with col2:
# # #             if 'TCP/TLS' in metrics:
# # #                 st.metric(
# # #                     "TCP/TLS Throughput",
# # #                     f"{metrics['TCP/TLS']['throughput_mbps']:.2f} Mbps", 
# # #                     f"{metrics['TCP/TLS']['packet_count']} packets"
# # #                 )
                
# # #         with col3:
# # #             if 'QUIC' in metrics:
# # #                 st.metric(
# # #                     "QUIC Goodput",
# # #                     f"{metrics['QUIC']['goodput_estimate']:.2f} Mbps",
# # #                     f"{metrics['QUIC']['efficiency_ratio']:.1f} bytes/pkt"
# # #                 )
                
# # #         with col4:
# # #             if 'TCP/TLS' in metrics:
# # #                 st.metric(
# # #                     "TCP/TLS Goodput", 
# # #                     f"{metrics['TCP/TLS']['goodput_estimate']:.2f} Mbps",
# # #                     f"{metrics['TCP/TLS']['efficiency_ratio']:.1f} bytes/pkt"
# # #                 )
        
# # #         with col5:
# # #             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# # #                 jitter_ratio = metrics['comparison'].get('jitter_ratio', 1)
# # #                 st.metric(
# # #                     "Jitter Ratio",
# # #                     f"{jitter_ratio:.2f}x",
# # #                     "Lower is better"
# # #                 )

# # #     def _plot_advanced_throughput_analysis(self, metrics: Dict[str, Any]):
# # #         """Plot advanced throughput analysis"""
# # #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# # #             return
            
# # #         fig = make_subplots(
# # #             rows=2, cols=2,
# # #             subplot_titles=('Total Throughput', 'Goodput Comparison', 
# # #                           'Packet Rate', 'Efficiency Ratio'),
# # #             specs=[[{"secondary_y": False}, {"secondary_y": False}],
# # #                    [{"secondary_y": False}, {"secondary_y": False}]]
# # #         )
        
# # #         protocols = ['QUIC', 'TCP/TLS']
        
# # #         # Total Throughput
# # #         throughputs = [metrics[p]['throughput_mbps'] for p in protocols]
# # #         fig.add_trace(
# # #             go.Bar(x=protocols, y=throughputs, name='Throughput',
# # #                   marker_color=[self.colors[p] for p in protocols]),
# # #             row=1, col=1
# # #         )
        
# # #         # Goodput Comparison
# # #         goodputs = [metrics[p]['goodput_estimate'] for p in protocols]
# # #         fig.add_trace(
# # #             go.Bar(x=protocols, y=goodputs, name='Goodput',
# # #                   marker_color=[self.light_colors[p] for p in protocols]),
# # #             row=1, col=2
# # #         )
        
# # #         # Packet Rate
# # #         packet_rates = [metrics[p]['packets_per_second'] for p in protocols]
# # #         fig.add_trace(
# # #             go.Bar(x=protocols, y=packet_rates, name='Packets/s',
# # #                   marker_color=[self.colors[p] for p in protocols]),
# # #             row=2, col=1
# # #         )
        
# # #         # Efficiency
# # #         efficiencies = [metrics[p]['efficiency_ratio'] for p in protocols]
# # #         fig.add_trace(
# # #             go.Bar(x=protocols, y=efficiencies, name='Efficiency',
# # #                   marker_color=[self.light_colors[p] for p in protocols]),
# # #             row=2, col=2
# # #         )
        
# # #         fig.update_layout(height=500, showlegend=False)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_efficiency_breakdown(self, metrics: Dict[str, Any]):
# # #         """Plot detailed efficiency breakdown"""
# # #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# # #             return
            
# # #         fig = go.Figure()
        
# # #         efficiency_metrics = ['efficiency_ratio', 'goodput_estimate', 'overhead_estimate', 'compression_efficiency']
# # #         metric_names = ['Bytes/Packet', 'Goodput (Mbps)', 'Overhead %', 'Compression %']
        
# # #         for i, (metric, name) in enumerate(zip(efficiency_metrics, metric_names)):
# # #             fig.add_trace(go.Bar(
# # #                 name=name,
# # #                 x=['QUIC', 'TCP/TLS'],
# # #                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
# # #                 marker_color=[self.colors['QUIC'] if i % 2 == 0 else self.light_colors['QUIC'],
# # #                             self.colors['TCP/TLS'] if i % 2 == 0 else self.light_colors['TCP/TLS']]
# # #             ))
        
# # #         fig.update_layout(
# # #             title='Efficiency Metrics Breakdown',
# # #             barmode='group',
# # #             height=400
# # #         )
# # #         st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_traffic_pattern_analysis(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# # #         """Analyze and plot traffic patterns"""
# # #         if quic_df.empty and tcp_df.empty:
# # #             st.info("No traffic data for pattern analysis")
# # #             return
            
# # #         fig = make_subplots(
# # #             rows=2, cols=2,
# # #             subplot_titles=('Traffic Volume Over Time', 'Cumulative Bytes',
# # #                           'Packet Size Distribution', 'Size Variation'),
# # #             specs=[[{"secondary_y": False}, {"secondary_y": False}],
# # #                    [{"secondary_y": False}, {"secondary_y": False}]]
# # #         )
        
# # #         # Ensure timestamps are properly converted
# # #         if not quic_df.empty:
# # #             quic_df = quic_df.copy()
# # #             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
# # #             quic_df = quic_df.sort_values('timestamp')
# # #             quic_df['time_elapsed'] = (quic_df['timestamp'] - quic_df['timestamp'].min()).dt.total_seconds()
            
# # #             # Traffic Volume Over Time
# # #             fig.add_trace(
# # #                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['length'],
# # #                           name='QUIC Packet Size', line=dict(color=self.colors['QUIC'])),
# # #                 row=1, col=1
# # #             )
            
# # #             # Cumulative Bytes
# # #             quic_df['cumulative_bytes'] = quic_df['length'].cumsum()
# # #             fig.add_trace(
# # #                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['cumulative_bytes'],
# # #                           name='QUIC Cumulative', line=dict(color=self.colors['QUIC'])),
# # #                 row=1, col=2
# # #             )
        
# # #         if not tcp_df.empty:
# # #             tcp_df = tcp_df.copy()
# # #             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
# # #             tcp_df = tcp_df.sort_values('timestamp')
# # #             tcp_df['time_elapsed'] = (tcp_df['timestamp'] - tcp_df['timestamp'].min()).dt.total_seconds()
            
# # #             # Traffic Volume Over Time
# # #             fig.add_trace(
# # #                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['length'],
# # #                           name='TCP Packet Size', line=dict(color=self.colors['TCP/TLS'])),
# # #                 row=1, col=1
# # #             )
            
# # #             # Cumulative Bytes
# # #             tcp_df['cumulative_bytes'] = tcp_df['length'].cumsum()
# # #             fig.add_trace(
# # #                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['cumulative_bytes'],
# # #                           name='TCP Cumulative', line=dict(color=self.colors['TCP/TLS'])),
# # #                 row=1, col=2
# # #             )
        
# # #         # Packet Size Distribution (Histogram)
# # #         if not quic_df.empty:
# # #             fig.add_trace(
# # #                 go.Histogram(x=quic_df['length'], name='QUIC Sizes',
# # #                             marker_color=self.colors['QUIC'], opacity=0.7),
# # #                 row=2, col=1
# # #             )
        
# # #         if not tcp_df.empty:
# # #             fig.add_trace(
# # #                 go.Histogram(x=tcp_df['length'], name='TCP Sizes',
# # #                             marker_color=self.colors['TCP/TLS'], opacity=0.7),
# # #                 row=2, col=1
# # #             )
        
# # #         # Size Variation (Coefficient of Variation)
# # #         size_variation_values = [0.5, 0.3]  # Default values
# # #         if not quic_df.empty and not tcp_df.empty:
# # #             quic_variation = quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
# # #             tcp_variation = tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
# # #             size_variation_values = [quic_variation, tcp_variation]
        
# # #         fig.add_trace(
# # #             go.Bar(x=['QUIC', 'TCP/TLS'], y=size_variation_values, 
# # #                    name='Size Variation', marker_color=[self.colors['QUIC'], self.colors['TCP/TLS']]),
# # #             row=2, col=2
# # #         )
        
# # #         fig.update_layout(height=600, showlegend=True)
# # #         st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_connection_analysis(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# # #         """Plot connection and network analysis"""
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             # Connection Diversity
# # #             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# # #                 fig = go.Figure()
# # #                 categories = ['Sources', 'Destinations', 'Ports']
# # #                 quic_values = [metrics['QUIC']['unique_sources'], 
# # #                               metrics['QUIC']['unique_destinations'],
# # #                               metrics['QUIC']['port_diversity']]
# # #                 tcp_values = [metrics['TCP/TLS']['unique_sources'],
# # #                              metrics['TCP/TLS']['unique_destinations'],
# # #                              metrics['TCP/TLS']['port_diversity']]
                
# # #                 fig.add_trace(go.Bar(name='QUIC', x=categories, y=quic_values,
# # #                                     marker_color=self.colors['QUIC']))
# # #                 fig.add_trace(go.Bar(name='TCP/TLS', x=categories, y=tcp_values,
# # #                                     marker_color=self.colors['TCP/TLS']))
                
# # #                 fig.update_layout(title='Connection Diversity', barmode='group')
# # #                 st.plotly_chart(fig, use_container_width=True)
        
# # #         with col2:
# # #             # Port Distribution
# # #             if not quic_df.empty or not tcp_df.empty:
# # #                 fig = go.Figure()
                
# # #                 if not quic_df.empty:
# # #                     port_counts = quic_df['dst_port'].value_counts().head(10)
# # #                     fig.add_trace(go.Bar(
# # #                         x=port_counts.index.astype(str), y=port_counts.values,
# # #                         name='QUIC Ports', marker_color=self.colors['QUIC']
# # #                     ))
                
# # #                 if not tcp_df.empty:
# # #                     port_counts = tcp_df['dst_port'].value_counts().head(10)
# # #                     fig.add_trace(go.Bar(
# # #                         x=port_counts.index.astype(str), y=port_counts.values,
# # #                         name='TCP Ports', marker_color=self.colors['TCP/TLS']
# # #                     ))
                
# # #                 fig.update_layout(title='Top Destination Ports')
# # #                 st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_packet_size_distribution(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# # #         """Plot detailed packet size distribution"""
# # #         fig = go.Figure()
        
# # #         if not quic_df.empty:
# # #             fig.add_trace(go.Box(
# # #                 y=quic_df['length'], name='QUIC Packet Sizes',
# # #                 marker_color=self.colors['QUIC']
# # #             ))
        
# # #         if not tcp_df.empty:
# # #             fig.add_trace(go.Box(
# # #                 y=tcp_df['length'], name='TCP Packet Sizes', 
# # #                 marker_color=self.colors['TCP/TLS']
# # #             ))
        
# # #         fig.update_layout(
# # #             title='Packet Size Distribution (Box Plot)',
# # #             yaxis_title='Packet Size (bytes)',
# # #             height=400
# # #         )
# # #         st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_timing_analysis(self, metrics: Dict[str, Any]):
# # #         """Plot timing and jitter analysis"""
# # #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# # #             return
            
# # #         fig = go.Figure()
        
# # #         timing_metrics = ['avg_interval_ms', 'jitter_ms', 'min_interval_ms', 'max_interval_ms']
# # #         metric_names = ['Avg Interval', 'Jitter', 'Min Interval', 'Max Interval']
        
# # #         for metric, name in zip(timing_metrics, metric_names):
# # #             fig.add_trace(go.Bar(
# # #                 name=name,
# # #                 x=['QUIC', 'TCP/TLS'],
# # #                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
# # #                 text=[f"{metrics['QUIC'].get(metric, 0):.1f}", f"{metrics['TCP/TLS'].get(metric, 0):.1f}"],
# # #                 textposition='auto'
# # #             ))
        
# # #         fig.update_layout(
# # #             title='Timing Analysis (ms)',
# # #             barmode='group',
# # #             height=400
# # #         )
# # #         st.plotly_chart(fig, use_container_width=True)

# # #     def _plot_network_quality_indicators(self, metrics: Dict[str, Any]):
# # #         """Plot network quality indicators"""
# # #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# # #             return
            
# # #         col1, col2, col3, col4 = st.columns(4)
        
# # #         with col1:
# # #             # Jitter indicator
# # #             quic_jitter = metrics['QUIC'].get('jitter_ms', 0)
# # #             st.metric("QUIC Jitter", f"{quic_jitter:.1f}ms", 
# # #                      "Lower is better" if quic_jitter < metrics['TCP/TLS'].get('jitter_ms', 100) else "Higher than TCP")
        
# # #         with col2:
# # #             # Burstiness indicator
# # #             quic_burst = metrics['QUIC'].get('burstiness', 0)
# # #             st.metric("QUIC Burstiness", f"{quic_burst:.3f}",
# # #                      "Closer to 0 is better")
        
# # #         with col3:
# # #             # Overhead indicator
# # #             quic_overhead = metrics['QUIC'].get('overhead_estimate', 0)
# # #             st.metric("QUIC Overhead", f"{quic_overhead:.1f}%",
# # #                      "Lower is better")
        
# # #         with col4:
# # #             # Stability indicator
# # #             quic_stability = 100 - min(100, metrics['QUIC'].get('traffic_volume_variation', 1) * 100)
# # #             st.metric("QUIC Stability", f"{quic_stability:.1f}%",
# # #                      "Higher is better")

# # #     def _plot_traffic_composition(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# # #         """Plot traffic composition analysis"""
# # #         col1, col2 = st.columns(2)
        
# # #         with col1:
# # #             # Protocol distribution pie chart
# # #             if not quic_df.empty or not tcp_df.empty:
# # #                 labels = ['QUIC', 'TCP/TLS']
# # #                 values = [len(quic_df), len(tcp_df)]
                
# # #                 fig = px.pie(values=values, names=labels, 
# # #                             title='Protocol Distribution by Packet Count',
# # #                             color=labels, color_discrete_map=self.colors)
# # #                 st.plotly_chart(fig, use_container_width=True)
        
# # #         with col2:
# # #             # Data volume distribution
# # #             if not quic_df.empty or not tcp_df.empty:
# # #                 labels = ['QUIC', 'TCP/TLS']
# # #                 values = [quic_df['length'].sum() if not quic_df.empty else 0,
# # #                          tcp_df['length'].sum() if not tcp_df.empty else 0]
                
# # #                 fig = px.pie(values=values, names=labels,
# # #                             title='Data Volume Distribution by Protocol',
# # #                             color=labels, color_discrete_map=self.colors)
# # #                 st.plotly_chart(fig, use_container_width=True)

# # #     def _show_advanced_metrics_table(self, metrics: Dict[str, Any]):
# # #         """Display comprehensive metrics table"""
# # #         if not metrics:
# # #             return
            
# # #         # Create detailed comparison table
# # #         comparison_data = []
# # #         metrics_to_show = {
# # #             'Throughput (Mbps)': 'throughput_mbps',
# # #             'Goodput (Mbps)': 'goodput_estimate', 
# # #             'Packet Count': 'packet_count',
# # #             'Avg Packet Size': 'avg_packet_size',
# # #             'Packets/s': 'packets_per_second',
# # #             'Unique Sources': 'unique_sources',
# # #             'Unique Destinations': 'unique_destinations',
# # #             'Port Diversity': 'port_diversity',
# # #             'Avg Interval (ms)': 'avg_interval_ms',
# # #             'Jitter (ms)': 'jitter_ms',
# # #             'Efficiency': 'efficiency_ratio',
# # #             'Overhead %': 'overhead_estimate',
# # #             'Burstiness': 'burstiness'
# # #         }
        
# # #         for display_name, metric_key in metrics_to_show.items():
# # #             row = {'Metric': display_name}
# # #             for protocol in ['QUIC', 'TCP/TLS']:
# # #                 if protocol in metrics:
# # #                     row[protocol] = metrics[protocol].get(metric_key, 0)
# # #             comparison_data.append(row)
        
# # #         if comparison_data:
# # #             df = pd.DataFrame(comparison_data)
# # #             st.dataframe(df.style.format({
# # #                 'QUIC': '{:.2f}',
# # #                 'TCP/TLS': '{:.2f}'
# # #             }), use_container_width=True, height=400)

# # #     def _display_trend_indicators(self, trends: Dict[str, Any]):
# # #         """Display trend indicators"""
# # #         col1, col2, col3, col4 = st.columns(4)
        
# # #         for protocol in ['QUIC', 'TCP/TLS']:
# # #             if protocol in trends:
# # #                 trend = trends[protocol]
# # #                 if protocol == 'QUIC':
# # #                     with col1:
# # #                         st.metric(f"{protocol} Throughput Trend", 
# # #                                  trend['throughput_trend'],
# # #                                  f"{trend['throughput_change']:+.1f}%")
# # #                     with col2:
# # #                         st.metric(f"{protocol} Packet Trend",
# # #                                  trend['packet_count_trend'],
# # #                                  "Volume change")
# # #                 else:
# # #                     with col3:
# # #                         st.metric(f"{protocol} Throughput Trend",
# # #                                  trend['throughput_trend'],
# # #                                  f"{trend['throughput_change']:+.1f}%")
# # #                     with col4:
# # #                         st.metric(f"{protocol} Efficiency Trend",
# # #                                  trend['efficiency_trend'],
# # #                                  "Efficiency change")

# # # def run_packet_capture(duration: int = 30, interface: str = "en0") -> Optional[Dict]:
# # #     """Execute packet capture service with sudo privileges"""
# # #     try:
# # #         # Get current directory
# # #         current_dir = os.path.dirname(os.path.abspath(__file__))
# # #         capture_script = os.path.join(current_dir, "packet_capture_service.py")
        
# # #         # Ensure the script is executable
# # #         if not os.access(capture_script, os.X_OK):
# # #             os.chmod(capture_script, 0o755)
        
# # #         # Run capture with sudo
# # #         result = subprocess.run(
# # #             ['sudo', 'python3', capture_script, str(duration), interface],
# # #             capture_output=True,
# # #             text=True,
# # #             timeout=duration + 10
# # #         )
        
# # #         if result.returncode == 0:
# # #             return json.loads(result.stdout)
# # #         else:
# # #             st.error(f"Capture service error: {result.stderr}")
# # #             return None
            
# # #     except subprocess.TimeoutExpired:
# # #         st.error("Packet capture timed out. Try a shorter duration.")
# # #         return None
# # #     except json.JSONDecodeError as e:
# # #         st.error(f"Failed to parse capture results: {e}")
# # #         return None
# # #     except Exception as e:
# # #         st.error(f"Error running capture: {e}")
# # #         return None

# # # def main():
# # #     # Page configuration
# # #     st.set_page_config(
# # #         page_title="QUIC Protocol Analyzer Pro",
# # #         page_icon="🔄",
# # #         layout="wide",
# # #         initial_sidebar_state="expanded"
# # #     )
    
# # #     st.title("🔄 Advanced QUIC vs TCP/TLS Protocol Analyzer Pro")
    
# # #     # Initialize session state
# # #     if 'capture_data' not in st.session_state:
# # #         st.session_state.capture_data = None
# # #     if 'analysis_results' not in st.session_state:
# # #         st.session_state.analysis_results = None
# # #     if 'analyzer' not in st.session_state:
# # #         st.session_state.analyzer = AdvancedPacketAnalyzer()
    
# # #     # Sidebar controls
# # #     st.sidebar.title("🎛️ Capture Controls")
    
# # #     # Interface selection
# # #     interfaces = ["en0", "eth0", "wlan0", "any"]
# # #     selected_interface = st.sidebar.selectbox(
# # #         "Network Interface",
# # #         interfaces,
# # #         help="Select the network interface to monitor"
# # #     )
    
# # #     # Capture duration
# # #     capture_duration = st.sidebar.slider(
# # #         "Capture Duration (seconds)",
# # #         min_value=10,
# # #         max_value=120,
# # #         value=30,
# # #         step=5,
# # #         help="How long to capture packets"
# # #     )
    
# # #     # Analysis mode
# # #     analysis_mode = st.sidebar.selectbox(
# # #         "Analysis Mode",
# # #         ["Basic", "Advanced", "Comprehensive"],
# # #         help="Level of detail in analysis"
# # #     )
    
# # #     # Control buttons
# # #     col1, col2 = st.sidebar.columns(2)
    
# # #     with col1:
# # #         if st.button("🚀 Start Capture", type="primary"):
# # #             with st.spinner(f"Capturing packets for {capture_duration} seconds..."):
# # #                 capture_data = run_packet_capture(capture_duration, selected_interface)
                
# # #                 if capture_data and 'error' not in capture_data:
# # #                     st.session_state.capture_data = capture_data
                    
# # #                     # Analyze packets
# # #                     analyzer = st.session_state.analyzer
# # #                     quic_df = pd.DataFrame(capture_data.get('quic_packets', []))
# # #                     tcp_df = pd.DataFrame(capture_data.get('tcp_packets', []))
                    
# # #                     analysis_results = analyzer.calculate_comprehensive_metrics(quic_df, tcp_df)
# # #                     st.session_state.analysis_results = (analysis_results, quic_df, tcp_df)
                    
# # #                     st.success(f"Capture completed! Got {len(quic_df)} QUIC and {len(tcp_df)} TCP packets")
# # #                 else:
# # #                     st.error("Capture failed. Check permissions and interface.")
    
# # #     with col2:
# # #         if st.button("🔄 Clear Results"):
# # #             st.session_state.capture_data = None
# # #             st.session_state.analysis_results = None
# # #             st.rerun()
    
# # #     # Display results if available
# # #     if st.session_state.analysis_results:
# # #         analysis_results, quic_df, tcp_df = st.session_state.analysis_results
# # #         visualizer = AdvancedVisualizer()
# # #         visualizer.create_comprehensive_dashboard(analysis_results, quic_df, tcp_df, st.session_state.analyzer)
        
# # #         # Raw data view
# # #         with st.expander("📋 View Raw Packet Data"):
# # #             tab1, tab2 = st.tabs(["QUIC Packets", "TCP/TLS Packets"])
            
# # #             with tab1:
# # #                 if not quic_df.empty:
# # #                     st.dataframe(quic_df, use_container_width=True)
# # #                 else:
# # #                     st.info("No QUIC packets captured")
            
# # #             with tab2:
# # #                 if not tcp_df.empty:
# # #                     st.dataframe(tcp_df, use_container_width=True)
# # #                 else:
# # #                     st.info("No TCP/TLS packets captured")
    
# # #     else:
# # #         # Enhanced welcome screen
# # #         st.markdown("""
# # #         ## 🚀 Welcome to QUIC Protocol Analyzer Pro
        
# # #         This advanced tool provides comprehensive real-time analysis and comparison of:
# # #         - **QUIC** (Quick UDP Internet Connections) 
# # #         - **TCP/TLS** (Traditional encrypted transport)
        
# # #         ### 📊 New Advanced Features:
        
# # #         **🎯 Performance Scoring**
# # #         - Overall performance score (0-100)
# # #         - Multi-factor performance evaluation
# # #         - Real-time performance trends
        
# # #         **📈 Advanced Analytics**
# # #         - Goodput vs Throughput analysis
# # #         - Protocol overhead estimation
# # #         - Traffic burstiness measurement
# # #         - Network stability indicators
        
# # #         **🔍 Deep Packet Analysis**
# # #         - Packet size distribution
# # #         - Timing and jitter analysis
# # #         - Connection diversity metrics
# # #         - Traffic pattern recognition
        
# # #         **🌐 Network Quality Metrics**
# # #         - Jitter and latency analysis
# # #         - Protocol efficiency scores
# # #         - Compression efficiency estimates
# # #         - Traffic composition breakdown
        
# # #         ### 🚀 Quick Start:
# # #         1. Select your network interface above
# # #         2. Set capture duration (10-120 seconds)
# # #         3. Choose analysis mode (Basic/Advanced/Comprehensive)
# # #         4. Click **Start Capture** to begin
# # #         5. Generate web traffic during capture for best results
        
# # #         ### 🔧 Requirements:
# # #         - Linux/macOS with Python 3.8+
# # #         - Sudo/root privileges for packet capture
# # #         - Active network traffic on selected interface
# # #         """)
        
# # #         # Demo data option
# # #         if st.button("🎮 Load Advanced Demo Data", type="secondary"):
# # #             # Create comprehensive demo data
# # #             demo_analysis = {
# # #                 'QUIC': {
# # #                     'packet_count': 150,
# # #                     'total_bytes': 187500,
# # #                     'avg_packet_size': 1250,
# # #                     'std_packet_size': 150,
# # #                     'throughput_mbps': 1.5,
# # #                     'packets_per_second': 5.0,
# # #                     'unique_sources': 3,
# # #                     'unique_destinations': 5,
# # #                     'port_diversity': 8,
# # #                     'avg_interval_ms': 12.5,
# # #                     'jitter_ms': 2.1,
# # #                     'min_interval_ms': 8.2,
# # #                     'max_interval_ms': 25.7,
# # #                     'burstiness': 0.15,
# # #                     'traffic_volume_variation': 0.12,
# # #                     'efficiency_ratio': 1250.0,
# # #                     'goodput_estimate': 1.2,
# # #                     'overhead_estimate': 4.0,
# # #                     'compression_efficiency': 65.0,
# # #                     'common_ports': {443: 120, 80: 30}
# # #                 },
# # #                 'TCP/TLS': {
# # #                     'packet_count': 200, 
# # #                     'total_bytes': 240000,
# # #                     'avg_packet_size': 1200,
# # #                     'std_packet_size': 180,
# # #                     'throughput_mbps': 1.92,
# # #                     'packets_per_second': 6.67,
# # #                     'unique_sources': 4,
# # #                     'unique_destinations': 6,
# # #                     'port_diversity': 10,
# # #                     'avg_interval_ms': 15.2,
# # #                     'jitter_ms': 3.4,
# # #                     'min_interval_ms': 10.1,
# # #                     'max_interval_ms': 32.8,
# # #                     'burstiness': 0.22,
# # #                     'traffic_volume_variation': 0.15,
# # #                     'efficiency_ratio': 1200.0,
# # #                     'goodput_estimate': 1.5,
# # #                     'overhead_estimate': 6.7,
# # #                     'compression_efficiency': 58.0,
# # #                     'common_ports': {443: 180, 80: 20}
# # #                 },
# # #                 'comparison': {
# # #                     'throughput_ratio': 0.78,
# # #                     'packet_size_ratio': 1.04,
# # #                     'efficiency_ratio': 1.04,
# # #                     'jitter_ratio': 0.62,
# # #                     'performance_score': 72.5
# # #                 }
# # #             }
            
# # #             st.session_state.analysis_results = (demo_analysis, pd.DataFrame(), pd.DataFrame())
# # #             st.rerun()

# # #     # Enhanced footer
# # #     st.sidebar.markdown("---")
# # #     st.sidebar.info(
# # #         "💡 **Pro Tip**: For comprehensive analysis, browse multiple HTTPS sites "
# # #         "and use different applications during capture to generate diverse traffic patterns."
# # #     )

# # # if __name__ == "__main__":
# # #     main()

# # import streamlit as st
# # import pandas as pd
# # import subprocess
# # import json
# # import os
# # import tempfile
# # from datetime import datetime, timedelta
# # import plotly.graph_objects as go
# # import plotly.express as px
# # from plotly.subplots import make_subplots
# # import numpy as np
# # from typing import Dict, Any, Tuple, Optional
# # import time
# # import scapy.all as scapy

# # class AdvancedPacketAnalyzer:
# #     def __init__(self):
# #         self.metrics_history = []
# #         self.traffic_patterns = []
        
# #     def calculate_comprehensive_metrics(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame) -> Dict[str, Any]:
# #         """Calculate comprehensive metrics for both protocols"""
# #         metrics = {}
        
# #         # QUIC Metrics
# #         if not quic_df.empty:
# #             quic_df = quic_df.copy()
# #             # Ensure timestamp conversion
# #             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
# #             quic_df = quic_df.sort_values('timestamp')
            
# #             # Basic metrics
# #             metrics['QUIC'] = {
# #                 'packet_count': len(quic_df),
# #                 'total_bytes': quic_df['length'].sum(),
# #                 'avg_packet_size': quic_df['length'].mean(),
# #                 'std_packet_size': quic_df['length'].std(),
# #                 'throughput_mbps': (quic_df['length'].sum() * 8) / 1e6,
# #                 'packets_per_second': len(quic_df) / max(1, (quic_df['timestamp'].max() - quic_df['timestamp'].min()).total_seconds()),
# #                 'unique_sources': quic_df['src_ip'].nunique(),
# #                 'unique_destinations': quic_df['dst_ip'].nunique(),
# #                 'port_diversity': quic_df['dst_port'].nunique(),
# #                 'common_ports': quic_df['dst_port'].value_counts().head(5).to_dict()
# #             }
            
# #             # Advanced timing metrics
# #             if len(quic_df) > 1:
# #                 time_diffs = quic_df['timestamp'].diff().dt.total_seconds().dropna()
# #                 metrics['QUIC'].update({
# #                     'avg_interval_ms': time_diffs.mean() * 1000,
# #                     'jitter_ms': time_diffs.std() * 1000,
# #                     'min_interval_ms': time_diffs.min() * 1000,
# #                     'max_interval_ms': time_diffs.max() * 1000,
# #                     'burstiness': self.calculate_burstiness(time_diffs),
# #                     'traffic_volume_variation': quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
# #                 })
            
# #             # Efficiency metrics
# #             metrics['QUIC'].update({
# #                 'efficiency_ratio': metrics['QUIC']['total_bytes'] / max(1, metrics['QUIC']['packet_count']),
# #                 'goodput_estimate': self.estimate_goodput(quic_df),
# #                 'overhead_estimate': self.estimate_protocol_overhead(quic_df, 'QUIC'),
# #                 'compression_efficiency': self.calculate_compression_efficiency(quic_df)
# #             })
        
# #         # TCP/TLS Metrics
# #         if not tcp_df.empty:
# #             tcp_df = tcp_df.copy()
# #             # Ensure timestamp conversion
# #             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
# #             tcp_df = tcp_df.sort_values('timestamp')
            
# #             # Basic metrics
# #             metrics['TCP/TLS'] = {
# #                 'packet_count': len(tcp_df),
# #                 'total_bytes': tcp_df['length'].sum(),
# #                 'avg_packet_size': tcp_df['length'].mean(),
# #                 'std_packet_size': tcp_df['length'].std(),
# #                 'throughput_mbps': (tcp_df['length'].sum() * 8) / 1e6,
# #                 'packets_per_second': len(tcp_df) / max(1, (tcp_df['timestamp'].max() - tcp_df['timestamp'].min()).total_seconds()),
# #                 'unique_sources': tcp_df['src_ip'].nunique(),
# #                 'unique_destinations': tcp_df['dst_ip'].nunique(),
# #                 'port_diversity': tcp_df['dst_port'].nunique(),
# #                 'common_ports': tcp_df['dst_port'].value_counts().head(5).to_dict()
# #             }
            
# #             # Advanced timing metrics
# #             if len(tcp_df) > 1:
# #                 time_diffs = tcp_df['timestamp'].diff().dt.total_seconds().dropna()
# #                 metrics['TCP/TLS'].update({
# #                     'avg_interval_ms': time_diffs.mean() * 1000,
# #                     'jitter_ms': time_diffs.std() * 1000,
# #                     'min_interval_ms': time_diffs.min() * 1000,
# #                     'max_interval_ms': time_diffs.max() * 1000,
# #                     'burstiness': self.calculate_burstiness(time_diffs),
# #                     'traffic_volume_variation': tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
# #                 })
            
# #             # Efficiency metrics
# #             metrics['TCP/TLS'].update({
# #                 'efficiency_ratio': metrics['TCP/TLS']['total_bytes'] / max(1, metrics['TCP/TLS']['packet_count']),
# #                 'goodput_estimate': self.estimate_goodput(tcp_df),
# #                 'overhead_estimate': self.estimate_protocol_overhead(tcp_df, 'TCP/TLS'),
# #                 'compression_efficiency': self.calculate_compression_efficiency(tcp_df)
# #             })
        
# #         # Comparison metrics
# #         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# #             quic_tput = metrics['QUIC']['throughput_mbps']
# #             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
            
# #             metrics['comparison'] = {
# #                 'throughput_ratio': quic_tput / tcp_tput if tcp_tput > 0 else float('inf'),
# #                 'packet_size_ratio': metrics['QUIC']['avg_packet_size'] / metrics['TCP/TLS']['avg_packet_size'] if metrics['TCP/TLS']['avg_packet_size'] > 0 else float('inf'),
# #                 'efficiency_ratio': metrics['QUIC']['efficiency_ratio'] / metrics['TCP/TLS']['efficiency_ratio'] if metrics['TCP/TLS']['efficiency_ratio'] > 0 else float('inf'),
# #                 'jitter_ratio': metrics['QUIC']['jitter_ms'] / metrics['TCP/TLS']['jitter_ms'] if metrics['TCP/TLS']['jitter_ms'] > 0 else float('inf'),
# #                 'performance_score': self.calculate_performance_score(metrics)
# #             }
        
# #         # Store for trend analysis
# #         self.metrics_history.append({
# #             'timestamp': datetime.now(),
# #             'metrics': metrics
# #         })
        
# #         return metrics

# #     def calculate_burstiness(self, intervals):
# #         """Calculate traffic burstiness (Burstiness Parameter)"""
# #         if len(intervals) < 2:
# #             return 0
# #         mean_interval = np.mean(intervals)
# #         std_interval = np.std(intervals)
# #         return (std_interval - mean_interval) / (std_interval + mean_interval) if (std_interval + mean_interval) > 0 else 0

# #     def estimate_goodput(self, df):
# #         """Estimate goodput (application layer throughput)"""
# #         # Simplified: assume larger packets have more application data
# #         large_packets = df[df['length'] > 100]  # Packets > 100 bytes
# #         if len(df) > 0:
# #             return (large_packets['length'].sum() * 8) / 1e6  # Mbps
# #         return 0

# #     def estimate_protocol_overhead(self, df, protocol):
# #         """Estimate protocol overhead"""
# #         avg_size = df['length'].mean()
# #         if protocol == 'QUIC':
# #             estimated_header = 50  # bytes for QUIC
# #         else:
# #             estimated_header = 80  # bytes for TCP+TLS
        
# #         if avg_size > estimated_header:
# #             return (estimated_header / avg_size) * 100
# #         return 0

# #     def calculate_compression_efficiency(self, df):
# #         """Calculate compression efficiency estimate"""
# #         # Simplified: ratio of large to small packets
# #         large_packets = len(df[df['length'] > 500])
# #         small_packets = len(df[df['length'] <= 100])
# #         total_packets = len(df)
        
# #         if total_packets > 0:
# #             return (large_packets / total_packets) * 100
# #         return 0

# #     def calculate_performance_score(self, metrics):
# #         """Calculate overall performance score (0-100)"""
# #         score = 0
# #         max_score = 0
        
# #         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# #             # Throughput contribution (30%)
# #             quic_tput = metrics['QUIC']['throughput_mbps']
# #             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
# #             if tcp_tput > 0:
# #                 throughput_score = min(100, (quic_tput / tcp_tput) * 50)
# #                 score += throughput_score
# #             max_score += 30
            
# #             # Efficiency contribution (25%)
# #             quic_eff = metrics['QUIC']['efficiency_ratio']
# #             tcp_eff = metrics['TCP/TLS']['efficiency_ratio']
# #             if tcp_eff > 0:
# #                 efficiency_score = min(25, (quic_eff / tcp_eff) * 25)
# #                 score += efficiency_score
# #             max_score += 25
            
# #             # Stability contribution (20%)
# #             quic_jitter = metrics['QUIC']['jitter_ms']
# #             tcp_jitter = metrics['TCP/TLS']['jitter_ms']
# #             if tcp_jitter > 0:
# #                 stability_score = min(20, (tcp_jitter / max(quic_jitter, 0.1)) * 10)
# #                 score += stability_score
# #             max_score += 20
            
# #             # Connection diversity (15%)
# #             quic_diversity = metrics['QUIC']['port_diversity']
# #             tcp_diversity = metrics['TCP/TLS']['port_diversity']
# #             if tcp_diversity > 0:
# #                 diversity_score = min(15, (quic_diversity / tcp_diversity) * 15)
# #                 score += diversity_score
# #             max_score += 15
            
# #             # Goodput efficiency (10%)
# #             quic_goodput = metrics['QUIC']['goodput_estimate']
# #             tcp_goodput = metrics['TCP/TLS']['goodput_estimate']
# #             if tcp_goodput > 0:
# #                 goodput_score = min(10, (quic_goodput / tcp_goodput) * 10)
# #                 score += goodput_score
# #             max_score += 10
        
# #         return min(100, (score / max_score * 100)) if max_score > 0 else 0

# #     def get_traffic_trends(self, window_minutes=5):
# #         """Get traffic trends over time"""
# #         if len(self.metrics_history) < 2:
# #             return {}
        
# #         cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
# #         recent_data = [m for m in self.metrics_history if m['timestamp'] > cutoff_time]
        
# #         trends = {}
# #         if len(recent_data) >= 2:
# #             for protocol in ['QUIC', 'TCP/TLS']:
# #                 if protocol in recent_data[0]['metrics']:
# #                     first = recent_data[0]['metrics'][protocol]
# #                     last = recent_data[-1]['metrics'][protocol]
                    
# #                     trends[protocol] = {
# #                         'throughput_trend': '📈' if last['throughput_mbps'] > first['throughput_mbps'] else '📉',
# #                         'throughput_change': ((last['throughput_mbps'] - first['throughput_mbps']) / first['throughput_mbps'] * 100) if first['throughput_mbps'] > 0 else 0,
# #                         'packet_count_trend': '📈' if last['packet_count'] > first['packet_count'] else '📉',
# #                         'efficiency_trend': '📈' if last['efficiency_ratio'] > first['efficiency_ratio'] else '📉'
# #                     }
        
# #         return trends

# # def get_available_interfaces():
# #     """Get available network interfaces on the system"""
# #     try:
# #         # Get all available interfaces using Scapy
# #         interfaces = scapy.get_if_list()
        
# #         # Filter and prioritize common macOS interfaces
# #         preferred_order = ['en0', 'en1', 'en2', 'en3', 'en4', 'eth0', 'wlan0']
        
# #         # Sort interfaces by preferred order
# #         sorted_interfaces = []
# #         for preferred in preferred_order:
# #             if preferred in interfaces:
# #                 sorted_interfaces.append(preferred)
        
# #         # Add any remaining interfaces
# #         for iface in interfaces:
# #             if iface not in sorted_interfaces:
# #                 sorted_interfaces.append(iface)
        
# #         return sorted_interfaces if sorted_interfaces else ['en0']  # Fallback to en0
        
# #     except Exception as e:
# #         st.error(f"Error detecting interfaces: {e}")
# #         # Return common macOS interfaces as fallback
# #         return ['en0', 'en1', 'en2', 'en3', 'en4']

# # class AdvancedVisualizer:
# #     def __init__(self):
# #         self.colors = {
# #             'QUIC': '#1f77b4',
# #             'TCP/TLS': '#ff7f0e',
# #             'HTTPS': '#2ca02c'
# #         }
# #         self.light_colors = {
# #             'QUIC': '#8fc1e3',
# #             'TCP/TLS': '#ffb366',
# #             'HTTPS': '#98df8a'
# #         }
    
# #     def create_comprehensive_dashboard(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame, analyzer: AdvancedPacketAnalyzer):
# #         """Create comprehensive performance dashboard with advanced visualizations"""
        
# #         # Performance Score Card
# #         st.subheader("🏆 Overall Performance Score")
# #         if 'comparison' in metrics:
# #             score = metrics['comparison'].get('performance_score', 0)
# #             col1, col2, col3 = st.columns([2, 1, 1])
            
# #             with col1:
# #                 # Create gauge chart for performance score
# #                 fig = go.Figure(go.Indicator(
# #                     mode = "gauge+number+delta",
# #                     value = score,
# #                     domain = {'x': [0, 1], 'y': [0, 1]},
# #                     title = {'text': "QUIC Performance Score"},
# #                     delta = {'reference': 50},
# #                     gauge = {
# #                         'axis': {'range': [None, 100]},
# #                         'bar': {'color': self.colors['QUIC']},
# #                         'steps': [
# #                             {'range': [0, 50], 'color': "lightgray"},
# #                             {'range': [50, 80], 'color': "lightyellow"},
# #                             {'range': [80, 100], 'color': "lightgreen"}
# #                         ],
# #                         'threshold': {
# #                             'line': {'color': "red", 'width': 4},
# #                             'thickness': 0.75,
# #                             'value': 90
# #                         }
# #                     }
# #                 ))
# #                 fig.update_layout(height=300)
# #                 st.plotly_chart(fig, use_container_width=True)
            
# #             with col2:
# #                 throughput_ratio = metrics['comparison'].get('throughput_ratio', 1)
# #                 st.metric("Throughput Ratio", f"{throughput_ratio:.2f}x", 
# #                          "QUIC vs TCP/TLS")
            
# #             with col3:
# #                 efficiency_ratio = metrics['comparison'].get('efficiency_ratio', 1)
# #                 st.metric("Efficiency Ratio", f"{efficiency_ratio:.2f}x",
# #                          "QUIC vs TCP/TLS")
        
# #         # Real-time Metrics Header
# #         st.subheader("📊 Real-time Performance Metrics")
# #         self._display_advanced_metrics_header(metrics)
        
# #         # Advanced Comparison Charts
# #         st.subheader("📈 Advanced Protocol Comparison")
# #         tab1, tab2, tab3, tab4 = st.tabs(["Throughput Analysis", "Efficiency Metrics", "Traffic Patterns", "Connection Analysis"])
        
# #         with tab1:
# #             self._plot_advanced_throughput_analysis(metrics)
        
# #         with tab2:
# #             self._plot_efficiency_breakdown(metrics)
        
# #         with tab3:
# #             self._plot_traffic_pattern_analysis(quic_df, tcp_df)
        
# #         with tab4:
# #             self._plot_connection_analysis(metrics, quic_df, tcp_df)
        
# #         # Statistical Analysis
# #         st.subheader("📊 Statistical Analysis")
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             self._plot_packet_size_distribution(quic_df, tcp_df)
        
# #         with col2:
# #             self._plot_timing_analysis(metrics)
        
# #         # Network Quality Indicators
# #         st.subheader("🌐 Network Quality Indicators")
# #         self._plot_network_quality_indicators(metrics)
        
# #         # Traffic Composition
# #         st.subheader("🔍 Traffic Composition Analysis")
# #         self._plot_traffic_composition(quic_df, tcp_df)
        
# #         # Detailed Metrics Table
# #         st.subheader("📋 Comprehensive Metrics Table")
# #         self._show_advanced_metrics_table(metrics)
        
# #         # Trends (if available)
# #         trends = analyzer.get_traffic_trends()
# #         if trends:
# #             st.subheader("📅 Performance Trends")
# #             self._display_trend_indicators(trends)

# #     def _display_advanced_metrics_header(self, metrics: Dict[str, Any]):
# #         """Display advanced metrics header with more indicators"""
# #         col1, col2, col3, col4, col5 = st.columns(5)
        
# #         with col1:
# #             if 'QUIC' in metrics:
# #                 st.metric(
# #                     "QUIC Throughput", 
# #                     f"{metrics['QUIC']['throughput_mbps']:.2f} Mbps",
# #                     f"{metrics['QUIC']['packet_count']} packets"
# #                 )
        
# #         with col2:
# #             if 'TCP/TLS' in metrics:
# #                 st.metric(
# #                     "TCP/TLS Throughput",
# #                     f"{metrics['TCP/TLS']['throughput_mbps']:.2f} Mbps", 
# #                     f"{metrics['TCP/TLS']['packet_count']} packets"
# #                 )
                
# #         with col3:
# #             if 'QUIC' in metrics:
# #                 st.metric(
# #                     "QUIC Goodput",
# #                     f"{metrics['QUIC']['goodput_estimate']:.2f} Mbps",
# #                     f"{metrics['QUIC']['efficiency_ratio']:.1f} bytes/pkt"
# #                 )
                
# #         with col4:
# #             if 'TCP/TLS' in metrics:
# #                 st.metric(
# #                     "TCP/TLS Goodput", 
# #                     f"{metrics['TCP/TLS']['goodput_estimate']:.2f} Mbps",
# #                     f"{metrics['TCP/TLS']['efficiency_ratio']:.1f} bytes/pkt"
# #                 )
        
# #         with col5:
# #             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# #                 jitter_ratio = metrics['comparison'].get('jitter_ratio', 1)
# #                 st.metric(
# #                     "Jitter Ratio",
# #                     f"{jitter_ratio:.2f}x",
# #                     "Lower is better"
# #                 )

# #     def _plot_advanced_throughput_analysis(self, metrics: Dict[str, Any]):
# #         """Plot advanced throughput analysis"""
# #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# #             return
            
# #         fig = make_subplots(
# #             rows=2, cols=2,
# #             subplot_titles=('Total Throughput', 'Goodput Comparison', 
# #                           'Packet Rate', 'Efficiency Ratio'),
# #             specs=[[{"secondary_y": False}, {"secondary_y": False}],
# #                    [{"secondary_y": False}, {"secondary_y": False}]]
# #         )
        
# #         protocols = ['QUIC', 'TCP/TLS']
        
# #         # Total Throughput
# #         throughputs = [metrics[p]['throughput_mbps'] for p in protocols]
# #         fig.add_trace(
# #             go.Bar(x=protocols, y=throughputs, name='Throughput',
# #                   marker_color=[self.colors[p] for p in protocols]),
# #             row=1, col=1
# #         )
        
# #         # Goodput Comparison
# #         goodputs = [metrics[p]['goodput_estimate'] for p in protocols]
# #         fig.add_trace(
# #             go.Bar(x=protocols, y=goodputs, name='Goodput',
# #                   marker_color=[self.light_colors[p] for p in protocols]),
# #             row=1, col=2
# #         )
        
# #         # Packet Rate
# #         packet_rates = [metrics[p]['packets_per_second'] for p in protocols]
# #         fig.add_trace(
# #             go.Bar(x=protocols, y=packet_rates, name='Packets/s',
# #                   marker_color=[self.colors[p] for p in protocols]),
# #             row=2, col=1
# #         )
        
# #         # Efficiency
# #         efficiencies = [metrics[p]['efficiency_ratio'] for p in protocols]
# #         fig.add_trace(
# #             go.Bar(x=protocols, y=efficiencies, name='Efficiency',
# #                   marker_color=[self.light_colors[p] for p in protocols]),
# #             row=2, col=2
# #         )
        
# #         fig.update_layout(height=500, showlegend=False)
# #         st.plotly_chart(fig, use_container_width=True)

# #     def _plot_efficiency_breakdown(self, metrics: Dict[str, Any]):
# #         """Plot detailed efficiency breakdown"""
# #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# #             return
            
# #         fig = go.Figure()
        
# #         efficiency_metrics = ['efficiency_ratio', 'goodput_estimate', 'overhead_estimate', 'compression_efficiency']
# #         metric_names = ['Bytes/Packet', 'Goodput (Mbps)', 'Overhead %', 'Compression %']
        
# #         for i, (metric, name) in enumerate(zip(efficiency_metrics, metric_names)):
# #             fig.add_trace(go.Bar(
# #                 name=name,
# #                 x=['QUIC', 'TCP/TLS'],
# #                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
# #                 marker_color=[self.colors['QUIC'] if i % 2 == 0 else self.light_colors['QUIC'],
# #                             self.colors['TCP/TLS'] if i % 2 == 0 else self.light_colors['TCP/TLS']]
# #             ))
        
# #         fig.update_layout(
# #             title='Efficiency Metrics Breakdown',
# #             barmode='group',
# #             height=400
# #         )
# #         st.plotly_chart(fig, use_container_width=True)

# #     def _plot_traffic_pattern_analysis(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# #         """Analyze and plot traffic patterns"""
# #         if quic_df.empty and tcp_df.empty:
# #             st.info("No traffic data for pattern analysis")
# #             return
            
# #         fig = make_subplots(
# #             rows=2, cols=2,
# #             subplot_titles=('Traffic Volume Over Time', 'Cumulative Bytes',
# #                           'Packet Size Distribution', 'Size Variation'),
# #             specs=[[{"secondary_y": False}, {"secondary_y": False}],
# #                    [{"secondary_y": False}, {"secondary_y": False}]]
# #         )
        
# #         # Ensure timestamps are properly converted
# #         if not quic_df.empty:
# #             quic_df = quic_df.copy()
# #             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
# #             quic_df = quic_df.sort_values('timestamp')
# #             quic_df['time_elapsed'] = (quic_df['timestamp'] - quic_df['timestamp'].min()).dt.total_seconds()
            
# #             # Traffic Volume Over Time
# #             fig.add_trace(
# #                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['length'],
# #                           name='QUIC Packet Size', line=dict(color=self.colors['QUIC'])),
# #                 row=1, col=1
# #             )
            
# #             # Cumulative Bytes
# #             quic_df['cumulative_bytes'] = quic_df['length'].cumsum()
# #             fig.add_trace(
# #                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['cumulative_bytes'],
# #                           name='QUIC Cumulative', line=dict(color=self.colors['QUIC'])),
# #                 row=1, col=2
# #             )
        
# #         if not tcp_df.empty:
# #             tcp_df = tcp_df.copy()
# #             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
# #             tcp_df = tcp_df.sort_values('timestamp')
# #             tcp_df['time_elapsed'] = (tcp_df['timestamp'] - tcp_df['timestamp'].min()).dt.total_seconds()
            
# #             # Traffic Volume Over Time
# #             fig.add_trace(
# #                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['length'],
# #                           name='TCP Packet Size', line=dict(color=self.colors['TCP/TLS'])),
# #                 row=1, col=1
# #             )
            
# #             # Cumulative Bytes
# #             tcp_df['cumulative_bytes'] = tcp_df['length'].cumsum()
# #             fig.add_trace(
# #                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['cumulative_bytes'],
# #                           name='TCP Cumulative', line=dict(color=self.colors['TCP/TLS'])),
# #                 row=1, col=2
# #             )
        
# #         # Packet Size Distribution (Histogram)
# #         if not quic_df.empty:
# #             fig.add_trace(
# #                 go.Histogram(x=quic_df['length'], name='QUIC Sizes',
# #                             marker_color=self.colors['QUIC'], opacity=0.7),
# #                 row=2, col=1
# #             )
        
# #         if not tcp_df.empty:
# #             fig.add_trace(
# #                 go.Histogram(x=tcp_df['length'], name='TCP Sizes',
# #                             marker_color=self.colors['TCP/TLS'], opacity=0.7),
# #                 row=2, col=1
# #             )
        
# #         # Size Variation (Coefficient of Variation)
# #         size_variation_values = [0.5, 0.3]  # Default values
# #         if not quic_df.empty and not tcp_df.empty:
# #             quic_variation = quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
# #             tcp_variation = tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
# #             size_variation_values = [quic_variation, tcp_variation]
        
# #         fig.add_trace(
# #             go.Bar(x=['QUIC', 'TCP/TLS'], y=size_variation_values, 
# #                    name='Size Variation', marker_color=[self.colors['QUIC'], self.colors['TCP/TLS']]),
# #             row=2, col=2
# #         )
        
# #         fig.update_layout(height=600, showlegend=True)
# #         st.plotly_chart(fig, use_container_width=True)

# #     def _plot_connection_analysis(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# #         """Plot connection and network analysis"""
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             # Connection Diversity
# #             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
# #                 fig = go.Figure()
# #                 categories = ['Sources', 'Destinations', 'Ports']
# #                 quic_values = [metrics['QUIC']['unique_sources'], 
# #                               metrics['QUIC']['unique_destinations'],
# #                               metrics['QUIC']['port_diversity']]
# #                 tcp_values = [metrics['TCP/TLS']['unique_sources'],
# #                              metrics['TCP/TLS']['unique_destinations'],
# #                              metrics['TCP/TLS']['port_diversity']]
                
# #                 fig.add_trace(go.Bar(name='QUIC', x=categories, y=quic_values,
# #                                     marker_color=self.colors['QUIC']))
# #                 fig.add_trace(go.Bar(name='TCP/TLS', x=categories, y=tcp_values,
# #                                     marker_color=self.colors['TCP/TLS']))
                
# #                 fig.update_layout(title='Connection Diversity', barmode='group')
# #                 st.plotly_chart(fig, use_container_width=True)
        
# #         with col2:
# #             # Port Distribution
# #             if not quic_df.empty or not tcp_df.empty:
# #                 fig = go.Figure()
                
# #                 if not quic_df.empty:
# #                     port_counts = quic_df['dst_port'].value_counts().head(10)
# #                     fig.add_trace(go.Bar(
# #                         x=port_counts.index.astype(str), y=port_counts.values,
# #                         name='QUIC Ports', marker_color=self.colors['QUIC']
# #                     ))
                
# #                 if not tcp_df.empty:
# #                     port_counts = tcp_df['dst_port'].value_counts().head(10)
# #                     fig.add_trace(go.Bar(
# #                         x=port_counts.index.astype(str), y=port_counts.values,
# #                         name='TCP Ports', marker_color=self.colors['TCP/TLS']
# #                     ))
                
# #                 fig.update_layout(title='Top Destination Ports')
# #                 st.plotly_chart(fig, use_container_width=True)

# #     def _plot_packet_size_distribution(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# #         """Plot detailed packet size distribution"""
# #         fig = go.Figure()
        
# #         if not quic_df.empty:
# #             fig.add_trace(go.Box(
# #                 y=quic_df['length'], name='QUIC Packet Sizes',
# #                 marker_color=self.colors['QUIC']
# #             ))
        
# #         if not tcp_df.empty:
# #             fig.add_trace(go.Box(
# #                 y=tcp_df['length'], name='TCP Packet Sizes', 
# #                 marker_color=self.colors['TCP/TLS']
# #             ))
        
# #         fig.update_layout(
# #             title='Packet Size Distribution (Box Plot)',
# #             yaxis_title='Packet Size (bytes)',
# #             height=400
# #         )
# #         st.plotly_chart(fig, use_container_width=True)

# #     def _plot_timing_analysis(self, metrics: Dict[str, Any]):
# #         """Plot timing and jitter analysis"""
# #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# #             return
            
# #         fig = go.Figure()
        
# #         timing_metrics = ['avg_interval_ms', 'jitter_ms', 'min_interval_ms', 'max_interval_ms']
# #         metric_names = ['Avg Interval', 'Jitter', 'Min Interval', 'Max Interval']
        
# #         for metric, name in zip(timing_metrics, metric_names):
# #             fig.add_trace(go.Bar(
# #                 name=name,
# #                 x=['QUIC', 'TCP/TLS'],
# #                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
# #                 text=[f"{metrics['QUIC'].get(metric, 0):.1f}", f"{metrics['TCP/TLS'].get(metric, 0):.1f}"],
# #                 textposition='auto'
# #             ))
        
# #         fig.update_layout(
# #             title='Timing Analysis (ms)',
# #             barmode='group',
# #             height=400
# #         )
# #         st.plotly_chart(fig, use_container_width=True)

# #     def _plot_network_quality_indicators(self, metrics: Dict[str, Any]):
# #         """Plot network quality indicators"""
# #         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
# #             return
            
# #         col1, col2, col3, col4 = st.columns(4)
        
# #         with col1:
# #             # Jitter indicator
# #             quic_jitter = metrics['QUIC'].get('jitter_ms', 0)
# #             st.metric("QUIC Jitter", f"{quic_jitter:.1f}ms", 
# #                      "Lower is better" if quic_jitter < metrics['TCP/TLS'].get('jitter_ms', 100) else "Higher than TCP")
        
# #         with col2:
# #             # Burstiness indicator
# #             quic_burst = metrics['QUIC'].get('burstiness', 0)
# #             st.metric("QUIC Burstiness", f"{quic_burst:.3f}",
# #                      "Closer to 0 is better")
        
# #         with col3:
# #             # Overhead indicator
# #             quic_overhead = metrics['QUIC'].get('overhead_estimate', 0)
# #             st.metric("QUIC Overhead", f"{quic_overhead:.1f}%",
# #                      "Lower is better")
        
# #         with col4:
# #             # Stability indicator
# #             quic_stability = 100 - min(100, metrics['QUIC'].get('traffic_volume_variation', 1) * 100)
# #             st.metric("QUIC Stability", f"{quic_stability:.1f}%",
# #                      "Higher is better")

# #     def _plot_traffic_composition(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
# #         """Plot traffic composition analysis"""
# #         col1, col2 = st.columns(2)
        
# #         with col1:
# #             # Protocol distribution pie chart
# #             if not quic_df.empty or not tcp_df.empty:
# #                 labels = ['QUIC', 'TCP/TLS']
# #                 values = [len(quic_df), len(tcp_df)]
                
# #                 fig = px.pie(values=values, names=labels, 
# #                             title='Protocol Distribution by Packet Count',
# #                             color=labels, color_discrete_map=self.colors)
# #                 st.plotly_chart(fig, use_container_width=True)
        
# #         with col2:
# #             # Data volume distribution
# #             if not quic_df.empty or not tcp_df.empty:
# #                 labels = ['QUIC', 'TCP/TLS']
# #                 values = [quic_df['length'].sum() if not quic_df.empty else 0,
# #                          tcp_df['length'].sum() if not tcp_df.empty else 0]
                
# #                 fig = px.pie(values=values, names=labels,
# #                             title='Data Volume Distribution by Protocol',
# #                             color=labels, color_discrete_map=self.colors)
# #                 st.plotly_chart(fig, use_container_width=True)

# #     def _show_advanced_metrics_table(self, metrics: Dict[str, Any]):
# #         """Display comprehensive metrics table"""
# #         if not metrics:
# #             return
            
# #         # Create detailed comparison table
# #         comparison_data = []
# #         metrics_to_show = {
# #             'Throughput (Mbps)': 'throughput_mbps',
# #             'Goodput (Mbps)': 'goodput_estimate', 
# #             'Packet Count': 'packet_count',
# #             'Avg Packet Size': 'avg_packet_size',
# #             'Packets/s': 'packets_per_second',
# #             'Unique Sources': 'unique_sources',
# #             'Unique Destinations': 'unique_destinations',
# #             'Port Diversity': 'port_diversity',
# #             'Avg Interval (ms)': 'avg_interval_ms',
# #             'Jitter (ms)': 'jitter_ms',
# #             'Efficiency': 'efficiency_ratio',
# #             'Overhead %': 'overhead_estimate',
# #             'Burstiness': 'burstiness'
# #         }
        
# #         for display_name, metric_key in metrics_to_show.items():
# #             row = {'Metric': display_name}
# #             for protocol in ['QUIC', 'TCP/TLS']:
# #                 if protocol in metrics:
# #                     row[protocol] = metrics[protocol].get(metric_key, 0)
# #             comparison_data.append(row)
        
# #         if comparison_data:
# #             df = pd.DataFrame(comparison_data)
# #             st.dataframe(df.style.format({
# #                 'QUIC': '{:.2f}',
# #                 'TCP/TLS': '{:.2f}'
# #             }), use_container_width=True, height=400)

# #     def _display_trend_indicators(self, trends: Dict[str, Any]):
# #         """Display trend indicators"""
# #         col1, col2, col3, col4 = st.columns(4)
        
# #         for protocol in ['QUIC', 'TCP/TLS']:
# #             if protocol in trends:
# #                 trend = trends[protocol]
# #                 if protocol == 'QUIC':
# #                     with col1:
# #                         st.metric(f"{protocol} Throughput Trend", 
# #                                  trend['throughput_trend'],
# #                                  f"{trend['throughput_change']:+.1f}%")
# #                     with col2:
# #                         st.metric(f"{protocol} Packet Trend",
# #                                  trend['packet_count_trend'],
# #                                  "Volume change")
# #                 else:
# #                     with col3:
# #                         st.metric(f"{protocol} Throughput Trend",
# #                                  trend['throughput_trend'],
# #                                  f"{trend['throughput_change']:+.1f}%")
# #                     with col4:
# #                         st.metric(f"{protocol} Efficiency Trend",
# #                                  trend['efficiency_trend'],
# #                                  "Efficiency change")

# # def run_packet_capture(duration: int = 30, interface: str = "en0") -> Optional[Dict]:
# #     """Execute packet capture service with sudo privileges"""
# #     try:
# #         # Get current directory
# #         current_dir = os.path.dirname(os.path.abspath(__file__))
# #         capture_script = os.path.join(current_dir, "packet_capture_service.py")
        
# #         # Ensure the script is executable
# #         if not os.access(capture_script, os.X_OK):
# #             os.chmod(capture_script, 0o755)
        
# #         # Run capture with sudo
# #         result = subprocess.run(
# #             ['sudo', 'python3', capture_script, str(duration), interface],
# #             capture_output=True,
# #             text=True,
# #             timeout=duration + 10
# #         )
        
# #         if result.returncode == 0:
# #             return json.loads(result.stdout)
# #         else:
# #             st.error(f"Capture service error: {result.stderr}")
# #             return None
            
# #     except subprocess.TimeoutExpired:
# #         st.error("Packet capture timed out. Try a shorter duration.")
# #         return None
# #     except json.JSONDecodeError as e:
# #         st.error(f"Failed to parse capture results: {e}")
# #         return None
# #     except Exception as e:
# #         st.error(f"Error running capture: {e}")
# #         return None

# # def main():
# #     # Page configuration
# #     st.set_page_config(
# #         page_title="QUIC Protocol Analyzer Pro",
# #         page_icon="🔄",
# #         layout="wide",
# #         initial_sidebar_state="expanded"
# #     )
    
# #     st.title("🔄 Advanced QUIC vs TCP/TLS Protocol Analyzer Pro")
    
# #     # Initialize session state
# #     if 'capture_data' not in st.session_state:
# #         st.session_state.capture_data = None
# #     if 'analysis_results' not in st.session_state:
# #         st.session_state.analysis_results = None
# #     if 'analyzer' not in st.session_state:
# #         st.session_state.analyzer = AdvancedPacketAnalyzer()
    
# #     # Sidebar controls
# #     st.sidebar.title("🎛️ Capture Controls")
    
# #     # Interface selection - dynamically detected
# #     interfaces = get_available_interfaces()
# #     selected_interface = st.sidebar.selectbox(
# #         "Network Interface",
# #         interfaces,
# #         help="Select the network interface to monitor"
# #     )
    
# #     # Show interface info
# #     st.sidebar.info(f"📡 Selected: {selected_interface}")
    
# #     # Capture duration
# #     capture_duration = st.sidebar.slider(
# #         "Capture Duration (seconds)",
# #         min_value=10,
# #         max_value=120,
# #         value=30,
# #         step=5,
# #         help="How long to capture packets"
# #     )
    
# #     # Analysis mode
# #     analysis_mode = st.sidebar.selectbox(
# #         "Analysis Mode",
# #         ["Basic", "Advanced", "Comprehensive"],
# #         help="Level of detail in analysis"
# #     )
    
# #     # Control buttons
# #     col1, col2 = st.sidebar.columns(2)
    
# #     with col1:
# #         if st.button("🚀 Start Capture", type="primary"):
# #             with st.spinner(f"Capturing packets for {capture_duration} seconds..."):
# #                 capture_data = run_packet_capture(capture_duration, selected_interface)
                
# #                 if capture_data and 'error' not in capture_data:
# #                     st.session_state.capture_data = capture_data
                    
# #                     # Analyze packets
# #                     analyzer = st.session_state.analyzer
# #                     quic_df = pd.DataFrame(capture_data.get('quic_packets', []))
# #                     tcp_df = pd.DataFrame(capture_data.get('tcp_packets', []))
                    
# #                     analysis_results = analyzer.calculate_comprehensive_metrics(quic_df, tcp_df)
# #                     st.session_state.analysis_results = (analysis_results, quic_df, tcp_df)
                    
# #                     st.success(f"Capture completed! Got {len(quic_df)} QUIC and {len(tcp_df)} TCP packets")
# #                 else:
# #                     st.error("Capture failed. Check permissions and interface.")
    
# #     with col2:
# #         if st.button("🔄 Clear Results"):
# #             st.session_state.capture_data = None
# #             st.session_state.analysis_results = None
# #             st.rerun()
    
# #     # Display results if available
# #     if st.session_state.analysis_results:
# #         analysis_results, quic_df, tcp_df = st.session_state.analysis_results
# #         visualizer = AdvancedVisualizer()
# #         visualizer.create_comprehensive_dashboard(analysis_results, quic_df, tcp_df, st.session_state.analyzer)
        
# #         # Raw data view
# #         with st.expander("📋 View Raw Packet Data"):
# #             tab1, tab2 = st.tabs(["QUIC Packets", "TCP/TLS Packets"])
            
# #             with tab1:
# #                 if not quic_df.empty:
# #                     st.dataframe(quic_df, use_container_width=True)
# #                 else:
# #                     st.info("No QUIC packets captured")
            
# #             with tab2:
# #                 if not tcp_df.empty:
# #                     st.dataframe(tcp_df, use_container_width=True)
# #                 else:
# #                     st.info("No TCP/TLS packets captured")
    
# #     else:
# #         # Enhanced welcome screen
# #         st.markdown("""
# #         ## 🚀 Welcome to QUIC Protocol Analyzer Pro
        
# #         This advanced tool provides comprehensive real-time analysis and comparison of:
# #         - **QUIC** (Quick UDP Internet Connections) 
# #         - **TCP/TLS** (Traditional encrypted transport)
        
# #         ### 📊 New Advanced Features:
        
# #         **🎯 Performance Scoring**
# #         - Overall performance score (0-100)
# #         - Multi-factor performance evaluation
# #         - Real-time performance trends
        
# #         **📈 Advanced Analytics**
# #         - Goodput vs Throughput analysis
# #         - Protocol overhead estimation
# #         - Traffic burstiness measurement
# #         - Network stability indicators
        
# #         **🔍 Deep Packet Analysis**
# #         - Packet size distribution
# #         - Timing and jitter analysis
# #         - Connection diversity metrics
# #         - Traffic pattern recognition
        
# #         **🌐 Network Quality Metrics**
# #         - Jitter and latency analysis
# #         - Protocol efficiency scores
# #         - Compression efficiency estimates
# #         - Traffic composition breakdown
        
# #         ### 🚀 Quick Start:
# #         1. Select your network interface above
# #         2. Set capture duration (10-120 seconds)
# #         3. Choose analysis mode (Basic/Advanced/Comprehensive)
# #         4. Click **Start Capture** to begin
# #         5. Generate web traffic during capture for best results
        
# #         ### 🔧 Requirements:
# #         - macOS/Linux with Python 3.8+
# #         - Sudo/root privileges for packet capture
# #         - Active network traffic on selected interface
# #         """)
        
# #         # Interface detection info
# #         st.sidebar.info(f"🔍 Detected interfaces: {', '.join(interfaces)}")
        
# #         # Demo data option
# #         if st.button("🎮 Load Advanced Demo Data", type="secondary"):
# #             # Create comprehensive demo data
# #             demo_analysis = {
# #                 'QUIC': {
# #                     'packet_count': 150,
# #                     'total_bytes': 187500,
# #                     'avg_packet_size': 1250,
# #                     'std_packet_size': 150,
# #                     'throughput_mbps': 1.5,
# #                     'packets_per_second': 5.0,
# #                     'unique_sources': 3,
# #                     'unique_destinations': 5,
# #                     'port_diversity': 8,
# #                     'avg_interval_ms': 12.5,
# #                     'jitter_ms': 2.1,
# #                     'min_interval_ms': 8.2,
# #                     'max_interval_ms': 25.7,
# #                     'burstiness': 0.15,
# #                     'traffic_volume_variation': 0.12,
# #                     'efficiency_ratio': 1250.0,
# #                     'goodput_estimate': 1.2,
# #                     'overhead_estimate': 4.0,
# #                     'compression_efficiency': 65.0,
# #                     'common_ports': {443: 120, 80: 30}
# #                 },
# #                 'TCP/TLS': {
# #                     'packet_count': 200, 
# #                     'total_bytes': 240000,
# #                     'avg_packet_size': 1200,
# #                     'std_packet_size': 180,
# #                     'throughput_mbps': 1.92,
# #                     'packets_per_second': 6.67,
# #                     'unique_sources': 4,
# #                     'unique_destinations': 6,
# #                     'port_diversity': 10,
# #                     'avg_interval_ms': 15.2,
# #                     'jitter_ms': 3.4,
# #                     'min_interval_ms': 10.1,
# #                     'max_interval_ms': 32.8,
# #                     'burstiness': 0.22,
# #                     'traffic_volume_variation': 0.15,
# #                     'efficiency_ratio': 1200.0,
# #                     'goodput_estimate': 1.5,
# #                     'overhead_estimate': 6.7,
# #                     'compression_efficiency': 58.0,
# #                     'common_ports': {443: 180, 80: 20}
# #                 },
# #                 'comparison': {
# #                     'throughput_ratio': 0.78,
# #                     'packet_size_ratio': 1.04,
# #                     'efficiency_ratio': 1.04,
# #                     'jitter_ratio': 0.62,
# #                     'performance_score': 72.5
# #                 }
# #             }
            
# #             st.session_state.analysis_results = (demo_analysis, pd.DataFrame(), pd.DataFrame())
# #             st.rerun()

# #     # Enhanced footer
# #     st.sidebar.markdown("---")
# #     st.sidebar.info(
# #         "💡 **Pro Tip**: For best results, use **en0** (WiFi) and browse HTTPS sites "
# #         "during capture to generate QUIC traffic."
# #     )

# # if __name__ == "__main__":
# #     main()


# import streamlit as st
# import pandas as pd
# import subprocess
# import json
# import os
# import tempfile
# from datetime import datetime, timedelta
# import plotly.graph_objects as go
# import plotly.express as px
# from plotly.subplots import make_subplots
# import numpy as np
# from typing import Dict, Any, Tuple, Optional
# import time
# import scapy.all as scapy

# class AdvancedPacketAnalyzer:
#     def __init__(self):
#         self.metrics_history = []
#         self.traffic_patterns = []
        
#     def calculate_comprehensive_metrics(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame) -> Dict[str, Any]:
#         """Calculate comprehensive metrics for both protocols"""
#         metrics = {}
        
#         # QUIC Metrics
#         if not quic_df.empty:
#             quic_df = quic_df.copy()
#             # Ensure timestamp conversion
#             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
#             quic_df = quic_df.sort_values('timestamp')
            
#             # Basic metrics
#             metrics['QUIC'] = {
#                 'packet_count': len(quic_df),
#                 'total_bytes': quic_df['length'].sum(),
#                 'avg_packet_size': quic_df['length'].mean(),
#                 'std_packet_size': quic_df['length'].std(),
#                 'throughput_mbps': (quic_df['length'].sum() * 8) / 1e6,
#                 'packets_per_second': len(quic_df) / max(1, (quic_df['timestamp'].max() - quic_df['timestamp'].min()).total_seconds()),
#                 'unique_sources': quic_df['src_ip'].nunique(),
#                 'unique_destinations': quic_df['dst_ip'].nunique(),
#                 'port_diversity': quic_df['dst_port'].nunique(),
#                 'common_ports': quic_df['dst_port'].value_counts().head(5).to_dict()
#             }
            
#             # Advanced timing metrics
#             if len(quic_df) > 1:
#                 time_diffs = quic_df['timestamp'].diff().dt.total_seconds().dropna()
#                 metrics['QUIC'].update({
#                     'avg_interval_ms': time_diffs.mean() * 1000,
#                     'jitter_ms': time_diffs.std() * 1000,
#                     'min_interval_ms': time_diffs.min() * 1000,
#                     'max_interval_ms': time_diffs.max() * 1000,
#                     'burstiness': self.calculate_burstiness(time_diffs),
#                     'traffic_volume_variation': quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
#                 })
            
#             # Efficiency metrics
#             metrics['QUIC'].update({
#                 'efficiency_ratio': metrics['QUIC']['total_bytes'] / max(1, metrics['QUIC']['packet_count']),
#                 'goodput_estimate': self.estimate_goodput(quic_df),
#                 'overhead_estimate': self.estimate_protocol_overhead(quic_df, 'QUIC'),
#                 'compression_efficiency': self.calculate_compression_efficiency(quic_df)
#             })
        
#         # TCP/TLS Metrics
#         if not tcp_df.empty:
#             tcp_df = tcp_df.copy()
#             # Ensure timestamp conversion
#             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
#             tcp_df = tcp_df.sort_values('timestamp')
            
#             # Basic metrics
#             metrics['TCP/TLS'] = {
#                 'packet_count': len(tcp_df),
#                 'total_bytes': tcp_df['length'].sum(),
#                 'avg_packet_size': tcp_df['length'].mean(),
#                 'std_packet_size': tcp_df['length'].std(),
#                 'throughput_mbps': (tcp_df['length'].sum() * 8) / 1e6,
#                 'packets_per_second': len(tcp_df) / max(1, (tcp_df['timestamp'].max() - tcp_df['timestamp'].min()).total_seconds()),
#                 'unique_sources': tcp_df['src_ip'].nunique(),
#                 'unique_destinations': tcp_df['dst_ip'].nunique(),
#                 'port_diversity': tcp_df['dst_port'].nunique(),
#                 'common_ports': tcp_df['dst_port'].value_counts().head(5).to_dict()
#             }
            
#             # Advanced timing metrics
#             if len(tcp_df) > 1:
#                 time_diffs = tcp_df['timestamp'].diff().dt.total_seconds().dropna()
#                 metrics['TCP/TLS'].update({
#                     'avg_interval_ms': time_diffs.mean() * 1000,
#                     'jitter_ms': time_diffs.std() * 1000,
#                     'min_interval_ms': time_diffs.min() * 1000,
#                     'max_interval_ms': time_diffs.max() * 1000,
#                     'burstiness': self.calculate_burstiness(time_diffs),
#                     'traffic_volume_variation': tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
#                 })
            
#             # Efficiency metrics
#             metrics['TCP/TLS'].update({
#                 'efficiency_ratio': metrics['TCP/TLS']['total_bytes'] / max(1, metrics['TCP/TLS']['packet_count']),
#                 'goodput_estimate': self.estimate_goodput(tcp_df),
#                 'overhead_estimate': self.estimate_protocol_overhead(tcp_df, 'TCP/TLS'),
#                 'compression_efficiency': self.calculate_compression_efficiency(tcp_df)
#             })
        
#         # Comparison metrics
#         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
#             quic_tput = metrics['QUIC']['throughput_mbps']
#             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
            
#             metrics['comparison'] = {
#                 'throughput_ratio': quic_tput / tcp_tput if tcp_tput > 0 else float('inf'),
#                 'packet_size_ratio': metrics['QUIC']['avg_packet_size'] / metrics['TCP/TLS']['avg_packet_size'] if metrics['TCP/TLS']['avg_packet_size'] > 0 else float('inf'),
#                 'efficiency_ratio': metrics['QUIC']['efficiency_ratio'] / metrics['TCP/TLS']['efficiency_ratio'] if metrics['TCP/TLS']['efficiency_ratio'] > 0 else float('inf'),
#                 'jitter_ratio': metrics['QUIC']['jitter_ms'] / metrics['TCP/TLS']['jitter_ms'] if metrics['TCP/TLS']['jitter_ms'] > 0 else float('inf'),
#                 'performance_score': self.calculate_performance_score(metrics)
#             }
        
#         # Store for trend analysis
#         self.metrics_history.append({
#             'timestamp': datetime.now(),
#             'metrics': metrics
#         })
        
#         return metrics

#     def calculate_burstiness(self, intervals):
#         """Calculate traffic burstiness (Burstiness Parameter)"""
#         if len(intervals) < 2:
#             return 0
#         mean_interval = np.mean(intervals)
#         std_interval = np.std(intervals)
#         return (std_interval - mean_interval) / (std_interval + mean_interval) if (std_interval + mean_interval) > 0 else 0

#     def estimate_goodput(self, df):
#         """Estimate goodput (application layer throughput)"""
#         # Simplified: assume larger packets have more application data
#         large_packets = df[df['length'] > 100]  # Packets > 100 bytes
#         if len(df) > 0:
#             return (large_packets['length'].sum() * 8) / 1e6  # Mbps
#         return 0

#     def estimate_protocol_overhead(self, df, protocol):
#         """Estimate protocol overhead"""
#         avg_size = df['length'].mean()
#         if protocol == 'QUIC':
#             estimated_header = 50  # bytes for QUIC
#         else:
#             estimated_header = 80  # bytes for TCP+TLS
        
#         if avg_size > estimated_header:
#             return (estimated_header / avg_size) * 100
#         return 0

#     def calculate_compression_efficiency(self, df):
#         """Calculate compression efficiency estimate"""
#         # Simplified: ratio of large to small packets
#         large_packets = len(df[df['length'] > 500])
#         small_packets = len(df[df['length'] <= 100])
#         total_packets = len(df)
        
#         if total_packets > 0:
#             return (large_packets / total_packets) * 100
#         return 0

#     def calculate_performance_score(self, metrics):
#         """Calculate overall performance score (0-100)"""
#         score = 0
#         max_score = 0
        
#         if 'QUIC' in metrics and 'TCP/TLS' in metrics:
#             # Throughput contribution (30%)
#             quic_tput = metrics['QUIC']['throughput_mbps']
#             tcp_tput = metrics['TCP/TLS']['throughput_mbps']
#             if tcp_tput > 0:
#                 throughput_score = min(100, (quic_tput / tcp_tput) * 50)
#                 score += throughput_score
#             max_score += 30
            
#             # Efficiency contribution (25%)
#             quic_eff = metrics['QUIC']['efficiency_ratio']
#             tcp_eff = metrics['TCP/TLS']['efficiency_ratio']
#             if tcp_eff > 0:
#                 efficiency_score = min(25, (quic_eff / tcp_eff) * 25)
#                 score += efficiency_score
#             max_score += 25
            
#             # Stability contribution (20%)
#             quic_jitter = metrics['QUIC']['jitter_ms']
#             tcp_jitter = metrics['TCP/TLS']['jitter_ms']
#             if tcp_jitter > 0:
#                 stability_score = min(20, (tcp_jitter / max(quic_jitter, 0.1)) * 10)
#                 score += stability_score
#             max_score += 20
            
#             # Connection diversity (15%)
#             quic_diversity = metrics['QUIC']['port_diversity']
#             tcp_diversity = metrics['TCP/TLS']['port_diversity']
#             if tcp_diversity > 0:
#                 diversity_score = min(15, (quic_diversity / tcp_diversity) * 15)
#                 score += diversity_score
#             max_score += 15
            
#             # Goodput efficiency (10%)
#             quic_goodput = metrics['QUIC']['goodput_estimate']
#             tcp_goodput = metrics['TCP/TLS']['goodput_estimate']
#             if tcp_goodput > 0:
#                 goodput_score = min(10, (quic_goodput / tcp_goodput) * 10)
#                 score += goodput_score
#             max_score += 10
        
#         return min(100, (score / max_score * 100)) if max_score > 0 else 0

#     def get_traffic_trends(self, window_minutes=5):
#         """Get traffic trends over time"""
#         if len(self.metrics_history) < 2:
#             return {}
        
#         cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
#         recent_data = [m for m in self.metrics_history if m['timestamp'] > cutoff_time]
        
#         trends = {}
#         if len(recent_data) >= 2:
#             for protocol in ['QUIC', 'TCP/TLS']:
#                 if protocol in recent_data[0]['metrics']:
#                     first = recent_data[0]['metrics'][protocol]
#                     last = recent_data[-1]['metrics'][protocol]
                    
#                     trends[protocol] = {
#                         'throughput_trend': '📈' if last['throughput_mbps'] > first['throughput_mbps'] else '📉',
#                         'throughput_change': ((last['throughput_mbps'] - first['throughput_mbps']) / first['throughput_mbps'] * 100) if first['throughput_mbps'] > 0 else 0,
#                         'packet_count_trend': '📈' if last['packet_count'] > first['packet_count'] else '📉',
#                         'efficiency_trend': '📈' if last['efficiency_ratio'] > first['efficiency_ratio'] else '📉'
#                     }
        
#         return trends

# def get_available_interfaces():
#     """Get available network interfaces on the system"""
#     try:
#         # Get all available interfaces using Scapy
#         interfaces = scapy.get_if_list()
        
#         # Filter and prioritize common macOS interfaces
#         preferred_order = ['en0', 'en1', 'en2', 'en3', 'en4', 'eth0', 'wlan0']
        
#         # Sort interfaces by preferred order
#         sorted_interfaces = []
#         for preferred in preferred_order:
#             if preferred in interfaces:
#                 sorted_interfaces.append(preferred)
        
#         # Add any remaining interfaces
#         for iface in interfaces:
#             if iface not in sorted_interfaces:
#                 sorted_interfaces.append(iface)
        
#         return sorted_interfaces if sorted_interfaces else ['en0']  # Fallback to en0
        
#     except Exception as e:
#         st.error(f"Error detecting interfaces: {e}")
#         # Return common macOS interfaces as fallback
#         return ['en0', 'en1', 'en2', 'en3', 'en4']

# class AdvancedVisualizer:
#     def __init__(self):
#         self.colors = {
#             'QUIC': '#1f77b4',
#             'TCP/TLS': '#ff7f0e',
#             'HTTPS': '#2ca02c'
#         }
#         self.light_colors = {
#             'QUIC': '#8fc1e3',
#             'TCP/TLS': '#ffb366',
#             'HTTPS': '#98df8a'
#         }
#         self.chart_counter = 0
    
#     def _get_unique_key(self, prefix="chart"):
#         """Generate unique keys for plotly charts"""
#         self.chart_counter += 1
#         return f"{prefix}_{self.chart_counter}"
    
#     def create_comprehensive_dashboard(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame, analyzer: AdvancedPacketAnalyzer):
#         """Create comprehensive performance dashboard with organized tabs"""
        
#         # Performance Score Card
#         st.subheader("🏆 Overall Performance Score")
#         if 'comparison' in metrics:
#             score = metrics['comparison'].get('performance_score', 0)
#             col1, col2, col3 = st.columns([2, 1, 1])
            
#             with col1:
#                 # Create gauge chart for performance score
#                 fig = go.Figure(go.Indicator(
#                     mode = "gauge+number+delta",
#                     value = score,
#                     domain = {'x': [0, 1], 'y': [0, 1]},
#                     title = {'text': "QUIC Performance Score"},
#                     delta = {'reference': 50},
#                     gauge = {
#                         'axis': {'range': [None, 100]},
#                         'bar': {'color': self.colors['QUIC']},
#                         'steps': [
#                             {'range': [0, 50], 'color': "lightgray"},
#                             {'range': [50, 80], 'color': "lightyellow"},
#                             {'range': [80, 100], 'color': "lightgreen"}
#                         ],
#                         'threshold': {
#                             'line': {'color': "red", 'width': 4},
#                             'thickness': 0.75,
#                             'value': 90
#                         }
#                     }
#                 ))
#                 fig.update_layout(height=300)
#                 st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("score_gauge"))
            
#             with col2:
#                 throughput_ratio = metrics['comparison'].get('throughput_ratio', 1)
#                 st.metric("Throughput Ratio", f"{throughput_ratio:.2f}x", 
#                          "QUIC vs TCP/TLS")
            
#             with col3:
#                 efficiency_ratio = metrics['comparison'].get('efficiency_ratio', 1)
#                 st.metric("Efficiency Ratio", f"{efficiency_ratio:.2f}x",
#                          "QUIC vs TCP/TLS")
        
#         # Real-time Metrics Header
#         st.subheader("📊 Real-time Performance Metrics")
#         self._display_advanced_metrics_header(metrics)
        
#         # Main Analysis Tabs
#         st.subheader("📈 Detailed Protocol Analysis")
#         main_tabs = st.tabs([
#             "🚀 Performance Overview", 
#             "📊 Statistical Analysis", 
#             "🌐 Network Quality", 
#             "🔍 Traffic Composition",
#             "📋 Detailed Metrics"
#         ])
        
#         with main_tabs[0]:
#             self._create_performance_overview_tab(metrics, quic_df, tcp_df)
        
#         with main_tabs[1]:
#             self._create_statistical_analysis_tab(metrics, quic_df, tcp_df)
        
#         with main_tabs[2]:
#             self._create_network_quality_tab(metrics)
        
#         with main_tabs[3]:
#             self._create_traffic_composition_tab(quic_df, tcp_df)
        
#         with main_tabs[4]:
#             self._create_detailed_metrics_tab(metrics)
        
#         # Trends (if available)
#         trends = analyzer.get_traffic_trends()
#         if trends:
#             st.subheader("📅 Performance Trends")
#             self._display_trend_indicators(trends)

#     def _create_performance_overview_tab(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Create performance overview tab"""
#         st.subheader("🚀 Performance Overview")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Throughput Analysis
#             self._plot_advanced_throughput_analysis(metrics)
        
#         with col2:
#             # Efficiency Breakdown
#             self._plot_efficiency_breakdown(metrics)
        
#         # Traffic Patterns
#         st.subheader("📈 Traffic Patterns")
#         self._plot_traffic_pattern_analysis(quic_df, tcp_df)
        
#         # Connection Analysis
#         st.subheader("🔗 Connection Analysis")
#         self._plot_connection_analysis(metrics, quic_df, tcp_df, "overview_connection")

#     def _create_statistical_analysis_tab(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Create statistical analysis tab"""
#         st.subheader("📊 Statistical Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Packet Size Distribution
#             self._plot_packet_size_distribution(quic_df, tcp_df)
        
#         with col2:
#             # Timing Analysis
#             self._plot_timing_analysis(metrics)
        
#         # Additional Statistical Charts
#         st.subheader("📈 Distribution Analysis")
#         col3, col4 = st.columns(2)
        
#         with col3:
#             # Traffic Volume Distribution
#             self._plot_traffic_volume_distribution(quic_df, tcp_df)
        
#         with col4:
#             # Interval Analysis
#             self._plot_interval_analysis(quic_df, tcp_df)

#     def _create_network_quality_tab(self, metrics: Dict[str, Any]):
#         """Create network quality indicators tab"""
#         st.subheader("🌐 Network Quality Indicators")
        
#         # Main quality indicators
#         self._plot_network_quality_indicators(metrics)
        
#         # Detailed quality metrics
#         st.subheader("📊 Detailed Quality Metrics")
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Stability Metrics
#             self._plot_stability_metrics(metrics)
        
#         with col2:
#             # Performance Consistency
#             self._plot_performance_consistency(metrics)

#     def _create_traffic_composition_tab(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Create traffic composition analysis tab"""
#         st.subheader("🔍 Traffic Composition Analysis")
        
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Protocol distribution
#             self._plot_traffic_composition(quic_df, tcp_df)
        
#         with col2:
#             # Port distribution
#             self._plot_port_distribution(quic_df, tcp_df)
        
#         # Additional composition analysis
#         st.subheader("📦 Packet Characteristics")
#         col3, col4 = st.columns(2)
        
#         with col3:
#             # Size categories
#             self._plot_packet_size_categories(quic_df, tcp_df)
        
#         with col4:
#             # Traffic flow patterns
#             self._plot_traffic_flow_patterns(quic_df, tcp_df)

#     def _create_detailed_metrics_tab(self, metrics: Dict[str, Any]):
#         """Create detailed metrics table tab"""
#         st.subheader("📋 Comprehensive Metrics Table")
#         self._show_advanced_metrics_table(metrics)

#     def _display_advanced_metrics_header(self, metrics: Dict[str, Any]):
#         """Display advanced metrics header with more indicators"""
#         col1, col2, col3, col4, col5 = st.columns(5)
        
#         with col1:
#             if 'QUIC' in metrics:
#                 st.metric(
#                     "QUIC Throughput", 
#                     f"{metrics['QUIC']['throughput_mbps']:.2f} Mbps",
#                     f"{metrics['QUIC']['packet_count']} packets"
#                 )
        
#         with col2:
#             if 'TCP/TLS' in metrics:
#                 st.metric(
#                     "TCP/TLS Throughput",
#                     f"{metrics['TCP/TLS']['throughput_mbps']:.2f} Mbps", 
#                     f"{metrics['TCP/TLS']['packet_count']} packets"
#                 )
                
#         with col3:
#             if 'QUIC' in metrics:
#                 st.metric(
#                     "QUIC Goodput",
#                     f"{metrics['QUIC']['goodput_estimate']:.2f} Mbps",
#                     f"{metrics['QUIC']['efficiency_ratio']:.1f} bytes/pkt"
#                 )
                
#         with col4:
#             if 'TCP/TLS' in metrics:
#                 st.metric(
#                     "TCP/TLS Goodput", 
#                     f"{metrics['TCP/TLS']['goodput_estimate']:.2f} Mbps",
#                     f"{metrics['TCP/TLS']['efficiency_ratio']:.1f} bytes/pkt"
#                 )
        
#         with col5:
#             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
#                 jitter_ratio = metrics['comparison'].get('jitter_ratio', 1)
#                 st.metric(
#                     "Jitter Ratio",
#                     f"{jitter_ratio:.2f}x",
#                     "Lower is better"
#                 )

#     def _plot_advanced_throughput_analysis(self, metrics: Dict[str, Any]):
#         """Plot advanced throughput analysis"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             st.info("No data available for throughput analysis")
#             return
            
#         fig = make_subplots(
#             rows=2, cols=2,
#             subplot_titles=('Total Throughput', 'Goodput Comparison', 
#                           'Packet Rate', 'Efficiency Ratio'),
#             specs=[[{"secondary_y": False}, {"secondary_y": False}],
#                    [{"secondary_y": False}, {"secondary_y": False}]]
#         )
        
#         protocols = ['QUIC', 'TCP/TLS']
        
#         # Total Throughput
#         throughputs = [metrics[p]['throughput_mbps'] for p in protocols]
#         fig.add_trace(
#             go.Bar(x=protocols, y=throughputs, name='Throughput',
#                   marker_color=[self.colors[p] for p in protocols]),
#             row=1, col=1
#         )
        
#         # Goodput Comparison
#         goodputs = [metrics[p]['goodput_estimate'] for p in protocols]
#         fig.add_trace(
#             go.Bar(x=protocols, y=goodputs, name='Goodput',
#                   marker_color=[self.light_colors[p] for p in protocols]),
#             row=1, col=2
#         )
        
#         # Packet Rate
#         packet_rates = [metrics[p]['packets_per_second'] for p in protocols]
#         fig.add_trace(
#             go.Bar(x=protocols, y=packet_rates, name='Packets/s',
#                   marker_color=[self.colors[p] for p in protocols]),
#             row=2, col=1
#         )
        
#         # Efficiency
#         efficiencies = [metrics[p]['efficiency_ratio'] for p in protocols]
#         fig.add_trace(
#             go.Bar(x=protocols, y=efficiencies, name='Efficiency',
#                   marker_color=[self.light_colors[p] for p in protocols]),
#             row=2, col=2
#         )
        
#         fig.update_layout(height=500, showlegend=False, title_text="Throughput Analysis")
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("throughput_analysis"))

#     def _plot_efficiency_breakdown(self, metrics: Dict[str, Any]):
#         """Plot detailed efficiency breakdown"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             st.info("No data available for efficiency analysis")
#             return
            
#         fig = go.Figure()
        
#         efficiency_metrics = ['efficiency_ratio', 'goodput_estimate', 'overhead_estimate', 'compression_efficiency']
#         metric_names = ['Bytes/Packet', 'Goodput (Mbps)', 'Overhead %', 'Compression %']
        
#         for i, (metric, name) in enumerate(zip(efficiency_metrics, metric_names)):
#             fig.add_trace(go.Bar(
#                 name=name,
#                 x=['QUIC', 'TCP/TLS'],
#                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
#                 marker_color=[self.colors['QUIC'] if i % 2 == 0 else self.light_colors['QUIC'],
#                             self.colors['TCP/TLS'] if i % 2 == 0 else self.light_colors['TCP/TLS']]
#             ))
        
#         fig.update_layout(
#             title='Efficiency Metrics Breakdown',
#             barmode='group',
#             height=400
#         )
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("efficiency_breakdown"))

#     def _plot_traffic_pattern_analysis(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Analyze and plot traffic patterns"""
#         if quic_df.empty and tcp_df.empty:
#             st.info("No traffic data for pattern analysis")
#             return
            
#         fig = make_subplots(
#             rows=2, cols=2,
#             subplot_titles=('Traffic Volume Over Time', 'Cumulative Bytes',
#                           'Packet Size Distribution', 'Size Variation'),
#             specs=[[{"secondary_y": False}, {"secondary_y": False}],
#                    [{"secondary_y": False}, {"secondary_y": False}]]
#         )
        
#         # Ensure timestamps are properly converted
#         if not quic_df.empty:
#             quic_df = quic_df.copy()
#             quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
#             quic_df = quic_df.sort_values('timestamp')
#             quic_df['time_elapsed'] = (quic_df['timestamp'] - quic_df['timestamp'].min()).dt.total_seconds()
            
#             # Traffic Volume Over Time
#             fig.add_trace(
#                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['length'],
#                           name='QUIC Packet Size', line=dict(color=self.colors['QUIC'])),
#                 row=1, col=1
#             )
            
#             # Cumulative Bytes
#             quic_df['cumulative_bytes'] = quic_df['length'].cumsum()
#             fig.add_trace(
#                 go.Scatter(x=quic_df['time_elapsed'], y=quic_df['cumulative_bytes'],
#                           name='QUIC Cumulative', line=dict(color=self.colors['QUIC'])),
#                 row=1, col=2
#             )
        
#         if not tcp_df.empty:
#             tcp_df = tcp_df.copy()
#             tcp_df['timestamp'] = pd.to_datetime(tcp_df['timestamp'])
#             tcp_df = tcp_df.sort_values('timestamp')
#             tcp_df['time_elapsed'] = (tcp_df['timestamp'] - tcp_df['timestamp'].min()).dt.total_seconds()
            
#             # Traffic Volume Over Time
#             fig.add_trace(
#                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['length'],
#                           name='TCP Packet Size', line=dict(color=self.colors['TCP/TLS'])),
#                 row=1, col=1
#             )
            
#             # Cumulative Bytes
#             tcp_df['cumulative_bytes'] = tcp_df['length'].cumsum()
#             fig.add_trace(
#                 go.Scatter(x=tcp_df['time_elapsed'], y=tcp_df['cumulative_bytes'],
#                           name='TCP Cumulative', line=dict(color=self.colors['TCP/TLS'])),
#                 row=1, col=2
#             )
        
#         # Packet Size Distribution (Histogram)
#         if not quic_df.empty:
#             fig.add_trace(
#                 go.Histogram(x=quic_df['length'], name='QUIC Sizes',
#                             marker_color=self.colors['QUIC'], opacity=0.7),
#                 row=2, col=1
#             )
        
#         if not tcp_df.empty:
#             fig.add_trace(
#                 go.Histogram(x=tcp_df['length'], name='TCP Sizes',
#                             marker_color=self.colors['TCP/TLS'], opacity=0.7),
#                 row=2, col=1
#             )
        
#         # Size Variation (Coefficient of Variation)
#         size_variation_values = [0.5, 0.3]  # Default values
#         if not quic_df.empty and not tcp_df.empty:
#             quic_variation = quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
#             tcp_variation = tcp_df['length'].std() / tcp_df['length'].mean() if tcp_df['length'].mean() > 0 else 0
#             size_variation_values = [quic_variation, tcp_variation]
        
#         fig.add_trace(
#             go.Bar(x=['QUIC', 'TCP/TLS'], y=size_variation_values, 
#                    name='Size Variation', marker_color=[self.colors['QUIC'], self.colors['TCP/TLS']]),
#             row=2, col=2
#         )
        
#         fig.update_layout(height=600, showlegend=True, title_text="Traffic Pattern Analysis")
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("traffic_patterns"))

#     def _plot_connection_analysis(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_df: pd.DataFrame, key_suffix=""):
#         """Plot connection and network analysis"""
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Connection Diversity
#             if 'QUIC' in metrics and 'TCP/TLS' in metrics:
#                 fig = go.Figure()
#                 categories = ['Sources', 'Destinations', 'Ports']
#                 quic_values = [metrics['QUIC']['unique_sources'], 
#                               metrics['QUIC']['unique_destinations'],
#                               metrics['QUIC']['port_diversity']]
#                 tcp_values = [metrics['TCP/TLS']['unique_sources'],
#                              metrics['TCP/TLS']['unique_destinations'],
#                              metrics['TCP/TLS']['port_diversity']]
                
#                 fig.add_trace(go.Bar(name='QUIC', x=categories, y=quic_values,
#                                     marker_color=self.colors['QUIC']))
#                 fig.add_trace(go.Bar(name='TCP/TLS', x=categories, y=tcp_values,
#                                     marker_color=self.colors['TCP/TLS']))
                
#                 fig.update_layout(title='Connection Diversity', barmode='group', height=300)
#                 st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key(f"connection_diversity_{key_suffix}"))
#             else:
#                 st.info("No connection data available")
        
#         with col2:
#             # Port Distribution
#             if not quic_df.empty or not tcp_df.empty:
#                 fig = go.Figure()
                
#                 if not quic_df.empty:
#                     port_counts = quic_df['dst_port'].value_counts().head(10)
#                     fig.add_trace(go.Bar(
#                         x=port_counts.index.astype(str), y=port_counts.values,
#                         name='QUIC Ports', marker_color=self.colors['QUIC']
#                     ))
                
#                 if not tcp_df.empty:
#                     port_counts = tcp_df['dst_port'].value_counts().head(10)
#                     fig.add_trace(go.Bar(
#                         x=port_counts.index.astype(str), y=port_counts.values,
#                         name='TCP Ports', marker_color=self.colors['TCP/TLS']
#                     ))
                
#                 fig.update_layout(title='Top Destination Ports', height=300)
#                 st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key(f"port_distribution_{key_suffix}"))
#             else:
#                 st.info("No port data available")

#     def _plot_packet_size_distribution(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot detailed packet size distribution"""
#         if quic_df.empty and tcp_df.empty:
#             st.info("No data for packet size distribution")
#             return
            
#         fig = go.Figure()
        
#         if not quic_df.empty:
#             fig.add_trace(go.Box(
#                 y=quic_df['length'], name='QUIC Packet Sizes',
#                 marker_color=self.colors['QUIC']
#             ))
        
#         if not tcp_df.empty:
#             fig.add_trace(go.Box(
#                 y=tcp_df['length'], name='TCP Packet Sizes', 
#                 marker_color=self.colors['TCP/TLS']
#             ))
        
#         fig.update_layout(
#             title='Packet Size Distribution (Box Plot)',
#             yaxis_title='Packet Size (bytes)',
#             height=400
#         )
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("packet_size_box"))

#     def _plot_timing_analysis(self, metrics: Dict[str, Any]):
#         """Plot timing and jitter analysis"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             st.info("No data for timing analysis")
#             return
            
#         fig = go.Figure()
        
#         timing_metrics = ['avg_interval_ms', 'jitter_ms', 'min_interval_ms', 'max_interval_ms']
#         metric_names = ['Avg Interval', 'Jitter', 'Min Interval', 'Max Interval']
        
#         for metric, name in zip(timing_metrics, metric_names):
#             fig.add_trace(go.Bar(
#                 name=name,
#                 x=['QUIC', 'TCP/TLS'],
#                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
#                 text=[f"{metrics['QUIC'].get(metric, 0):.1f}", f"{metrics['TCP/TLS'].get(metric, 0):.1f}"],
#                 textposition='auto'
#             ))
        
#         fig.update_layout(
#             title='Timing Analysis (ms)',
#             barmode='group',
#             height=400
#         )
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("timing_analysis"))

#     def _plot_network_quality_indicators(self, metrics: Dict[str, Any]):
#         """Plot network quality indicators"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             st.info("No data for network quality analysis")
#             return
            
#         st.subheader("📊 Quality Metrics")
        
#         col1, col2, col3, col4 = st.columns(4)
        
#         with col1:
#             # Jitter indicator
#             quic_jitter = metrics['QUIC'].get('jitter_ms', 0)
#             tcp_jitter = metrics['TCP/TLS'].get('jitter_ms', 100)
#             st.metric("QUIC Jitter", f"{quic_jitter:.1f}ms", 
#                      "Lower is better" if quic_jitter < tcp_jitter else "Higher than TCP")
        
#         with col2:
#             # Burstiness indicator
#             quic_burst = metrics['QUIC'].get('burstiness', 0)
#             st.metric("QUIC Burstiness", f"{quic_burst:.3f}",
#                      "Closer to 0 is better")
        
#         with col3:
#             # Overhead indicator
#             quic_overhead = metrics['QUIC'].get('overhead_estimate', 0)
#             st.metric("QUIC Overhead", f"{quic_overhead:.1f}%",
#                      "Lower is better")
        
#         with col4:
#             # Stability indicator
#             quic_stability = 100 - min(100, metrics['QUIC'].get('traffic_volume_variation', 1) * 100)
#             st.metric("QUIC Stability", f"{quic_stability:.1f}%",
#                      "Higher is better")
        
#         # Additional quality charts
#         st.subheader("📈 Quality Comparison")
#         self._plot_quality_comparison(metrics)

#     def _plot_traffic_composition(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot traffic composition analysis"""
#         if quic_df.empty and tcp_df.empty:
#             st.info("No data for traffic composition")
#             return
            
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Protocol distribution pie chart
#             labels = ['QUIC', 'TCP/TLS']
#             values = [len(quic_df), len(tcp_df)]
            
#             fig = px.pie(values=values, names=labels, 
#                         title='Protocol Distribution by Packet Count',
#                         color=labels, color_discrete_map=self.colors)
#             st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("protocol_distribution"))
        
#         with col2:
#             # Data volume distribution
#             labels = ['QUIC', 'TCP/TLS']
#             values = [quic_df['length'].sum() if not quic_df.empty else 0,
#                      tcp_df['length'].sum() if not tcp_df.empty else 0]
            
#             fig = px.pie(values=values, names=labels,
#                         title='Data Volume Distribution by Protocol',
#                         color=labels, color_discrete_map=self.colors)
#             st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("data_volume_distribution"))

#     # Additional methods for new tab content
#     def _plot_traffic_volume_distribution(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot traffic volume distribution"""
#         if quic_df.empty and tcp_df.empty:
#             return
            
#         fig = go.Figure()
        
#         if not quic_df.empty:
#             fig.add_trace(go.Violin(y=quic_df['length'], name='QUIC', 
#                                   box_visible=True, meanline_visible=True,
#                                   marker_color=self.colors['QUIC']))
        
#         if not tcp_df.empty:
#             fig.add_trace(go.Violin(y=tcp_df['length'], name='TCP/TLS',
#                                   box_visible=True, meanline_visible=True,
#                                   marker_color=self.colors['TCP/TLS']))
        
#         fig.update_layout(title='Traffic Volume Distribution', height=300)
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("traffic_volume_violin"))

#     def _plot_interval_analysis(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot interval analysis"""
#         # Placeholder for interval analysis
#         st.info("Interval analysis would show packet arrival patterns")
#         # This would require timestamp analysis which is already covered in other charts

#     def _plot_stability_metrics(self, metrics: Dict[str, Any]):
#         """Plot stability metrics"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             return
            
#         stability_data = {
#             'Metric': ['Jitter', 'Burstiness', 'Stability', 'Consistency'],
#             'QUIC': [
#                 metrics['QUIC'].get('jitter_ms', 0),
#                 metrics['QUIC'].get('burstiness', 0),
#                 100 - min(100, metrics['QUIC'].get('traffic_volume_variation', 1) * 100),
#                 95  # Placeholder
#             ],
#             'TCP/TLS': [
#                 metrics['TCP/TLS'].get('jitter_ms', 0),
#                 metrics['TCP/TLS'].get('burstiness', 0),
#                 100 - min(100, metrics['TCP/TLS'].get('traffic_volume_variation', 1) * 100),
#                 85  # Placeholder
#             ]
#         }
        
#         df = pd.DataFrame(stability_data)
#         st.dataframe(df, use_container_width=True, key=self._get_unique_key("stability_table"))

#     def _plot_performance_consistency(self, metrics: Dict[str, Any]):
#         """Plot performance consistency"""
#         # Placeholder for performance consistency chart
#         fig = go.Figure()
#         fig.add_trace(go.Indicator(
#             mode = "gauge+number",
#             value = 85,
#             title = {'text': "Performance Consistency"},
#             gauge = {'axis': {'range': [None, 100]}}
#         ))
#         fig.update_layout(height=250)
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("consistency_gauge"))

#     def _plot_port_distribution(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot port distribution analysis"""
#         # Create a unique port distribution chart
#         if not quic_df.empty or not tcp_df.empty:
#             fig = go.Figure()
            
#             if not quic_df.empty:
#                 port_counts = quic_df['dst_port'].value_counts().head(8)
#                 fig.add_trace(go.Bar(
#                     x=port_counts.index.astype(str), y=port_counts.values,
#                     name='QUIC Ports', marker_color=self.colors['QUIC']
#                 ))
            
#             if not tcp_df.empty:
#                 port_counts = tcp_df['dst_port'].value_counts().head(8)
#                 fig.add_trace(go.Bar(
#                     x=port_counts.index.astype(str), y=port_counts.values,
#                     name='TCP Ports', marker_color=self.colors['TCP/TLS']
#                 ))
            
#             fig.update_layout(title='Destination Port Distribution', height=300)
#             st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("composition_port_distribution"))

#     def _plot_packet_size_categories(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot packet size categories"""
#         if quic_df.empty and tcp_df.empty:
#             return
            
#         # Define size categories
#         size_bins = [0, 100, 500, 1000, 1500, float('inf')]
#         size_labels = ['Tiny (<100)', 'Small (100-500)', 'Medium (500-1000)', 'Large (1000-1500)', 'Huge (1500+)']
        
#         fig = go.Figure()
        
#         if not quic_df.empty:
#             quic_categories = pd.cut(quic_df['length'], bins=size_bins, labels=size_labels)
#             quic_counts = quic_categories.value_counts()
#             fig.add_trace(go.Bar(name='QUIC', x=quic_counts.index, y=quic_counts.values,
#                                marker_color=self.colors['QUIC']))
        
#         if not tcp_df.empty:
#             tcp_categories = pd.cut(tcp_df['length'], bins=size_bins, labels=size_labels)
#             tcp_counts = tcp_categories.value_counts()
#             fig.add_trace(go.Bar(name='TCP/TLS', x=tcp_counts.index, y=tcp_counts.values,
#                                marker_color=self.colors['TCP/TLS']))
        
#         fig.update_layout(title='Packet Size Categories', barmode='group', height=300)
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("size_categories"))

#     def _plot_traffic_flow_patterns(self, quic_df: pd.DataFrame, tcp_df: pd.DataFrame):
#         """Plot traffic flow patterns"""
#         # Placeholder for traffic flow analysis
#         st.info("Traffic flow patterns analysis would show communication patterns between sources and destinations")

#     def _plot_quality_comparison(self, metrics: Dict[str, Any]):
#         """Plot quality comparison between protocols"""
#         if 'QUIC' not in metrics or 'TCP/TLS' not in metrics:
#             return
            
#         quality_metrics = ['jitter_ms', 'burstiness', 'overhead_estimate']
#         metric_names = ['Jitter (ms)', 'Burstiness', 'Overhead (%)']
        
#         fig = go.Figure()
        
#         for i, (metric, name) in enumerate(zip(quality_metrics, metric_names)):
#             fig.add_trace(go.Bar(
#                 name=name,
#                 x=['QUIC', 'TCP/TLS'],
#                 y=[metrics['QUIC'].get(metric, 0), metrics['TCP/TLS'].get(metric, 0)],
#                 marker_color=[self.colors['QUIC'], self.colors['TCP/TLS']]
#             ))
        
#         fig.update_layout(title='Quality Metrics Comparison', barmode='group', height=300)
#         st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("quality_comparison"))

#     def _show_advanced_metrics_table(self, metrics: Dict[str, Any]):
#         """Display comprehensive metrics table"""
#         if not metrics:
#             st.info("No metrics data available")
#             return
            
#         # Create detailed comparison table
#         comparison_data = []
#         metrics_to_show = {
#             'Throughput (Mbps)': 'throughput_mbps',
#             'Goodput (Mbps)': 'goodput_estimate', 
#             'Packet Count': 'packet_count',
#             'Avg Packet Size': 'avg_packet_size',
#             'Packets/s': 'packets_per_second',
#             'Unique Sources': 'unique_sources',
#             'Unique Destinations': 'unique_destinations',
#             'Port Diversity': 'port_diversity',
#             'Avg Interval (ms)': 'avg_interval_ms',
#             'Jitter (ms)': 'jitter_ms',
#             'Efficiency': 'efficiency_ratio',
#             'Overhead %': 'overhead_estimate',
#             'Burstiness': 'burstiness'
#         }
        
#         for display_name, metric_key in metrics_to_show.items():
#             row = {'Metric': display_name}
#             for protocol in ['QUIC', 'TCP/TLS']:
#                 if protocol in metrics:
#                     row[protocol] = metrics[protocol].get(metric_key, 0)
#             comparison_data.append(row)
        
#         if comparison_data:
#             df = pd.DataFrame(comparison_data)
#             st.dataframe(df.style.format({
#                 'QUIC': '{:.2f}',
#                 'TCP/TLS': '{:.2f}'
#             }), use_container_width=True, height=400, key=self._get_unique_key("metrics_table"))

#     def _display_trend_indicators(self, trends: Dict[str, Any]):
#         """Display trend indicators"""
#         col1, col2, col3, col4 = st.columns(4)
        
#         for protocol in ['QUIC', 'TCP/TLS']:
#             if protocol in trends:
#                 trend = trends[protocol]
#                 if protocol == 'QUIC':
#                     with col1:
#                         st.metric(f"{protocol} Throughput Trend", 
#                                  trend['throughput_trend'],
#                                  f"{trend['throughput_change']:+.1f}%")
#                     with col2:
#                         st.metric(f"{protocol} Packet Trend",
#                                  trend['packet_count_trend'],
#                                  "Volume change")
#                 else:
#                     with col3:
#                         st.metric(f"{protocol} Throughput Trend",
#                                  trend['throughput_trend'],
#                                  f"{trend['throughput_change']:+.1f}%")
#                     with col4:
#                         st.metric(f"{protocol} Efficiency Trend",
#                                  trend['efficiency_trend'],
#                                  "Efficiency change")

# def run_packet_capture(duration: int = 30, interface: str = "en0") -> Optional[Dict]:
#     """Execute packet capture service with sudo privileges"""
#     try:
#         # Get current directory
#         current_dir = os.path.dirname(os.path.abspath(__file__))
#         capture_script = os.path.join(current_dir, "packet_capture_service.py")
        
#         # Ensure the script is executable
#         if not os.access(capture_script, os.X_OK):
#             os.chmod(capture_script, 0o755)
        
#         # Run capture with sudo
#         result = subprocess.run(
#             ['sudo', 'python3', capture_script, str(duration), interface],
#             capture_output=True,
#             text=True,
#             timeout=duration + 10
#         )
        
#         if result.returncode == 0:
#             return json.loads(result.stdout)
#         else:
#             st.error(f"Capture service error: {result.stderr}")
#             return None
            
#     except subprocess.TimeoutExpired:
#         st.error("Packet capture timed out. Try a shorter duration.")
#         return None
#     except json.JSONDecodeError as e:
#         st.error(f"Failed to parse capture results: {e}")
#         return None
#     except Exception as e:
#         st.error(f"Error running capture: {e}")
#         return None

# def main():
#     # Page configuration
#     st.set_page_config(
#         page_title="QUIC Protocol Analyzer Pro",
#         page_icon="🔄",
#         layout="wide",
#         initial_sidebar_state="expanded"
#     )
    
#     st.title("🔄 Advanced QUIC vs TCP/TLS Protocol Analyzer Pro")
    
#     # Initialize session state
#     if 'capture_data' not in st.session_state:
#         st.session_state.capture_data = None
#     if 'analysis_results' not in st.session_state:
#         st.session_state.analysis_results = None
#     if 'analyzer' not in st.session_state:
#         st.session_state.analyzer = AdvancedPacketAnalyzer()
    
#     # Sidebar controls
#     st.sidebar.title("🎛️ Capture Controls")
    
#     # Interface selection - dynamically detected
#     interfaces = get_available_interfaces()
#     selected_interface = st.sidebar.selectbox(
#         "Network Interface",
#         interfaces,
#         help="Select the network interface to monitor"
#     )
    
#     # Show interface info
#     st.sidebar.info(f"📡 Selected: {selected_interface}")
    
#     # Capture duration
#     capture_duration = st.sidebar.slider(
#         "Capture Duration (seconds)",
#         min_value=10,
#         max_value=120,
#         value=30,
#         step=5,
#         help="How long to capture packets"
#     )
    
#     # Control buttons
#     col1, col2 = st.sidebar.columns(2)
    
#     with col1:
#         if st.button("🚀 Start Capture", type="primary"):
#             with st.spinner(f"Capturing packets for {capture_duration} seconds..."):
#                 capture_data = run_packet_capture(capture_duration, selected_interface)
                
#                 if capture_data and 'error' not in capture_data:
#                     st.session_state.capture_data = capture_data
                    
#                     # Analyze packets
#                     analyzer = st.session_state.analyzer
#                     quic_df = pd.DataFrame(capture_data.get('quic_packets', []))
#                     tcp_df = pd.DataFrame(capture_data.get('tcp_packets', []))
                    
#                     analysis_results = analyzer.calculate_comprehensive_metrics(quic_df, tcp_df)
#                     st.session_state.analysis_results = (analysis_results, quic_df, tcp_df)
                    
#                     st.success(f"Capture completed! Got {len(quic_df)} QUIC and {len(tcp_df)} TCP packets")
#                 else:
#                     st.error("Capture failed. Check permissions and interface.")
    
#     with col2:
#         if st.button("🔄 Clear Results"):
#             st.session_state.capture_data = None
#             st.session_state.analysis_results = None
#             st.rerun()
    
#     # Display results if available
#     if st.session_state.analysis_results:
#         analysis_results, quic_df, tcp_df = st.session_state.analysis_results
#         visualizer = AdvancedVisualizer()
#         visualizer.create_comprehensive_dashboard(analysis_results, quic_df, tcp_df, st.session_state.analyzer)
        
#         # Raw data view
#         with st.expander("📋 View Raw Packet Data"):
#             tab1, tab2 = st.tabs(["QUIC Packets", "TCP/TLS Packets"])
            
#             with tab1:
#                 if not quic_df.empty:
#                     st.dataframe(quic_df, use_container_width=True)
#                 else:
#                     st.info("No QUIC packets captured")
            
#             with tab2:
#                 if not tcp_df.empty:
#                     st.dataframe(tcp_df, use_container_width=True)
#                 else:
#                     st.info("No TCP/TLS packets captured")
    
#     else:
#         # Enhanced welcome screen
#         st.markdown("""
#         ## 🚀 Welcome to QUIC Protocol Analyzer Pro
        
#         This advanced tool provides comprehensive real-time analysis and comparison of:
#         - **QUIC** (Quick UDP Internet Connections) 
#         - **TCP/TLS** (Traditional encrypted transport)
        
#         ### 🏗️ Organized Analysis Tabs:
        
#         **🚀 Performance Overview**
#         - Throughput and efficiency analysis
#         - Traffic patterns and connection analysis
#         - Real-time performance metrics
        
#         **📊 Statistical Analysis** 
#         - Packet size distributions
#         - Timing and interval analysis
#         - Advanced statistical metrics
        
#         **🌐 Network Quality**
#         - Jitter and stability indicators
#         - Quality metrics comparison
#         - Performance consistency
        
#         **🔍 Traffic Composition**
#         - Protocol distribution analysis
#         - Port and packet characteristics
#         - Traffic flow patterns
        
#         **📋 Detailed Metrics**
#         - Comprehensive metrics table
#         - Protocol comparison data
#         - All calculated parameters
        
#         ### 🚀 Quick Start:
#         1. Select your network interface above
#         2. Set capture duration (10-120 seconds)
#         3. Click **Start Capture** to begin
#         4. Generate web traffic during capture for best results
#         5. Explore different analysis tabs for detailed insights
        
#         ### 🔧 Requirements:
#         - macOS/Linux with Python 3.8+
#         - Sudo/root privileges for packet capture
#         - Active network traffic on selected interface
#         """)
        
#         # Interface detection info
#         st.sidebar.info(f"🔍 Detected interfaces: {', '.join(interfaces)}")
        
#         # Demo data option
#         if st.button("🎮 Load Advanced Demo Data", type="secondary"):
#             # Create comprehensive demo data
#             demo_analysis = {
#                 'QUIC': {
#                     'packet_count': 150,
#                     'total_bytes': 187500,
#                     'avg_packet_size': 1250,
#                     'std_packet_size': 150,
#                     'throughput_mbps': 1.5,
#                     'packets_per_second': 5.0,
#                     'unique_sources': 3,
#                     'unique_destinations': 5,
#                     'port_diversity': 8,
#                     'avg_interval_ms': 12.5,
#                     'jitter_ms': 2.1,
#                     'min_interval_ms': 8.2,
#                     'max_interval_ms': 25.7,
#                     'burstiness': 0.15,
#                     'traffic_volume_variation': 0.12,
#                     'efficiency_ratio': 1250.0,
#                     'goodput_estimate': 1.2,
#                     'overhead_estimate': 4.0,
#                     'compression_efficiency': 65.0,
#                     'common_ports': {443: 120, 80: 30}
#                 },
#                 'TCP/TLS': {
#                     'packet_count': 200, 
#                     'total_bytes': 240000,
#                     'avg_packet_size': 1200,
#                     'std_packet_size': 180,
#                     'throughput_mbps': 1.92,
#                     'packets_per_second': 6.67,
#                     'unique_sources': 4,
#                     'unique_destinations': 6,
#                     'port_diversity': 10,
#                     'avg_interval_ms': 15.2,
#                     'jitter_ms': 3.4,
#                     'min_interval_ms': 10.1,
#                     'max_interval_ms': 32.8,
#                     'burstiness': 0.22,
#                     'traffic_volume_variation': 0.15,
#                     'efficiency_ratio': 1200.0,
#                     'goodput_estimate': 1.5,
#                     'overhead_estimate': 6.7,
#                     'compression_efficiency': 58.0,
#                     'common_ports': {443: 180, 80: 20}
#                 },
#                 'comparison': {
#                     'throughput_ratio': 0.78,
#                     'packet_size_ratio': 1.04,
#                     'efficiency_ratio': 1.04,
#                     'jitter_ratio': 0.62,
#                     'performance_score': 72.5
#                 }
#             }
            
#             st.session_state.analysis_results = (demo_analysis, pd.DataFrame(), pd.DataFrame())
#             st.rerun()

#     # Enhanced footer
#     st.sidebar.markdown("---")
#     st.sidebar.info(
#         "💡 **Pro Tip**: Use **en0** (WiFi) and browse HTTPS sites "
#         "during capture to generate QUIC traffic. Explore different tabs for specialized analysis."
#     )

# if __name__ == "__main__":
#     main()

import streamlit as st
import pandas as pd
import subprocess
import json
import os
import tempfile
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from typing import Dict, Any, Tuple, Optional
import time
import scapy.all as scapy

class AdvancedPacketAnalyzer:
    def __init__(self):
        self.metrics_history = []
        self.traffic_patterns = []
        
    def calculate_comprehensive_metrics(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame) -> Dict[str, Any]:
        """Calculate comprehensive metrics for all three protocols"""
        metrics = {}
        
        # QUIC Metrics
        if not quic_df.empty:
            quic_df = quic_df.copy()
            # Ensure timestamp conversion
            quic_df['timestamp'] = pd.to_datetime(quic_df['timestamp'])
            quic_df = quic_df.sort_values('timestamp')
            
            # Basic metrics
            metrics['QUIC'] = {
                'packet_count': len(quic_df),
                'total_bytes': quic_df['length'].sum(),
                'avg_packet_size': quic_df['length'].mean(),
                'std_packet_size': quic_df['length'].std(),
                'throughput_mbps': (quic_df['length'].sum() * 8) / 1e6,
                'packets_per_second': len(quic_df) / max(1, (quic_df['timestamp'].max() - quic_df['timestamp'].min()).total_seconds()),
                'unique_sources': quic_df['src_ip'].nunique(),
                'unique_destinations': quic_df['dst_ip'].nunique(),
                'port_diversity': quic_df['dst_port'].nunique(),
                'common_ports': quic_df['dst_port'].value_counts().head(5).to_dict()
            }
            
            # Advanced timing metrics
            if len(quic_df) > 1:
                time_diffs = quic_df['timestamp'].diff().dt.total_seconds().dropna()
                metrics['QUIC'].update({
                    'avg_interval_ms': time_diffs.mean() * 1000,
                    'jitter_ms': time_diffs.std() * 1000,
                    'min_interval_ms': time_diffs.min() * 1000,
                    'max_interval_ms': time_diffs.max() * 1000,
                    'burstiness': self.calculate_burstiness(time_diffs),
                    'traffic_volume_variation': quic_df['length'].std() / quic_df['length'].mean() if quic_df['length'].mean() > 0 else 0
                })
            
            # Efficiency metrics
            metrics['QUIC'].update({
                'efficiency_ratio': metrics['QUIC']['total_bytes'] / max(1, metrics['QUIC']['packet_count']),
                'goodput_estimate': self.estimate_goodput(quic_df),
                'overhead_estimate': self.estimate_protocol_overhead(quic_df, 'QUIC'),
                'compression_efficiency': self.calculate_compression_efficiency(quic_df)
            })
        
        # TCP/TLS Metrics
        if not tcp_tls_df.empty:
            tcp_tls_df = tcp_tls_df.copy()
            # Ensure timestamp conversion
            tcp_tls_df['timestamp'] = pd.to_datetime(tcp_tls_df['timestamp'])
            tcp_tls_df = tcp_tls_df.sort_values('timestamp')
            
            # Basic metrics
            metrics['TCP/TLS'] = {
                'packet_count': len(tcp_tls_df),
                'total_bytes': tcp_tls_df['length'].sum(),
                'avg_packet_size': tcp_tls_df['length'].mean(),
                'std_packet_size': tcp_tls_df['length'].std(),
                'throughput_mbps': (tcp_tls_df['length'].sum() * 8) / 1e6,
                'packets_per_second': len(tcp_tls_df) / max(1, (tcp_tls_df['timestamp'].max() - tcp_tls_df['timestamp'].min()).total_seconds()),
                'unique_sources': tcp_tls_df['src_ip'].nunique(),
                'unique_destinations': tcp_tls_df['dst_ip'].nunique(),
                'port_diversity': tcp_tls_df['dst_port'].nunique(),
                'common_ports': tcp_tls_df['dst_port'].value_counts().head(5).to_dict()
            }
            
            # Advanced timing metrics
            if len(tcp_tls_df) > 1:
                time_diffs = tcp_tls_df['timestamp'].diff().dt.total_seconds().dropna()
                metrics['TCP/TLS'].update({
                    'avg_interval_ms': time_diffs.mean() * 1000,
                    'jitter_ms': time_diffs.std() * 1000,
                    'min_interval_ms': time_diffs.min() * 1000,
                    'max_interval_ms': time_diffs.max() * 1000,
                    'burstiness': self.calculate_burstiness(time_diffs),
                    'traffic_volume_variation': tcp_tls_df['length'].std() / tcp_tls_df['length'].mean() if tcp_tls_df['length'].mean() > 0 else 0
                })
            
            # Efficiency metrics
            metrics['TCP/TLS'].update({
                'efficiency_ratio': metrics['TCP/TLS']['total_bytes'] / max(1, metrics['TCP/TLS']['packet_count']),
                'goodput_estimate': self.estimate_goodput(tcp_tls_df),
                'overhead_estimate': self.estimate_protocol_overhead(tcp_tls_df, 'TCP/TLS'),
                'compression_efficiency': self.calculate_compression_efficiency(tcp_tls_df)
            })
        
        # HTTPS Metrics
        if not https_df.empty:
            https_df = https_df.copy()
            # Ensure timestamp conversion
            https_df['timestamp'] = pd.to_datetime(https_df['timestamp'])
            https_df = https_df.sort_values('timestamp')
            
            # Basic metrics
            metrics['HTTPS'] = {
                'packet_count': len(https_df),
                'total_bytes': https_df['length'].sum(),
                'avg_packet_size': https_df['length'].mean(),
                'std_packet_size': https_df['length'].std(),
                'throughput_mbps': (https_df['length'].sum() * 8) / 1e6,
                'packets_per_second': len(https_df) / max(1, (https_df['timestamp'].max() - https_df['timestamp'].min()).total_seconds()),
                'unique_sources': https_df['src_ip'].nunique(),
                'unique_destinations': https_df['dst_ip'].nunique(),
                'port_diversity': https_df['dst_port'].nunique(),
                'common_ports': https_df['dst_port'].value_counts().head(5).to_dict()
            }
            
            # Advanced timing metrics
            if len(https_df) > 1:
                time_diffs = https_df['timestamp'].diff().dt.total_seconds().dropna()
                metrics['HTTPS'].update({
                    'avg_interval_ms': time_diffs.mean() * 1000,
                    'jitter_ms': time_diffs.std() * 1000,
                    'min_interval_ms': time_diffs.min() * 1000,
                    'max_interval_ms': time_diffs.max() * 1000,
                    'burstiness': self.calculate_burstiness(time_diffs),
                    'traffic_volume_variation': https_df['length'].std() / https_df['length'].mean() if https_df['length'].mean() > 0 else 0
                })
            
            # Efficiency metrics
            metrics['HTTPS'].update({
                'efficiency_ratio': metrics['HTTPS']['total_bytes'] / max(1, metrics['HTTPS']['packet_count']),
                'goodput_estimate': self.estimate_goodput(https_df),
                'overhead_estimate': self.estimate_protocol_overhead(https_df, 'HTTPS'),
                'compression_efficiency': self.calculate_compression_efficiency(https_df)
            })
        
        # Comparison metrics
        protocols_present = [p for p in ['QUIC', 'TCP/TLS', 'HTTPS'] if p in metrics]
        if len(protocols_present) >= 2:
            # Use TCP/TLS as baseline if available, otherwise use first protocol
            baseline = 'TCP/TLS' if 'TCP/TLS' in metrics else protocols_present[0]
            baseline_tput = metrics[baseline]['throughput_mbps']
            
            comparison_data = {}
            for protocol in protocols_present:
                if protocol != baseline and baseline_tput > 0:
                    comparison_data[f'{protocol}_vs_{baseline}'] = metrics[protocol]['throughput_mbps'] / baseline_tput
            
            metrics['comparison'] = comparison_data
            metrics['comparison']['performance_score'] = self.calculate_performance_score(metrics)
        
        # Store for trend analysis
        self.metrics_history.append({
            'timestamp': datetime.now(),
            'metrics': metrics
        })
        
        return metrics

    def calculate_burstiness(self, intervals):
        """Calculate traffic burstiness (Burstiness Parameter)"""
        if len(intervals) < 2:
            return 0
        mean_interval = np.mean(intervals)
        std_interval = np.std(intervals)
        return (std_interval - mean_interval) / (std_interval + mean_interval) if (std_interval + mean_interval) > 0 else 0

    def estimate_goodput(self, df):
        """Estimate goodput (application layer throughput)"""
        # Simplified: assume larger packets have more application data
        large_packets = df[df['length'] > 100]  # Packets > 100 bytes
        if len(df) > 0:
            return (large_packets['length'].sum() * 8) / 1e6  # Mbps
        return 0

    def estimate_protocol_overhead(self, df, protocol):
        """Estimate protocol overhead"""
        avg_size = df['length'].mean()
        if protocol == 'QUIC':
            estimated_header = 50  # bytes for QUIC
        elif protocol == 'HTTPS':
            estimated_header = 70  # bytes for HTTPS (TCP + TLS headers)
        else:  # TCP/TLS
            estimated_header = 80  # bytes for TCP+TLS
        
        if avg_size > estimated_header:
            return (estimated_header / avg_size) * 100
        return 0

    def calculate_compression_efficiency(self, df):
        """Calculate compression efficiency estimate"""
        # Simplified: ratio of large to small packets
        large_packets = len(df[df['length'] > 500])
        small_packets = len(df[df['length'] <= 100])
        total_packets = len(df)
        
        if total_packets > 0:
            return (large_packets / total_packets) * 100
        return 0

    def calculate_performance_score(self, metrics):
        """Calculate overall performance score (0-100)"""
        score = 0
        max_score = 0
        
        protocols = [p for p in ['QUIC', 'TCP/TLS', 'HTTPS'] if p in metrics]
        if len(protocols) >= 2:
            baseline = 'TCP/TLS' if 'TCP/TLS' in metrics else protocols[0]
            baseline_tput = metrics[baseline]['throughput_mbps']
            
            for protocol in protocols:
                if protocol != baseline and baseline_tput > 0:
                    ratio = metrics[protocol]['throughput_mbps'] / baseline_tput
                    protocol_score = min(100, ratio * 50)
                    score += protocol_score
                    max_score += 50
        
        return min(100, (score / max_score * 100)) if max_score > 0 else 0

    def get_traffic_trends(self, window_minutes=5):
        """Get traffic trends over time"""
        if len(self.metrics_history) < 2:
            return {}
        
        cutoff_time = datetime.now() - timedelta(minutes=window_minutes)
        recent_data = [m for m in self.metrics_history if m['timestamp'] > cutoff_time]
        
        trends = {}
        if len(recent_data) >= 2:
            for protocol in ['QUIC', 'TCP/TLS', 'HTTPS']:
                if protocol in recent_data[0]['metrics']:
                    first = recent_data[0]['metrics'][protocol]
                    last = recent_data[-1]['metrics'][protocol]
                    
                    trends[protocol] = {
                        'throughput_trend': '📈' if last['throughput_mbps'] > first['throughput_mbps'] else '📉',
                        'throughput_change': ((last['throughput_mbps'] - first['throughput_mbps']) / first['throughput_mbps'] * 100) if first['throughput_mbps'] > 0 else 0,
                        'packet_count_trend': '📈' if last['packet_count'] > first['packet_count'] else '📉',
                        'efficiency_trend': '📈' if last['efficiency_ratio'] > first['efficiency_ratio'] else '📉'
                    }
        
        return trends

def get_available_interfaces():
    """Get available network interfaces on the system"""
    try:
        # Get all available interfaces using Scapy
        interfaces = scapy.get_if_list()
        
        # Filter and prioritize common macOS interfaces
        preferred_order = ['en0', 'en1', 'en2', 'en3', 'en4', 'eth0', 'wlan0']
        
        # Sort interfaces by preferred order
        sorted_interfaces = []
        for preferred in preferred_order:
            if preferred in interfaces:
                sorted_interfaces.append(preferred)
        
        # Add any remaining interfaces
        for iface in interfaces:
            if iface not in sorted_interfaces:
                sorted_interfaces.append(iface)
        
        return sorted_interfaces if sorted_interfaces else ['en0']  # Fallback to en0
        
    except Exception as e:
        st.error(f"Error detecting interfaces: {e}")
        # Return common macOS interfaces as fallback
        return ['en0', 'en1', 'en2', 'en3', 'en4']

class AdvancedVisualizer:
    def __init__(self):
        self.colors = {
            'QUIC': '#1f77b4',      # Blue
            'TCP/TLS': '#ff7f0e',   # Orange
            'HTTPS': '#2ca02c'      # Green
        }
        self.light_colors = {
            'QUIC': '#8fc1e3',
            'TCP/TLS': '#ffb366',
            'HTTPS': '#98df8a'
        }
        self.chart_counter = 0
    
    def _get_unique_key(self, prefix="chart"):
        """Generate unique keys for plotly charts"""
        self.chart_counter += 1
        return f"{prefix}_{self.chart_counter}"
    
    def create_comprehensive_dashboard(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame, analyzer: AdvancedPacketAnalyzer):
        """Create comprehensive performance dashboard with organized tabs"""
        
        # Performance Score Card
        st.subheader("🏆 Overall Performance Score")
        if 'comparison' in metrics:
            score = metrics['comparison'].get('performance_score', 0)
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                # Create gauge chart for performance score
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Protocol Performance Score"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "lightyellow"},
                            {'range': [80, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("score_gauge"))
            
            # Show comparison ratios
            protocols_present = [p for p in ['QUIC', 'TCP/TLS', 'HTTPS'] if p in metrics]
            baseline = 'TCP/TLS' if 'TCP/TLS' in protocols_present else protocols_present[0] if protocols_present else 'TCP/TLS'
            
            for i, protocol in enumerate(protocols_present):
                if protocol != baseline:
                    ratio_key = f'{protocol}_vs_{baseline}'
                    ratio = metrics['comparison'].get(ratio_key, 1)
                    if i == 0:
                        with col2:
                            st.metric(f"{protocol} Ratio", f"{ratio:.2f}x", f"vs {baseline}")
                    elif i == 1:
                        with col3:
                            st.metric(f"{protocol} Ratio", f"{ratio:.2f}x", f"vs {baseline}")
                    elif i == 2:
                        with col4:
                            st.metric(f"{protocol} Ratio", f"{ratio:.2f}x", f"vs {baseline}")
        
        # Real-time Metrics Header
        st.subheader("📊 Real-time Performance Metrics")
        self._display_advanced_metrics_header(metrics)
        
        # Protocol Summary
        st.subheader("🔍 Protocol Summary")
        self._display_protocol_summary(quic_df, tcp_tls_df, https_df)
        
        # Main Analysis Tabs
        st.subheader("📈 Detailed Protocol Analysis")
        main_tabs = st.tabs([
            "🚀 Performance Overview", 
            "📊 Statistical Analysis", 
            "🌐 Network Quality", 
            "🔍 Traffic Composition",
            "📋 Detailed Metrics"
        ])
        
        with main_tabs[0]:
            self._create_performance_overview_tab(metrics, quic_df, tcp_tls_df, https_df)
        
        with main_tabs[1]:
            self._create_statistical_analysis_tab(metrics, quic_df, tcp_tls_df, https_df)
        
        with main_tabs[2]:
            self._create_network_quality_tab(metrics)
        
        with main_tabs[3]:
            self._create_traffic_composition_tab(quic_df, tcp_tls_df, https_df)
        
        with main_tabs[4]:
            self._create_detailed_metrics_tab(metrics)
        
        # Trends (if available)
        trends = analyzer.get_traffic_trends()
        if trends:
            st.subheader("📅 Performance Trends")
            self._display_trend_indicators(trends)

    def _display_protocol_summary(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Display protocol summary"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_packets = len(quic_df) + len(tcp_tls_df) + len(https_df)
            st.metric("Total Packets", total_packets)
        
        with col2:
            quic_percent = (len(quic_df) / total_packets * 100) if total_packets > 0 else 0
            st.metric("QUIC", f"{len(quic_df)}", f"{quic_percent:.1f}%")
        
        with col3:
            tcp_tls_percent = (len(tcp_tls_df) / total_packets * 100) if total_packets > 0 else 0
            st.metric("TCP/TLS", f"{len(tcp_tls_df)}", f"{tcp_tls_percent:.1f}%")
        
        with col4:
            https_percent = (len(https_df) / total_packets * 100) if total_packets > 0 else 0
            st.metric("HTTPS", f"{len(https_df)}", f"{https_percent:.1f}%")

    def _create_performance_overview_tab(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Create performance overview tab"""
        st.subheader("🚀 Performance Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Throughput Analysis
            self._plot_advanced_throughput_analysis(metrics)
        
        with col2:
            # Efficiency Breakdown
            self._plot_efficiency_breakdown(metrics)
        
        # Traffic Patterns
        st.subheader("📈 Traffic Patterns")
        self._plot_traffic_pattern_analysis(quic_df, tcp_tls_df, https_df)
        
        # Connection Analysis
        st.subheader("🔗 Connection Analysis")
        self._plot_connection_analysis(metrics, quic_df, tcp_tls_df, https_df, "overview_connection")

    def _create_statistical_analysis_tab(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Create statistical analysis tab"""
        st.subheader("📊 Statistical Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Packet Size Distribution
            self._plot_packet_size_distribution(quic_df, tcp_tls_df, https_df)
        
        with col2:
            # Timing Analysis
            self._plot_timing_analysis(metrics)
        
        # Additional Statistical Charts
        st.subheader("📈 Distribution Analysis")
        col3, col4 = st.columns(2)
        
        with col3:
            # Traffic Volume Distribution
            self._plot_traffic_volume_distribution(quic_df, tcp_tls_df, https_df)
        
        with col4:
            # Protocol Comparison
            self._plot_protocol_comparison(metrics)

    def _create_network_quality_tab(self, metrics: Dict[str, Any]):
        """Create network quality indicators tab"""
        st.subheader("🌐 Network Quality Indicators")
        
        # Main quality indicators
        self._plot_network_quality_indicators(metrics)
        
        # Detailed quality metrics
        st.subheader("📊 Detailed Quality Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            # Stability Metrics
            self._plot_stability_metrics(metrics)
        
        with col2:
            # Performance Consistency
            self._plot_performance_consistency(metrics)

    def _create_traffic_composition_tab(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Create traffic composition analysis tab"""
        st.subheader("🔍 Traffic Composition Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Protocol distribution
            self._plot_traffic_composition(quic_df, tcp_tls_df, https_df)
        
        with col2:
            # Port distribution
            self._plot_port_distribution(quic_df, tcp_tls_df, https_df)
        
        # Additional composition analysis
        st.subheader("📦 Packet Characteristics")
        col3, col4 = st.columns(2)
        
        with col3:
            # Size categories
            self._plot_packet_size_categories(quic_df, tcp_tls_df, https_df)
        
        with col4:
            # Traffic flow patterns
            self._plot_traffic_flow_patterns(quic_df, tcp_tls_df, https_df)

    def _create_detailed_metrics_tab(self, metrics: Dict[str, Any]):
        """Create detailed metrics table tab"""
        st.subheader("📋 Comprehensive Metrics Table")
        self._show_advanced_metrics_table(metrics)

    def _display_advanced_metrics_header(self, metrics: Dict[str, Any]):
        """Display advanced metrics header with more indicators"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if not available_protocols:
            st.info("No protocol data available")
            return
            
        cols = st.columns(len(available_protocols))
        
        for i, protocol in enumerate(available_protocols):
            with cols[i]:
                st.metric(
                    f"{protocol} Throughput", 
                    f"{metrics[protocol]['throughput_mbps']:.2f} Mbps",
                    f"{metrics[protocol]['packet_count']} packets"
                )

    def _plot_advanced_throughput_analysis(self, metrics: Dict[str, Any]):
        """Plot advanced throughput analysis"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if len(available_protocols) < 2:
            st.info("Need at least 2 protocols for throughput analysis")
            return
            
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Throughput', 'Goodput Comparison', 
                          'Packet Rate', 'Efficiency Ratio'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Total Throughput
        throughputs = [metrics[p]['throughput_mbps'] for p in available_protocols]
        fig.add_trace(
            go.Bar(x=available_protocols, y=throughputs, name='Throughput',
                  marker_color=[self.colors[p] for p in available_protocols]),
            row=1, col=1
        )
        
        # Goodput Comparison
        goodputs = [metrics[p]['goodput_estimate'] for p in available_protocols]
        fig.add_trace(
            go.Bar(x=available_protocols, y=goodputs, name='Goodput',
                  marker_color=[self.light_colors[p] for p in available_protocols]),
            row=1, col=2
        )
        
        # Packet Rate
        packet_rates = [metrics[p]['packets_per_second'] for p in available_protocols]
        fig.add_trace(
            go.Bar(x=available_protocols, y=packet_rates, name='Packets/s',
                  marker_color=[self.colors[p] for p in available_protocols]),
            row=2, col=1
        )
        
        # Efficiency
        efficiencies = [metrics[p]['efficiency_ratio'] for p in available_protocols]
        fig.add_trace(
            go.Bar(x=available_protocols, y=efficiencies, name='Efficiency',
                  marker_color=[self.light_colors[p] for p in available_protocols]),
            row=2, col=2
        )
        
        fig.update_layout(height=500, showlegend=False, title_text="Throughput Analysis")
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("throughput_analysis"))

    def _plot_efficiency_breakdown(self, metrics: Dict[str, Any]):
        """Plot detailed efficiency breakdown"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if len(available_protocols) < 2:
            st.info("Need at least 2 protocols for efficiency analysis")
            return
            
        fig = go.Figure()
        
        efficiency_metrics = ['efficiency_ratio', 'goodput_estimate', 'overhead_estimate', 'compression_efficiency']
        metric_names = ['Bytes/Packet', 'Goodput (Mbps)', 'Overhead %', 'Compression %']
        
        for i, (metric, name) in enumerate(zip(efficiency_metrics, metric_names)):
            fig.add_trace(go.Bar(
                name=name,
                x=available_protocols,
                y=[metrics[p].get(metric, 0) for p in available_protocols],
                marker_color=[self.colors[p] if i % 2 == 0 else self.light_colors[p] for p in available_protocols]
            ))
        
        fig.update_layout(
            title='Efficiency Metrics Breakdown',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("efficiency_breakdown"))

    def _plot_traffic_pattern_analysis(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Analyze and plot traffic patterns"""
        if quic_df.empty and tcp_tls_df.empty and https_df.empty:
            st.info("No traffic data for pattern analysis")
            return
            
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Traffic Volume Over Time', 'Cumulative Bytes',
                          'Packet Size Distribution', 'Protocol Distribution'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Prepare data for all protocols
        protocols_data = [
            ('QUIC', quic_df, self.colors['QUIC']),
            ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
            ('HTTPS', https_df, self.colors['HTTPS'])
        ]
        
        # Traffic Volume Over Time and Cumulative Bytes
        for protocol_name, df, color in protocols_data:
            if not df.empty:
                df = df.copy()
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df = df.sort_values('timestamp')
                df['time_elapsed'] = (df['timestamp'] - df['timestamp'].min()).dt.total_seconds()
                
                # Traffic Volume Over Time
                fig.add_trace(
                    go.Scatter(x=df['time_elapsed'], y=df['length'],
                              name=f'{protocol_name} Size', line=dict(color=color)),
                    row=1, col=1
                )
                
                # Cumulative Bytes
                df['cumulative_bytes'] = df['length'].cumsum()
                fig.add_trace(
                    go.Scatter(x=df['time_elapsed'], y=df['cumulative_bytes'],
                              name=f'{protocol_name} Cumulative', line=dict(color=color)),
                    row=1, col=2
                )
        
        # Packet Size Distribution (Histogram)
        for protocol_name, df, color in protocols_data:
            if not df.empty:
                fig.add_trace(
                    go.Histogram(x=df['length'], name=f'{protocol_name} Sizes',
                                marker_color=color, opacity=0.7),
                    row=2, col=1
                )
        
        # Protocol Distribution
        protocol_counts = [
            len(quic_df), len(tcp_tls_df), len(https_df)
        ]
        protocol_names = ['QUIC', 'TCP/TLS', 'HTTPS']
        
        fig.add_trace(
            go.Bar(x=protocol_names, y=protocol_counts,
                   marker_color=[self.colors[p] for p in protocol_names]),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=True, title_text="Traffic Pattern Analysis")
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("traffic_patterns"))

    def _plot_connection_analysis(self, metrics: Dict[str, Any], quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame, key_suffix=""):
        """Plot connection and network analysis"""
        col1, col2 = st.columns(2)
        
        with col1:
            # Connection Diversity
            protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
            available_protocols = [p for p in protocols if p in metrics]
            
            if available_protocols:
                fig = go.Figure()
                categories = ['Sources', 'Destinations', 'Ports']
                
                for protocol in available_protocols:
                    values = [metrics[protocol]['unique_sources'], 
                             metrics[protocol]['unique_destinations'],
                             metrics[protocol]['port_diversity']]
                    fig.add_trace(go.Bar(name=protocol, x=categories, y=values,
                                        marker_color=self.colors[protocol]))
                
                fig.update_layout(title='Connection Diversity', barmode='group', height=300)
                st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key(f"connection_diversity_{key_suffix}"))
            else:
                st.info("No connection data available")
        
        with col2:
            # Port Distribution
            protocols_data = [
                ('QUIC', quic_df, self.colors['QUIC']),
                ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
                ('HTTPS', https_df, self.colors['HTTPS'])
            ]
            
            has_data = any(not df.empty for _, df, _ in protocols_data)
            if has_data:
                fig = go.Figure()
                
                for protocol_name, df, color in protocols_data:
                    if not df.empty:
                        port_counts = df['dst_port'].value_counts().head(8)
                        fig.add_trace(go.Bar(
                            x=port_counts.index.astype(str), y=port_counts.values,
                            name=f'{protocol_name} Ports', marker_color=color
                        ))
                
                fig.update_layout(title='Top Destination Ports', height=300)
                st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key(f"port_distribution_{key_suffix}"))
            else:
                st.info("No port data available")

    def _plot_packet_size_distribution(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot detailed packet size distribution"""
        if quic_df.empty and tcp_tls_df.empty and https_df.empty:
            st.info("No data for packet size distribution")
            return
            
        fig = go.Figure()
        
        protocols_data = [
            ('QUIC', quic_df, self.colors['QUIC']),
            ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
            ('HTTPS', https_df, self.colors['HTTPS'])
        ]
        
        for protocol_name, df, color in protocols_data:
            if not df.empty:
                fig.add_trace(go.Box(
                    y=df['length'], name=protocol_name,
                    marker_color=color
                ))
        
        fig.update_layout(
            title='Packet Size Distribution (Box Plot)',
            yaxis_title='Packet Size (bytes)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("packet_size_box"))

    def _plot_timing_analysis(self, metrics: Dict[str, Any]):
        """Plot timing and jitter analysis"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if len(available_protocols) < 2:
            st.info("Need at least 2 protocols for timing analysis")
            return
            
        fig = go.Figure()
        
        timing_metrics = ['avg_interval_ms', 'jitter_ms', 'min_interval_ms', 'max_interval_ms']
        metric_names = ['Avg Interval', 'Jitter', 'Min Interval', 'Max Interval']
        
        for metric, name in zip(timing_metrics, metric_names):
            fig.add_trace(go.Bar(
                name=name,
                x=available_protocols,
                y=[metrics[p].get(metric, 0) for p in available_protocols],
                text=[f"{metrics[p].get(metric, 0):.1f}" for p in available_protocols],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Timing Analysis (ms)',
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("timing_analysis"))

    def _plot_network_quality_indicators(self, metrics: Dict[str, Any]):
        """Plot network quality indicators"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if not available_protocols:
            st.info("No data for network quality analysis")
            return
            
        st.subheader("📊 Quality Metrics")
        
        # Create columns dynamically based on available protocols
        cols = st.columns(len(available_protocols))
        
        for i, protocol in enumerate(available_protocols):
            with cols[i]:
                # Jitter indicator
                jitter = metrics[protocol].get('jitter_ms', 0)
                st.metric(f"{protocol} Jitter", f"{jitter:.1f}ms", "Lower is better")
                
                # Burstiness indicator
                burstiness = metrics[protocol].get('burstiness', 0)
                st.metric(f"{protocol} Burstiness", f"{burstiness:.3f}", "Closer to 0 is better")
                
                # Overhead indicator
                overhead = metrics[protocol].get('overhead_estimate', 0)
                st.metric(f"{protocol} Overhead", f"{overhead:.1f}%", "Lower is better")
                
                # Stability indicator
                stability = 100 - min(100, metrics[protocol].get('traffic_volume_variation', 1) * 100)
                st.metric(f"{protocol} Stability", f"{stability:.1f}%", "Higher is better")

    def _plot_traffic_composition(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot traffic composition analysis"""
        if quic_df.empty and tcp_tls_df.empty and https_df.empty:
            st.info("No data for traffic composition")
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            # Protocol distribution pie chart
            labels = ['QUIC', 'TCP/TLS', 'HTTPS']
            values = [len(quic_df), len(tcp_tls_df), len(https_df)]
            
            fig = px.pie(values=values, names=labels, 
                        title='Protocol Distribution by Packet Count',
                        color=labels, color_discrete_map=self.colors)
            st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("protocol_distribution"))
        
        with col2:
            # Data volume distribution
            labels = ['QUIC', 'TCP/TLS', 'HTTPS']
            values = [quic_df['length'].sum() if not quic_df.empty else 0,
                     tcp_tls_df['length'].sum() if not tcp_tls_df.empty else 0,
                     https_df['length'].sum() if not https_df.empty else 0]
            
            fig = px.pie(values=values, names=labels,
                        title='Data Volume Distribution by Protocol',
                        color=labels, color_discrete_map=self.colors)
            st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("data_volume_distribution"))

    # Additional methods for new tab content
    def _plot_traffic_volume_distribution(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot traffic volume distribution"""
        if quic_df.empty and tcp_tls_df.empty and https_df.empty:
            return
            
        fig = go.Figure()
        
        protocols_data = [
            ('QUIC', quic_df, self.colors['QUIC']),
            ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
            ('HTTPS', https_df, self.colors['HTTPS'])
        ]
        
        for protocol_name, df, color in protocols_data:
            if not df.empty:
                fig.add_trace(go.Violin(y=df['length'], name=protocol_name, 
                                      box_visible=True, meanline_visible=True,
                                      marker_color=color))
        
        fig.update_layout(title='Traffic Volume Distribution', height=300)
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("traffic_volume_violin"))

    def _plot_protocol_comparison(self, metrics: Dict[str, Any]):
        """Plot protocol comparison"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if len(available_protocols) < 2:
            return
            
        comparison_metrics = ['throughput_mbps', 'packets_per_second', 'efficiency_ratio']
        metric_names = ['Throughput (Mbps)', 'Packets/s', 'Efficiency']
        
        fig = go.Figure()
        
        for i, (metric, name) in enumerate(zip(comparison_metrics, metric_names)):
            fig.add_trace(go.Bar(
                name=name,
                x=available_protocols,
                y=[metrics[p].get(metric, 0) for p in available_protocols],
                marker_color=[self.colors[p] for p in available_protocols]
            ))
        
        fig.update_layout(title='Protocol Performance Comparison', barmode='group', height=300)
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("protocol_comparison"))

    def _plot_stability_metrics(self, metrics: Dict[str, Any]):
        """Plot stability metrics"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in metrics]
        
        if not available_protocols:
            return
            
        stability_data = {'Metric': ['Jitter (ms)', 'Burstiness', 'Stability (%)', 'Overhead (%)']}
        
        for protocol in available_protocols:
            stability_data[protocol] = [
                metrics[protocol].get('jitter_ms', 0),
                metrics[protocol].get('burstiness', 0),
                100 - min(100, metrics[protocol].get('traffic_volume_variation', 1) * 100),
                metrics[protocol].get('overhead_estimate', 0)
            ]
        
        df = pd.DataFrame(stability_data)
        st.dataframe(df, use_container_width=True, key=self._get_unique_key("stability_table"))

    def _plot_performance_consistency(self, metrics: Dict[str, Any]):
        """Plot performance consistency"""
        # Placeholder for performance consistency chart
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode = "gauge+number",
            value = 85,
            title = {'text': "Performance Consistency"},
            gauge = {'axis': {'range': [None, 100]}}
        ))
        fig.update_layout(height=250)
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("consistency_gauge"))

    def _plot_port_distribution(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot port distribution analysis"""
        # Create a unique port distribution chart
        protocols_data = [
            ('QUIC', quic_df, self.colors['QUIC']),
            ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
            ('HTTPS', https_df, self.colors['HTTPS'])
        ]
        
        has_data = any(not df.empty for _, df, _ in protocols_data)
        if has_data:
            fig = go.Figure()
            
            for protocol_name, df, color in protocols_data:
                if not df.empty:
                    port_counts = df['dst_port'].value_counts().head(6)
                    fig.add_trace(go.Bar(
                        x=port_counts.index.astype(str), y=port_counts.values,
                        name=f'{protocol_name} Ports', marker_color=color
                    ))
            
            fig.update_layout(title='Destination Port Distribution', height=300)
            st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("composition_port_distribution"))

    def _plot_packet_size_categories(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot packet size categories"""
        if quic_df.empty and tcp_tls_df.empty and https_df.empty:
            return
            
        # Define size categories
        size_bins = [0, 100, 500, 1000, 1500, float('inf')]
        size_labels = ['Tiny (<100)', 'Small (100-500)', 'Medium (500-1000)', 'Large (1000-1500)', 'Huge (1500+)']
        
        fig = go.Figure()
        
        protocols_data = [
            ('QUIC', quic_df, self.colors['QUIC']),
            ('TCP/TLS', tcp_tls_df, self.colors['TCP/TLS']),
            ('HTTPS', https_df, self.colors['HTTPS'])
        ]
        
        for protocol_name, df, color in protocols_data:
            if not df.empty:
                categories = pd.cut(df['length'], bins=size_bins, labels=size_labels)
                counts = categories.value_counts()
                fig.add_trace(go.Bar(name=protocol_name, x=counts.index, y=counts.values,
                                   marker_color=color))
        
        fig.update_layout(title='Packet Size Categories', barmode='group', height=300)
        st.plotly_chart(fig, use_container_width=True, key=self._get_unique_key("size_categories"))

    def _plot_traffic_flow_patterns(self, quic_df: pd.DataFrame, tcp_tls_df: pd.DataFrame, https_df: pd.DataFrame):
        """Plot traffic flow patterns"""
        # Placeholder for traffic flow analysis
        st.info("Traffic flow patterns analysis would show communication patterns between sources and destinations")

    def _show_advanced_metrics_table(self, metrics: Dict[str, Any]):
        """Display comprehensive metrics table"""
        if not metrics:
            st.info("No metrics data available")
            return
            
        # Create detailed comparison table
        comparison_data = []
        metrics_to_show = {
            'Throughput (Mbps)': 'throughput_mbps',
            'Goodput (Mbps)': 'goodput_estimate', 
            'Packet Count': 'packet_count',
            'Avg Packet Size': 'avg_packet_size',
            'Packets/s': 'packets_per_second',
            'Unique Sources': 'unique_sources',
            'Unique Destinations': 'unique_destinations',
            'Port Diversity': 'port_diversity',
            'Avg Interval (ms)': 'avg_interval_ms',
            'Jitter (ms)': 'jitter_ms',
            'Efficiency': 'efficiency_ratio',
            'Overhead %': 'overhead_estimate',
            'Burstiness': 'burstiness'
        }
        
        for display_name, metric_key in metrics_to_show.items():
            row = {'Metric': display_name}
            for protocol in ['QUIC', 'TCP/TLS', 'HTTPS']:
                if protocol in metrics:
                    row[protocol] = metrics[protocol].get(metric_key, 0)
            comparison_data.append(row)
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df.style.format({
                'QUIC': '{:.2f}',
                'TCP/TLS': '{:.2f}',
                'HTTPS': '{:.2f}'
            }), use_container_width=True, height=400, key=self._get_unique_key("metrics_table"))

    def _display_trend_indicators(self, trends: Dict[str, Any]):
        """Display trend indicators"""
        protocols = ['QUIC', 'TCP/TLS', 'HTTPS']
        available_protocols = [p for p in protocols if p in trends]
        
        if not available_protocols:
            return
            
        cols = st.columns(len(available_protocols))
        
        for i, protocol in enumerate(available_protocols):
            with cols[i]:
                trend = trends[protocol]
                st.metric(f"{protocol} Throughput", 
                         trend['throughput_trend'],
                         f"{trend['throughput_change']:+.1f}%")
                st.metric(f"{protocol} Packets",
                         trend['packet_count_trend'],
                         "Volume trend")

def run_packet_capture(duration: int = 30, interface: str = "en0") -> Optional[Dict]:
    """Execute packet capture service with sudo privileges"""
    try:
        # Get current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        capture_script = os.path.join(current_dir, "packet_capture_service.py")
        
        # Ensure the script is executable
        if not os.access(capture_script, os.X_OK):
            os.chmod(capture_script, 0o755)
        
        # Run capture with sudo
        result = subprocess.run(
            ['sudo', 'python3', capture_script, str(duration), interface],
            capture_output=True,
            text=True,
            timeout=duration + 10
        )
        
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            st.error(f"Capture service error: {result.stderr}")
            return None
            
    except subprocess.TimeoutExpired:
        st.error("Packet capture timed out. Try a shorter duration.")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse capture results: {e}")
        return None
    except Exception as e:
        st.error(f"Error running capture: {e}")
        return None

def main():
    # Page configuration
    st.set_page_config(
        page_title="QUIC Protocol Analyzer Pro",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🔄 Advanced QUIC vs TCP/TLS vs HTTPS Protocol Analyzer")
    
    # Initialize session state
    if 'capture_data' not in st.session_state:
        st.session_state.capture_data = None
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = AdvancedPacketAnalyzer()
    
    # Sidebar controls
    st.sidebar.title("🎛️ Capture Controls")
    
    # Interface selection - dynamically detected
    interfaces = get_available_interfaces()
    selected_interface = st.sidebar.selectbox(
        "Network Interface",
        interfaces,
        help="Select the network interface to monitor"
    )
    
    # Show interface info
    st.sidebar.info(f"📡 Selected: {selected_interface}")
    
    # Capture duration
    capture_duration = st.sidebar.slider(
        "Capture Duration (seconds)",
        min_value=10,
        max_value=120,
        value=30,
        step=5,
        help="How long to capture packets"
    )
    
    # Control buttons
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🚀 Start Capture", type="primary"):
            with st.spinner(f"Capturing packets for {capture_duration} seconds..."):
                capture_data = run_packet_capture(capture_duration, selected_interface)
                
                if capture_data and 'error' not in capture_data:
                    st.session_state.capture_data = capture_data
                    
                    # Analyze packets
                    analyzer = st.session_state.analyzer
                    quic_df = pd.DataFrame(capture_data.get('quic_packets', []))
                    tcp_tls_df = pd.DataFrame(capture_data.get('tcp_tls_packets', []))
                    https_df = pd.DataFrame(capture_data.get('https_packets', []))
                    
                    analysis_results = analyzer.calculate_comprehensive_metrics(quic_df, tcp_tls_df, https_df)
                    st.session_state.analysis_results = (analysis_results, quic_df, tcp_tls_df, https_df)
                    
                    total_packets = len(quic_df) + len(tcp_tls_df) + len(https_df)
                    st.success(f"Capture completed! Got {total_packets} total packets "
                              f"({len(quic_df)} QUIC, {len(tcp_tls_df)} TCP/TLS, {len(https_df)} HTTPS)")
                else:
                    st.error("Capture failed. Check permissions and interface.")
    
    with col2:
        if st.button("🔄 Clear Results"):
            st.session_state.capture_data = None
            st.session_state.analysis_results = None
            st.rerun()
    
    # Display results if available
    if st.session_state.analysis_results:
        analysis_results, quic_df, tcp_tls_df, https_df = st.session_state.analysis_results
        visualizer = AdvancedVisualizer()
        visualizer.create_comprehensive_dashboard(analysis_results, quic_df, tcp_tls_df, https_df, st.session_state.analyzer)
        
        # Raw data view
        with st.expander("📋 View Raw Packet Data"):
            tab1, tab2, tab3 = st.tabs(["QUIC Packets", "TCP/TLS Packets", "HTTPS Packets"])
            
            with tab1:
                if not quic_df.empty:
                    st.dataframe(quic_df, use_container_width=True)
                else:
                    st.info("No QUIC packets captured")
            
            with tab2:
                if not tcp_tls_df.empty:
                    st.dataframe(tcp_tls_df, use_container_width=True)
                else:
                    st.info("No TCP/TLS packets captured")
                    
            with tab3:
                if not https_df.empty:
                    st.dataframe(https_df, use_container_width=True)
                else:
                    st.info("No HTTPS packets captured")
    
    else:
        # Enhanced welcome screen
        st.markdown("""
        ## 🚀 Welcome to QUIC vs TCP/TLS vs HTTPS Protocol Analyzer
        
        This advanced tool provides comprehensive real-time analysis and comparison of:
        - **QUIC** (Quick UDP Internet Connections) 
        - **TCP/TLS** (Traditional encrypted transport)
        - **HTTPS** (HTTP over TLS - web traffic)
        
        ### 🏗️ Organized Analysis Tabs:
        
        **🚀 Performance Overview**
        - Throughput and efficiency analysis across all protocols
        - Traffic patterns and connection analysis
        - Real-time performance metrics
        
        **📊 Statistical Analysis** 
        - Packet size distributions for all protocols
        - Timing and interval analysis
        - Advanced statistical metrics
        
        **🌐 Network Quality**
        - Jitter and stability indicators
        - Quality metrics comparison
        - Performance consistency
        
        **🔍 Traffic Composition**
        - Protocol distribution analysis
        - Port and packet characteristics
        - Traffic flow patterns
        
        **📋 Detailed Metrics**
        - Comprehensive metrics table
        - Protocol comparison data
        - All calculated parameters
        
        ### 🚀 Quick Start:
        1. Select your network interface above
        2. Set capture duration (10-120 seconds)
        3. Click **Start Capture** to begin
        4. Generate web traffic during capture for best results
        5. Explore different analysis tabs for detailed insights
        
        ### 🔧 Requirements:
        - macOS/Linux with Python 3.8+
        - Sudo/root privileges for packet capture
        - Active network traffic on selected interface
        """)
        
        # Interface detection info
        st.sidebar.info(f"🔍 Detected interfaces: {', '.join(interfaces)}")
        
        # Demo data option
        if st.button("🎮 Load Advanced Demo Data", type="secondary"):
            # Create comprehensive demo data
            demo_analysis = {
                'QUIC': {
                    'packet_count': 150,
                    'total_bytes': 187500,
                    'avg_packet_size': 1250,
                    'std_packet_size': 150,
                    'throughput_mbps': 1.5,
                    'packets_per_second': 5.0,
                    'unique_sources': 3,
                    'unique_destinations': 5,
                    'port_diversity': 8,
                    'avg_interval_ms': 12.5,
                    'jitter_ms': 2.1,
                    'min_interval_ms': 8.2,
                    'max_interval_ms': 25.7,
                    'burstiness': 0.15,
                    'traffic_volume_variation': 0.12,
                    'efficiency_ratio': 1250.0,
                    'goodput_estimate': 1.2,
                    'overhead_estimate': 4.0,
                    'compression_efficiency': 65.0,
                    'common_ports': {443: 120, 80: 30}
                },
                'TCP/TLS': {
                    'packet_count': 200, 
                    'total_bytes': 240000,
                    'avg_packet_size': 1200,
                    'std_packet_size': 180,
                    'throughput_mbps': 1.92,
                    'packets_per_second': 6.67,
                    'unique_sources': 4,
                    'unique_destinations': 6,
                    'port_diversity': 10,
                    'avg_interval_ms': 15.2,
                    'jitter_ms': 3.4,
                    'min_interval_ms': 10.1,
                    'max_interval_ms': 32.8,
                    'burstiness': 0.22,
                    'traffic_volume_variation': 0.15,
                    'efficiency_ratio': 1200.0,
                    'goodput_estimate': 1.5,
                    'overhead_estimate': 6.7,
                    'compression_efficiency': 58.0,
                    'common_ports': {443: 180, 80: 20}
                },
                'HTTPS': {
                    'packet_count': 180,
                    'total_bytes': 216000,
                    'avg_packet_size': 1200,
                    'std_packet_size': 200,
                    'throughput_mbps': 1.73,
                    'packets_per_second': 6.0,
                    'unique_sources': 5,
                    'unique_destinations': 8,
                    'port_diversity': 12,
                    'avg_interval_ms': 16.7,
                    'jitter_ms': 4.2,
                    'min_interval_ms': 11.5,
                    'max_interval_ms': 35.2,
                    'burstiness': 0.25,
                    'traffic_volume_variation': 0.17,
                    'efficiency_ratio': 1200.0,
                    'goodput_estimate': 1.4,
                    'overhead_estimate': 5.8,
                    'compression_efficiency': 62.0,
                    'common_ports': {443: 160, 80: 20}
                },
                'comparison': {
                    'QUIC_vs_TCP/TLS': 0.78,
                    'HTTPS_vs_TCP/TLS': 0.90,
                    'performance_score': 75.5
                }
            }
            
            st.session_state.analysis_results = (demo_analysis, pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
            st.rerun()

    # Enhanced footer
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 **Pro Tip**: Use **en0** (WiFi) and browse HTTPS sites "
        "during capture to generate all three protocol types for comparison."
    )

if __name__ == "__main__":
    main()