import meshtastic.serial_interface

radio = meshtastic.serial_interface.SerialInterface()

radio.sendTelemetry(
    destinationId="!00000001",
    telemetryType="power_metrics",
    wantResponse=True
)

radio.close()