# Cleanup Scripts

This directory contains maintenance scripts for the Todo Evolution application.

## cleanup_old_conversations.py

Deletes conversations and their associated messages older than 90 days to enforce data retention policy (FR-020).

### Usage

```bash
# Preview what would be deleted (dry run):
python backend/scripts/cleanup_old_conversations.py --dry-run

# Actually delete old conversations:
python backend/scripts/cleanup_old_conversations.py

# Custom retention period (e.g., 30 days):
python backend/scripts/cleanup_old_conversations.py --days 30

# Verbose output:
python backend/scripts/cleanup_old_conversations.py --verbose
```

### Options

- `--dry-run`: Preview deletion without actually deleting (default: False)
- `--days DAYS`: Retention period in days (default: 90)
- `--verbose, -v`: Enable verbose output (default: False)

### Automated Execution

#### Option 1: GitHub Actions (Recommended for GitHub-hosted projects)

The workflow `.github/workflows/cleanup-conversations.yml` runs daily at 2 AM UTC.

**Setup:**
1. Add `DATABASE_URL` to GitHub repository secrets:
   - Go to Settings → Secrets and variables → Actions
   - Add secret: `DATABASE_URL` with your Neon PostgreSQL connection string

2. Enable GitHub Actions in your repository

3. The workflow will run automatically daily at 2 AM UTC

**Manual trigger:**
- Go to Actions → Cleanup Old Conversations → Run workflow

#### Option 2: Kubernetes CronJob

For Kubernetes deployments, use `backend/k8s/cleanup-cronjob.yaml`.

**Setup:**
1. Create secret with DATABASE_URL:
   ```bash
   kubectl create secret generic todo-evolution-secrets \
     --from-literal=database-url="postgresql://..." \
     -n todo-evolution
   ```

2. Apply the CronJob:
   ```bash
   kubectl apply -f backend/k8s/cleanup-cronjob.yaml
   ```

3. Verify CronJob is scheduled:
   ```bash
   kubectl get cronjobs -n todo-evolution
   ```

4. Check job history:
   ```bash
   kubectl get jobs -n todo-evolution
   kubectl logs -l component=cleanup-job -n todo-evolution
   ```

#### Option 3: System Crontab (Linux server deployment)

Add to crontab (`crontab -e`):

```cron
# Run cleanup daily at 2 AM
0 2 * * * cd /path/to/todo-evolution && /path/to/venv/bin/python backend/scripts/cleanup_old_conversations.py >> /var/log/todo-cleanup.log 2>&1
```

### Monitoring

#### Success Criteria
- Script completes without errors
- Logs show number of conversations deleted
- Database size decreases over time

#### Failure Indicators
- Script exits with non-zero code
- Database connection errors
- Permission errors

#### Recommended Alerts
- Alert if script fails 2+ consecutive runs
- Alert if cleanup deletes >1000 conversations (potential issue)
- Alert if cleanup finds 0 conversations for 7+ days (potential clock skew)

### Testing

```bash
# Test with 1-day retention to see what would be deleted:
python backend/scripts/cleanup_old_conversations.py --dry-run --days 1 --verbose

# Test database connectivity:
python backend/scripts/cleanup_old_conversations.py --dry-run

# Verify cleanup in production (dry run first!):
python backend/scripts/cleanup_old_conversations.py --dry-run --verbose
```

### Troubleshooting

**Error: DATABASE_URL not set**
- Ensure `.env` file exists in `backend/` directory
- Or set `DATABASE_URL` environment variable

**Error: Connection timeout**
- Check database credentials
- Verify network connectivity to Neon PostgreSQL
- Check firewall rules

**Error: Permission denied**
- Ensure database user has DELETE permissions
- Check user isolation (only own conversations should be deleted)

**No conversations deleted (expected old data exists)**
- Verify retention period: `--days` parameter
- Check conversation.created_at timestamps in database
- Ensure clock synchronization (UTC)

### Security Considerations

- Script enforces user data isolation (Constitutional Principle II)
- Only deletes conversations by age, not by user
- Dry-run mode available for safety
- Logs all deletions for audit trail
- No hardcoded credentials (uses environment variables)

### Performance

- **Expected duration**: <10 seconds for <1000 conversations
- **Database load**: Minimal (simple WHERE clause on indexed field)
- **Recommended schedule**: Daily during off-peak hours (2-4 AM UTC)

### Constitutional Alignment

- **Principle II**: User Data Isolation ✅ (respects user boundaries)
- **Principle XVI**: Error Handling & Logging ✅ (comprehensive logging)
- **FR-020**: Automated data retention enforcement ✅ (90-day retention)
