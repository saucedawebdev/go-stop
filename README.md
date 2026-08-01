# GoStop

A production-quality Progressive Web App that displays a full-screen visual cue card for **GO** and **STOP** communication. Designed for professionals who need a simple, distraction-free way to signal during activities.

No accounts. No analytics. No ads. No tracking. No databases. Just a perfect visual cue card.

## Features

- **Instant launch** — Full-screen bright green **GO** card on open
- **Tap to flip** — Smooth 3D horizontal flip animation (~450ms) between GO and STOP
- **Native feel** — Apple-inspired UI optimized for iPhone, responsive on iPad
- **Offline first** — Service worker caches all assets; works without internet after first visit
- **Installable PWA** — Add to Home Screen on iPhone for standalone, full-screen experience
- **Accessible** — VoiceOver, ARIA labels, keyboard support (Space / Enter), reduced motion
- **Haptics** — Gentle vibration on flip when supported
- **Zero dependencies** — Vanilla HTML, CSS, and JavaScript only

## Project Structure

```
GoStop/
├── index.html              # App shell and PWA meta tags
├── styles.css              # Layout, 3D flip, typography, accessibility
├── app.js                  # Flip logic, haptics, service worker registration
├── manifest.webmanifest    # PWA manifest
├── service-worker.js       # Offline caching
├── README.md
└── icons/
    ├── icon.svg            # Editable source icon
    ├── generate-icons.py   # Script to regenerate PNG sizes
    ├── icon-1024.png
    ├── icon-512.png
    ├── icon-512-maskable.png
    ├── icon-192.png
    ├── icon-180.png
    ├── apple-touch-icon.png
    ├── favicon-32.png
    └── favicon-16.png
```

## Running Locally

Because GoStop uses a service worker, run it through a local web server (not `file://`).

**Python 3:**

```bash
cd GoStop
python3 -m http.server 8080
```

Open [http://localhost:8080](http://localhost:8080) in your browser.

**Node.js (if installed):**

```bash
npx serve .
```

## Deploying to GitHub Pages

1. Create a new GitHub repository (e.g. `GoStop`).
2. Push all project files to the repository root (or `/docs` folder).
3. In GitHub: **Settings → Pages → Source** → select your branch and folder.
4. Wait for deployment. Your app will be live at:

   `https://<username>.github.io/<repo-name>/`

All asset paths are relative, so the app works from any subdirectory without configuration changes.

## Installing on iPhone

1. Open the deployed URL (or local server URL) in **Safari**.
2. Tap the **Share** button (square with arrow).
3. Scroll down and tap **Add to Home Screen**.
4. Tap **Add**.

GoStop launches in standalone mode — no browser chrome, full-screen cue card, portrait preferred.

### Tips

- Use Safari for installation (required for Add to Home Screen on iOS).
- After first launch with network, the app works fully offline.
- Flip the card by tapping anywhere on screen, or using Space / Enter with an external keyboard.

## Offline Support

The service worker precaches all HTML, CSS, JavaScript, manifest, and icon assets on first load. Subsequent visits serve from cache instantly, even without a network connection.

To update cached content after deploying changes, increment the `CACHE_NAME` version in `service-worker.js`.

## Accessibility

- **VoiceOver** — Live region announces GO / STOP on each flip
- **Keyboard** — Space and Enter flip the card; focus ring visible on keyboard navigation
- **Reduced motion** — 3D flip replaced with a smooth fade when system setting is enabled
- **Dynamic Type** — Fluid typography scales across iPhone SE through iPad
- **Safe areas** — Respects notches, Dynamic Island, and home indicator insets
- **Dark Mode** — Slightly adjusted green/red tones for OLED displays

## Replacing App Icons

1. Edit `icons/icon.svg` in any vector editor, **or** modify `icons/generate-icons.py`.
2. Regenerate PNG sizes:

   ```bash
   python3 -m pip install pillow   # one-time
   python3 icons/generate-icons.py
   ```

3. Icons are automatically referenced in `index.html` and `manifest.webmanifest`.

Required sizes: 1024, 512, 192, 180, 32, and 16 pixels.

## Colors

| State | Color   | Hex     |
|-------|---------|---------|
| GO    | Green   | `#34C759` |
| STOP  | Red     | `#FF3B30` |
| Text  | White   | `#FFFFFF` |

## License

MIT — use freely for personal and professional communication needs.
