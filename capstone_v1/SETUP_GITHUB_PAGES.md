# GitHub Pages Setup Instructions

This guide will help you set up GitHub Pages for your repository.

## Prerequisites

1. A GitHub account
2. A repository (create one if you haven't already)
3. Git installed on your local machine

## Step 1: Initialize Git Repository (if not already done)

```bash
cd /path/to/capstone_v1
git init
git add .
git commit -m "Initial commit with documentation"
```

## Step 2: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click the **+** icon → **New repository**
3. Name your repository (e.g., `notebooks` or `capstone-project`)
4. Choose public or private
5. **Do NOT** initialize with README, .gitignore, or license (if you already have files)
6. Click **Create repository**

## Step 3: Connect Local Repository to GitHub

```bash
# Add remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Enable GitHub Pages

### Method 1: Using GitHub Actions (Recommended)

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. Click **Save**

The workflow (`.github/workflows/deploy-gh-pages.yml`) will automatically:

- Build the Jekyll site when you push to `main` or `master`
- Deploy to GitHub Pages
- Update the site automatically

### Method 2: Using gh-pages Branch

1. Go to **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Branch: `gh-pages`
4. Folder: `/ (root)` or `/docs`
5. Click **Save**

Then create the gh-pages branch:

```bash
# Build the site
cd docs
bundle install
bundle exec jekyll build
cd ..

# Create and switch to gh-pages branch
git checkout -b gh-pages

# Copy built files (if deploying from root)
cp -r docs/_site/* .
git add .
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages

# Switch back to main
git checkout main
```

## Step 5: Access Your Site

After deployment (usually takes 1-2 minutes), your site will be available at:

- `https://YOUR_USERNAME.github.io/REPO_NAME/`
- Or if repository name is `notebooks`: `https://YOUR_USERNAME.github.io/notebooks/`

## Step 6: Update Base URL (Important!)

Edit `docs/_config.yml` and update the `baseurl`:

```yaml
baseurl: /REPO_NAME  # Replace REPO_NAME with your repository name
```

If your repository is at the root of your GitHub Pages site, use:

```yaml
baseurl: ""  # Empty string
```

## Automatic Deployment

Once set up, every time you push to the `main` branch:

1. GitHub Actions will automatically build the site
2. Deploy it to GitHub Pages
3. Your site will update within 1-2 minutes

## Manual Deployment

If you need to deploy manually:

```bash
# Use the deployment script
./scripts/deploy-gh-pages.sh

# Or manually
cd docs
bundle install
bundle exec jekyll build
```

## Troubleshooting

### Site Not Appearing

1. **Check Actions Tab**: Go to **Actions** in your repository to see if the workflow ran successfully
2. **Wait**: It can take 1-2 minutes for the site to appear
3. **Check Settings**: Verify GitHub Pages is enabled in Settings → Pages
4. **Check Base URL**: Ensure `baseurl` in `_config.yml` matches your repository name

### Build Failures

1. **Check Ruby Version**: GitHub Actions uses Ruby 3.1
2. **Check Dependencies**: Ensure `Gemfile` is correct
3. **Check Logs**: Review the Actions tab for error messages

### 404 Errors

1. **Base URL**: Make sure `baseurl` in `_config.yml` is correct
2. **File Paths**: Check that markdown files have correct front matter
3. **Links**: Verify internal links use the correct base URL

## Custom Domain (Optional)

To use a custom domain:

1. **Add CNAME file**:

   ```bash
   echo "yourdomain.com" > docs/CNAME
   git add docs/CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS**:
   - Add a CNAME record pointing to `YOUR_USERNAME.github.io`
   - Wait for DNS propagation

3. **Enable in GitHub**:
   - Go to **Settings** → **Pages**
   - Enter your custom domain
   - Enable HTTPS (automatic)

## Next Steps

1. **Customize**: Edit `docs/_config.yml` to customize your site
2. **Add Content**: Add more markdown files to `docs/`
3. **Update**: Push changes to automatically update the site
4. **Monitor**: Check the Actions tab to monitor deployments

## Useful Commands

```bash
# Preview site locally
cd docs
bundle exec jekyll serve

# Build site
bundle exec jekyll build

# Check git status
git status

# Push changes
git add .
git commit -m "Update documentation"
git push origin main
```

## Support

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

**Note**: The first deployment may take a few minutes. Subsequent deployments are usually faster.
