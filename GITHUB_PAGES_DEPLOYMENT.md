# 🚀 GitHub Pages Deployment Guide

## 📋 Prerequisites

1. **GitHub Account**: Create account at [github.com](https://github.com)
2. **Git Installed**: Download from [git-scm.com](https://git-scm.com)
3. **Node.js**: Download from [nodejs.org](https://nodejs.org)

## 🎯 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. Go to [github.com](https://github.com) and login
2. Click **"New Repository"**
3. Repository name: `smartai-fashion-platform`
4. Make it **Public**
5. Check **"Add a README file"**
6. Click **"Create repository"**

### Step 2: Upload Your Code

```bash
# Navigate to your demo1 folder
cd demo1

# Initialize git (if not already done)
git init

# Add GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/smartai-fashion-platform.git

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: SmartAI Fashion Platform"

# Push to GitHub
git push -u origin main
```

### Step 3: Prepare Frontend for GitHub Pages

1. **Install GitHub Pages package**:
```bash
cd frontend
npm install --save-dev gh-pages
```

2. **Update package.json**:
Add these lines to `frontend/package.json`:
```json
{
  "homepage": "https://YOUR_USERNAME.github.io/smartai-fashion-platform",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  }
}
```

3. **Update API URLs for production**:
Create `frontend/src/config.js`:
```javascript
const config = {
  API_BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-url.herokuapp.com'  // Replace with your backend URL
    : 'http://localhost:8000'
};

export default config;
```

4. **Update API calls in components**:
Replace `http://localhost:8000` with `config.API_BASE_URL` in all frontend files.

### Step 4: Deploy Frontend to GitHub Pages

```bash
cd frontend
npm run deploy
```

This will:
- Build the React app
- Create a `gh-pages` branch
- Deploy to GitHub Pages

### Step 5: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section
4. Source: **Deploy from a branch**
5. Branch: **gh-pages**
6. Folder: **/ (root)**
7. Click **Save**

### Step 6: Deploy Backend (Choose One Option)

#### Option A: Heroku (Recommended)

1. **Create Heroku account**: [heroku.com](https://heroku.com)
2. **Install Heroku CLI**: [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)

```bash
# Login to Heroku
heroku login

# Create Heroku app
cd backend
heroku create your-app-name-backend

# Add Python buildpack
heroku buildpacks:set heroku/python

# Set environment variables
heroku config:set OPENAI_API_KEY=your-openai-api-key

# Deploy
git add .
git commit -m "Deploy backend to Heroku"
git push heroku main
```

#### Option B: Railway

1. **Create Railway account**: [railway.app](https://railway.app)
2. **Connect GitHub repository**
3. **Deploy backend folder**
4. **Set environment variables**

#### Option C: Vercel

1. **Create Vercel account**: [vercel.com](https://vercel.com)
2. **Import GitHub repository**
3. **Configure build settings for backend**

### Step 7: Update Frontend API Configuration

After backend deployment, update `frontend/src/config.js`:
```javascript
const config = {
  API_BASE_URL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-app.herokuapp.com'  // Your actual backend URL
    : 'http://localhost:8000'
};
```

Redeploy frontend:
```bash
cd frontend
npm run deploy
```

## 🎉 Your Live Demo URLs

- **Frontend**: `https://YOUR_USERNAME.github.io/smartai-fashion-platform`
- **Backend**: `https://your-backend-app.herokuapp.com`

## 🔧 Configuration Files Needed

### 1. Frontend `package.json` additions:
```json
{
  "homepage": "https://YOUR_USERNAME.github.io/smartai-fashion-platform",
  "scripts": {
    "predeploy": "npm run build",
    "deploy": "gh-pages -d build"
  },
  "devDependencies": {
    "gh-pages": "^4.0.0"
  }
}
```

### 2. Backend `Procfile` (for Heroku):
```
web: python simple_best_in_me.py
```

### 3. Backend `runtime.txt` (for Heroku):
```
python-3.9.16
```

## 🚨 Important Notes

### CORS Configuration
Make sure your backend allows your GitHub Pages domain:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://YOUR_USERNAME.github.io"  # Add this line
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Environment Variables
- **Never commit API keys** to GitHub
- Use environment variables for sensitive data
- Set them in your hosting platform (Heroku, Railway, etc.)

### Demo Mode
- Your demo data will work perfectly on GitHub Pages
- Real OpenAI API calls will work if backend is properly deployed
- Fallback to demo images if API quota is exceeded

## 🔄 Update Process

To update your live demo:

1. **Make changes locally**
2. **Test thoroughly**
3. **Commit and push to GitHub**:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```
4. **Redeploy frontend**:
```bash
cd frontend
npm run deploy
```
5. **Backend updates automatically** (if using Heroku/Railway with auto-deploy)

## 🎯 Final Checklist

- [ ] GitHub repository created and code uploaded
- [ ] Frontend deployed to GitHub Pages
- [ ] Backend deployed to cloud platform
- [ ] API URLs updated in frontend config
- [ ] CORS configured for GitHub Pages domain
- [ ] Environment variables set securely
- [ ] Demo scenarios tested on live site
- [ ] README.md updated with live demo links

## 🎊 Success!

Your SmartAI Fashion Platform is now live and accessible to the world!

**Share your demo**: `https://YOUR_USERNAME.github.io/smartai-fashion-platform`