---
name: flight-to-calendar
description: Add booked flights to the user's Google Calendar - one event per flight leg, timezone-correct duration math, sunset/sunrise seat-side hints for golden-hour legs. Use when the user provides a booking / e-ticket / PNR / flight details (or points to an itinerary file) and says "add my flights to the calendar", "put the trip on my calendar", or similar.
---

# flight-to-calendar

Add flights the user has **already booked** to their Google Calendar.

> 🤖 R2-D2 moment: navigation is literally the astromech's day job — plotting courses,
> logging coordinates, keeping the records straight while Luke is busy being distracted.

## 🚦 Iron rules (every one of these was paid for with a real mistake)

1. **Never fabricate flights.** Flight numbers, departure/arrival times, aircraft types come exclusively from the user's booking details or files. Missing a leg or a time → **ask directly**; don't guess, don't fill in from "typical schedules". Align every leg's data before touching the calendar.

2. **One leg = one event.** An outbound with a connection = 2 events; the layover gap then shows naturally on the calendar. Never merge a whole journey into one big event.

3. **Timezone handling (the easiest thing to get wrong — follow exactly)**:
   - Each event's `timeZone` = the **departure airport's** IANA timezone.
   - `startTime` = local departure time; `endTime` = the **arrival local time converted back into the departure timezone** (this is what makes the event's duration correct).
   - ⚠️ Neighboring airports can differ; the +9 vs +8 one-hour gap is the classic miss:
     - **UTC+8**: Taipei TPE / Hong Kong HKG / Manila MNL / Shanghai PVG / Kuala Lumpur KUL / Singapore SIN
     - **UTC+9**: Seoul ICN / Tokyo NRT·HND / Osaka KIX / Nagoya NGO / Fukuoka FUK / Sapporo CTS
     - **UTC+7**: Bangkok BKK / Hanoi HAN / Ho Chi Minh SGN / Jakarta CGK
   - Google renders events in whatever timezone the user is currently in, so as long as the stored **instant** is correct, display takes care of itself; put local times in the description for reference.

   **Worked example** (CX418 HKG 14:25 → ICN 19:05):
   - HKG is +8, ICN is +9.
   - `timeZone` = `Asia/Hong_Kong`, `startTime` = `...T14:25:00`.
   - Arrival 19:05 ICN local (+9) converted to HKG (+8) = **18:05** → `endTime` = `...T18:05:00`.
   - Duration = 3h40m (correct); description notes "arrives ICN 19:05 local (KST/UTC+9)".

4. **Title format**: `✈️ <flight no.> <origin>→<destination> (<PNR>)`
   - **No cabin class by default** (the calendar is for yourself, not for showing off; add it if the user asks).
   - Example: `✈️ CX489 TPE→HKG (D8M7E7)`

5. **Sunset / sunrise seat side**: if a leg hits magic hour (evening arrival for sunset, dawn departure for sunrise), work out which side to sit on and note it in the title or description.
   - Principle (sunset = sun in the west): flying **northeast** → **left (A)**; **southeast** → **right (K)**; **southwest** → **right (K)**; **northwest** → **left (A)**; due east/west → either side.
   - **Sunrise (sun in the east) — flip every answer.**
   - Known examples: HKG→TPE (northeast) sunset left (A); HKG→MNL (southeast) sunset right (K).

6. **Color**: `colorId` = `7` (Peacock teal) for all flights — the trip pops out at a glance.

7. **Description field** carries: flight no. + aircraft, airports (with terminals) + local times, PNR, connection relationships with adjacent legs, sunset hints, timezone notes.

## Steps

1. **Gather data**: per leg, confirm flight number, departure airport (terminal), arrival airport (terminal), local times, aircraft, PNR. If the data is in a file (e-ticket, master itinerary), read and cross-check leg by leg; when unsure, ask.
2. **Compute timezones**: per leg set `timeZone` (departure airport), `startTime` (local departure), `endTime` (arrival local converted to departure tz).
3. **Create leg by leg**: use Google Calendar `create_event` (default primary calendar); multiple legs can be created in parallel in one message.
4. **Report**: paste each event's link + one-line highlights (total legs, "local vs displayed" reminders for cross-timezone legs, sunset seats).

## Tool requirements

- **Google Calendar MCP** (connector): `create_event` / `update_event` — a hard dependency; without the Calendar connector this skill cannot run.
- If the tools are deferred, load them first via ToolSearch with `select:...create_event`.
- Default primary calendar unless the user specifies another.

## Notes

- This registers **already-booked** flights — it is not booking or changing tickets → no payment or external submission involved; just create events.
- For later changes/deletions, use `update_event` / delete with the same timezone and title rules.
