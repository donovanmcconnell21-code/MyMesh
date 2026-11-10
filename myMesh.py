import json

RED = "\033[31m"
RESET = "\033[0m"

try:
	with open("nodes.json", "r") as file:
		nodes = json.load(file)
except FileNotFoundError:
	nodes = []

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

print("Welcome to MyMesh!")
while True:
	print("MENU")
	print("1. Register node(s)")
	print("2. Show Nodes")
	print("3. Save and Exit")
	choice = input("Please choose a menu option:")
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
		with open("nodes.json", "w") as file:
			json.dump(nodes, file, indent=4)
		break
	else:
		invalid_option()