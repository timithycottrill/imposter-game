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

## Final delivery

- Final application commit: `4d7d794c1ad8475b32b08617f7fa91a4e589de5f`.
- Public deployment: https://timithycottrill.github.io/imposter-game/
- Final HTTPS verification: 102 full mobile browser rounds passed directly against the public URL, including offline reload/play, manifest/installability, keyboard controls, and privacy checks. No console errors or installability errors.
- APK build and Android lint: passed.
- Real APK installed on an Android 35 emulator; three complete offline rounds passed using native touch events. Count controls, hidden roles, correct answers, repeated New Round, restart, and count persistence passed. First launch was tested with Wi-Fi and mobile data disabled.
- APK: https://github.com/timithycottrill/imposter-game/releases/download/android-latest/IMPOSTER.apk
- Size: 4,044,150 bytes. SHA-256: `5dcd45f247c4cc78fe54ceb2dbf67edbb1608ac6b8b221802794421d3d09bc59`.
- Website test/deploy/live verification run: https://github.com/timithycottrill/imposter-game/actions/runs/39648801024
- Android build/lint/emulator/release run: https://github.com/timithycottrill/imposter-game/actions/runs/39648800737
- APK uses a development signing certificate. Physical Samsung hardware and Google Play distribution are not verified.

The Android accessibility test also found that the count output's accessible name omitted its numeric value. The label now includes the selected count; the affected browser and Android tests were repeated and passed.


## Picture and Topics Edition 1.1

- Application commit: `047d21b76d04b6c89d67ac8325da97ad2afa49ab`.
- 349 word/hint/picture entries; all 302 original hints revised, plus 47 holiday entries.
- 11 choices: Random Mix, Holidays, Animals, Food & Drink, Nature, Space, Sports & Games, Music, Places, Travel & Vehicles, Everyday Things.
- Eight engine tests passed, including 1,282 complete simulated rounds, picture coverage, distinct stable player scenes, topic filtering, and topic persistence.
- 102 complete mobile browser rounds passed against the live HTTPS site, with topic selection, offline Holiday play, offline picture caching, no private hint/word-picture disclosure to the imposter, unique player scene variants, and no console or installability errors.
- APK compilation and Android lint passed. Three full offline native touch rounds, first offline launch, controls, role privacy, correct answers, New Round, restart, and count persistence passed on an Android 35 emulator.
- The restart test now waits for the setup screen rather than assuming startup completes in two seconds.
- APK: https://github.com/timithycottrill/imposter-game/releases/download/android-v1.1.0/IMPOSTER.apk
- Size: 5,245,683 bytes. SHA-256: `83a45e4971fb970d632cc84fba09bda1803978e13c36fb3c5d96eca9738d25e0`.
- Web test/deploy/live check: https://github.com/timithycottrill/imposter-game/actions/runs/39687958585
- Android build/lint/offline check/release: https://github.com/timithycottrill/imposter-game/actions/runs/39687958633
- The picture subjects are bundled illustrations with procedurally randomized scenes, not a runtime image-generation API. Physical Samsung hardware testing remains unverified. The APK is development-signed; upgrading from a differently signed test build requires uninstalling that older build first.


## Semi-vague hints edition 1.1.1

- Approved level applied throughout the 349-entry library: Elephant → Herd; Pizza → Sharing; Dinosaur → Ancient; Penguin → Colony; Toothbrush → Routine.
- Application commit: `6ed384b6734392fbaf566cc15f5deb62f5e19f15`.
- All eight engine tests passed (including 1,282 simulated full rounds), as did production compilation, 102 complete mobile browser rounds against the public HTTPS URL, Android compilation/lint, and three offline Android emulator rounds including cold restart.
- Existing topics, images, private roles, and New Round behavior are preserved.
- Web verification: https://github.com/timithycottrill/imposter-game/actions/runs/39689620878
- Android verification: https://github.com/timithycottrill/imposter-game/actions/runs/39689620854
- APK: https://github.com/timithycottrill/imposter-game/releases/download/android-v1.1.1/IMPOSTER.apk
- Size: 5245751 bytes. Digest: `sha256:b7582e70220d26dfcb557489af467b7c131bc750a1afae9a31835113df622c9e`.
- Development-signed APK; physical Samsung hardware remains unverified.
