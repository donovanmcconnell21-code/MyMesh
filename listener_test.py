import meshtastic.serial_interface
from pubsub import pub
import json
from datetime import datetime

try:
	with open("telemetry_history.json", "r") as file:
		telemetry_history = json.load(file)
except FileNotFoundError:
	telemetry_history = []
#print(f"Telemetry History Length: {len(telemetry_history)}")

try:
	with open("nodes.json", "r") as file:
		nodes = json.load(file)
except FileNotFoundError:
	nodes = []

def request_telemetry(radio, node_id):
	print(f"Requesting power telemetry from {node_id}...")
	radio.sendTelemetry(
		destinationId = node_id,
		telemetryType = "power_metrics",
		wantResponse = True
	)
	print(f"Requested Telemetry")

def save_telemetry_history():
	with open("telemetry_history.json", "w") as file:
		json.dump(telemetry_history, file, indent=4)
		print(f"\nSaved file!\n")

def on_receive(packet, interface):
	for node in nodes:
		if packet["fromId"] == node["ID"]:
			print(f"\nNode ID: {packet["fromId"]}")
			print(f"My name: {node["name"]}")
			has_solar = node.get("has_solar", False)
			print(f"Has solar: {has_solar}\n")
			telemetry = packet.get("decoded", {}).get("telemetry", {})
			power_metrics = telemetry.get("powerMetrics", {})
			device_metrics = telemetry.get("deviceMetrics", {})
			if has_solar:
				if power_metrics:
					solar_voltage = power_metrics.get("ch3Voltage", None)
					solar_current = power_metrics.get("ch3Current", None)
					print(f"Solar Voltage: {solar_voltage} V")
					print(f"Solar Current: {solar_current} mA")
					if solar_current is None or solar_voltage is None:
						print(f"Cannot calculate mW: Missing Solar Voltage or Current")
					else:
						timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
						solar_mW = (solar_voltage * solar_current)
						telemetry_record = {
							"node_id": packet["fromId"],
							"timestamp": timestamp,
							"solar_voltage": solar_voltage,
							"solar_current": solar_current,
							"solar_mW": solar_mW,
							"type": "power"
						}
						telemetry_history.append(telemetry_record)
						print(f"Solar mW: {solar_mW} mW")
						#print(f"New Telem. Hist. Length: {len(telemetry_history)}")
						save_telemetry_history()
			if device_metrics:
				timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
				#print(f"Device Metrics: {device_metrics}")	
				battery_voltage = device_metrics.get("voltage", None)
				battery_level = device_metrics.get("batteryLevel", None)
				if battery_voltage is not None:
					print(f"Battery voltage is {battery_voltage}")
					if battery_level == 101:
						battery_level = None
						print(f"Battery Level is None")
					telemetry_record = {
						"node_id": packet["fromId"],
						"timestamp": timestamp,
						"voltage": battery_voltage,
						"battery_level": battery_level,
						"type": "device"
					}
					telemetry_history.append(telemetry_record)
					save_telemetry_history()
				#print(battery_level, battery_voltage)

if __name__ == "__main__":
	pub.subscribe(on_receive, "meshtastic.receive.telemetry")

	radio = meshtastic.serial_interface.SerialInterface()

	for node in nodes:
		has_solar = node.get("has_solar", False)
		if has_solar:
			request_telemetry(radio, node["ID"])

	input("Press ENTER to stop listening...")
	print()

	radio.close()