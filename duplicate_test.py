import listener_test

packet = {
	"id": 321654987,
	"decoded": {
		"telemetry": {}
	}
}

packet2 = {
	"fromId": "!c959ed45",
	"id": 987654321,
	"decoded": {
		"telemetry": {}
	}
}

packet3 = {
	"fromId": "!c959ed45",
	"id": 789456123,
	"decoded": {
		"telemetry": {}
	}
}

packet4 = {
	"fromId": "!c959ed45",
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