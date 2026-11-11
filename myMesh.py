#IMPORTS
import json
import meshtastic.serial_interface
from datetime import datetime

#CONSTANTS
RED = "\033[31m"
RESET = "\033[0m"

#GET FILE
try:
	with open("nodes.json", "r") as file:
		nodes = json.load(file)
except FileNotFoundError:
	nodes = []

#FUNCTIONS
def show_nodes(nodes):
	print()
	print("=====")
	print("Registered Nodes:")
	for node in nodes:
		print(f"{node["name"]} - {node["ID"]}")
	print("=====")
	print()

def register_node():
	while True:
		node_name = input("Node Name: ")
		node_name = node_name.strip()
		if len(node_name) > 0:
			break
		else:
			print_error(f"\n EMPTY NODE NAME IS INVALID\n")
	while True:
		node_id = input("Node ID: ")
		node_id = node_id.strip().lower()
		if len(node_id) > 0:
			break
		else:
			print_error(f"\n EMPTY NODE ID IS INVALID\n")
	node = {
		"name": 	node_name,
		"ID":	node_id
	}
	return node

def print_error(text):
	print(f"{RED}{text}{RESET}")

def invalid_option():
	print_error(f"\n===!===\nINVALID OPTION\n===!===\n")

def show_node_telemetry(nodes):
	radio = meshtastic.serial_interface.SerialInterface()
	connection = radio.devPath
	if connection is None:
		print_error(f"\nERROR: Could not connect to a Meshtastic device.\n")
		return
	try:
		known_nodes = radio.nodes

		print(f"\nMyMesh - My Node Telemetry")
		for node in nodes:
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
	finally:
		radio.close()
		print(f"Serial connection closed!\n")

#MAIN CODE
print("Welcome to MyMesh!")
while True:
	print("MENU")
	print("1. Register node(s)")
	print("2. Show Nodes")
	print("3. Show Node Telemetry")
	print("4. Save and Exit")
	choice = input("Please choose a menu option: ")
	if choice == "1":
		attempted_node = 0
		dupe_node = 0
		registered_node = 0
		while True:
			try:
				num_nodes = int(input("How many nodes would you like to register? "))
				if num_nodes > 0:
					break
				else:
					print_error("Please enter a number greater than 0")
			except ValueError:
				print_error("Please enter a whole number!")
		for i in range(num_nodes):
			node = register_node()
			attempted_node += 1
			found = False
			for existing_node in nodes:
				if node["ID"] == existing_node["ID"].strip().lower():
					found = True
					dupe_node += 1
					break
			if found:
				print()
				print_error("===!===")
				print_error(f"{node["name"]} is a duplicate and was not saved.")
				print_error(f"===!===\n\n")
			else:
				nodes.append(node)
				registered_node +=1
		show_nodes(nodes)
		print(f"Registration Summary:\n {attempted_node} attempted nodes\n {RED}{dupe_node} duplicate nodes{RESET}\n {registered_node} nodes registered\n")
		#TODO if there are 0 dupe nodes, we don't need red text
	elif choice == "2":
		show_nodes(nodes)
	elif choice == "3":
		show_node_telemetry(nodes)
	elif choice == "4":
		with open("nodes.json", "w") as file:
			json.dump(nodes, file, indent=4)
		break
	else:
		invalid_option()