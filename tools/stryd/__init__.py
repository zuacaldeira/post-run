"""Pulling the training plan out of Stryd PowerCenter.

Nothing in here runs in the browser. The app is a static page served with
`connect-src 'self'`, so it cannot call stryd.com at all: the CSP forbids it,
Stryd sends no CORS headers for our origin, and a credential shipped to a
browser is a published credential. So the sync runs on the server, holds the
token, and leaves a plain `plan.json` next to the app for it to read
same-origin.
"""
