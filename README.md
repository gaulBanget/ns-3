# Simulasi ruang kuliah dengan NS3

🎯 Premis Simulasi:
Dalam sebuah laboratorium komputer di Universitas Syiah Kuala, 24 PC siswa bersiap mengikuti ujian online melalui satu Access Point (AP) WiFi 6 (802.11ax). Tantangannya? Memastikan komunikasi data antara AP dan client tetap stabil meski semua device mengirim paket secara bersamaan. Inilah yang dihadirkan oleh simulasi maintes01Seek.cc menggunakan NS-3!

🔧 Teknologi Inti:
1. NS-3 dengan WiFi 802.11ax
     Simulasi ini memodelkan CSMA 1-persistent secara implisit melalui mekanisme DCF (Distributed Coordination Function) pada WiFi.

     Parameter kritis:
       RTS/CTS Threshold diatur otomatis berdasarkan ukuran paket (500/1000 bytes)
       Grid mobility dengan AP di pusat (25,25) untuk cakupan optimal
       Two-way traffic (Client↔AP) pada port berbeda (9 dan 10)

2. Python Analytics (maintes01Seek_analyze.py)
     Mengolah output XML FlowMonitor menjadi metrik kinerja:

   throughput = (rx_bytes * 8) / duration / 1e6  # Mbps
   pdr = rx_packets / tx_packets  # Packet Delivery Ratio
