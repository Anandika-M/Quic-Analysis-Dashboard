import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st
import numpy as np
from datetime import datetime, timedelta

class AdvancedVisualizer:
    def __init__(self):
        self.color_scheme = {
            'QUIC': '#1f77b4',
            'TLS': '#ff7f0e', 
            'HTTPS': '#2ca02c'
        }
        
    def create_comprehensive_dashboard(self, analysis_results, realtime_metrics, capture_stats):
        """Create advanced dashboard with multiple visualizations"""
        st.title("🔄 Advanced QUIC vs TCP/TLS/HTTPS Protocol Analysis")
        
        # Real-time metrics header
        self._display_realtime_header(realtime_metrics, capture_stats)
        
        # Performance comparison charts
        st.subheader("📊 Comprehensive Performance Comparison")
        self._plot_advanced_comparison(analysis_results)
        
        # Throughput over time
        st.subheader("📈 Throughput Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            self._plot_throughput_comparison(analysis_results)
        with col2:
            self._plot_latency_distribution(analysis_results)
        
        # Protocol efficiency
        st.subheader("⚡ Protocol Efficiency Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            self._plot_efficiency_metrics(analysis_results)
        with col2:
            self._plot_packet_analysis(analysis_results)
        
        # Detailed metrics table
        st.subheader("🔍 Detailed Metrics Analysis")
        self._display_detailed_metrics(analysis_results)
        
        # Trends over time (if available)
        if hasattr(st.session_state, 'metrics_history'):
            st.subheader("📅 Metrics Trends Over Time")
            self._plot_metrics_trends()

    def _display_realtime_header(self, realtime_metrics, capture_stats):
        """Display real-time metrics header"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            quic_metrics = realtime_metrics.get('quic', {})
            st.metric(
                "QUIC Packets/s", 
                quic_metrics.get('packet_count', 0),
                f"{quic_metrics.get('throughput_bps', 0)/1e6:.2f} Mbps"
            )
        
        with col2:
            tls_metrics = realtime_metrics.get('tls', {})
            st.metric(
                "TLS Packets/s",
                tls_metrics.get('packet_count', 0),
                f"{tls_metrics.get('throughput_bps', 0)/1e6:.2f} Mbps"
            )
            
        with col3:
            https_metrics = realtime_metrics.get('https', {})
            st.metric(
                "HTTPS Packets/s",
                https_metrics.get('packet_count', 0),
                f"{https_metrics.get('throughput_bps', 0)/1e6:.2f} Mbps"
            )
            
        with col4:
            duration = capture_stats.get('capture_duration', 0)
            st.metric(
                "Capture Duration",
                f"{duration:.1f}s",
                "Active" if capture_stats.get('capture_active', False) else "Stopped"
            )

    def _plot_advanced_comparison(self, analysis_results):
        """Create advanced comparison charts"""
        if not analysis_results:
            st.warning("No data available for comparison")
            return
            
        protocols = list(analysis_results.keys())
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Throughput (Mbps)', 'Latency (ms)', 
                          'Packet Loss (%)', 'Protocol Efficiency (%)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Throughput comparison
        throughput_data = [analysis_results[p].get('avg_throughput_mbps', 0) for p in protocols]
        fig.add_trace(
            go.Bar(x=protocols, y=throughput_data, name='Throughput', 
                  marker_color=[self.color_scheme.get(p, '#333') for p in protocols]),
            row=1, col=1
        )
        
        # Latency comparison
        latency_data = [analysis_results[p].get('avg_latency_ms', 0) for p in protocols]
        fig.add_trace(
            go.Bar(x=protocols, y=latency_data, name='Latency',
                  marker_color=[self.color_scheme.get(p, '#333') for p in protocols]),
            row=1, col=2
        )
        
        # Packet loss comparison
        loss_data = [analysis_results[p].get('packet_loss_estimate', 0) for p in protocols]
        fig.add_trace(
            go.Bar(x=protocols, y=loss_data, name='Packet Loss',
                  marker_color=[self.color_scheme.get(p, '#333') for p in protocols]),
            row=2, col=1
        )
        
        # Efficiency comparison
        efficiency_data = [analysis_results[p].get('protocol_efficiency', 0) for p in protocols]
        fig.add_trace(
            go.Bar(x=protocols, y=efficiency_data, name='Efficiency',
                  marker_color=[self.color_scheme.get(p, '#333') for p in protocols]),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    def _plot_throughput_comparison(self, analysis_results):
        """Plot throughput comparison with peak vs average"""
        if not analysis_results:
            return
            
        protocols = list(analysis_results.keys())
        avg_throughput = [analysis_results[p].get('avg_throughput_mbps', 0) for p in protocols]
        peak_throughput = [analysis_results[p].get('peak_throughput_mbps', 0) for p in protocols]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Average Throughput',
            x=protocols,
            y=avg_throughput,
            marker_color=[self.color_scheme.get(p, '#333') for p in protocols]
        ))
        
        fig.add_trace(go.Bar(
            name='Peak Throughput',
            x=protocols,
            y=peak_throughput,
            marker_color=[self.color_scheme.get(p, '#666') for p in protocols]
        ))
        
        fig.update_layout(
            title='Throughput: Average vs Peak',
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _plot_latency_distribution(self, analysis_results):
        """Plot latency distribution metrics"""
        if not analysis_results:
            return
            
        protocols = list(analysis_results.keys())
        
        metrics = ['avg_latency_ms', 'min_latency_ms', 'max_latency_ms']
        metric_names = ['Average', 'Minimum', 'Maximum']
        
        fig = go.Figure()
        
        for i, metric in enumerate(metrics):
            values = [analysis_results[p].get(metric, 0) for p in protocols]
            fig.add_trace(go.Bar(
                name=metric_names[i],
                x=protocols,
                y=values,
                marker_color=px.colors.qualitative.Set3[i]
            ))
        
        fig.update_layout(
            title='Latency Distribution (ms)',
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _plot_efficiency_metrics(self, analysis_results):
        """Plot protocol efficiency metrics"""
        if not analysis_results:
            return
            
        protocols = list(analysis_results.keys())
        
        efficiency_metrics = {
            'Protocol Efficiency': 'protocol_efficiency',
            'Goodput Ratio': 'goodput_ratio',
            'Throughput Stability': 'throughput_stability'
        }
        
        fig = go.Figure()
        
        for metric_name, metric_key in efficiency_metrics.items():
            values = [analysis_results[p].get(metric_key, 0) for p in protocols]
            fig.add_trace(go.Bar(
                name=metric_name,
                x=protocols,
                y=values,
                text=[f'{v:.1f}%' for v in values],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='Efficiency Metrics (%)',
            barmode='group',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _plot_packet_analysis(self, analysis_results):
        """Plot packet analysis metrics"""
        if not analysis_results:
            return
            
        protocols = list(analysis_results.keys())
        
        fig = go.Figure()
        
        # Packet sizes
        avg_sizes = [analysis_results[p].get('avg_packet_size', 0) for p in protocols]
        fig.add_trace(go.Bar(
            name='Avg Packet Size',
            x=protocols,
            y=avg_sizes,
            text=[f'{v:.0f} bytes' for v in avg_sizes],
            textposition='auto',
            marker_color=[self.color_scheme.get(p, '#333') for p in protocols]
        ))
        
        fig.update_layout(
            title='Average Packet Size',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _display_detailed_metrics(self, analysis_results):
        """Display detailed metrics table"""
        if not analysis_results:
            return
            
        # Create comprehensive metrics table
        metrics_data = []
        for protocol, metrics in analysis_results.items():
            row = {'Protocol': protocol}
            row.update(metrics)
            metrics_data.append(row)
        
        df = pd.DataFrame(metrics_data)
        
        # Format numeric columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        format_dict = {col: "{:.2f}" for col in numeric_columns}
        
        st.dataframe(
            df.style.format(format_dict),
            use_container_width=True
        )

    def _plot_metrics_trends(self):
        """Plot metrics trends over time (placeholder for future implementation)"""
        st.info("Metrics trends visualization will be available with extended capture duration")

    def create_protocol_breakdown(self, capture_stats):
        """Create protocol breakdown pie chart"""
        if not any(capture_stats.values()):
            return
            
        labels = ['QUIC', 'TLS', 'HTTPS']
        values = [
            capture_stats.get('total_quic_packets', 0),
            capture_stats.get('total_tls_packets', 0),
            capture_stats.get('total_https_packets', 0)
        ]
        
        if sum(values) > 0:
            fig = px.pie(
                names=labels,
                values=values,
                title="Protocol Distribution",
                color=labels,
                color_discrete_map={
                    'QUIC': self.color_scheme['QUIC'],
                    'TLS': self.color_scheme['TLS'],
                    'HTTPS': self.color_scheme['HTTPS']
                }
            )
            st.plotly_chart(fig, use_container_width=True)