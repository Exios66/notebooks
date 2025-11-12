# GitHub Pages Quick Start

## 🚀 Quick Deployment (5 minutes)

### 1. Initialize Git (if needed)
```bash
cd capstone_v1
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repository
- Go to github.com → New repository
- Name it (e.g., `notebooks`)
- Don't initialize with README
- Click Create

### 3. Connect and Push
```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Enable GitHub Pages
1. Go to repository → **Settings** → **Pages**
2. Source: Select **GitHub Actions**
3. Click **Save**

### 5. Update Base URL
Edit `docs/_config.yml`:
```yaml
baseurl: /REPO_NAME  # Replace with your repository name
```

### 6. Push Changes
```bash
git add docs/_config.yml
git commit -m "Update baseurl"
git push
```

### 7. Wait & Access
- Wait 1-2 minutes
- Visit: `https://YOUR_USERNAME.github.io/REPO_NAME/`

## ✅ Done!

Your site will automatically update when you push to `main` branch.

## 📚 Full Documentation

- [Complete Setup Guide](SETUP_GITHUB_PAGES.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Deployment Guide (Detailed)](docs/DEPLOYMENT_GUIDE.md)

## 🔧 Troubleshooting

**Site not appearing?**
- Check Actions tab for build status
- Verify Pages is enabled in Settings
- Wait 1-2 minutes for deployment

**404 errors?**
- Check `baseurl` in `_config.yml`
- Ensure it matches your repository name

**Build failing?**
- Check Actions tab for error logs
- Verify Ruby version (3.1+)
- Run `bundle install` locally to test

