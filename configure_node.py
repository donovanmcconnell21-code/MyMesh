import meshtastic.serial_interface
from meshtastic.protobuf import config_pb2

def change_device_role(radio):
	device = radio.localNode.localConfig.device
	device_role = config_pb2.Config.DeviceConfig.Role.Name(device.role)
	roles = config_pb2.Config.DeviceConfig.Role.keys()
	print(f"Current Role: {device_role}")
	print()
	print("Available Roles:")
	for number, role in enumerate(roles, start=0):
		print(f"{number}. {role}")
	while True:
		try:
			role_choice = input(f"Select a Device Role (0-{len(roles)-1}): ")
			role_choice = int(role_choice)
			if role_choice < 0 or role_choice >= len(roles):
				raise ValueError
			break
		except ValueError:
			print(f"Invalid selection. Enter a number between 0 and {len(roles)-1}.")
	print(f"Current role: {device_role}")
	print(f"Proposed change: {roles[role_choice]}")
	new_role_value = config_pb2.Config.DeviceConfig.Role.Value(roles[role_choice])
	if new_role_value == device.role:
		print()
		print("Device is already configured with that role.")
		return
	print(f"Meshtastic Role Value: {new_role_value}")
	while True:
		accept = input("Accept this change? (y/n): ")
		accept = accept.strip().lower()
		if accept == "y":
			device.role = new_role_value
			radio.localNode.writeConfig("device")
			print()
			print("Device configuration change sent. Node may reboot.")
			return True
		elif accept == "n":
			print()
			print("Change cancelled.")
			return False
		else:
			print("Please enter y or n")

def show_device_settings(radio):
	device = radio.localNode.localConfig.device
	device_role = config_pb2.Config.DeviceConfig.Role.Name(device.role)
	device_rebroadcast_mode = config_pb2.Config.DeviceConfig.RebroadcastMode.Name(device.rebroadcast_mode)
	device_broadcast_sec = device.node_info_broadcast_secs
	device_buzzer_gpio = device.buzzer_gpio
	device_tzdef = device.tzdef
	print(f"Device Role: {device_role}")
	print(f"Device Rebroadcast Mode: {device_rebroadcast_mode}")
	print(f"Device Broadcast Seconds: {device_broadcast_sec}")
	print(f"Device Buzzer GPIO: {device_buzzer_gpio}")
	print(f"Device tzdef: {device_tzdef}")

def device_settings(radio):
	while True:
		print()
		print("MyMesh - Device Settings")
		print("-------------------------")
		print("1. View Device Settings")
		print("2. Change Device Role")
		print("3. Back")
		print()
		choice = input("Please choose a menu option: ")
		if choice == "1":
			show_device_settings(radio)
		elif choice == "2":
			if change_device_role(radio):
				return True
		elif choice == "3":
			return
		else:
			invalid_option()


def configuration_menu(radio):
	while True:
		print()
		print("MyMesh - Configure Node")
		print("-------------------------")
		print("1. Lora Settings")
		print("2. Device Settings")
		print("3. Back")
		print()
		choice = input("Please select a menu option: ")
		if choice == "1":
			lora_settings(radio)
		elif choice == "2":
			if device_settings(radio):
				return True
		elif choice == "3":
			return
		else:
			invalid_option()


def change_hop_limit(radio):
	current_hop_limit = radio.localNode.localConfig.lora.hop_limit
	print()
	print(f"Current hop limit: {current_hop_limit}")
	new_hop_limit = input("Please enter new hop limit: ")
	new_hop_limit =  int(new_hop_limit)
	if new_hop_limit < 1 or new_hop_limit > 7:
		raise ValueError
	if current_hop_limit == new_hop_limit:
		print()
		print(f"Device is already configured with {current_hop_limit} hops.")
		return
	print()
	print(f"Current hop limit: {current_hop_limit} hops")
	print(f"Proposed change: {new_hop_limit} hops")
	while True:
		accept = input("Accept this change? (y/n): ")
		accept = accept.strip().lower()
		if accept == "y":
			radio.localNode.localConfig.lora.hop_limit = new_hop_limit
			radio.localNode.writeConfig("lora")
			print()
			print("Configuration change sent to node.")
			break
		elif accept == "n":
			print()
			print("Change cancelled.")
			break
		else:
			print("Please enter y or n")
	print()

def show_lora_settings(radio):
	lora_config = radio.localNode.localConfig.lora
	use_preset = lora_config.use_preset
	hop_limit = lora_config.hop_limit
	tx_enabled = lora_config.tx_enabled
	tx_power = lora_config.tx_power
	print()
	print(f"MyMesh - Lora Configuration")
	print("---------------------------")
	print(f"Use Preset: {use_preset}")
	print(f"Hop Limit: {hop_limit}")
	print(f"TX Enabled: {tx_enabled}")
	print(f"TX Power: {tx_power} dBm")
	print()

def lora_settings(radio):
	while True:
		print()
		print("MyMesh - LoRa Settings")
		print("-------------------------")
		print("1. View Lora Settings")
		print("2. Change Hop Limit")
		print("3. Back")
		choice = input("Please choose a menu option: ")
		print()
		if choice == "1":
			show_lora_settings(radio)
		elif choice == "2":
			while True:
				try:
					change_hop_limit(radio)
					break
				except ValueError:
					print()
					print("Please enter a hop limit between 1 and 7")
		elif choice == "3":
			return
		else:
			invalid_option()

def invalid_option():
	print(f"\n===!===\nINVALID OPTION\n===!===\n")

def configure_node():
	radio = meshtastic.serial_interface.SerialInterface()
	connection = radio.devPath
	if connection is None:
		print(f"\nERROR: Could not connect to a Meshtastic device.\n")
		return
	try:
		configuration_menu(radio)
	finally:
		radio.close()

if __name__ == "__main__":
	configure_node()