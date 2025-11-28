#!/bin/bash
#
# Fix SSH Slow Connection Issues
#
# This script fixes common SSH performance issues by disabling
# DNS reverse lookup, GSSAPI authentication, and other slow features.
#
# Run this script on your SERVER (not in CI/CD):
#   sudo bash scripts/fix-ssh-slow-connection.sh
#

set -e

echo "🔧 Fixing SSH slow connection issues..."
echo ""

# Backup current sshd_config
BACKUP_FILE="/etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)"
echo "📋 Creating backup: $BACKUP_FILE"
sudo cp /etc/ssh/sshd_config "$BACKUP_FILE"

# Create temporary file for new config
TMP_FILE=$(mktemp)

echo "⚙️  Updating SSH configuration..."

# Disable DNS reverse lookup (MAJOR performance issue)
if ! sudo grep -q "^UseDNS no" /etc/ssh/sshd_config; then
    echo "  - Disabling DNS reverse lookup (UseDNS no)"
    echo "UseDNS no" | sudo tee -a /etc/ssh/sshd_config > /dev/null
else
    echo "  ✓ DNS reverse lookup already disabled"
fi

# Disable GSSAPI authentication (can cause delays)
if ! sudo grep -q "^GSSAPIAuthentication no" /etc/ssh/sshd_config; then
    echo "  - Disabling GSSAPI authentication"
    echo "GSSAPIAuthentication no" | sudo tee -a /etc/ssh/sshd_config > /dev/null
else
    echo "  ✓ GSSAPI authentication already disabled"
fi

# Speed up key exchange
if ! sudo grep -q "^GSSAPIKeyExchange no" /etc/ssh/sshd_config; then
    echo "  - Disabling GSSAPI key exchange"
    echo "GSSAPIKeyExchange no" | sudo tee -a /etc/ssh/sshd_config > /dev/null
else
    echo "  ✓ GSSAPI key exchange already disabled"
fi

# Optional: Increase MaxStartups for concurrent connections
if ! sudo grep -q "^MaxStartups" /etc/ssh/sshd_config; then
    echo "  - Setting MaxStartups to 10:30:60"
    echo "MaxStartups 10:30:60" | sudo tee -a /etc/ssh/sshd_config > /dev/null
else
    echo "  ✓ MaxStartups already configured"
fi

# Optional: Set LoginGraceTime to reduce hanging connections
if ! sudo grep -q "^LoginGraceTime" /etc/ssh/sshd_config; then
    echo "  - Setting LoginGraceTime to 30s"
    echo "LoginGraceTime 30" | sudo tee -a /etc/ssh/sshd_config > /dev/null
else
    echo "  ✓ LoginGraceTime already configured"
fi

echo ""
echo "🔍 Validating SSH configuration..."
if sudo sshd -t; then
    echo "✅ SSH configuration is valid"
else
    echo "❌ SSH configuration is invalid!"
    echo "Restoring backup..."
    sudo cp "$BACKUP_FILE" /etc/ssh/sshd_config
    exit 1
fi

echo ""
echo "🔄 Restarting SSH service..."
if sudo systemctl restart sshd 2>/dev/null || sudo systemctl restart ssh 2>/dev/null; then
    echo "✅ SSH service restarted successfully"
else
    echo "⚠️  Could not restart SSH service automatically"
    echo "Please run manually:"
    echo "  sudo systemctl restart sshd  (or)  sudo systemctl restart ssh"
fi

echo ""
echo "=========================================="
echo "✅ SSH optimization complete!"
echo "=========================================="
echo ""
echo "Changes made:"
echo "  • Disabled DNS reverse lookup (UseDNS no)"
echo "  • Disabled GSSAPI authentication"
echo "  • Optimized connection limits"
echo ""
echo "Expected improvement:"
echo "  • SSH connection time: 14 minutes → 2-5 seconds"
echo ""
echo "Backup saved to: $BACKUP_FILE"
echo ""
echo "Test from your local machine:"
echo "  time ssh -v your-server 'echo OK'"
echo ""
