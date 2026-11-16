import listener_test
listener_test.nodes = [
    {"name": "Test Node", "ID": "!00000001", "has_solar": True}
]

packet = {
	"id": 321654987,
	"decoded": {
		"telemetry": {}
	}
}

packet2 = {
	"fromId": "!00000001",
	"id": 987654321,
	"decoded": {
		"telemetry": {}
	}
}

packet3 = {
	"fromId": "!00000001",
	"id": 789456123,
	"decoded": {
		"telemetry": {}
	}
}

packet4 = {
	"fromId": "!00000001",
	"id": 123789456,
	"decoded": {
		"telemetry": {}
	}
}

listener_test.on_receive(packet, None)
listener_test.on_receive(packet2, None)
listener_test.on_receive(packet3, None)
listener_test.on_receive(packet4, None)
listener_test.on_receive(packet, None)
listener_test.on_receive(packet4, None)