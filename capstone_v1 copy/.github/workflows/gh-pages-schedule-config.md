# GitHub Pages Auto-Refresh Configuration

This document explains how to configure the automatic GitHub Pages refresh schedule.

## Current Configuration

The GitHub Pages site is automatically rebuilt and deployed:

- **On every push** to `main` or `master` branch (when docs change)
- **On manual trigger** via GitHub Actions UI
- **On schedule**: Every 15 minutes by default

## Adjusting the Schedule

### Method 1: Edit the Workflow File (Recommended)

Edit `.github/workflows/deploy-gh-pages.yml` and modify the cron expression:

```yaml
schedule:
  - cron: '*/15 * * * *'  # Change this line
```

**Cron Expression Format**: `minute hour day month day-of-week`

**Common Intervals**:

- `*/15 * * * *` - Every 15 minutes (current)
- `*/30 * * * *` - Every 30 minutes
- `0 * * * *` - Every hour (at :00)
- `0 */2 * * *` - Every 2 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 0 * * 0` - Weekly on Sunday at midnight UTC
- `0 0 1 * *` - Monthly on the 1st at midnight UTC

**Examples**:

```yaml
# Every 30 minutes
schedule:
  - cron: '*/30 * * * *'

# Every hour
schedule:
  - cron: '0 * * * *'

# Every 2 hours
schedule:
  - cron: '0 */2 * * *'

# Daily at 3 AM UTC
schedule:
  - cron: '0 3 * * *'

# Disable scheduled runs (comment out or remove)
# schedule:
#   - cron: '*/15 * * * *'
```

### Method 2: Use Repository Variables (Optional)

1. Go to **Repository Settings** → **Secrets and variables** → **Actions** → **Variables**
2. Add a new variable:
   - **Name**: `GITHUB_PAGES_REFRESH_INTERVAL`
   - **Value**: `15min`, `30min`, `1hour`, `2hours`, `daily`, or `disabled`

Note: This is currently informational only. The actual schedule is controlled by the cron expression in the workflow file.

## Disabling Scheduled Deployments

To disable automatic scheduled deployments:

1. **Comment out the schedule** in `.github/workflows/deploy-gh-pages.yml`:

   ```yaml
   # schedule:
   #   - cron: '*/15 * * * *'
   ```

2. Or **remove the schedule section** entirely

The workflow will still run on:

- Push events (when docs change)
- Manual triggers via GitHub Actions UI

## How It Works

1. **Change Detection**: On scheduled runs, the workflow checks if there are any changes in:
   - `docs/` directory
   - `api_wrapper/` directory (source code that might affect docs)

   It checks the last 5 commits to determine if changes exist.

2. **Smart Deployment**: If no changes are detected in recent commits, the deployment is skipped to save resources.

3. **Force Rebuild**: You can force a rebuild even without changes by:
   - Using manual trigger via GitHub Actions UI
   - The workflow will always deploy on push events (when docs change)

## Monitoring

To monitor scheduled deployments:

1. Go to **Actions** tab in your GitHub repository
2. Click on **Deploy to GitHub Pages** workflow
3. View scheduled runs (they'll be marked with a clock icon)

## Troubleshooting

### Scheduled runs not executing

1. **Check GitHub Actions is enabled**: Repository Settings → Actions → General
2. **Verify cron syntax**: Use [crontab.guru](https://crontab.guru/) to validate
3. **Check workflow file**: Ensure it's in `.github/workflows/` directory
4. **Review Actions tab**: Check for any error messages

### Too frequent deployments

- Increase the cron interval (e.g., change `*/15` to `*/30` for 30 minutes)
- Or disable scheduled runs and rely on push triggers only

### Deployments always running

- The workflow includes change detection for scheduled runs
- If you want to disable change detection, modify the workflow to always deploy

## Best Practices

1. **Balance frequency with resources**: More frequent = more GitHub Actions minutes used
2. **Use push triggers for immediate updates**: Changes pushed to main will deploy immediately
3. **Monitor usage**: Check Actions tab to see resource consumption
4. **Test changes**: Use manual trigger to test before relying on schedule

## Timezone Note

GitHub Actions schedules use **UTC timezone**. To convert to your local time:

- Use a timezone converter
- Or adjust the cron expression accordingly

Example: If you want 3 AM EST (UTC-5), use `0 8 * * *` (8 AM UTC = 3 AM EST).
