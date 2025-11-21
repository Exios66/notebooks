# Deployment Guide

This guide explains how to deploy the documentation site to GitHub Pages.

> **Quick Start**: See [SETUP_GITHUB_PAGES.md](../SETUP_GITHUB_PAGES.md) for complete setup instructions.

## GitHub Pages Deployment

### Option 1: Automatic Deployment (Jekyll)

1. **Push to GitHub:**

   ```text
   git add .
   git commit -m "Add documentation"
   git push origin main
   ```

2. **Enable GitHub Pages:**
   - Go to repository Settings
   - Navigate to Pages section
   - Select source branch (usually `main` or `gh-pages`)
   - Select folder: `/docs`
   - Click Save

3. **Access your site:**
   - URL: `https://yourusername.github.io/notebooks/`
   - GitHub will automatically build and deploy using Jekyll

### Option 2: Static HTML Deployment

If you prefer static HTML without Jekyll:

1. **Build static files** (if using Jekyll):

   ```bash
   bundle exec jekyll build
   ```

2. **Or use the static HTML files directly** in the `docs/` folder

3. **Deploy:**
   - Push to GitHub
   - Enable GitHub Pages pointing to `/docs` folder
   - The `.nojekyll` file will skip Jekyll processing

## Local Development

### With Jekyll

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Visit: <http://localhost:4000>

### Without Jekyll

Simply open the HTML files in a browser:

- `index.html` - Home page
- `chatbot-interface.html` - Chatbot UI
- Other markdown files can be viewed with a markdown viewer

## Custom Domain

To use a custom domain:

1. Add `CNAME` file in `docs/` folder:

   ```text
   yourdomain.com
   ```

2. Configure DNS settings as per GitHub Pages documentation

## Troubleshooting

### Jekyll Build Errors

- Ensure Ruby and Bundler are installed
- Run `bundle update`
- Check `_config.yml` for errors

### GitHub Pages Not Updating

- Check repository Settings → Pages
- Verify branch and folder are correct
- Wait a few minutes for build to complete
- Check Actions tab for build logs

### Theme Issues

- Verify theme is listed in `_config.yml`
- Check that theme files are present
- Try clearing browser cache

## File Structure

```text
docs/
├── _config.yml           # Jekyll configuration
├── _layouts/             # HTML layouts
├── index.md              # Home page
├── STARTUP_GUIDE.md      # Complete startup guide
├── Gemfile               # Ruby dependencies
└── README.md             # Documentation README
```
