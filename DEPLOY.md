# Railway Deployment Guide 🚀

## Quick Deploy Steps

### 1. **Prepare Repository**
```bash
# Add all deployment files to git
git add .
git commit -m "Add Railway deployment files"
git push origin main
```

### 2. **Deploy to Railway**

#### Option A: One-Click Deploy
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-repo-url)

#### Option B: Manual Deploy
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `tbot` repository
5. Railway will automatically detect it's a Python app

### 3. **Set Environment Variables**
In Railway dashboard:
1. Go to your project → Variables tab
2. Add these variables:
   ```
   TELEGRAM_BOT_TOKEN = 8209765539:AAG_Zcp4PER__SlSmpepgvDAE9wJQvFbtyA
   DEBUG = false
   ```

### 4. **Deploy!**
- Railway will automatically build and deploy
- Your bot will be running 24/7
- Check logs in Railway dashboard

## 📊 **Deployment Files Added**

✅ `Procfile` - Tells Railway how to run your app  
✅ `Dockerfile` - Container configuration  
✅ `railway.toml` - Railway-specific settings  
✅ Updated `.env.example` - Template for environment variables  
✅ Updated `config.py` - Railway environment support  

## 🔧 **Railway Features You Get**

- **24/7 Uptime**: No cold starts like other free services
- **Auto Scaling**: Handles traffic spikes automatically  
- **GitHub Integration**: Auto-deploy on every push
- **Environment Variables**: Secure token storage
- **Logs & Monitoring**: Real-time bot monitoring
- **Custom Domains**: Optional custom URL

## 💰 **Free Tier Limits**

- $5 credit per month (enough for small bots)
- No sleeping/downtime
- 1GB RAM, shared CPU
- Automatic scaling within limits

## 🚨 **Important Notes**

1. **Never commit real tokens**: Use Railway environment variables
2. **Monitor usage**: Check Railway dashboard for credit usage
3. **Logs access**: Railway dashboard → your project → Logs tab

## 🔄 **After Deployment**

Your bot will be live at Railway's generated URL, but since it's a Telegram bot, users still interact via [@PumpingTbot](https://t.me/PumpingTbot).

## 📞 **Support**

If deployment fails:
1. Check Railway logs for errors
2. Verify environment variables are set
3. Check that your bot token is valid
4. Ensure repository is public or Railway has access

Happy deploying! 🎉