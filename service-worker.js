/**
 * GoStop Service Worker
 * Offline-first caching for all app assets.
 * Paths resolve relative to this script so the app works on GitHub Pages subpaths.
 */

const CACHE_NAME = 'gostop-v2';

/** Resolve a path relative to the service worker script location. */
function asset(path) {
  return new URL(path.replace(/^\.\//, ''), self.location.href).href;
}

/** All assets to precache for offline use */
const PRECACHE_ASSETS = [
  asset('./'),
  asset('./index.html'),
  asset('./styles.css'),
  asset('./app.js'),
  asset('./manifest.webmanifest'),
  asset('./icons/icon-192.png'),
  asset('./icons/icon-512.png'),
  asset('./icons/icon-512-maskable.png'),
  asset('./icons/icon-1024.png'),
  asset('./icons/icon-180.png'),
  asset('./icons/apple-touch-icon.png'),
  asset('./icons/favicon-32.png'),
  asset('./icons/favicon-16.png'),
];

/**
 * Install: precache all assets.
 * @param {ExtendableEvent} event
 */
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then(function (cache) {
        return cache.addAll(PRECACHE_ASSETS);
      })
      .then(function () {
        return self.skipWaiting();
      })
  );
});

/**
 * Activate: remove old caches.
 * @param {ExtendableEvent} event
 */
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches
      .keys()
      .then(function (cacheNames) {
        return Promise.all(
          cacheNames
            .filter(function (name) {
              return name !== CACHE_NAME;
            })
            .map(function (name) {
              return caches.delete(name);
            })
        );
      })
      .then(function () {
        return self.clients.claim();
      })
  );
});

/**
 * Fetch: serve from cache, fall back to network.
 * @param {FetchEvent} event
 */
self.addEventListener('fetch', function (event) {
  if (event.request.method !== 'GET') return;

  event.respondWith(
    caches.match(event.request).then(function (cached) {
      if (cached) return cached;

      return fetch(event.request).then(function (response) {
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }

        var responseClone = response.clone();
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(event.request, responseClone);
        });

        return response;
      });
    })
  );
});
