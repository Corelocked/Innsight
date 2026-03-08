# 🚀 Vercel Deployment Checklist

## Pre-Deployment
- [-] Push all code to Git repository (GitHub/GitLab/Bitbucket)
- [-] Ensure `.env` and secrets are NOT committed
- [-] Verify `requirements.txt` contains only slim dependencies
- [ ] Test locally with `npm start` (frontend) and Python API

## Vercel Setup
- [ ] Create Vercel account at [vercel.com](https://vercel.com)
- [ ] Import Git repository in Vercel dashboard
- [ ] Set root directory to project root (not voice-order-ui)
- [ ] Build command: `cd voice-order-ui && npm run build`
- [ ] Output directory: `voice-order-ui/build`

## Environment Variables (Required)
Configure in: Vercel Dashboard → Project → Settings → Environment Variables

### Frontend Variables
- [ ] `REACT_APP_API_URL` = optional; leave unset for same-origin API in production
- [ ] `REACT_APP_FIREBASE_API_KEY` = Your Firebase API key
- [ ] `REACT_APP_FIREBASE_AUTH_DOMAIN` = Your Firebase auth domain
- [ ] `REACT_APP_FIREBASE_PROJECT_ID` = Your Firebase project ID
- [ ] `REACT_APP_FIREBASE_STORAGE_BUCKET` = Your Firebase storage bucket
- [ ] `REACT_APP_FIREBASE_MESSAGING_SENDER_ID` = Your Firebase sender ID
- [ ] `REACT_APP_FIREBASE_APP_ID` = Your Firebase app ID

### Backend Variables (Optional)
- [ ] `DATABASE_URL` = PostgreSQL connection string (if using DB)
- [ ] `SECRET_KEY` = Random secret for sessions (if needed)

## Deployment
- [ ] Click "Deploy" in Vercel dashboard
- [ ] Wait for build to complete (2-5 minutes)
- [ ] Check deployment logs for errors

## Post-Deployment Testing
- [ ] Visit your Vercel URL
- [ ] Test user registration/login
- [ ] Test voice input functionality
- [ ] Test text input submission
- [ ] Test feedback submission
- [ ] Check browser console for errors
- [ ] Check Vercel function logs for API errors

## Performance Verification
- [ ] First request (cold start): 3-5 seconds ✓
- [ ] Subsequent requests: <500ms ✓
- [ ] Frontend loads in <2 seconds ✓
- [ ] No console errors ✓

## Optional Improvements
- [ ] Set up custom domain
- [ ] Enable Vercel Analytics
- [ ] Configure error monitoring (Sentry)
- [ ] Set up uptime monitoring
- [ ] Add rate limiting
- [ ] Migrate to hosted database (PostgreSQL)

## Troubleshooting
If deployment fails:
1. Check build logs in Vercel dashboard
2. Verify all environment variables are set
3. Test locally with `vercel dev`
4. Check `requirements.txt` is the slim version
5. Review `DEPLOYMENT.md` for detailed troubleshooting

## Quick Links
- Vercel Dashboard: https://vercel.com/dashboard
- Firebase Console: https://console.firebase.google.com
- Documentation: See `DEPLOYMENT.md`
- Optimizations: See `OPTIMIZATION.md`

---
✅ All items checked? You're ready to deploy!
