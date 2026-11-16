# MyMesh

**MyMesh** is an experimental Python command-line project for working with personal [Meshtastic](https://meshtastic.org/) nodes. It currently supports local node registration, telemetry monitoring, and a separate CLI for viewing and changing selected radio settings.

This is also a hands-on Python learning project. Features are being added incrementally, and the code is **not yet production-ready**.

## Current features

### Main application — `myMesh.py`

- Register Meshtastic nodes with a friendly name, node ID, and `has_solar` flag.
- Reject duplicate node IDs, view the registered list, and save registrations to `nodes.json`.
- View a snapshot of registered nodes from the connected radio's node database, including available battery, voltage, SNR, last-heard, hop-count, and MQTT information.
- Run a live monitoring session and request power telemetry from registered solar nodes.
- Capture incoming device and solar measurements in `telemetry_history.json`.
- Skip duplicate packet IDs seen recently during the current process (a bounded 100-packet cache).
- Save telemetry history via a temporary file and atomic replacement to reduce the risk of a partially written history file.

The snapshot and live monitoring modes are separate. **Historical charts and a historical browsing menu are not implemented yet.**

### Node configurator — `configure_node.py`

The standalone configurator uses nested terminal menus and a **USB serial connection** to the attached Meshtastic node.

| Settings area | Available actions |
| --- | --- |
| LoRa | View preset usage, hop limit, TX enablement, and configured TX power; change hop limit (1–7) |
| Device | View role, rebroadcast mode, NodeInfo broadcast interval, buzzer GPIO, and timezone definition; change device role |

Configuration changes require confirmation. Both implemented editors detect when the requested value already matches the current value. Device roles are displayed by their protobuf enum names, and a confirmed role write exits the menus because the node may reboot or disconnect. A fresh connection is needed to verify that the device retained a change.

**Current integration gap:** the main application's menu displays `6. Configure Node`, but that selection is **not yet wired up** in `myMesh.py`. Run `configure_node.py` directly for now. Other configuration categories, settings search, profiles, backups, and BLE/TCP connections are future work.

## Requirements

- **Python 3.12 or newer.** Some existing f-strings rely on syntax supported in Python 3.12+; the supplied development environment uses Python 3.13.
- A compatible Meshtastic device connected to the computer over USB serial, with a working firmware/configuration setup.
- The Python packages `meshtastic` and `PyPubSub`.

Versions found in the reviewed development environment: `meshtastic==2.7.11` and `PyPubSub==4.0.7`. These are observed development versions, not a formal compatibility matrix or a requirements lockfile.

## Setup

Run these commands from the MyMesh project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install meshtastic PyPubSub
```

On Windows, activate with `.venv\Scripts\activate` instead. The application currently assumes that relative JSON paths resolve from your **current working directory**, so launch it from the repository root.

## Run the applications

### Main MyMesh menu

```bash
python myMesh.py
```

| Option | Action |
| --- | --- |
| 1 | Register node(s) |
| 2 | Show registered nodes |
| 3 | Show node telemetry snapshot |
| 4 | Save nodes |
| 5 | Start monitoring |
| 6 | Configure node — **listed but not connected yet** |
| 7 | Save and exit |
| 8 | Exit without saving node-list changes |

With option 5, the program requests power telemetry from solar-capable registered nodes and listens for incoming telemetry until you press **Enter**. Monitoring only runs while the program remains open. Exiting without saving node registrations does **not** undo telemetry data already written during monitoring.

### Standalone node configuration

```bash
python configure_node.py
```

Choose **LoRa Settings** or **Device Settings** and use the nested menus to inspect settings or make supported changes. For device-role changes, choose a role only after understanding its effect on message rebroadcasting and connectivity. Some writes can reboot the radio. Back up important settings separately before experimenting.

## Local data

`nodes.json` contains registrations like the following **fictional examples**:

```json
[
  {"name": "Portable Node", "ID": "!00000001", "has_solar": false},
  {"name": "Solar Node", "ID": "!22222222", "has_solar": true}
]
```

`telemetry_history.json` contains records with a local ISO timestamp, node ID, packet ID (when present), type, and measurements. For example:

```json
{
  "node_id": "!00000001",
  "packet_id": 123456789,
  "timestamp": "2026-11-15T10:30:00-06:00",
  "voltage": 4.1,
  "battery_level": null,
  "type": "device"
}
```

```json
{
  "node_id": "!22222222",
  "packet_id": 123456790,
  "timestamp": "2026-11-15T10:31:00-06:00",
  "solar_voltage": 4.4,
  "solar_current": 85.0,
  "solar_mW": 374.0,
  "type": "power"
}
```

Solar measurement handling currently assumes `powerMetrics.ch3Voltage` is in volts and `powerMetrics.ch3Current` is in milliamps. Milliwatts are calculated as `volts × milliamps`. This channel mapping is specific to the solar-node setup used during development; other hardware may use different channels. A battery level of `101` is stored as JSON `null` rather than a percentage.

The telemetry listener currently loads and rewrites the full history list when saving. Duplicate prevention is limited to recently seen packet IDs within the running process; it does not deduplicate across restarts.

**Privacy:** `.gitignore` excludes the local node list, telemetry history, node-info export, and virtual environment. Do not upload the complete working directory or an archive containing those files. Review development scripts for hard-coded node IDs before publishing them, and treat exported Meshtastic configurations as potentially sensitive because they may include channel keys or location settings.

## Project files

| File | Purpose |
| --- | --- |
| `myMesh.py` | Main menu, node registration, node snapshots, and monitoring sessions |
| `configure_node.py` | Standalone nested CLI for viewing/changing selected LoRa and Device settings |
| `listener_test.py` | Telemetry callback, power-metrics requests, and JSON history persistence; imported by `myMesh.py` |
| `duplicate_test.py` | Manual duplicate-packet experiments; not an automated test suite |
| `radio_test.py`, `telemetry_test.py`, `force_metrics.py` | Hardware/development experiments; inspect before running because they can access a connected node |
| `TODO.md` | Current backlog, deferred improvements, and future ideas |

## Known limitations

- The configuration menu is not yet reachable through main-menu option 6.
- Settings coverage is limited to two editable fields; the configurator is not a complete replacement for the Meshtastic app.
- There is no automatic config backup, write-error recovery, or post-reboot verification.
- JSON loading does not yet recover gracefully from malformed files, and telemetry history will need a more scalable storage approach.
- File paths are relative to the launch directory; incoming telemetry output can overlap interactive prompts.
- No automated test suite is established; functionality has been tested manually with a USB-connected node and simulated packets.
- Bluetooth, TCP, remote configuration, historical charts, and always-on Raspberry Pi monitoring are not implemented.

See [TODO.md](TODO.md) for the working backlog.

## Authorship and AI disclosure

The MyMesh application code is written by the project author as part of learning Python. ChatGPT has been used for instruction, debugging guidance, and code review rather than for writing the application code.

This README was drafted and updated by ChatGPT (OpenAI) at the author's request after reviewing the project files.
