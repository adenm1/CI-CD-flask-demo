# CI/CD Troubleshooting Guide

## SSH Handshake Failure - Fixed 2025-11-28

### Issue Description
Deployment workflow was failing with the error:
```
ssh: handshake failed: EOF
```

This occurred at the "Copy files to server" step in the deploy.yml workflow.

### Root Cause
The SSH connection was timing out or being abruptly closed by the server. Common causes:
1. **Default timeout too short** - The actions had no explicit timeout configuration
2. **Network latency** - Connection between GitHub Actions and server experiencing delays
3. **Server load** - SSH daemon overwhelmed or slow to respond
4. **Large file transfer** - Default timeout insufficient for transferring all project files

### Solution Applied

#### 1. Added SSH Connection Test Step
Added a preliminary SSH connection test before file transfer:
```yaml
- name: Test SSH connection
  uses: appleboy/ssh-action@v1.0.3
  with:
    timeout: 30s
    command_timeout: 10s
    script: |
      echo "✅ SSH connection successful"
      echo "Server: $(hostname)"
```

**Benefits:**
- Validates SSH credentials before attempting file transfer
- Fails fast if SSH is not working
- Provides diagnostic information about the server

#### 2. Added Explicit Timeouts to All SSH Actions
Added `timeout` and `command_timeout` to all SSH steps:

| Step | Timeout | Reason |
|------|---------|--------|
| Test SSH connection | 30s | Quick validation |
| Copy files to server | 10m | Large file transfer |
| Stop services | 5m | Docker cleanup can be slow |
| Deploy with Docker Compose | 10m | Build + migration + startup |
| Verify deployment | 5m | Health checks with retries |
| Cleanup old images | 2m | Docker pruning |
| Report to dashboard | 2m | API call with retries |

#### 3. Updated Step Numbering
Fixed emoji numbering in workflow steps for better readability:
- 7️⃣ → SSH Connection Test
- 8️⃣ → Copy files to server
- 9️⃣ → Stop services
- 🔟 → Deploy with Docker Compose
- 1️⃣1️⃣ → Verify deployment
- 1️⃣2️⃣ → Cleanup
- 1️⃣3️⃣ → Report to dashboard

### Testing the Fix

After applying this fix, verify by:

1. **Push to main branch:**
   ```bash
   git add .
   git commit -m "fix: resolve SSH timeout in deployment workflow"
   git push origin main
   ```

2. **Monitor the workflow:**
   ```bash
   gh run watch
   ```

3. **Check specific step logs:**
   ```bash
   gh run view --log
   ```

### Additional Recommendations

If SSH issues persist, check:

1. **SSH Key Format**
   - Ensure `SSH_KEY` secret contains a valid private key
   - Key should be in OpenSSH format (starts with `-----BEGIN OPENSSH PRIVATE KEY-----`)
   - No extra whitespace or line breaks

2. **Server SSH Configuration**
   - SSH daemon running: `sudo systemctl status sshd`
   - Port 22 open in firewall
   - Max SSH sessions not exceeded

3. **GitHub Actions IP Ranges**
   - If using IP whitelisting, add GitHub Actions IP ranges
   - See: https://api.github.com/meta (look for `actions` IPs)

4. **Network Issues**
   - Check server network connectivity
   - Verify DNS resolution
   - Test SSH from another machine: `ssh -v user@server`

### Alternative Solutions (Not Implemented)

If timeout issues continue, consider:

1. **Use rsync instead of scp:**
   ```yaml
   - name: Deploy with rsync
     uses: burnett01/rsync-deployments@5.2
     with:
       switches: -avzr --delete
       path: /
       remote_path: /opt/ci-cd-flask-demo
   ```

2. **Deploy via Docker registry:**
   - Build image in GitHub Actions
   - Push to Docker Hub/GHCR
   - Pull on server (faster than file transfer)

3. **Use GitHub Actions self-hosted runner:**
   - Run on the deployment server itself
   - Eliminates SSH entirely
   - See: https://docs.github.com/en/actions/hosting-your-own-runners

### Related Files Modified
- `.github/workflows/deploy.yml` - Added timeouts and connection test

### References
- [appleboy/ssh-action documentation](https://github.com/appleboy/ssh-action)
- [appleboy/scp-action documentation](https://github.com/appleboy/scp-action)
- [GitHub Actions timeout documentation](https://docs.github.com/en/actions/learn-github-actions/workflow-syntax-for-github-actions#jobsjob_idstepstimeout-minutes)
