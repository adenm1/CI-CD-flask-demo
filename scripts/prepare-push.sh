#!/bin/bash

# Prepare project for push - cleanup and validation
set -e

echo "🧹 Cleaning up deprecated files..."

# Remove old src/ directory
if [ -d "src" ]; then
    echo "  Removing src/ directory..."
    rm -rf src/
fi

# Remove .trash directory
if [ -d ".trash" ]; then
    echo "  Removing .trash/ directory..."
    rm -rf .trash/
fi

# Remove .venv if accidentally tracked
if [ -d ".venv" ] && git ls-files --error-unmatch .venv >/dev/null 2>&1; then
    echo "  Removing .venv from git..."
    git rm -rf --cached .venv
fi

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "📋 Checking project structure..."

# Check required directories exist
required_dirs=("backend" "frontend" "backend/api" "frontend/src")
for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir exists"
    else
        echo "  ❌ $dir is missing!"
        exit 1
    fi
done

# Check required files exist
required_files=(
    "backend/app.py"
    "backend/config/settings.py"
    "frontend/package.json"
    "frontend/vite.config.ts"
    "Dockerfile"
    "docker-compose.yml"
    "requirements.txt"
    ".env.example"
    "Claude.md"
    "README.md"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file exists"
    else
        echo "  ❌ $file is missing!"
        exit 1
    fi
done

echo ""
echo "✅ All required files and directories present!"
echo ""
echo "📊 Git status:"
git status --short

echo ""
echo "✅ Ready to commit and push!"
echo ""
echo "Next steps:"
echo "  1. Review changes: git status"
echo "  2. Add all changes: git add ."
echo "  3. Commit: git commit -m 'your message'"
echo "  4. Push: git push origin main"
