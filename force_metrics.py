import meshtastic.serial_interface

radio = meshtastic.serial_interface.SerialInterface()
node_id = input("Enter node ID: ")

radio.sendTelemetry(
    destinationId = node_id,
    telemetryType="power_metrics",
    wantResponse=True
)

radio.close()