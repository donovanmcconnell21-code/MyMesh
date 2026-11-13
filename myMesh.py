#IMPORTS
import json
import meshtastic.serial_interface
from datetime import datetime
import listener_test
from pubsub import pub

#CONSTANTS
RED = "\033[31m"
RESET = "\033[0m"
GREEN = "\033[32m"

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
		print(f"{node["name"]} - {node["ID"]} - has_solar: {node.get("has_solar", False)}")
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
	while True:
		has_solar = input(f"Does this node have solar? (y/n) ")
		has_solar = has_solar.strip().lower()
		if has_solar == "y":
			has_solar = True
			break
		elif has_solar == "n":
			has_solar = False
			break
		else:
			print_error("INVALID RESPONSE - Please enter y or n")
	node = {
		"name": 	node_name,
		"ID":	node_id,
		"has_solar": has_solar
	}
	return node

def print_error(text):
	print(f"{RED}{text}{RESET}")

def print_success(text):
	print(f"{GREEN}{text}{RESET}")

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

def save_nodes():
	with open("nodes.json", "w") as file:
		json.dump(nodes, file, indent=4)
	print(f"\nNodes Saved to nodes.json !\n")

def start_monitoring(nodes):
	radio = meshtastic.serial_interface.SerialInterface()
	connection = radio.devPath
	if connection is None:
		print_error(f"\nERROR: Could not connect to a Meshtastic device.\n")
		return
	try:
		print_success(f"Starting monitoring nodes...")
		listener_test.nodes = nodes
		pub.subscribe(listener_test.on_receive, "meshtastic.receive.telemetry")
		for node in nodes:
			has_solar = node.get("has_solar", False)
			if has_solar:
				try:
					listener_test.request_telemetry(radio, node["ID"])
				except Exception as error:
					print_error(f"ERROR: {node["name"]}: {error}")

		input("Press ENTER to stop monitoring... ")
	finally:
		pub.unsubscribe(listener_test.on_receive, "meshtastic.receive.telemetry")
		print(f"Finished listening\n")
		radio.close()
		print(f"Serial connection closed!\n")

#MAIN CODE
print("Welcome to MyMesh!")
while True:
	print("MENU")
	print("1. Register node(s)")
	print("2. Show Nodes")
	print("3. Show Node Telemetry")
	print("4. Save Nodes")
	print("5. Start Monitoring")
	print("6. Save and Exit")
	print("7. Don't Save and Exit")
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
		print(
		f"Registration Summary:\n"
		f"{attempted_node} attempted nodes\n"
		f"{f'{RED}{dupe_node} duplicate nodes{RESET}' if dupe_node != 0 else f'{GREEN}{dupe_node} duplicate nodes'}{RESET}\n"
		f"{registered_node} nodes registered\n"
		)
	elif choice == "2":
		show_nodes(nodes)
	elif choice == "3":
		show_node_telemetry(nodes)
	elif choice == "4":
		save_nodes()
	elif choice == "5":
		start_monitoring(nodes)
	elif choice == "6":
		save_nodes()
		break
	elif choice == "7":
		break
	else:
		invalid_option()