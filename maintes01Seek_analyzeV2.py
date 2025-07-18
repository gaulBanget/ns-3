import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import csv

#####################
# Simulasi ruang ujian
# 1 AP 802.11ax
# 24 Clients/PC
# Author: Arie Budiansyah
# Prodi: Informatika
# Universitas Syiah Kuala
# 2025
#########################

# Parse file XML
tree = ET.parse("scratch/naufalOld/flow-stats__maintes01Seek.xml")
root = tree.getroot()

flow_stats = []

# Data collection (unchanged)
for flow in root.findall(".//FlowStats/Flow"):
    try:
        tx_packets = int(flow.attrib.get('txPackets', '0'))
        rx_packets = int(flow.attrib.get('rxPackets', '0'))
        tx_bytes = int(flow.attrib.get('txBytes', '0'))
        rx_bytes = int(flow.attrib.get('rxBytes', '0'))
        delay_sum = float(flow.attrib.get('delaySum', '0').replace('ns', ''))
        jitter_sum = float(flow.attrib.get('jitterSum', '0').replace('ns', ''))
        time_first_tx = float(flow.attrib.get('timeFirstTxPacket', '0').replace('ns', ''))
        time_last_rx = float(flow.attrib.get('timeLastRxPacket', '0').replace('ns', ''))

        duration = (time_last_rx - time_first_tx) / 1e9
        throughput = (rx_bytes * 8) / duration / 1e6 if duration > 0 else 0
        pdr = rx_packets / tx_packets if tx_packets > 0 else 0
        avg_delay = (delay_sum / rx_packets) / 1e6 if rx_packets > 0 else 0
        avg_jitter = (jitter_sum / rx_packets) / 1e6 if rx_packets > 0 else 0
        packet_loss = (tx_packets - rx_packets) / tx_packets if tx_packets > 0 else 0

        flow_stats.append({
            "flowId": flow.attrib.get("flowId", "N/A"),
            "throughput": throughput,
            "pdr": pdr,
            "delay": avg_delay,
            "jitter": avg_jitter,
            "loss": packet_loss
        })

    except Exception as e:
        print(f"⚠️ Skipping flow due to error: {e}")

# Save to CSV (unchanged)
with open("flow-stats__maintes01Seek.csv", "w", newline="") as csvfile:
    fieldnames = ["flowId", "throughput", "pdr", "delay", "jitter", "loss"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for stat in flow_stats:
        writer.writerow(stat)

# Visualization metrics
metrics = ["throughput", "pdr", "delay", "jitter", "loss"]
titles = {
    "throughput": "Throughput (Mbps)",
    "pdr": "Packet Delivery Ratio",
    "delay": "Average Delay (ms)",
    "jitter": "Average Jitter (ms)",
    "loss": "Packet Loss Ratio"
}

# Create both bar and line graphs
for metric in metrics:
    values = [flow[metric] for flow in flow_stats]
    #flow_ids = [f"Flow {i+1}" for i in range(len(values))]
    
    # Create bar chart (existing)
    plt.figure(figsize=(12, 5))
    #plt.bar(flow_ids, values)
    plt.bar(range(len(values)), values)
    plt.title(f"{titles[metric]} (Bar Chart)")
    plt.xlabel("Flow ID")
    plt.ylabel(titles[metric])
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"scratch/naufalOld/bar_{metric}.png")
    plt.close()
    
    # Create line graph (new)
    plt.figure(figsize=(12, 5))
    #plt.plot(flow_ids, values, marker='o', linestyle='-', color='b', linewidth=2)
    plt.plot(range(len(values)), values, marker='o', linestyle='-', color='b', linewidth=2)
    plt.title(f"{titles[metric]} Trend (Line Graph)")
    plt.xlabel("Flow ID")
    plt.ylabel(titles[metric])
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    
    # Add horizontal line for average
    avg_value = sum(values)/len(values)
    plt.axhline(y=avg_value, color='r', linestyle='--', 
                label=f'Average: {avg_value:.2f}')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(f"scratch/naufalOld/line_{metric}.png")
    plt.close()

    # Create combined chart (bonus)
    plt.figure(figsize=(12, 5))
    #plt.bar(flow_ids, values, alpha=0.6, label='Per Flow')
    plt.bar(range(len(values)), values)
    #plt.plot(flow_ids, values, marker='o', color='r', label='Trend')
    plt.plot(range(len(values)), values, marker='o', color='r', label='Trend')
    plt.title(f"{titles[metric]} (Combined View)")
    plt.xlabel("Flow ID")
    plt.ylabel(titles[metric])
    plt.xticks(rotation=45)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"scratch/naufalOld/combined_{metric}.png")
    plt.close()

print("✅ Analisis selesai. Output grafik:")
print(f"✅ Bar charts: scratch/naufalOld/bar_[metric].png")
print(f"✅ Line graphs: scratch/naufalOld/line_[metric].png")
print(f"✅ Combined views: scratch/naufalOld/combined_[metric].png")
print(f"✅ Total flow yang dianalisis: {len(flow_stats)}")
print("📄 Data lengkap disimpan ke: flow-stats__maintes01Seek.csv")
