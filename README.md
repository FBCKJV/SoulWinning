# ✝ Soul Winner — Door-to-Door Evangelism Map PWA

A free, open-source Progressive Web App for church soul-winning teams.
Track door-to-door visits on a live map, sync across all team devices in real time,
and see at a glance where your teams have been.

![Soul Winner App Screenshot](https://via.placeholder.com/800x450/0f1724/f59e0b?text=Soul+Winner+PWA)

---

## Features

- 📍 **One-tap visit logging** at your GPS location
- 🗺️ **Real-time map** showing all team visits across all devices
- 🌡️ **Heatmap layer** revealing coverage density at a glance
- 👥 **Multi-team support** with color-coded markers per team
- 🔍 **Filter by team** using the chip bar on the map
- 📊 **Stats bar** — total visits, today's count, per-team breakdown
- 📴 **Full offline mode** — visits are queued and auto-synced when back online
- 📤 **JSON export/import** for backup and cross-device data
- 🌙 **Dark theme** — easy to read at night on a doorstep
- 📲 **Installable PWA** — add to home screen, works like a native app

---

## Quick Setup (15 minutes)

### Step 1 — Get the Files

Download or clone this repository:
```bash
git clone https://github.com/YOURUSERNAME/church-soulwinner.git
```

Or just download `index.html`, `sw.js`, and `manifest.json`.

---

### Step 2 — Create a Firebase Project (free)

1. Go to **https://console.firebase.google.com**
2. Click **"Add project"** → name it (e.g. `grace-soulwinner`) → Create
3. Disable Google Analytics when asked (not needed)

---

### Step 3 — Enable Realtime Database

1. In the left sidebar → **Build → Realtime Database**
2. Click **"Create Database"**
3. Choose your nearest region
4. Start in **"Test mode"** (we'll secure it in Step 5)
5. Copy the database URL — it looks like:
   `https://YOUR-PROJECT-default-rtdb.firebaseio.com`

---

### Step 4 — Enable Anonymous Authentication

1. Sidebar → **Build → Authentication → Get started**
2. Click **"Sign-in method"** tab
3. Enable **Anonymous** → Save

This lets each phone/device get a unique ID without any login form.

---

### Step 5 — Set Security Rules

In Realtime Database → **Rules** tab, replace everything with:

```json
{
  "rules": {
    "visits": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "congregation": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

Click **Publish**. This means only your app's authenticated users (anonymous sign-in counts) can read or write data — random people on the internet cannot.

---

### Step 6 — Get Your Firebase Config

1. Click the ⚙️ gear icon → **Project settings**
2. Scroll to **"Your apps"** section → click **"</>"** to add a web app
3. App nickname: `soul-winner-web` → **Register app**
4. You'll see a `firebaseConfig` object — copy the values

---

### Step 7 — Add Your Config to the App

**Option A — Edit the HTML file directly** (best for permanent deployment):

Open `index.html` and find `FIREBASE_CONFIG_DEFAULT` (search for it). Replace the empty strings with your values:

```javascript
const FIREBASE_CONFIG_DEFAULT = {
  apiKey:      "AIzaSyABC...",
  authDomain:  "grace-soulwinner.firebaseapp.com",
  databaseURL: "https://grace-soulwinner-default-rtdb.firebaseio.com",
  projectId:   "grace-soulwinner",
  appId:       "1:123456789:web:abc123def456",
};
```

**Option B — Use the in-app config editor** (no code editing):

Open the app → tap ☰ → **Firebase Setup** → paste your values → Save & Connect.
Config is stored in the browser's localStorage. Good for testing, but Option A is preferred for permanent installs.

---

### Step 8 — Customize for Your Church

Open `index.html` and search for these config sections:

**`CHURCH_CONFIG`** — Set your map starting location:
```javascript
const CHURCH_CONFIG = {
  defaultCenter: [41.7958, -71.5301], // ← Your church's lat/lng
  defaultZoom: 13,
  defaultName: 'Grace Baptist',       // ← Your church name
};
```

Find your lat/lng at: https://www.latlong.net/

**`TEAMS`** — Add/rename/remove teams:
```javascript
const TEAMS = [
  { id: 'team-a', label: 'Team A', color: '#f59e0b' },
  { id: 'team-b', label: 'Team B', color: '#3b82f6' },
  // Add as many as you need!
  { id: 'pastor', label: 'Pastor\'s Team', color: '#22c55e' },
];
```

**`OUTCOMES`** — Customize the quick-select visit outcomes:
```javascript
const OUTCOMES = [
  { id: 'gospel',  emoji: '✝️', label: 'Gospel shared' },
  // Add any outcome types relevant to your ministry
];
```

---

### Step 9 — Deploy to GitHub Pages

1. Create a new GitHub repository (e.g. `church-soulwinner`)
2. Upload your three files: `index.html`, `sw.js`, `manifest.json`
3. Go to **Settings → Pages**
4. Source: **"Deploy from a branch"** → Branch: `main` → Folder: `/ (root)`
5. Click Save — your app will be live at:
   **`https://YOURUSERNAME.github.io/church-soulwinner/`**

Share that URL with your soul-winning teams. Each person:
1. Opens the URL in their browser
2. Taps **"Add to Home Screen"** (iOS: Share → Add to Home Screen; Android: browser menu → Install)
3. The app installs like a native app — works offline too

---

## How It Works for Teams

Each team member:
1. Opens the app on their phone
2. Selects their team from the dropdown
3. Walks to a door, knocks
4. After visiting, taps the **amber 📍 button**
5. Chooses an outcome (Gospel shared, Left tract, Not home, etc.)
6. Optionally adds a note → **Save Visit**

The visit appears instantly on everyone's map. Teams can see where others have been and avoid doubling up streets.

---

## Sharing with Another Church

Each church needs their own Firebase project (Steps 2–6 above). The free Firebase Spark plan supports:
- 1 GB stored data (plenty for years of visits)
- 10 GB/month data transfer
- 100 simultaneous connections

Steps for another church:
1. Create their own Firebase project
2. Download the same `index.html` / `sw.js` / `manifest.json`
3. Add their own Firebase config (Step 7, Option A or B)
4. Change `CHURCH_CONFIG.defaultCenter` to their town
5. Deploy to their own GitHub Pages or any static host

Their data stays completely separate from yours.

---

## File Structure

```
church-soulwinner/
├── index.html     ← The entire app (map, UI, logic)
├── sw.js          ← Service worker (offline + tile caching)
├── manifest.json  ← PWA install manifest
└── README.md      ← This file
```

---

## Data Structure (Firebase)

```json
{
  "visits": {
    "VISIT_ID": {
      "id":        "abc123",
      "lat":       41.7958,
      "lng":       -71.5301,
      "timestamp": 1719158400000,
      "notes":     "Gospel shared · Family asked for follow-up",
      "team":      "team-a",
      "userId":    "firebase-anon-uid"
    }
  }
}
```

---

## Privacy Notes

- No email, name, or personal information is ever collected
- Anonymous Firebase authentication assigns a random device ID only
- GPS coordinates are only stored at the moment you tap "Log Visit"
- Your Firebase database is private to your church (rules require authentication)
- All data can be exported and deleted at any time

---

## Troubleshooting

**Map is blank / no tiles**
→ Check your internet connection. If offline, the map shows cached tiles from previous sessions.

**"Firebase auth failed"**
→ Double-check your `databaseURL` and `apiKey` values. Ensure Anonymous Auth is enabled in your Firebase console.

**GPS not working on iPhone**
→ iOS requires HTTPS for location access. GitHub Pages uses HTTPS automatically. If testing locally, use `localhost`.

**Visits not syncing**
→ Check the sync badge (top-right). If it shows "Offline", you have no internet connection. Visits are queued and will sync automatically when you're back online.

**"Storage full" toast**
→ The app auto-trims the oldest 25% of locally cached visits to free space. All data remains in Firebase. Export a backup first if concerned.

---

## License

MIT License — free to use, modify, and share for any ministry purpose.

Built with ❤️ for the local church.
