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

---

## D. Working on it on your computer

```bash
git clone https://github.com/zuacaldeira/post-run.git
cd post-run
git checkout claude/video-full-width-card-aueowt
```

It is one HTML file plus a service worker -- no build step, no dependencies, no
`npm install`. Edit `index.html`, reload, done.

### Serve it, do not open the file

```bash
python3 -m http.server 8000        # then http://localhost:8000/
```

Opening `index.html` directly (a `file://` URL) looks like it works, but service
workers do not register outside a secure origin, so you silently lose offline
mode, caching and the self-update -- and you will be debugging a different app
from the one you deploy. `localhost` counts as secure, so a plain local server
gives you the real thing. Any static server does; the one above ships with
Python and serves every MIME type this app needs.

### The service worker will lie to you while you edit

The app deliberately serves itself from cache and only picks up a change on the
*next* load. That is correct in production and maddening in an editor: you save,
reload, and see the old page. In DevTools → Application → Service Workers, tick
**Update on reload** and **Bypass for network** while you work. To get back to a
clean slate, Application → Storage → **Clear site data** unregisters the worker
and drops the cache.

The self-reload also holds off while a session is running or any card has been
touched -- so if you clicked a card to test something, the update is waiting on
purpose, not broken. Reset the board or reload by hand.

### Check it the way it ships

```bash
docker build -t post-run:dev .
docker run --rm -p 8080:80 post-run:dev      # http://localhost:8080
```

Same nginx, same headers, same CSP as production. Worth doing before you push
anything that adds an external script, font or image: the CSP in
`deploy/nginx.conf` allows this origin plus YouTube and nothing else, so a new
third-party URL fails here first rather than on the server. `deploy/README.md`
covers deployment itself.

### Claude Code locally

```bash
npm install -g @anthropic-ai/claude-code
cd post-run && claude
```

Same assistant as this session, running against the working copy on your machine.
