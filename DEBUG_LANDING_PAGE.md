# Landing Page Redirect Issue - Quick Fix

## Problem
Landing page appears for a second then disappears (redirects to /tasks)

## Cause
You have an auth token stored from previous testing, so the page automatically redirects authenticated users to /tasks.

## Solution 1: Clear Browser Storage (Quick)

### Chrome/Edge/Brave:
1. Open http://localhost:3000
2. Press **F12** (open Developer Tools)
3. Go to **Console** tab
4. Type this and press Enter:
   ```javascript
   localStorage.clear()
   ```
5. Press **F5** to refresh the page
6. Landing page should now stay visible ✅

### Firefox:
1. Open http://localhost:3000
2. Press **F12**
3. Go to **Console** tab
4. Type: `localStorage.clear()`
5. Refresh (F5)

## Solution 2: Use Incognito/Private Window

1. Open **Incognito/Private Window** (Ctrl+Shift+N in Chrome)
2. Go to http://localhost:3000
3. Landing page will be visible (no stored token)

## Solution 3: Sign Out First

1. If you can catch the /tasks page before redirect:
   - Click **Sign Out** button
2. OR manually go to: http://localhost:3000/tasks
   - Click **Sign Out**
3. Then go back to http://localhost:3000

## Verification

After clearing localStorage:
- ✅ Landing page stays visible
- ✅ "Get Started" and "Sign In" buttons work
- ✅ No automatic redirect

To test the redirect (should happen when signed in):
1. Click "Get Started" or "Sign In"
2. Sign in with credentials
3. Landing page should now redirect to /tasks ✅
4. This is correct behavior!

## Expected Behavior

**Not Signed In**: Landing page visible (no redirect)
**Signed In**: Auto-redirect to /tasks (user already authenticated)
