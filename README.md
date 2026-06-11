# SocialBD 🇧🇩

বাংলাদেশের নিজস্ব সোশ্যাল মিডিয়া প্ল্যাটফর্ম — Django দিয়ে তৈরি।

## ✨ ফিচারসমূহ

- ✅ User Registration & Login
- ✅ News Feed
- ✅ পোস্ট তৈরি (ছবি সহ)
- ✅ Like ও Comment
- ✅ বন্ধু অনুরোধ সিস্টেম
- ✅ প্রোফাইল পেজ ও কভার ফটো
- ✅ বিজ্ঞপ্তি সিস্টেম
- ✅ মানুষ খোঁজার সুবিধা
- ✅ বন্ধু সাজেশন

## 🚀 লোকাল সেটআপ

```bash
# ১. রিপোজিটরি ক্লোন করুন
git clone https://github.com/yourusername/socialbd.git
cd socialbd

# ২. Virtual environment তৈরি করুন
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ৩. প্যাকেজ ইনস্টল করুন
pip install -r requirements.txt

# ৪. .env ফাইল তৈরি করুন
cp .env.example .env
# .env ফাইলে SECRET_KEY পরিবর্তন করুন

# ৫. Database migration করুন
python manage.py migrate

# ৬. Admin user তৈরি করুন
python manage.py createsuperuser

# ৭. Server চালু করুন
python manage.py runserver
```

তারপর browser-এ যান: http://localhost:8000

## 🌐 GitHub-এ Deploy

```bash
git init
git add .
git commit -m "Initial SocialBD commit"
git remote add origin https://github.com/yourusername/socialbd.git
git push -u origin main
```

## 🏗️ Railway/Render-এ Host করুন (বিনামূল্যে)

1. [Railway.app](https://railway.app) বা [Render.com](https://render.com) এ যান
2. GitHub repo connect করুন
3. Environment variables সেট করুন:
   - `SECRET_KEY` = একটি random string
   - `DEBUG` = False
   - `ALLOWED_HOSTS` = yourdomain.com

## 📁 প্রজেক্ট স্ট্রাকচার

```
socialbd/
├── accounts/       # User model, login, profile
├── posts/          # Post, Like, Comment
├── friends/        # Friend Request system
├── notifications/  # Notification system
├── templates/      # HTML templates
├── static/         # CSS, JS, Images
├── socialbd/       # Django settings
└── manage.py
```

## 🎨 টেক স্ট্যাক

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5 + Custom CSS
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Font**: Hind Siliguri (বাংলা সাপোর্ট)
