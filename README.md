# Tuesday 24 November 2026 — the day's world news in one image

[![status](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/emasinves0-commits/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/emasinves0-commits/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

A 1024x1024 poster summing up **Tuesday 24 November 2026**: 32 stories across all six regions, each tied to a press/wire source dated 24 November (UTC or local). Rendered by `draw24.py` (Python + PIL, deterministic) into `entry.png`; `main.ts` copies it to `$MAKEFUN_OUTPUT_DIR` (default `out/`).

```
python3 draw24.py entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Stories by region

### Europe (5)
3. PUTIN VOWS RETALIATION; RUSSIA HITS ZAPORIZHZHIA — _Al Jazeera · Kyiv Independent · AP_
6. UK RECORDS ITS DEADLIEST HEAT YEAR: 5,258 — _Reuters_
14. Zelensky confirms drone hit on cargo ship Sparta II, Gulf of Finland — _Kyiv Independent_
15. Danish court backs "ghetto law" used to evict "non-Western" residents — _Al Jazeera_
16. Turkish Air Force helicopter crashes in Eskişehir, 5 crew dead — _AP_

### Middle East (4)
2. ISRAEL KILLS HAMAS INTERNAL-SECURITY CHIEF — _Al Jazeera · Washington Post · Reuters_
11. DRONE HITS RIYADH FINANCIAL TOWER — _Al Jazeera_
17. UK sanctions Houthi group and four senior officials over abuses — _Al Jazeera_
18. Ras Al Khaimah: bus hits stationary truck, 13 dead, 14 hurt — _Gulf News_

### Americas (6)
7. ARMED MEN HOLD HOSTAGES IN CARTAGENA STORE — _Al Jazeera_
8. MEXICO WILL TRY "EL CHAPO ISIDRO" ITSELF — _Al Jazeera_
10. ARMY TO BLOW UP LEAD EXPLOSIVES IN IOWA — _Al Jazeera_
19. Colombia: Villavicencio car bomb, 23+ hurt; ex-FARC rebels blamed — _Al Jazeera_
20. US House counsel denies backing raid on Rep. Ilhan Omar's home — _Al Jazeera_
21. Pennsylvania reports ninth measles death in ongoing outbreak — _Al Jazeera_

### Asia-Pacific (6)
5. ASIAN STOCKS SURGE: TAIWAN +9.1% IN A DAY — _ABC (AU)_
9. GARMENT STRIKE HALTS 481 BANGLADESH FACTORIES — _The Business Standard · Daily Star_
12. MALAYSIA TO RETURN 6,500+ ROHINGYA TO MYANMAR — _Al Jazeera_
22. Hanoi hot-pot restaurant gas blast: 7 dead, 9 hurt — _VnExpress_
23. Sheikh Hasina says she will return to Bangladesh on Dec 16 — _Reuters_
24. Russian jets near Ulleung Island trigger South Korea air-raid alert — _Al Jazeera_

### Africa (6)
4. COURT REINSTATES SENEGAL AS AFRICA CUP CHAMPION — _allAfrica (CAS release) · AP_
13. NIGERIA BOAT DISASTER TOLL HITS 32 — _allAfrica_
25. Amnesty: Ethiopian shelling of Alamata killed 14+; seeks war-crimes probe — _allAfrica_
26. Sudan: 19.5 million face crisis-level hunger or worse — _allAfrica_
27. DR Congo: Ituri fighting traps Ebola responders in a maternity ward — _allAfrica_
28. Ghana beat Morocco 1–0 to win the Amputee Football World Cup — _allAfrica_

### Oceania (5)
1. SOLOMONS SCRAP CHINA SECURITY PACT — _ABC (AU) · RNZ · REPORTED, unnamed sources_
29. ASX 200 closes +1.8% at 8,726, first gain in nearly two weeks — _ABC (AU)_
30. US leases 31.5M acres of American Samoa seabed for deep-sea mining — _RNZ_
31. Labor–Greens deal gives Australians a right to sue social platforms — _ABC (AU)_
32. Cyber attack on Allied Media delays New Zealand newspapers — _RNZ_

## Not 24 November (excluded on purpose)
- 22 NOV — COP31 climate talks end with no deal
- 22 NOV — Ukraine drones sink corvette Merkury, Benghazi
- 23 NOV — Nvidia reinstates CEO Jensen Huang
- 25 NOV — Shenzhou-24 launches with a Pakistani astronaut
- 25 NOV — Australia–Solomons treaty signed in Canberra

See `BUILD-REPORT.md` for method, eye-check log and determinism hash.

License: MIT.
