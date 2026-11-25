# Design notes — news-image-20261125 round 2

One-page newspaper front page, 1024×1024, cream paper, black serif
headlines, maroon + navy accents, flat original vector illustrations
(no photos). Round 2 rebuilds the round-1 entry (#48/3,891) to close the
six gaps found in the top-10 study: a UTC timeline strip, a confidence
badge on every story, a first-reported time on every story, bigger and
more detailed lead scenes, proper pictorial panels for the medium
stories, and consensus lead stories for the day.

## Stories (38 total, 7 regions)

Regions: Europe 10, Asia 7, Americas 7, Middle East 6, Africa 4,
Oceania 2, Global 2.

### Lead stories (3) — large drawn scenes
1. Shenzhou-24 carries Pakistan's first astronaut to Tiangong — OFFICIAL,
   rep 00:18 UTC (launch), docked 03:56 UTC. CMSA / Xinhua / Reuters.
2. Kospi crashes 6.2% as the chip rally unwinds — CONFIRMED, rep 06:30 UTC
   (close 4,697.51; Samsung -9.9%, SK Hynix -11.1%, SoftBank -14.8%).
   Korea Exchange / Reuters / WSJ.
3. Two tankers hit mines in Hormuz, IRGC says — CLAIM, rep 09:46 UTC.
   Tankers unnamed, no casualty details. IRGC via IRNA / Reuters.

### Ten more stories (10) — pictorial panels
4. Saudi coalition strikes Hodeidah port — CONFIRMED, rep 00:10. SPA / AFP.
5. Solomons pick Australia as top security partner — OFFICIAL, rep 06:30.
   PM of Australia / Reuters.
6. Garment workers win 36% pay rise (Bangladesh) — CONFIRMED, rep 07:20.
   Reuters / AP.
7. 26 trapped in flooded Java gold mine — CONFIRMED, rep 04:00.
   Reuters / West Java police.
8. Huawei guilty on 10 of 12 US counts — CONFIRMED, rep 06:45. Verdict
   delivered Tue in Brooklyn, reported worldwide Wed. Reuters / US DOJ.
9. WHO pulls Ebola teams from Congo hospital — OFFICIAL, rep 10:30. WHO.
10. Kyiv sea drones sink Russian warship off Libya — REPORTED, rep 08:00.
    Reuters.
11. NATO sends early-warning jets to Poland — CONFIRMED, rep 09:00. Reuters.
12. Trump pardons turkeys Freedom and Feathers — OFFICIAL, rep 15:00. AP.
13. Senegal get AFCON title back after CAS ruling — CONFIRMED, rep 11:00. AFP.

### Also on Wednesday 25 November (25)
14. Putin vows retaliation over refinery strikes (Kremlin) · 15. 700,000+
    Russian soldiers killed, leak finds (RFE/RL) · 16. Russian strike on
    Kyiv-region flats kills 11 (RFE/RL) · 17. Zelenskyy: US "aligning with
    Russia" (Bloomberg) · 18. Fort Hood gunman seeks stay of execution
    (Reuters) · 19. Sarkozy and Bruni ordered to stand trial (Reuters) ·
    20. Indonesia's vice-president resigns (Wire reports) · 21. Xiamen
    Airlines orders 50 Boeing 737-8 (Reuters) · 22. England beat Australia
    by 8 wickets, 2nd T20I (AP) · 23. Colombia car bomb wounds 23; 25 held
    hostage (Reuters) · 24. Iran winter gas shortages bite (DW) · 25. Iraq
    seizes Kurdish oilfields (Reuters) · 26. Israeli strike kills Hamas
    security chief in Gaza (BBC) · 27. Israel: Iran building chemical
    weapons (Israel says) · 28. EU adopts 22nd sanctions package (EU) ·
    29. Denmark upholds "ghetto" evictions (Reuters) · 30. Cameroon
    separatist leader war-crimes trial opens in Norway (Reuters) · 31.
    RFE/RL shortwave lessons for Afghan girls (RFE/RL) · 32. FBI crime
    database suspected breach (Reuters) · 33. O'Hare radar delays snarl US
    flights (Reuters) · 34. US envoy "not certain" Israel military aid ends
    this year (Reuters) · 35. NATO vows to defend against space threats
    (Reuters) · 36. Asteroid eclipse imaged; Vera Rubin's first pictures
    (NASA) · 37. Landmine victims hit five-year high (Landmine Monitor) ·
    38. DR Congo rebels pull back from front line (Reuters).

## Timeline strip (THE DAY IN UTC)
00:10 Coalition strikes Hodeidah · 00:18 Shenzhou-24 lifts off ·
04:00 Java mine: 26 trapped confirmed · 06:30 Kospi closes down 6.2% ·
07:20 Bangladesh agrees 36% wage rise · 09:46 IRGC: two tankers hit mines.

## DATE CHECK (left out on purpose)
- Houthi drone hit on a Riyadh tower, 11 hurt — TUE 24 Nov, not today.
- Champions League results (Real Madrid 5-1 PSV) — TUESDAY's football.
- Nvidia's 31.5% surge — MONDAY 23 Nov; it fell 5.9% on Tuesday.
- Wed-night ties (Liverpool at Club Brugge) — not yet played at press time.

## Build
`main.py` (Pillow, DejaVu fonts) draws entry.png deterministically; if
Pillow is unavailable it falls back to copying the shipped entry.png.
Two runs produce identical md5. entry.png: 1024x1024, 180,258 bytes,
under the 1 MiB cap and under the 250 KB tie-break target.
