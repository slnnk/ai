---
system: telegram-desktop
status: verified
checked: 2026-10-21
tags: [desktop, audio, freeze]
---
# Telegram Desktop: freeze correlated with audio device recreation

## Task
Investigate the user-reported recurring freeze when an incoming message arrives.

## Context
Ubuntu 20.04.6 workstation; official local executable `~/Telegram/Telegram`, version 7.3.2, Qt 6.11.2. Application log: `~/.local/share/TelegramDesktop/log.txt`.

## Actions
Read application log, host process/thread wait states, recent user/kernel journals and `pactl info`. Host diagnostics required execution outside process isolation. GDB attach was rejected by ptrace protection; `sudo -n gdb` required a password, so the initial agent attempts collected no stack. The user subsequently ran sudo GDB locally; read `~/telegram-stack.txt` (307 lines), ending with successful detach. Initially no runtime change was performed. After reviewing the stack and proposal, the user explicitly approved terminating the frozen Telegram and relaunching with `ALSOFT_DRIVERS=pulse` (`Да`). At 15:44 MSK terminated old PID 64899 and started PID 73307 with the approved backend override plus local OpenAL diagnostic logging. No persistent launcher/audio configuration or packages were changed.

## Findings
- At 15:30:48 MSK the last application log line was `Audio Info: recreating audio device and reattaching the tracks`.
- At the same second `pipewire-media-session` reported `no node found for 51, stream error`.
- At 15:35 the main Telegram thread waited in `futex_wait_queue_me`; this alone does not prove a deadlock. Audio threads included `ALSoftP0` and PipeWire loops. PulseAudio 13.99.1 responded to a read-only query.
- About 5.9 GiB memory was available; no kernel journal entries appeared in the preceding 30 minutes.
- User-collected stack confirms the GUI thread blocks while playing a notification: `Window::Notifications::System::showNext()` -> `Media::Audio::Track::playWithLooping()` -> `Media::Audio::AttachToDevice()` -> `alcCreateContext()` -> `PipeWirePlayback::start()` -> `pw_thread_loop_wait()` -> `pthread_cond_wait()`. The exact lower-level PipeWire failure remains unverified; notification/audio involvement is now directly established.
- Similar symptom and log line were reported on Windows in [upstream issue 29769](https://github.com/telegramdesktop/tdesktop/issues/29769); this supports a diagnostic direction, not proof of an identical defect or fix.

## Changes
Updated the existing pinned launcher `~/.local/share/applications/org.telegram.desktop._79cb295b486a3125956cdd4d7255c270.desktop` after the user reported successful notification playback and requested persistence. Main `Exec` now uses `/usr/bin/env ALSOFT_DRIVERS=pulse DESKTOPINTEGRATION=1 /home/slnnk/Telegram/Telegram -- %U`; `DBusActivatable=false` makes GNOME use this command. `DESKTOPINTEGRATION=1` prevents Telegram from overwriting the customized launcher on startup, as implemented in [upstream InstallLauncher](https://github.com/telegramdesktop/tdesktop/blob/dev/Telegram/SourceFiles/platform/linux/specific_linux.cpp). Backup: `~/ai-data/telegram-desktop/launcher-before-pulse.desktop`. Quit action and URI arguments preserved.

## Status and risks
Notification playback is confirmed blocked in the OpenAL PipeWire backend. The user approved a Telegram-only restart with `ALSOFT_DRIVERS=pulse`. Relaunch succeeded; process environment contains that override and `~/ai-data/telegram-desktop/openal-pulse.log` confirms `Initialized backend "pulse"` and `Added "pulse" for playback`. Backend selection is documented by [OpenAL Soft](https://github.com/kcat/openal-soft/blob/master/docs/env-vars.txt).

The user confirmed normal operation after the PulseAudio restart and requested persistence for launches from the pinned panel icon. The existing pinned desktop ID was verified through the read-only GNOME favorite-apps list and its local launcher updated. GIO parses the final launch command and URI support correctly. The old desktop validator rejects the pre-existing upstream `SingleMainWindow` key; a temporary validation copy excluding only that existing key passes. No runtime relaunch or GNOME settings mutation was performed in the persistence step. End-to-end launch from the panel remains for the next normal user launch; long-term stability is untested. No further implementation work is outstanding, and no backlog item is required. Logs are in `~/ai-data/telegram-desktop/`; the user-collected stack remains at `~/telegram-stack.txt`.

## Portable lesson
None.
