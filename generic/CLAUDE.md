# Soul Winner — Setup Guide for Claude

> **For the person reading this:** give this file to Claude and ask for help setting up Soul Winner.
> - **Claude Code:** open this folder in Claude Code and say "help me set this up". Claude reads this file automatically.
> - **claude.ai (or the Claude app):** start a new chat, attach this file, and say "help me set this up".
>
> Plan on about 20–30 minutes. You'll need a Google account (for Firebase) and a free GitHub account (to put the app online).

---

## Instructions for Claude

You're helping a church volunteer set up **Soul Winner**, a free door-to-door evangelism map their soul-winning teams use on their phones. Assume the person is not technical. Your job is to get them from this folder of files to a working app their teams can open on their phones.

### How to guide them

- **One step at a time.** Give one small step, then wait for them to say it's done (or send a screenshot) before going on. Never paste the whole guide at once.
- **Say exactly where to click.** Use the button and menu names they'll see on screen. If what they see doesn't match (websites change), ask for a screenshot and adapt.
- **Plain words.** Say "database", not "RTDB". Explain a term once if you need it.
- **Check as you go.** At the end of each part, confirm it worked before moving on.
- **Edit only what this guide says to edit.** `index.html` is large (about 600 KB) and has whole libraries built in. Change only the settings blocks listed below and leave the rest alone.
- **Their Firebase settings aren't secret passwords**, but they are specific to their church. They can paste them to you. Never put one church's settings into another church's files.

### Can you edit the files directly?

- **If you have file tools (Claude Code):** make the edits yourself in `index.html` and `report.html`, then show them what changed.
- **If you're in a chat without file access:** don't ask them to paste `index.html` (it's too big). Have them edit in the GitHub website editor instead (Part 5 puts the files on GitHub first, then Part 6 edits them there). Give exact "find this line, replace it with this" instructions, and tell them to use the editor's search (Ctrl+F, or ⌘F on a Mac).

### Gather this first

Ask for these near the start (they can change them later):

1. **Church name** (shown at the top of the app).
2. **Town or neighborhood** where they usually go out. You'll turn it into map coordinates for the starting view.
3. **Teams:** how many, and what to call them. The default is Team A to Team E. Short names work best on a phone.

---

## Part 1 — Create a Firebase project

Firebase is Google's free service that stores visits and syncs them between every team member's phone.

1. Go to **https://console.firebase.google.com** and sign in with a Google account. A church account is better than a personal one, so the project outlives any one volunteer.
2. Click **Create a project** (or **Add project**). Name it after the church, e.g. `grace-baptist-soulwinning`.
3. When asked about **Google Analytics**, turn it off. It isn't needed.
4. Wait for "Your project is ready", then click **Continue**.

**Cost:** the free "Spark" plan is plenty (1 GB of storage, which is years of visits). Firebase doesn't ask for a credit card on this plan. If it ever asks them to upgrade or add billing, stop and tell them they don't need to.

## Part 2 — Turn on the database

1. In the left menu: **Build → Realtime Database**. Make sure it's **Realtime Database**, not "Firestore Database".
2. Click **Create Database**.
3. Choose the location closest to them (e.g. United States).
4. Choose **Start in locked mode**. You'll set the real rules in Part 4.
5. At the top of the database page there's a web address like
   `https://grace-baptist-soulwinning-default-rtdb.firebaseio.com`
   Have them copy it. This is the **databaseURL**.

## Part 3 — Turn on anonymous sign-in

This gives each phone its own ID without anyone needing a login.

1. Left menu: **Build → Authentication → Get started**.
2. Open the **Sign-in method** tab.
3. Click **Anonymous**, switch it **on**, and click **Save**.

## Part 4 — Set the database rules

Rules decide who can read and write. These rules allow only phones running the app (signed in anonymously) and block everyone else.

1. **Realtime Database → Rules** tab.
2. Replace everything in the box with:

```json
{
  "rules": {
    "visits":       { ".read": "auth != null", ".write": "auth != null" },
    "beacons":      { ".read": "auth != null", ".write": "auth != null" },
    "live":         { ".read": "auth != null", ".write": "auth != null" },
    "congregation": { ".read": "auth != null", ".write": "auth != null" }
  }
}
```

3. Click **Publish**.

## Part 5 — Register the web app and get the settings

1. Click the **gear icon ⚙️** (next to "Project Overview") → **Project settings**.
2. Scroll to **Your apps** and click the **web icon `</>`**.
3. App nickname: `soul-winner-web`. Leave "Firebase Hosting" unchecked. Click **Register app**.
4. A code box appears with a `firebaseConfig` that looks like this:

```js
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "grace-baptist-soulwinning.firebaseapp.com",
  databaseURL: "https://grace-baptist-soulwinning-default-rtdb.firebaseio.com",
  projectId: "grace-baptist-soulwinning",
  storageBucket: "...",
  messagingSenderId: "...",
  appId: "1:1234567890:web:abc123..."
};
```

5. Have them copy the whole thing and paste it to you. You need five values: **apiKey, authDomain, databaseURL, projectId, appId**. Ignore the others.
   - If `databaseURL` is missing from that box (this happens when the database was created after the app was registered), use the address from Part 2.

## Part 6 — Put their settings into the app

There are **two files** to edit: `index.html` (the app) and `report.html` (the reports page).

### 6a. Firebase settings in `index.html`

Search for `FIREBASE_CONFIG_DEFAULT`. Fill in the empty quotes:

```js
const FIREBASE_CONFIG_DEFAULT = {
  apiKey:            'AIzaSy...',
  authDomain:        'grace-baptist-soulwinning.firebaseapp.com',
  databaseURL:       'https://grace-baptist-soulwinning-default-rtdb.firebaseio.com',
  projectId:         'grace-baptist-soulwinning',
  appId:             '1:1234567890:web:abc123...',
};
```

### 6b. The same settings in `report.html`

Search for `Fallback`. Fill in the same five values in the `return { ... }` block right below it.

### 6c. Church settings in `index.html`

Search for `CHURCH_CONFIG`:

```js
const CHURCH_CONFIG = {
  defaultCenter: [41.7958, -71.5301], // ← latitude, longitude of their area
  defaultZoom:   13,                  // ← 13 shows a town, 15 a neighborhood
  defaultName: 'Soul Winner',         // ← church name
};
```

- Work out `defaultCenter` from the town they gave you (latitude first, then longitude; west longitudes are negative in the US). If you aren't sure of the coordinates, have them find their church on **https://www.latlong.net** and read off the numbers.
- The app also asks for a church name on first launch. `defaultName` is what shows if nobody types one.

### 6d. Teams (optional) — in both files

Search for `const TEAMS` in **index.html**. Each team has an `id`, a `label`, a `color` and a one-letter `letter` (shown on the live-location badge). Rename, add or remove teams as they asked. Keep each `id` short with no spaces (e.g. `'team-a'`) and never change an `id` after teams start logging visits, or old visits lose their team.

Then make the same change in `const TEAMS` in **report.html**. That list has `id`, `label` and `color` only, and it **must match** index.html.

Leave `OUTCOMES` alone unless they ask. The pin colors depend on the outcome wording.

## Part 7 — Put the app online (GitHub Pages, free)

Phones need the app at a secure web address (`https://…`), both for GPS and to install it.

1. Sign in at **https://github.com** (free account).
2. Click **+** (top right) → **New repository**. Name it e.g. `soulwinning`. Choose **Public** (free GitHub Pages needs a public repository). Click **Create repository**.
3. On the new page, click **uploading an existing file**. Drag in **every file from this folder**: `index.html`, `report.html`, `sw.js`, `manifest.json` and the three `.png` icons. Leave out this `CLAUDE.md` if they like; it does no harm either way. Click **Commit changes**.
4. Go to **Settings → Pages**. Under "Build and deployment", set Source to **Deploy from a branch**, Branch to **main** and the folder to **/ (root)**, then **Save**.
5. After a minute or two the page shows the address, like `https://their-username.github.io/soulwinning/`.

**If you're in a chat and they're editing on GitHub:** after uploading, they can make the Part 6 edits right on GitHub. Open the file, click the **pencil ✏️** (Edit), use Ctrl+F to find each spot, make the change, then **Commit changes**. The live site updates within a couple of minutes.

**Public repository note:** their Firebase settings will be visible in the code. That's normal for Firebase web apps, since the database rules from Part 4 are what keep strangers out. Mention it so it's not a surprise.

## Part 8 — Test it

Walk them through this on their own phone:

1. Open the address in the phone's browser and allow location access.
2. Pick a team at the top, tap the amber **LOG VISIT** button, choose an outcome, and **Save**.
   - ✅ Expected: "✓ Visit saved & synced", and the badge at the top right says **Synced**.
3. Open the same address on a **second phone or a computer**. The test visit should appear there within a few seconds.
4. Open **☰ → Reports & Analysis**. The visit should be listed.
5. Delete the test visit: tap its pin, then **Delete**.

### If something's wrong

| What they see | Likely cause | Fix |
|---|---|---|
| Badge says **Offline**, nothing syncs | Settings still blank or mistyped | Re-check Part 6a. Even one wrong character in `databaseURL` breaks it. |
| "Firebase auth failed" | Anonymous sign-in is off | Part 3 |
| Visits save on one phone but don't show on another | Rules not published, or the wrong database | Part 4. Also make sure `databaseURL` matches the address on the Realtime Database page. |
| "Permission denied" in the browser console | Rules are still in locked mode | Part 4 |
| Reports page says "No Firebase config found" | `report.html` not filled in | Part 6b |
| GPS never locks | Not on `https://`, or location blocked | Use the GitHub Pages address, and allow location in the phone's settings for the browser. |
| Old version still showing after an edit | Phone cached the app | Wait a couple of minutes, then close and reopen the app (or reload twice). |

## Part 9 — Hand it to the teams

Give them a short message to send to their soul-winning teams, filled in with their address:

> Open **https://their-username.github.io/soulwinning/** on your phone.
> - **iPhone:** in Safari, tap Share → **Add to Home Screen**.
> - **Android:** in Chrome, tap ⋮ → **Install app** (or Add to Home screen).
>
> Pick your team at the top. After each door, tap the amber **LOG VISIT** button, choose what happened, and Save. Press and hold on a house to log a visit right there. Everyone's visits show up on everyone's map.

Then remind them:
- **Back up now and then:** ☰ → **Export JSON** saves a copy of all visits.
- **Live location** (☰ → Share My Live Location) lets teams see each other on the map. It's off until someone turns it on.

---

## Reference: what's in this folder

| File | What it is | Edit it? |
|---|---|---|
| `index.html` | The whole app: map, buttons, syncing | Only the blocks in Part 6 |
| `report.html` | Reports: totals, streets, follow-up list | Only the blocks in Part 6 |
| `sw.js` | Lets the app work offline | No |
| `manifest.json` | Lets phones install it like an app | Optional: the app `name` |
| `icon-192.png`, `icon-512.png`, `apple-touch-icon.png` | App icons | Optional: replace with the church's own, same sizes |
| `CLAUDE.md` | This guide | No |
