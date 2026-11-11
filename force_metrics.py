import meshtastic.serial_interface

radio = meshtastic.serial_interface.SerialInterface()

radio.sendTelemetry(
    destinationId="!c959ed45",
    telemetryType="power_metrics",
    wantResponse=True
)

radio.close()