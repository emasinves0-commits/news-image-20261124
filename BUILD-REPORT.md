# BUILD REPORT — news-image-20261124: "Tuesday 24 November 2026"

- **Bounty:** Sum up 24 November's world news in one image (pot $100, deadline 26 Nov 2026 00:00 UTC).
- **Built:** 25 Nov 2026 (UTC), one session: research -> fresh renderer -> 3 fix rounds + a final full re-read -> report.
- **Files:** `draw24.py` (renderer, written fresh this session, no prior code opened), `entry.png` (1024x1024), `main.ts`, `README.md`, `LICENSE`, `.makefun/owner.json`, `eyecheck/` (crops read during verification).
- **Entry:** `entry.png`, 1024x1024 RGB, **278,232 bytes** (limit 1 MiB).
- **Determinism:** three independent renders gave the same sha256 `5fb0d5402c32dea4fd3f210df86c83ebc9fbf1ca3ae6d77b31e3d336b051ed21`. No timestamps, no randomness in the render path (a fixed-seed LCG only scatters a few stars in one art panel). Re-verified after the last edit.

## Research method
The search tool's index was thin for 24 Nov, so stories were taken only from pages that carry the date: Wikipedia's Current Events portal for 24 Nov (11 items, each citing a wire/press URL dated 2026-11-24), Al Jazeera / ABC (AU) / allAfrica / RNZ / Kyiv Independent articles whose URLs or page stamps are 24 Nov, and the Wikipedia Deaths list. Leads were opened in full and cross-read (Al Jazeera, ABC, allAfrica, Kyiv Independent). AP, Reuters, Guardian, Washington Post and NYT could not be fetched directly from this machine; stories attributed to them are cited via Wikipedia's dated entries that link to those URLs (or via the Al Jazeera/Kyiv Independent copy of the same fact). Daily briefings (Democracy Now, Just Security) were used only as leads: most of their items turned out to be 22–23 Nov events, so they were not used for the poster unless re-found on a 24 Nov page.

**Traps caught by date-checking** (each looked like a 24 Nov story but is not): Shenzhou-24 launch (25 Nov 00:18 UTC), COP31 collapse (22 Nov), Nvidia reinstating Huang (23 Nov), Australia–Solomons treaty signing (25 Nov), Ukrainian strike on corvette Merkury (22 Nov), South Korea's AI-cheating bounty (18 Nov), Gomez "resignation" (could not confirm a 24 Nov source — dropped).

## Story set — 32 stories, 6 regions (asserted in code: counts sum to total)
| Region | Count | Stories (pin number: headline) |
|---|---|---|
| EUROPE | 5 | 3 PUTIN VOWS RETALIATION; RUSSIA HITS ZAPORIZHZHIA; 6 UK RECORDS ITS DEADLIEST HEAT YEAR: 5,258; 14 Zelensky confirms drone hit on cargo ship Sparta II, Gulf of Finland; 15 Danish court backs "ghetto law" used to evict "non-Western" residents; 16 Turkish Air Force helicopter crashes in Eskişehir, 5 crew dead |
| MIDDLE EAST | 4 | 2 ISRAEL KILLS HAMAS INTERNAL-SECURITY CHIEF; 11 DRONE HITS RIYADH FINANCIAL TOWER; 17 UK sanctions Houthi group and four senior officials over abuses; 18 Ras Al Khaimah: bus hits stationary truck, 13 dead, 14 hurt |
| AMERICAS | 6 | 7 ARMED MEN HOLD HOSTAGES IN CARTAGENA STORE; 8 MEXICO WILL TRY "EL CHAPO ISIDRO" ITSELF; 10 ARMY TO BLOW UP LEAD EXPLOSIVES IN IOWA; 19 Colombia: Villavicencio car bomb, 23+ hurt; ex-FARC rebels blamed; 20 US House counsel denies backing raid on Rep. Ilhan Omar's home; 21 Pennsylvania reports ninth measles death in ongoing outbreak |
| ASIA-PACIFIC | 6 | 5 ASIAN STOCKS SURGE: TAIWAN +9.1% IN A DAY; 9 GARMENT STRIKE HALTS 481 BANGLADESH FACTORIES; 12 MALAYSIA TO RETURN 6,500+ ROHINGYA TO MYANMAR; 22 Hanoi hot-pot restaurant gas blast: 7 dead, 9 hurt; 23 Sheikh Hasina says she will return to Bangladesh on Dec 16; 24 Russian jets near Ulleung Island trigger South Korea air-raid alert |
| AFRICA | 6 | 4 COURT REINSTATES SENEGAL AS AFRICA CUP CHAMPION; 13 NIGERIA BOAT DISASTER TOLL HITS 32; 25 Amnesty: Ethiopian shelling of Alamata killed 14+; seeks war-crimes probe; 26 Sudan: 19.5 million face crisis-level hunger or worse; 27 DR Congo: Ituri fighting traps Ebola responders in a maternity ward; 28 Ghana beat Morocco 1–0 to win the Amputee Football World Cup |
| OCEANIA | 5 | 1 SOLOMONS SCRAP CHINA SECURITY PACT; 29 ASX 200 closes +1.8% at 8,726, first gain in nearly two weeks; 30 US leases 31.5M acres of American Samoa seabed for deep-sea mining; 31 Labor–Greens deal gives Australians a right to sue social platforms; 32 Cyber attack on Allied Media delays New Zealand newspapers |

- **Leads (3):** 1 Solomons scrap China pact (ABC, RNZ), 2 Israel kills Hamas security chief (Al Jazeera, WaPo, Reuters), 3 Putin vows retaliation / Zaporizhzhia strike (Al Jazeera, Kyiv Independent, AP).
- **Small panels (10):** 4–13, each with its own art function (cup, candlesticks, thermometer, supermarket, scales, factory, bunker, tower, border fence, boat).
- **ALSO list (19):** 14–32, one line each, region-coloured chips, source in parentheses.
- **Data strip (6):** 9.1% Taiwan shares · 5,258 UK heat deaths · 1,680 Gaza dead since ceasefire · 481 Bangladesh factories halted · 6,500+ Rohingya · 31.5M acres American Samoa seabed.
- **UTC strip (5 beats):** overnight Zaporizhzhia strike -> ~05:00 UTC ASX close -> Putin remarks / Solomons pact end -> Gaza strike -> CAS ruling. Order is approximate except the ASX close (4pm AEDT = 05:00 UTC); the strip says so.
- **DATE CHECK (5 excluded, real dates):** COP31 ends, no deal — 22 Nov · Ukraine drones sink corvette Merkury, Benghazi — 22 Nov · Nvidia reinstates Huang — 23 Nov · Shenzhou-24 launch — 25 Nov · Australia–Solomons treaty signed — 25 Nov.
- **Certainty labels:** CLAIM on Hamas "war crime", Cartagena hostage counts (25 vs 30), Houthi blame for the Riyadh drone, green-group lead-plume warning; REPORTED on anonymous-source Solomons story and the Zaporizhzhia toll.

## Diagnosis — structure used and why
Same winning structure as the previous day's poster (prose report only): 3 huge leads + 10 smalls + ALSO list + data strip + pinned map + region bar + UTC strip + DATE CHECK + sources/certainty footer, with the legibility-first rule: no text below 10px (asserted in `F()`; sizes used 10–15 plus 25/29 display), banners 15px, bodies 11px. 32 stories rather than 43 to buy type size. Leads chosen as the day's three most consequential, geographically spread (Oceania/geopolitics, Middle East/war, Europe/war). Layout is a left column (ALSO + UTC) against a right column (map + insets), which kept both full width of the page and every line legible.

## Eye-check log (every crop read at full resolution; crops in `eyecheck/`)
**Round 1** (first render, 0 renderer warnings but visible defects):
1. Masthead summary line touched the 30px title — title cut to 29px, summary moved down. FIXED.
2. Data-strip numbers collided with their labels; two labels wrapped as "(Al / Jazeera)" — strip made 4px taller, labels shortened, source on its own line. FIXED.
3. Lead chip hid "5-" of the "5-STOREY BLOCK" art label — chip moved into the red banner. FIXED.
4. Small panel 8 (Mexico): handcuffs read as the letters "GO" — replaced with scales of justice. FIXED.
5. UTC strip showed a tofu box for "≈" — replaced with "~". FIXED.
6. ME inset title tag covered pin 2 (Gaza) — tag moved top-right. FIXED.
7. ALSO chips cramped — replaced by 20x12 rounded rectangles, line step 13.5px. FIXED.
8. Map pins clipped at edges (30, 32) — clamp widened. FIXED.
**Round 2:**
9. Red Sea / Persian Gulf polygons drew a wide diagonal band in the ME inset — rebuilt. FIXED.
10. ME inset labels "Riyadh" / "Ras Al Khaimah" overlapped; Sanaa label hidden by the title tag — label shortened to "RAK", lat range extended, tag moved. FIXED.
11. Inset marker box ("ME") drawn over pins 25/26 — markers now drawn under the pins inside the map tile. FIXED.
**Round 3:**
12. Panel 7 (Cartagena) art illegible (tape covered silhouettes, "STORE" lost on awning) — redrawn with sign band "SUPERMARKET", visible silhouettes, tape low. FIXED.
13. Story 5 cited Nvidia's CEO return as its cause while DATE CHECK excludes that event (23 Nov) — headline/body reworded to state the 23 Nov date explicitly. FIXED.
**Final re-read (round 4):** full poster re-read in two halves + map 2x + panel 5/7 zooms + pin-32 corner zoom: **zero defects**. Every sub-label in every art panel checked (SECURITY PACT 2022 / CHINA – SOLOMONS / NOT RENEWED / SOLOMON ISLANDS; GAZA · DRONE STRIKE / ABU NAHL, 50; 5-STOREY BLOCK / REFINERY HIT / RETALIATION?; 1–0; +9.1%; SUPERMARKET; 481; LEAD; MYANMAR) — none appears in a second panel. Region bar: EUROPE 5 · MIDDLE EAST 4 · AMERICAS 6 · ASIA-PACIFIC 6 · AFRICA 6 · OCEANIA 5 = 32. All six data numbers read. All 32 pins present and numbered (world map: 23, Europe inset: 3 6 14 15 16, Middle East inset: 2 11 17 18).
**300px test** (`eyecheck/r4_300px.png`): masthead date, three lead banners, six data numbers read clearly; pins visible as numbered coloured dots; small bodies and ALSO list blur out as designed.

## Known nits (not defects)
- Story 14 (Sparta II): the drone strike was 21 Nov; what is dated 24 Nov is Zelensky's confirmation (Kyiv Independent) — the line says "confirms".
- Story 19: the Villavicencio bomb itself was 23 Nov (Wikipedia); the 24 Nov news is the president blaming ex-FARC rebels and the toll reaching 23+.
- Story 4 pin sits on Dakar (subject: Senegal), though the ruling was in Lausanne; story 28 pin sits on Accra (venue not verified).
- Zaporizhzhia wounded count varied by source and hour (40 / 44 / 48), so the poster says "40+".
- Story 5 uses ABC's 4:13pm AEDT snapshot (Nikkei +3.9%, KOSPI +7.1%); earlier in the session they were +4.5% / +7.5%.
- Map shapes are schematic (hand-keyed polygons); the Middle East inset is vertically stretched and says so.
- Attributions to AP/Reuters/WaPo/Guardian rest on Wikipedia's dated Current Events entries (direct fetch of those sites was blocked here).
- Obituaries on Wikipedia's 24 Nov Deaths list (e.g. A. Samad Said, Martha Firestone Ford) were found but not used, to protect space for hard news.
- Not pushed: no git credentials on this machine (per brief); commits are local only.
