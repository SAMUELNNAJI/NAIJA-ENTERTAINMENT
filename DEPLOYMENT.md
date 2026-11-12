# Deployment Guide — The Nigerian Entrepreneur (Django) on a VPS

**Domain:** `thenigeriaentrepreneur.com`  
*(Note: you wrote "thenigeriaentreprenuer.com" in your request, but the project files use "thenigerianentrepreneur.com". Use the spelling your registrar actually has. The guide below uses `thenigeriaentrepreneur.com`.)*

This guide deploys the Django app on an Ubuntu VPS with **nginx + gunicorn + systemd + PostgreSQL + Certbot (Let's Encrypt SSL)**.

---

## Phase 0 — Before you start

1. **Buy/create a VPS** (Ubuntu 22.04 or 24.04 LTS recommended). Note its public IP.
2. **Point your domain DNS** at the VPS IP:
   - `A` record: `thenigeriaentrepreneur.com` → `<VPS_IP>`
   - `A` record (or CNAME): `www.thenigeriaentrepreneur.com` → `<VPS_IP>`
3. **Open these ports** on the VPS firewall / cloud security group:
   - `22` SSH, `80` HTTP, `443` HTTPS
4. Make sure you have the repo locally and can push to GitHub (or your Git host).

---

## Phase 1 — Prepare the VPS (run on the server)

SSH into your VPS as root (or a sudo user):

```bash
ssh root@<VPS_IP>
```

### 1.1 Update and install basics

```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv python3-dev \
    nginx postgresql postgresql-contrib libpq-dev git curl build-essential \
    ufw certbot python3-certbot-nginx
```

### 1.2 Configure firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
```

### 1.3 Create a deploy user

```bash
adduser --disabled-password --gecos "" naija
usermod -aG www-data naija
```

Switch to the `naija` user:

```bash
su - naija
```

---

## Phase 2 — Deploy the project code

### 2.1 Clone the repo

```bash
mkdir -p /opt/naija && cd /opt/naija
git clone <your-repo-url> .
```

### 2.2 Create virtualenv and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 2.3 Create production `.env`

Copy the template and fill in real values:

```bash
cp deploy/.env.production.example .env
nano .env   # edit with your real SECRET_KEY, DB password, ZeptoMail token, etc.
```

Generate a strong secret key:

```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 2.4 Set up PostgreSQL (recommended for production)

Back as root (exit the `naija` shell first):

```bash
sudo -u postgres psql
```

In the postgres prompt:

```sql
CREATE DATABASE naija;
CREATE USER naija WITH PASSWORD 'CHANGE_ME_STRONG_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE naija TO naija;
\q
```

Update `DATABASE_URL` in `/opt/naija/.env` to match:

```
DATABASE_URL=postgres://naija:CHANGE_ME_STRONG_PASSWORD@localhost:5432/naija
```

Switch back to `naija` user (`su - naija`) and run migrations:

```bash
cd /opt/naija
source .venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

Create a superuser (you'll use this to log into `/admin/`):

```bash
python manage.py createsuperuser
```

---

## Phase 3 — Run gunicorn via systemd

### 3.1 Install the systemd service (as root)

```bash
sudo cp /opt/naija/deploy/gunicorn.service /etc/systemd/system/naija.service
sudo systemctl daemon-reload
sudo systemctl enable --now naija
sudo systemctl status naija
```

Gunicorn now listens on `127.0.0.1:8000`.

### 3.2 Install nginx config (as root)

```bash
sudo cp /opt/naija/deploy/nginx.conf /etc/nginx/sites-available/thenigeriaentrepreneur.com
sudo ln -sf /etc/nginx/sites-available/thenigeriaentrepreneur.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable --now nginx
```

---

## Phase 4 — SSL with Certbot (Let's Encrypt)

Make sure your DNS A records are already pointing at the VPS (Phase 0).

```bash
sudo certbot --nginx -d thenigeriaentrepreneur.com -d www.thenigeriaentrepreneur.com
```

Follow the prompts (enter email, agree to TOS, choose redirect HTTP→HTTPS).

Certbot will:
- Obtain an SSL certificate
- Update your nginx config to listen on 443
- Set up auto-renewal

Test auto-renewal:

```bash
sudo certbot renew --dry-run
```

---

## Phase 5 — Verify the site

Visit: `https://thenigeriaentrepreneur.com`

- Homepage should load.
- Admin: `https://thenigeriaentrepreneur.com/admin/` (login with the superuser you created).
- Static/CSS should load (check browser dev tools for 404s on `/static/`).

---

## Phase 6 — Ongoing maintenance

### Deploy new code

```bash
ssh naija@<VPS_IP>
cd /opt/naija
git pull
source .venv/bin/activate
pip install -r requirements.txt   # if requirements changed
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart naija
```

### Restart after changes

```bash
sudo systemctl restart naija
sudo systemctl reload nginx
```

### View logs

```bash
sudo journalctl -u naija -f          # gunicorn / app logs
sudo tail -f /var/log/nginx/error.log   # nginx errors
```

---

## Important settings notes

Your `config/settings.py` already supports production via env vars:

| Variable | Production value |
|---|---|
| `DJANGO_DEBUG` | `0` |
| `DJANGO_SECRET_KEY` | long random key (never commit) |
| `DJANGO_ALLOWED_HOSTS` | `thenigeriaentrepreneur.com,www.thenigeriaentrepreneur.com,<VPS_IP>` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://thenigeriaentrepreneur.com,https://www.thenigeriaentrepreneur.com` |
| `DATABASE_URL` | postgres URL (or leave unset to keep sqlite) |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` |
| `ZEPTOMAIL_SMTP_TOKEN` | your real ZeptoMail SMTP token |

**Domain spelling:** Make sure every place that references the domain (`ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `PUBLIC_SITE_URL`, Certbot, nginx `server_name`) uses the exact domain registered with your registrar (`thenigeriaentrepreneur.com` vs `thenigeriaentreprenuer.com`).
