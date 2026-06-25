# Assam Tea Company Website

Streamlit site for Assam Tea Company: home, products, checkout, legal pages,
and an order-management admin page, backed by a local SQLite database.

## Run locally

```bash
python -m pip install -r requirements.txt
cp .env.example .env   # then fill in ADMIN_PASSWORD (and Razorpay keys if using online payment)
streamlit run app.py
```

Environment variables are read directly from the shell, so either `export`
them before running, or use a tool like `python-dotenv`/`direnv` to load
`.env` automatically - Streamlit itself does not read `.env` files.

All visible website text, prices, stock status, and legal-page content are
editable in `data/business.json`. Business details (phone, FSSAI/GST number,
address) and legal-page bodies in that file currently contain
`REPLACE WITH...` placeholders that must be filled in with real information
before launch.

## Required environment variables

| Variable | Required? | Purpose |
|---|---|---|
| `ADMIN_PASSWORD` | Yes, to use `/Admin` | Gates the order-management page at `pages/Admin.py`. |
| `RAZORPAY_KEY_ID` / `RAZORPAY_KEY_SECRET` | No | If set, checkout creates a real Razorpay payment link. If unset, checkout falls back to the manual "we'll call you" flow. |
| `DATABASE_URL` | No | If set (e.g. `postgresql://user:pass@host/dbname`), orders are stored there instead of local SQLite. Required if deploying to Streamlit Community Cloud (see below). |
| `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` / `FROM_EMAIL` | No | If all of `SMTP_HOST`/`SMTP_USER`/`SMTP_PASSWORD` are set, customers who enter an email at checkout receive an order confirmation. If unset, checkout works the same but skips sending email. |

## Order data

By default, orders submitted at checkout are saved to `data/orders.db`
(SQLite, created automatically, gitignored). View and manage them at the
`/Admin` page of the running app.

If `DATABASE_URL` is set, orders go to that database instead (via
SQLAlchemy - Postgres is the tested target, e.g. a free-tier instance on
Supabase, Railway, or Neon). The same `backend.py` functions work
transparently against either backend; nothing else in the app changes.

## Deploying

**Option A - Streamlit Community Cloud (simplest):** push this repo to
GitHub, connect it at share.streamlit.io, set `app.py` as the entry point,
and add secrets under the app's "Secrets" settings in TOML format, e.g.:

```toml
ADMIN_PASSWORD = "your-password"
RAZORPAY_KEY_ID = "..."
RAZORPAY_KEY_SECRET = "..."
DATABASE_URL = "postgresql://user:pass@host/dbname"
```

**Important:** on Streamlit Community Cloud, the local filesystem is not
durable storage - it can reset on redeploy, which would silently wipe
`data/orders.db`. Set `DATABASE_URL` to a real hosted Postgres database
before relying on this deployment target for real customer orders. If you
self-host instead (a VM with persistent disk), local SQLite is fine as-is
and `DATABASE_URL` can stay unset.

**Option B - your own server/VM:** install `requirements.txt`, set the
environment variables above, and run:

```bash
streamlit run app.py --server.port 80 --server.address 0.0.0.0
```

behind a reverse proxy (e.g. Caddy or nginx) that provides HTTPS.

## Testing

```bash
python -m pip install -r requirements-dev.txt
pytest
```

The suite covers: every page rendering without exceptions, checkout total
calculation, the order backend (save/list/update against a temp SQLite db),
and graceful fallback behavior for the optional email integration when
unconfigured. Two regression tests guard against bugs found during manual
QA: the custom footer must never use a `<footer>` tag (it collided with the
chrome-hiding CSS rule and made the footer invisible), and the add-to-bag
handler must clear `st.query_params` (otherwise the router bounced back to
the product page instead of reaching checkout).

## Monitoring

`notifications.py` logs (via Python's standard `logging` module) whenever
an order-confirmation email fails to send, without interrupting checkout -
the order is already saved by that point regardless. `backend.py` raises
normally on database errors, since a failed order save is something the
customer needs to see (they'd otherwise believe they ordered successfully).

Where to see these logs depends on your hosting choice:
- **Streamlit Community Cloud:** open the app, click "Manage app" (bottom
  right) to view the live log stream.
- **Self-hosted VM:** logs go to stdout/stderr of the `streamlit run`
  process - capture them with your process manager (e.g. `journalctl -u
  <service>` if running under systemd, or redirect to a file).

There is no external error-tracking/alerting service wired up (e.g. Sentry).
For a small-scale site this is optional; add one later if order volume
grows enough that you need to be paged on failures rather than checking
logs manually.

## SEO notes

Per-page meta description / Open Graph tags are injected automatically.
`static/robots.txt` exists but Streamlit serves it at `/app/static/robots.txt`,
not the domain root `/robots.txt` that crawlers expect by convention - true
root-level `robots.txt`/`sitemap.xml` support would require a reverse proxy
rule mapping `/robots.txt` to that file, or moving off Streamlit's built-in
server.
