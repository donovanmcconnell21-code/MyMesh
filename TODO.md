# MyMesh TODOs

MyMesh is an incremental Python learning project. Completed items reflect the code and manual tests available at this checkpoint; they are not a claim of complete automated or hardware-wide testing.

## Current priorities — integration and safety

- [ ] **Connect `myMesh.py` menu option 6** to the existing `configure_node.configure_node()` entry point. The option is displayed but currently falls through to invalid-option handling.
- [ ] Handle serial errors during configuration writes and cleanup, especially if a device-role change reboots or disconnects the node.
- [ ] Verify written configuration by reconnecting/readback; clearly distinguish “write sent” from “verified on device.”
- [ ] Add a configuration backup/export step before making disruptive changes; protect any exported channel keys or precise positions.
- [ ] Handle malformed `nodes.json` and `telemetry_history.json` gracefully (invalid JSON, wrong data shapes, helpful error messages).
- [ ] Make data paths independent of the launch working directory.
- [ ] Check for accidental publication of real node IDs in tracked test scripts before sharing the repository publicly.

## Node configuration — next features

- [x] Build a standalone `configure_node.py` with nested Configure Node, LoRa, and Device menus.
- [x] Read and display selected LoRa settings.
- [x] Change LoRa hop limit with range validation, confirmation, and no-op detection; verify persistence manually after reconnecting.
- [x] Read and display selected Device settings with readable role and rebroadcast-mode enums.
- [x] List available device roles dynamically; validate selection, skip unchanged values, and require confirmation.
- [x] Apply Device Role changes and exit nested menus; verify `CLIENT` ↔ `CLIENT_MUTE` changes manually after reconnecting.
- [ ] Add **Change Rebroadcast Mode** to Device Settings after reviewing mode behavior and safe defaults.
- [ ] Expand LoRa and Device settings coverage beyond the current editable fields.
- [ ] Consider a Back/Cancel option during role selection before reaching the confirmation prompt.
- [ ] Factor shared validation and confirmation behavior into reusable helpers when additional editors justify it.
- [ ] Add a “search settings” feature.
- [ ] Add Bluetooth LE connection support.
- [ ] Let the user select USB, BLE, or TCP connection methods.
- [ ] Design reusable node configuration profiles for different node types.
- [ ] Support exporting, backing up, reviewing, and applying node configuration profiles.
- [ ] Consider which settings are safe or supported to change remotely versus through a direct connection.

## Monitoring, telemetry, and storage

- [x] Fix stale node registrations during monitoring by sharing the current registration list with the listener.
- [x] Separate current node snapshots and live monitoring into distinct operations.
- [x] Add a manual **Save Nodes** option, plus save/exit and exit-without-save choices.
- [x] Detect duplicate registration IDs and avoid duplicate warning messages when none exist.
- [x] Handle errors from individual telemetry requests without stopping the entire monitoring session.
- [x] Skip incoming packets missing `fromId`.
- [x] Detect duplicate telemetry packet IDs within a running process.
- [x] Bound in-memory duplicate detection to the most recent 100 packet keys.
- [x] Use temporary-file + atomic replacement for telemetry-history JSON saves; manually verify successful replacement and removal of the temporary file.
- [x] Check for a missing serial connection in standalone `listener_test.py` before sending requests or attempting cleanup.
- [ ] Improve live terminal output so asynchronous telemetry does not overlap menus/prompts.
- [ ] Handle delayed telemetry responses; avoid stopping a session before expected replies arrive.
- [ ] Handle duplicate measurements across restarts and distinguish packet deduplication from measurement deduplication.
- [ ] Improve history storage performance as it grows; avoid rewriting the entire JSON file for every incoming record.
- [ ] Improve reliability for concurrent callbacks/writes, write failures, and interrupted saves (atomic replacement alone does not solve all of these).
- [ ] Make node-registration saving atomic as well.
- [ ] Improve numeric precision/formatting for solar measurements.
- [ ] Build a historical telemetry viewer and graphs for solar generation, battery voltage, and other metrics.
- [ ] Add a delete-registered-node option.
- [ ] Narrow broad `except Exception` handling to expected Meshtastic errors where practical.

## Testing, documentation, and cleanup

- [x] Write and update `README.md` with setup, dependencies, features, limitations, and data-file guidance.
- [x] Verify repeated telemetry snapshot connections work (manual menu option 3 testing).
- [x] Handle missing serial connections in the main application without calling `close()` on an incompletely initialized interface.
- [ ] Add automated tests using simulated telemetry packets and mock radio/configuration objects; existing `*_test.py` scripts are manual experiments.
- [ ] Add a reproducible dependency manifest (`requirements.txt` or project metadata) and document supported versions.
- [ ] Validate node IDs/formats and guard against malformed registration records.
- [ ] Review and safely retire or organize older hardware experiments once they are no longer useful.

## Future ideas

- [ ] Explore an always-on Raspberry Pi monitoring deployment.
- [ ] Explore broadcasting a daily dad joke to the mesh using icanhazdadjoke (consider API availability, airtime, and network etiquette).
