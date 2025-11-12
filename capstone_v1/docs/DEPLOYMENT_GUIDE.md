# GitHub Pages Deployment Guide

This guide explains how to deploy the documentation site to GitHub Pages using automated workflows or manual methods.

## Quick Start

### Automatic Deployment (Recommended)

The repository includes a GitHub Actions workflow that automatically deploys the site when you push to the `main` or `master` branch.

1. **Enable GitHub Pages in Repository Settings:**
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Pages**
   - Under **Source**, select **GitHub Actions**
   - Save the settings

2. **Push your changes:**
   ```bash
   git add .
   git commit -m "Update documentation"
   git push origin main
   ```

3. **Monitor deployment:**
   - Go to the **Actions** tab in your repository
   - Watch the "Deploy to GitHub Pages" workflow run
   - Once complete, your site will be live

4. **Access your site:**
   - URL: `https://yourusername.github.io/notebooks/`
   - Or: `https://yourusername.github.io/repository-name/`

## Manual Deployment

### Option 1: Using Jekyll (Recommended for Development)

1. **Install dependencies:**
   ```bash
   cd docs
   bundle install
   ```

2. **Build the site:**
   ```bash
   bundle exec jekyll build
   ```

3. **Preview locally:**
   ```bash
   bundle exec jekyll serve
   ```
   Visit: http://localhost:4000

4. **Deploy using script:**
   ```bash
   ./scripts/deploy-gh-pages.sh
   ```

### Option 2: Using gh-pages Branch

1. **Create or checkout gh-pages branch:**
   ```bash
   git checkout -b gh-pages
   # Or if branch exists:
   git checkout gh-pages
   ```

2. **Build the site:**
   ```bash
   cd docs
   bundle exec jekyll build
   ```

3. **Copy built files to root:**
   ```bash
   cp -r _site/* ../
   cd ..
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Deploy documentation"
   git push origin gh-pages
   ```

5. **Configure GitHub Pages:**
   - Go to repository **Settings** → **Pages**
   - Select source: **Deploy from a branch**
   - Branch: `gh-pages`
   - Folder: `/ (root)`
   - Click **Save**

### Option 3: Using Git Subtree

```bash
# Build the site
cd docs
bundle exec jekyll build
cd ..

# Deploy using subtree
git subtree push --prefix docs/_site origin gh-pages
```

## GitHub Actions Workflow

The repository includes `.github/workflows/deploy-gh-pages.yml` which:

- Triggers on pushes to `main`/`master` branch
- Builds the Jekyll site
- Deploys to GitHub Pages automatically
- Uses the latest GitHub Actions for Pages deployment

### Workflow Features

- **Automatic**: Deploys on every push to main/master
- **Fast**: Uses caching for faster builds
- **Reliable**: Uses official GitHub Actions
- **Secure**: Uses OIDC for authentication

## Configuration

### Jekyll Configuration

The `_config.yml` file contains:

- Site title and description
- Base URL configuration
- Theme settings (Minima)
- Navigation structure
- Plugin configuration

### Custom Domain

To use a custom domain:

1. **Add CNAME file:**
   ```bash
   echo "yourdomain.com" > docs/CNAME
   ```

2. **Configure DNS:**
   - Add CNAME record pointing to `yourusername.github.io`
   - Wait for DNS propagation

3. **Enable in GitHub:**
   - Go to repository **Settings** → **Pages**
   - Enter your custom domain
   - Enable HTTPS (automatic)

## Troubleshooting

### Build Failures

**Problem**: Jekyll build fails
- **Solution**: Check Ruby version (requires 3.1+)
- **Solution**: Run `bundle update`
- **Solution**: Check `_config.yml` for syntax errors

### Site Not Updating

**Problem**: Changes not appearing on site
- **Solution**: Wait 1-2 minutes for GitHub to rebuild
- **Solution**: Check Actions tab for build errors
- **Solution**: Clear browser cache
- **Solution**: Verify branch and folder settings

### 404 Errors

**Problem**: Pages return 404
- **Solution**: Check baseurl in `_config.yml`
- **Solution**: Verify file paths are correct
- **Solution**: Ensure markdown files have front matter

### Theme Issues

**Problem**: Theme not loading
- **Solution**: Verify theme in `_config.yml`
- **Solution**: Check Gemfile includes theme gem
- **Solution**: Run `bundle install`

## Local Development

### Setup

```bash
# Install Ruby (if not installed)
# macOS: brew install ruby
# Linux: sudo apt-get install ruby ruby-dev
# Windows: Use RubyInstaller

# Install Bundler
gem install bundler

# Install dependencies
cd docs
bundle install
```

### Development Server

```bash
# Start Jekyll server
bundle exec jekyll serve

# With live reload
bundle exec jekyll serve --livereload

# Custom port
bundle exec jekyll serve --port 4001
```

### File Structure

```
docs/
├── _config.yml          # Jekyll configuration
├── _layouts/            # HTML layouts
├── _site/               # Built site (generated)
├── .nojekyll            # Skip Jekyll processing flag
├── index.md             # Home page
├── *.md                 # Documentation pages
├── chatbot-interface.html  # Interactive UI
├── Gemfile              # Ruby dependencies
└── README.md            # Documentation README
```

## Best Practices

1. **Test Locally**: Always test changes locally before pushing
2. **Commit Often**: Small, frequent commits are easier to debug
3. **Check Actions**: Monitor GitHub Actions for build status
4. **Use Markdown**: Keep documentation in Markdown format
5. **Version Control**: Don't commit `_site/` directory
6. **Base URL**: Update `baseurl` in `_config.yml` for your repository

## Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Minima Theme](https://github.com/jekyll/minima)
- [GitHub Actions for Pages](https://github.com/actions/deploy-pages)

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review GitHub Actions logs
3. Check Jekyll build output locally
4. Verify repository settings

---

**Last Updated**: 2024  
**Maintained by**: Capstone Project Team

