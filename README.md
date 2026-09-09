# Factorio Astra

Local autonomous play on Factorio 2.0.77. Original starting state is preserved in `~/Library/Application Support/factorio/saves/astra-start.zip`.

## Tools

- `native-input.swift` / `native-input`: macOS keyboard and mouse events with sufficient key-down duration for Factorio. Activates Factorio, preserves the text clipboard when pasting. Unicode entry is available as a fallback.
- `mods/astra-control_0.1.0`: custom `/astra` command accepts JSON actions and exports a snapshot every 120 game ticks to `~/Library/Application Support/factorio/script-output/astra/state.json`.
- `play.py`: sends actions and reads snapshots. Example: `python3 play.py send '[{"op":"walk","to":[10,10]}]'`.
- Official version-matched runtime API reference downloaded to `runtime-api.json` from https://lua-api.factorio.com/2.0.77/runtime-api.json.

## Rules

No item spawning, teleportation, research completion, altered speed, resource creation, map revelation, or player stat changes. Movement uses `walking_state`; mining uses `mining_state` and consumes normal game time; crafting uses `begin_crafting`; construction uses `pipette` and `build_from_cursor` with inventory consumption and distance checks. Transfers require the player to reach the entity and remove actual source items before inserting them, returning any unaccepted amount. Observation only includes charted chunks in the player's vicinity. Mod use affects vanilla Steam achievement eligibility.

## Action vocabulary

`walk`: to, tolerance, timeout (ticks). `mine`: at/name or id, ticks. `craft`: recipe, count. `build`: name, at, direction (north=0/east=4/south=8/west=12). `put` / `take`: at/name or id, inventory, item, count. `recipe`: target, recipe. `research`: name. `rotate`: target. `wait`: ticks. `save`: name. `stop` clears pending actions. `observe`: radius. `batch`: actions.

An exception stops the queue and writes an audit entry. Walking timeout does not imply successful arrival; inspect the snapshot. Mining intervals do not imply a particular yield; inspect actual inventory. `audit.jsonl` records action results. Restarting Factorio is necessary after modifying the mod.


Timing helpers: `wait_crafting` waits for the player's actual hand-crafting queue to empty; use after crafting and travel, before constructing those items. `wait_research` with a technology `name` waits for its actual normal research completion. Neither advances time nor grants progress. Transfer `player_inventory: "character_ammo"` moves existing equipped magazines to a turret, since Factorio may place newly crafted ammo directly in that inventory. Equipment is now included in observations.


Large batches now use stored plans to avoid lost keyboard characters. `play.py` writes a JSON action list into the mod's `plans.lua`, archives the exact actions under `plans/`, reloads the mod, checks `controller_plan_version`, then sends only a short `/astra` plan reference. The plan still runs the same guarded normal movement/crafting/mining/building/transfers. Console command parsing is protected by `pcall`; rejection logs an error instead of terminating the game session. Native input explicitly releases movement keys before/after typing; idle controller state stops walking.

Combat safety uses actual equipped weapon and ammunition. It keeps a target until it dies, fires at nearby enemy units, and retreats using ordinary walking when outnumbered or hurt. Combat retreat clears the action queue; inspect the audit and resume only uncompleted actions. Death clears the queue and writes `alive:false` so a frozen previous observation cannot be mistaken for a live character. Respawn still uses the normal game UI.

## Saved checkpoint — 2026-09-09

Factorio was saved and closed at the user's request. The rocket has not been launched; rocket-silo research was about 18.9% at the last observation. Copper supply to the remote circuit factory was restored from two existing copper-plate buffers after the original mining sites depleted. Both cable assemblers and the electronic-circuit assembler were observed working. Yellow science had not yet visibly restarted.

- `saves/astra-session-end-2026-09-09.zip`: validated final save, including the world and controller state.
- `session/checkpoint.json`: checkpoint metadata and save SHA-256.
- `session/state.json`, `session/inspection.json`: last observations; their ticks differ.
- `session/audit.jsonl`: recorded action results, including failures and partial plans.
- `PROGRESS.md`: chronological working notes; later corrections supersede earlier plans.
- `plans/` and root JSON files: historical actions and route plans. Do not replay them wholesale against the final save.

### Rebuild local helpers

On macOS with Xcode command-line tools installed:

```sh
swiftc native-input.swift -o native-input
swiftc window-layout.swift -o window-layout
```

Python 3 runs the local scripts. Native input requires macOS Accessibility permission. Install `mods/astra-control_0.1.0` into the Factorio user-data `mods` directory, copy the checkpoint into `saves`, and load it manually when resuming. The game is intentionally closed; importing or cloning this repository does not resume play. `restart.py` targets an older autosave and should not be used to load this final checkpoint unchanged.

`observe` is a top-level console action; it cannot be nested inside an action batch. `build` does not apply a `filters` field: follow it with `inserter_filter`. Verify completed actions and inventory before retrying any interrupted plan.

`runtime-api.json` is the downloaded official Factorio 2.0.77 API reference; Factorio itself is not included. Locally compiled binaries and Python caches are excluded.
