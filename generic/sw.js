// ============================================================
//  Soul Winner PWA — Service Worker
//  Caches app shell + map tiles for offline use
// ============================================================

const CACHE_VERSION = 'sw-v1';
const TILE_CACHE    = 'map-tiles-v1';

// App shell files to cache on install
const SHELL_ASSETS = [
  './index.html',
  './manifest.json'
];

// ── Install: cache app shell ─────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_VERSION)
      .then(cache => cache.addAll(SHELL_ASSETS))
      .then(() => self.skipWaiting())
  );
});

// ── Activate: remove old caches ──────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(k => k !== CACHE_VERSION && k !== TILE_CACHE)
          .map(k => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: cache-first for tiles, network-first for app ──────
self.addEventListener('fetch', event => {
  const url = event.request.url;

  // Map tile requests — cache-first strategy
  if (
    url.includes('tile.openstreetmap.org') ||
    url.includes('basemaps.cartocdn.com') ||
    url.includes('tiles.stadiamaps.com')
  ) {
    event.respondWith(
      caches.open(TILE_CACHE).then(cache =>
        cache.match(event.request).then(cached => {
          if (cached) return cached;
          return fetch(event.request)
            .then(response => {
              // Only cache successful tile responses
              if (response.ok) {
                cache.put(event.request, response.clone());
              }
              return response;
            })
            .catch(() => new Response('', { status: 503 }));
        })
      )
    );
    return;
  }

  // Firebase / CDN requests — always network (no offline cache)
  if (
    url.includes('firebase') ||
    url.includes('googleapis.com') ||
    url.includes('unpkg.com') ||
    url.includes('cdnjs.cloudflare.com')
  ) {
    return; // Let browser handle normally
  }

  // App shell — network-first, fallback to cache
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_VERSION).then(c => c.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
