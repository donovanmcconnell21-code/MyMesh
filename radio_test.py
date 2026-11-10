import meshtastic.serial_interface
from datetime import datetime 
import json

try:
	with open("nodes.json", "r") as file:
		my_nodes = json.load(file)
except FileNotFoundError:
	my_nodes = []

radio = meshtastic.serial_interface.SerialInterface()
node_num = radio.myInfo.my_node_num
node_hex_id = "!" + hex(node_num)[2:]
known_nodes = radio.nodes

print(f"\nMyMesh - My Node Telemetry")
for node in my_nodes:
	node_id_norm	= node["ID"].strip().lower()
	node_choice 	= node_id_norm

	if node_id_norm not in known_nodes:
		print(f"-----------------------\n{node_id_norm}/{node["name"]} not found in database\n")
		continue

	node_data	= known_nodes.get(node_choice, {})
	device_metrics 	= node_data.get("deviceMetrics",{})
	battery			= device_metrics.get("batteryLevel", "Unknown")
	voltage 			= device_metrics.get("voltage", "Unknown")
	long_name			= node_data.get("user", {}).get("longName", "Unknown")
	snr				= node_data.get("snr", "Unknown")
	last_heard		= node_data.get("lastHeard")
	if last_heard not in (None, 0):
		formatted_last_heard = datetime.fromtimestamp(last_heard).strftime("%b %d, %Y at %r")
	else:
		formatted_last_heard = "Unknown"
	hops_away		= node_data.get("hopsAway", "Unknown")
	via_mqtt		= node_data.get("viaMqtt", "Unknown")

	print("-----------------------")
	print(f"My Name: {node["name"]}")
	print(f"Meshtastic Name: {long_name}")
	print(f"Node ID: {node_choice}\n")
	if battery == 101:
		print("Battery Level: External Power")
	else:
		print(f"Battery Level: {battery}")
	if voltage == "Unknown":
		print("Voltage: Unknown")
	else:
		print(f"Voltage: {voltage} V")
	if snr == "Unknown":
		print("SNR: Unknown")
	else:
		print(f"SNR: {snr} dB")
	if last_heard is None:
		print("Last Heard: Unknown")
	else:
		print(f"Last heard: {formatted_last_heard}")
	print(f"Hops away: {hops_away}")
	print(f"Via MQTT? {via_mqtt}")

radio.close()