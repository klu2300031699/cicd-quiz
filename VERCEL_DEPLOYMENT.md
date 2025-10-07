# Deploy Django QuizMaster to Vercel

## Prerequisites
- GitHub account
- Vercel account (free tier works)
- Git installed on your computer

## Step 1: Push Your Project to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Django QuizMaster ready for Vercel"
   ```

2. **Create a new repository on GitHub**:
   - Go to https://github.com/new
   - Name it something like `django-quizmaster`
   - Don't initialize with README (you already have files)
   - Click "Create repository"

3. **Push your code to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/django-quizmaster.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Set Up PostgreSQL Database

**Important**: Vercel's serverless environment doesn't support SQLite. You need PostgreSQL.

### Option A: Use Vercel Postgres (Recommended)
1. Go to https://vercel.com/dashboard
2. Click "Storage" → "Create Database"
3. Select "Postgres"
4. Choose your database region
5. Click "Create"
6. Copy the `DATABASE_URL` connection string

### Option B: Use External PostgreSQL (e.g., Neon, Supabase)
1. Sign up for a free PostgreSQL service:
   - Neon: https://neon.tech (recommended)
   - Supabase: https://supabase.com
   - ElephantSQL: https://elephantsql.com
2. Create a new database
3. Copy the connection string (DATABASE_URL)

## Step 3: Deploy to Vercel

1. **Go to Vercel**:
   - Visit https://vercel.com
   - Click "Add New" → "Project"

2. **Import your GitHub repository**:
   - Select your GitHub account
   - Find and import your `django-quizmaster` repository

3. **Configure Environment Variables**:
   Click "Environment Variables" and add:
   
   - **SESSION_SECRET**: Generate a random secret key
     ```bash
     # Generate with: python -c "import secrets; print(secrets.token_urlsafe(50))"
     ```
   
   - **DATABASE_URL**: Your PostgreSQL connection string
     ```
     postgresql://user:password@host:port/database
     ```
   
   - **DEBUG** (optional): Set to `False` or leave empty for production

4. **Deploy**:
   - Click "Deploy"
   - Wait for build to complete (3-5 minutes)
   - Your app will be live at `https://your-project.vercel.app`

## Step 4: Initialize Database

After first deployment, you need to run migrations:

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login and link project**:
   ```bash
   vercel login
   vercel link
   ```

3. **Run migrations**:
   ```bash
   vercel exec python manage.py migrate
   ```

4. **Create superuser** (for admin access):
   ```bash
   vercel exec python manage.py createsuperuser
   ```

## Step 5: Load Initial Data (Optional)

If you want to load your quiz data:
```bash
vercel exec python manage.py setup_initial_data
```

## Troubleshooting

### Build Fails
- Check build logs in Vercel dashboard
- Verify all environment variables are set correctly
- Ensure `requirements.txt` has all dependencies

### Database Connection Issues
- Verify DATABASE_URL is correct
- Check PostgreSQL database is accessible
- Ensure SSL mode is configured if required

### Static Files Not Loading
- Run: `vercel exec python manage.py collectstatic --noinput`
- Check `vercel.json` configuration

### Application Errors
- Check runtime logs in Vercel dashboard
- Verify SECRET_KEY is set
- Ensure DEBUG is False in production

## Updating Your App

To deploy updates:
```bash
git add .
git commit -m "Your update message"
git push origin main
```

Vercel will automatically redeploy when you push to GitHub!

## Important Notes

1. **Database Migration**: Your local SQLite database won't transfer to Vercel. You'll start with a fresh PostgreSQL database.

2. **User Data**: You'll need to recreate users and quiz content in the production database.

3. **Environment Variables**: Never commit `.env` files or secrets to GitHub.

4. **Custom Domain**: You can add a custom domain in Vercel project settings.

5. **Monitoring**: Check Vercel dashboard for logs, analytics, and performance metrics.

## Cost

- **Vercel**: Free tier includes generous limits (100GB bandwidth, unlimited deployments)
- **PostgreSQL**: 
  - Vercel Postgres: Free tier available
  - Neon: Free tier with 0.5GB storage
  - Supabase: Free tier with 500MB storage

## Support

For issues:
- Vercel Docs: https://vercel.com/docs
- Django Deployment: https://docs.djangoproject.com/en/5.2/howto/deployment/
