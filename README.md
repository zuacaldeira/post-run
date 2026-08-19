# Post-Run — install on your phone

Two ways. Start with A; it takes about five minutes and needs nothing installed.

---

## A. Home-screen app (PWA) — recommended

A service worker needs HTTPS, so the files have to be served from somewhere. GitHub Pages
is free and quickest.

1. Create a new **public** repo (e.g. `post-run`) and upload every file in this folder to
   the repo root — `index.html`, `bg.mp4`, `poster.jpg`, `sw.js`, `manifest.webmanifest`
   and the three icons.
2. Repo **Settings → Pages → Source: Deploy from a branch**, branch `main`, folder `/root`.
   Wait ~1 minute for the URL: `https://<user>.github.io/post-run/`
3. Open that URL in **Chrome on your phone** → menu (⋮) → **Add to Home screen** /
   **Install app**.

You get an icon, no browser chrome, and the whole routine cached offline. Only the
YouTube demonstrations need a connection.

### What you lose versus the APK
- The screen-awake flag is `navigator.wakeLock` instead of the native one — it works in
  Chrome but Android may still dim under aggressive battery saving.
- No launcher presence beyond the home-screen icon.

Everything else — autopilot, sound cues, vibration, the flip, the log — is identical.

---

## B. Native APK

Needs Android Studio (~1 GB) or the command-line SDK, on a computer.

**Android Studio:** File → Open → select the `PostRunRoutine` folder → let it sync (it
generates the Gradle wrapper) → plug the phone in with USB debugging on → Run ▶.

**Command line**, if you already have a JDK 17 and the Android SDK:

```bash
cd PostRunRoutine
gradle wrapper            # only needed once; the wrapper JAR is not shipped here
./gradlew assembleDebug
# APK at app/build/outputs/apk/debug/app-debug.apk
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

To sideload without a cable: copy the APK to the phone, tap it, and allow
"Install unknown apps" for your file manager.

Gains over the PWA: `FLAG_KEEP_SCREEN_ON` (reliable during long holds), fullscreen video
handling, and YouTube links opening in the YouTube app.

---

## C. Just the file, no install

Copy `index.html`, `bg.mp4` and `poster.jpg` into one folder on the phone and open the
HTML with Chrome. Works, but no icon and no offline guarantee — fine for a one-off try.
