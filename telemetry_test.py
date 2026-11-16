#IMPORTS
import json
from datetime import datetime
import meshtastic.serial_interface

#GET FILE
try:
	with open("telemetry_history.json", "r") as file:
		telemetry_history = json.load(file)
except FileNotFoundError:
	telemetry_history = []

#CONNECT TO RADIO
def collect_telemetry():
	radio = meshtastic.serial_interface.SerialInterface()
	connection = radio.devPath
	if connection is None:
		print(f"\nERROR: Could not connect to a Meshtastic device.\n")
		return
	try:
		#FAKE NODE FOR NOW
		nodes = {
			"ID": "!00000001"
		}
		# TODO PULL FROM nodes.json?

		#GET VARIABLES
		node_id_norm	= nodes["ID"].strip().lower()
		node_choice 	= node_id_norm
		known_nodes = radio.nodes
		node_data	= known_nodes.get(node_choice, {})
		node_data_keys = known_nodes.get(node_choice, {})
		print(node_data_keys)
		device_metrics 	= node_data.get("deviceMetrics",{})
		power_metrics		= node_data.get("powerMetrics", {})
		battery			= device_metrics.get("batteryLevel", "Unknown")
		print(node_choice in known_nodes)
		print(f"Device Metrics: {device_metrics}")
		print(f"Power Metrics: {power_metrics}")
		if battery in (101, "Unknown"):
			battery = None
		voltage 			= device_metrics.get("voltage", "Unknown")
		if voltage == "Unknown":
			print(f"Voltage is unknown - record not saved!")
			return
		last_heard = node_data.get("lastHeard")
		if last_heard not in (None, 0):
			formatted_last_heard = datetime.fromtimestamp(last_heard).astimezone().isoformat(timespec="seconds")
		else:
			formatted_last_heard = "Unknown"
		print(f"Last heard: {formatted_last_heard}")
		
		#REGISTER HISTORY
		timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
		print(f"Timestamp: {timestamp}")
		telemetry_record = {"node_id": node_id_norm, "timestamp": timestamp, "voltage": voltage, "battery_level": battery}
		telemetry_history.append(telemetry_record)

		#WRITE CHANGES
		# with open("telemetry_history.json", "w") as file:
		# 	json.dump(telemetry_history, file, indent=4)
		# print(voltage)
		# print(battery)
		print(telemetry_record)

	finally:
		#CLOSE SERIAL CONNECTION
		radio.close()
		print(f"Serial connection closed!\n")

collect_telemetry()