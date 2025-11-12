#!/bin/bash
# Script to clean up disk space for Jekyll/Bundler installation

echo "🧹 Starting disk space cleanup..."
echo ""

# Check current disk space
echo "📊 Current disk space:"
df -h . | tail -1
echo ""

# Clean pip cache (saves ~3.6GB)
echo "🧹 Cleaning pip cache..."
pip cache purge 2>/dev/null || echo "  (pip cache already clean or pip not available)"
echo ""

# Clean Homebrew cache (saves ~978MB)
echo "🧹 Cleaning Homebrew cache..."
if command -v brew &> /dev/null; then
    brew cleanup --prune=all 2>/dev/null || echo "  (Homebrew cleanup failed or not needed)"
else
    echo "  (Homebrew not installed)"
fi
echo ""

# Clean Python cache
echo "🧹 Cleaning Python cache..."
find ~/Library/Caches/com.apple.python -type f -name "*.pyc" -delete 2>/dev/null || true
find ~/Library/Caches/com.apple.python -type d -empty -delete 2>/dev/null || true
echo ""

# Clean temporary files
echo "🧹 Cleaning temporary files..."
rm -rf /var/folders/*/*/T/* 2>/dev/null || echo "  (Some temp files could not be removed)"
echo ""

# Clean bundler cache if it exists
echo "🧹 Cleaning bundler cache..."
rm -rf ~/.bundle/cache 2>/dev/null || true
rm -rf ~/.gem/cache 2>/dev/null || true
echo ""

# Final disk space check
echo "📊 Disk space after cleanup:"
df -h . | tail -1
echo ""
echo "✅ Cleanup complete!"
echo ""
echo "💡 If you still need more space, consider:"
echo "   - Emptying Trash"
echo "   - Removing old downloads"
echo "   - Uninstalling unused applications"
echo "   - Using macOS Storage Management (Apple menu > About This Mac > Storage)"

