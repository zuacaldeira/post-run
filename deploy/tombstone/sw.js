/* The last service worker this origin will ever serve.
 *
 * A redirect cannot reach an installed app: its own worker answers first and
 * goes on serving a cache of a product that no longer exists. So the final act
 * of this one is to take itself out -- drop every cache, unregister, and let
 * the page underneath do the rest.
 */
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (e) => e.waitUntil((async () => {
  for (const key of await caches.keys()) await caches.delete(key);
  await self.registration.unregister();
  for (const client of await self.clients.matchAll({ type: "window" })) {
    client.navigate(client.url);
  }
})()));
