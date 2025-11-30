# QUIC vs TCP/TLS vs HTTPS Protocol Analyzer

A comprehensive network protocol analyzer that compares QUIC, TCP/TLS, and HTTPS performance in real-time.

## Features

- **Real-time Packet Capture**: Capture and analyze network traffic in real-time
- **Three Protocol Comparison**: QUIC vs TCP/TLS vs HTTPS
- **Advanced Analytics**: Throughput, latency, jitter, efficiency metrics
- **Interactive Visualizations**: Plotly charts with real-time updates
- **Comprehensive Metrics**: 15+ performance indicators per protocol
- **Organized Dashboard**: Tab-based interface for different analysis types

## Protocols Analyzed

1. **QUIC** (Quick UDP Internet Connections)
   - Modern transport protocol
   - Built-in encryption
   - Multiplexed streams
   - Faster connection establishment

2. **TCP/TLS** (Traditional Encrypted Transport)
   - Standard TCP with TLS encryption
   - Reliable ordered delivery
   - Widely supported

3. **HTTPS** (HTTP over TLS)
   - Web traffic analysis
   - TLS handshake detection
   - Application layer metrics
## Project Structure 
```bash
   Quic-Analysis-Dashboard/
QUIC/
│
├── analysis.py           # Functions for analyzing captured QUIC/HTTPS packet data.
│
├── app.py                # Main application script — runs the dashboard.
│
├── https_capture.py      # Script to capture HTTPS traffic packets.
│
├── packet_capture_service.py   # Background/continuous packet capture service for QUIC/HTTPS.
│
├── packet_capture.py     # Core logic for capturing QUIC packets from network interfaces.
│
├── README.md             # Documentation describing the project, setup, usage, etc.
│
├── realtime_monitor.py   # Real-time monitoring module — live packet or traffic visualization.
│
├── requirements.txt      # List of required Python packages needed to run the project.
│
└── visualization.py      # Code for plotting/analyzing results (graphs, charts, visual dashboards).
   ```

## Installation

1. Clone or download the project files
   ```bash
      git clone https://github.com/Anandika-M/Quic-Analysis-Dashboard.git
      cd Quic-Analysis-Dashboard
2. Install dependencies:
   ```bash
      pip install -r requirements.txt

## Usage 

1. Start the Real-Time Dashboard
   ```bash
      python app.py
The app runs on streamlit platform and Dashboard opens at: http://127.0.0.1:8050/
