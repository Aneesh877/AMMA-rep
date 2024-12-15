// Define a cache name
const CACHE_NAME = 'ani-movies-games-cache-v1';

// List of assets to cache
const urlsToCache = [
    '/',
    '/static/logo.jpg',
    '/static/py/app.py',
    '/dashboard',
    '/home',
    '/login',
    '/register'
];

// Install event
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            console.log('Opened cache');
            return cache.addAll(urlsToCache);
        })
    );
});

// Fetch event
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            // If a cached response is found, return it; otherwise fetch from the network
            return response || fetch(event.request);
        })
    );
});

// Activate event
self.addEventListener('activate', event => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    if (!cacheWhitelist.includes(cacheName)) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
