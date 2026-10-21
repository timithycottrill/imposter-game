# Validation record

- TypeScript strict check and Vite production build: passed.
- Node engine suite: 6 tests passed; 1,150 full rounds, including all 3–20 player counts and 150 consecutive New Round cycles at 20 players.
- Playwright production UI: 102 complete touchscreen rounds passed.
- Exactly one imposter, identical ordinary-player word, no word on imposter UI, no hint in private screens: passed.
- Start, count controls and bounds, next player, final-player transition, answer identity, and repeated New Round: passed.
- Count persistence and reload returning to hidden setup: passed.
- Keyboard Enter/Space controls, rapid double tap privacy guard, app-switch hiding: passed.
- Mobile layout checks: 360×780, 360×640, 412×915, 320×568, 780×360; no scrolling detected on checked screens.
- PWA manifest, icons, service worker control, Chromium installability diagnostics: passed (no installability errors).
- Network disabled, page reload, full round, and New Round: passed.
- JavaScript console errors / detected role disclosures: zero.

A touchscreen test caught an incorrect `click.detail` guard that rejected successive taps at the same button position. The guard was removed and replaced with a short time gate; the full suite then passed. Installability tests use a persistent Chromium profile because private browser contexts cannot install PWAs.

Actual Galaxy hardware and Samsung-specific installation UI have not been tested. Publication and Android results are recorded separately when verified; local PWA tests do not imply a successful deployment or Android execution.
