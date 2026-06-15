#!/bin/bash
# deploy.sh — one-command setup for AWS EC2 (Ubuntu 22.04 LTS, t2.micro)
#
# Before running:
#   1. Open ports 22, 80, 443 in your EC2 Security Group
#   2. Point your domain's A record to this instance's public IP
#   3. Upload your project files (or git clone from your repo)
#
# Run with:  chmod +x deploy.sh && ./deploy.sh

set -e

echo "==> Updating system packages..."
sudo apt-get update -y && sudo apt-get upgrade -y

echo "==> Installing Docker..."
curl -fsSL https://get.docker.com | sudo bash
sudo usermod -aG docker "$USER"

echo "==> Installing Docker Compose plugin..."
sudo apt-get install -y docker-compose-plugin

echo "==> Installing Nginx..."
sudo apt-get install -y nginx

echo "==> Installing Certbot..."
sudo apt-get install -y certbot python3-certbot-nginx

# ── App setup ──────────────────────────────────────────────────────────────────
echo ""
read -rp "Enter your domain name (e.g. connectiq.example.com): " DOMAIN

# Create .env from template if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "==> Opening .env for editing — fill in your real credentials, then save and exit."
    sleep 2
    nano .env
fi

# ── Nginx config ───────────────────────────────────────────────────────────────
echo "==> Configuring Nginx for $DOMAIN..."
sudo cp nginx/nginx.conf /etc/nginx/sites-available/connectiq
sudo sed -i "s/YOUR_DOMAIN/$DOMAIN/g" /etc/nginx/sites-available/connectiq
sudo ln -sf /etc/nginx/sites-available/connectiq /etc/nginx/sites-enabled/connectiq
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# ── SSL certificate ────────────────────────────────────────────────────────────
echo "==> Obtaining SSL certificate from Let's Encrypt..."
read -rp "Enter your email (for Let's Encrypt expiry notices): " ADMIN_EMAIL
sudo certbot --nginx \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" \
    --non-interactive \
    --agree-tos \
    -m "$ADMIN_EMAIL"

# Auto-renew cron (certbot installs its own timer, this is a belt-and-suspenders backup)
(crontab -l 2>/dev/null; echo "0 3 * * * sudo certbot renew --quiet && sudo systemctl reload nginx") | crontab -

# ── Start app ──────────────────────────────────────────────────────────────────
echo "==> Building and starting the app with Docker Compose..."
sudo docker compose up -d --build

echo ""
echo "=========================================="
echo " Deployment complete!"
echo " Visit: https://$DOMAIN"
echo "=========================================="
echo ""
echo "Useful commands:"
echo "  View logs:    sudo docker compose logs -f"
echo "  Restart app:  sudo docker compose restart"
echo "  Update app:   git pull && sudo docker compose up -d --build"
