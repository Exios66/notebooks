#!/bin/bash
# Script to manually deploy documentation to GitHub Pages
# This script builds the Jekyll site and prepares it for deployment

set -e

echo "🚀 Starting GitHub Pages deployment..."

# Navigate to docs directory
cd "$(dirname "$0")/../docs"

# Check if bundle is installed
if ! command -v bundle &> /dev/null; then
    echo "❌ Error: Bundler is not installed."
    echo "Install it with: gem install bundler"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
bundle install

# Build the site
echo "🔨 Building Jekyll site..."
bundle exec jekyll build

# Check if build was successful
if [ ! -d "_site" ]; then
    echo "❌ Error: Build failed. _site directory not found."
    exit 1
fi

echo "✅ Build successful!"
echo ""
echo "📝 Next steps:"
echo "1. If using GitHub Actions, push to main/master branch"
echo "2. If deploying manually:"
echo "   - Copy _site/* to gh-pages branch"
echo "   - Or use: git subtree push --prefix docs/_site origin gh-pages"
echo ""
echo "🌐 Your site will be available at:"
echo "   https://yourusername.github.io/notebooks/"

