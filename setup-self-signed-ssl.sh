#!/bin/bash

# Self-Signed SSL Certificate Setup
# Use this when you don't have a domain name

SERVER_IP=${1:-"your-server-ip"}

echo "🔐 Creating self-signed SSL certificate for IP: $SERVER_IP"

# Create SSL directory
mkdir -p ssl

# Generate self-signed certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout ssl/privkey.pem \
  -out ssl/fullchain.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=$SERVER_IP" \
  -addext "subjectAltName=IP:$SERVER_IP"

if [ $? -eq 0 ]; then
  echo "✅ Self-signed certificate created successfully!"
  echo "📁 Certificate location: ./ssl/"
  echo ""
  echo "⚠️  WARNING: This is a self-signed certificate."
  echo "   Browsers will show a security warning."
  echo "   This is OK for development/testing."
  echo ""
  echo "📝 Next steps:"
  echo "   1. Update nginx.conf to use self-signed certificate"
  echo "   2. Restart nginx: docker compose restart nginx"
else
  echo "❌ Failed to create certificate"
  exit 1
fi