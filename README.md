# 🏫 SchoolOS — AI-Powered School Management Platform

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-blue?style=for-the-badge)](https://taupe-phoenix-96552e.netlify.app)
[![Backend](https://img.shields.io/badge/Backend-Railway-purple?style=for-the-badge)](https://schoolos-backend-production.up.railway.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

> A complete multi-tenant SaaS school management platform powered by Claude AI (Anthropic). Built with Django, React, and PostgreSQL.

---

## 🌐 Live Demo

| Service | URL |
|---------|-----|
| 🌐 Frontend | https://taupe-phoenix-96552e.netlify.app |
| ⚙️ Backend API | https://schoolos-backend-production.up.railway.app |

**Demo credentials:**
- Username: `admin`
- Password: `Admin123!`

---

## ✨ Features

### 🤖 AI-Powered (Claude API)
- **AI Chatbot** — answers parent queries about fees, attendance & results
- **Auto Report Cards** — generates personalised student comments instantly
- **Smart Attendance Alerts** — auto-drafts parent alert messages
- **Fee Default Prediction** — predicts at-risk families before they default

### 📚 School Management
- **Multi-tenant SaaS** — each school gets its own PostgreSQL schema & subdomain
- **Student Management** — profiles, attendance, results, parent linking
- **Fee Management** — invoices, bKash/Nagad/cash payments, AI risk scores
- **Attendance Tracking** — daily marking, monthly trends, calendar view
- **Teacher Management** — staff profiles, subjects, schedules
- **AI Report Cards** — term-wise results with AI-generated comments
- **Parent Portal** — mobile-friendly portal for parents

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Tailwind CSS |
| Backend | Django 4.2, Django REST Framework |
| Database | PostgreSQL (multi-tenant via django-tenants) |
| AI | Anthropic Claude API |
| Auth | JWT (djangorestframework-simplejwt) |
| Task Queue | Celery + Redis |
| Deployment | Railway (backend) + Netlify (frontend) |

---

## 🚀 Quick Start

### 1. Clone the repo
```bash
schoolos/
├── lgsedu/          # Django project config
├── tenants/         # Multi-tenant models (School, Domain)
├── core/            # Students, Parents, Grades
├── management/      # Teachers, Attendance, Results
├── fees/            # Fee structure, Invoices, Payments
├── ai_features/     # All 4 AI features + Celery tasks
└── api/             # REST API views
---

## 💰 SaaS Pricing Tiers

| Plan | Students | Price |
|------|----------|-------|
| Free | Up to 100 | ৳0/mo |
| Starter | Up to 500 | ৳2,500/mo |
| Growth | Up to 2,000 | ৳6,000/mo |
| Scale | Unlimited | ৳12,000/mo |

---

## 📸 Screenshots

### Dashboard
![Dashboard](https://via.placeholder.com/800x400/0F1117/3B82F6?text=SchoolOS+Dark+Dashboard)

### Students Management
![Students](https://via.placeholder.com/800x400/0F1117/10B981?text=Students+Management)

### AI Report Cards
![Report Cards](https://via.placeholder.com/800x400/0F1117/8B5CF6?text=AI+Report+Cards)

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

---

## 📄 License

MIT License — feel free to use this for your school!

---

**Built with ❤️ for Bangladeshi schools · Powered by Claude AI**
