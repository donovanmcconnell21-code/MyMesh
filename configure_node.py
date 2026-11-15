import meshtastic.serial_interface

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
			print()
			print("Device settings coming soon")
			print()
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