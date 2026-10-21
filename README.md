# IMPOSTER

- [Play the verified HTTPS game](https://timithycottrill.github.io/imposter-game/)
- [Download IMPOSTER.apk](https://github.com/timithycottrill/imposter-game/releases/download/android-latest/IMPOSTER.apk)
- [Android release details](https://github.com/timithycottrill/imposter-game/releases/tag/android-latest)

Minimal offline pass-and-play party game for 3–20 players. React, TypeScript, Vite, a PWA, and a Capacitor Android app. No backend, accounts, analytics, or external gameplay services.

## Play

Choose 3–20 players and tap **Start Round**. Pass the phone to each player and let them tap **Reveal** privately. Exactly one sees **IMPOSTER**; everyone else sees the same word. Hide the role before passing the phone. After the last player, discuss the single broad hint together, then reveal the answer. **New Round** keeps the player count and independently randomizes another round. Change player count from the answer screen.

Only player count is saved in local storage. Reloading returns to setup. Switching apps hides an open private role. All gameplay information stays on the device. Like any client-side game, the word data can be inspected through developer tools; this is privacy during normal play, not a security boundary against inspecting the code.

## Development

Node 24 recommended.

```sh
npm ci
npm test
npm run build
npm run preview
```

The engine in `src/engine.ts` is independent of React. Its central state machine only permits valid transitions. NEW_ROUND is an event from ANSWER back to PASS_PHONE, with newly generated round data, rather than a screen that could retain stale role visibility. Random indices use crypto rejection sampling, with a non-cryptographic fallback for old WebViews. The 302 curated word/hint pairs are selected together and the immediately preceding word is excluded.

## Tests

```sh
npm test
pip install playwright
python -m playwright install chromium
CHROMIUM_PATH=/path/to/chromium npm run test:ui
```

Start `npm run preview` first for UI tests. `GAME_URL` can target the HTTPS deployment or a repository subpath. Six engine tests cover 1,150 complete rounds, count limits, rejection sampling, privacy, resets, and consecutive same-imposter selection. Playwright exercises 102 full touchscreen rounds, count changes, keyboard controls, private transitions, manifest/installability checks, offline reload and a full offline round, and multiple mobile viewports. The tests emit `artifacts/ui-results.json` and a setup screenshot.

Local production browser tests passed with Chromium at 360×780 (touch, DPR 3), plus layout checks at 360×640, 412×915, 320×568, and 780×360. No console errors or detected transition disclosures. Actual Samsung hardware installation remains a separate verification step.

## GitHub Pages

`.github/workflows/pages.yml` builds, tests, and deploys `dist`. All Vite, manifest, and service worker paths are relative, supporting `https://timithycottrill.github.io/imposter-game/`. In repository Settings → Pages, select **GitHub Actions** if automatic configuration is unavailable. HTTPS is provided by GitHub Pages. A workflow being present does not establish that deployment is live; check the completed Pages deployment and test the resulting URL.

## Samsung installation

Open the deployed HTTPS address in Chrome. Let the first load finish, then use Chrome’s menu → **Install app** or **Add to Home screen**. Launch it from the installed icon. It runs standalone and works offline after the service worker has cached the first load. Browser installation availability depends on Chrome and device settings.

For an APK: download the provided `.apk`, open it on Android, and allow installation from the browser or file manager when prompted. The development APK is signed with an Android debug certificate and is not a Play Store release. It bundles the game locally, so first launch also works offline. Android 7.0+ and an up-to-date Android System WebView are required.

## Android builds

```sh
npm run build
npm run android:sync
cd android
./gradlew assembleDebug lintDebug
```

Requires a full JDK 21 and Android SDK 36. `.github/workflows/android.yml` produces a downloadable `imposter-android-apk` artifact. Debug signing keys are machine-specific; builds from another machine may require uninstalling the previous debug app before installing. Local build files, signing keys, and credentials are excluded from Git.
