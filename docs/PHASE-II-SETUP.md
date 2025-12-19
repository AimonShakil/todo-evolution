# Phase II Setup Guide

**Status**: STEP 0 - Environment Setup & Migration Planning
**Branch**: 003-phase-ii-web-app
**Date**: 2025-12-15

## 🎯 STEP 0 Overview

This guide walks you through environment setup for Phase II. Total time: 4-6 hours.

---

## ✅ Tasks Completed (Automated)

- [x] **T001**: Feature branch `003-phase-ii-web-app` created
- [x] Backend directory structure created
- [x] **BETTER_AUTH_SECRET** generated: `HgkFzYWVxdJjobxlsZRKcSypijaYRuGmXL9Ck+RyNfg=`
- [x] **JWT_SECRET** generated: `jIfhrD71meAWGP2mUim8M3R83udusoW03Tkch9iPQ+E=`
- [x] `backend/.env.example` created
- [x] `backend/.gitignore` created
- [x] `backend/README.md` created
- [x] **STEP 0.4-0.5**: Research completed (FastAPI + Next.js 16 + Better Auth patterns)
- [x] **STEP 0.6**: Database migration strategy documented (`specs/003-phase-ii-web-app/data-model.md`)
- [x] **STEP 0.7**: Alembic setup complete (`backend/ALEMBIC_SETUP.md`, virtual environment, dependencies installed)

---

## 📋 Manual Steps Required (You Need to Do These)

### STEP 0.1: Create Neon PostgreSQL Project (10-15 minutes)

**1. Sign up for Neon** (if you haven't already):
   - Go to: https://console.neon.tech
   - Click "Sign Up" (or "Sign In" if you have an account)
   - Sign up with GitHub, Google, or email

**2. Create New Project**:
   - Click "New Project" button
   - **Project Name**: `todo-evolution`
   - **Region**: Choose closest to you:
     - `us-east-1` (US East - Virginia)
     - `us-west-2` (US West - Oregon)
     - `eu-central-1` (Europe - Frankfurt)
   - **PostgreSQL Version**: 16 (default, latest)
   - **Compute Size**: Leave default (0.25 vCPU is fine for development)
   - Click "Create Project"

**3. Get Connection String**:
   - After project creation, you'll see the dashboard
   - Look for "Connection Details" or "Connection String"
   - You'll see something like:
   ```
   postgresql://neondb_owner:xxxxx@ep-cool-name-12345.us-east-1.aws.neon.tech/neondb?sslmode=require
   ```
   - **COPY THIS ENTIRE STRING** (click the copy icon)

**4. (Optional) Rename Database**:
   - Default database is `neondb` (this is fine to use)
   - OR create new database:
     - Click "Databases" in sidebar
     - Click "New Database"
     - Name: `todo-evolution`
     - Owner: `neondb_owner`
     - Click "Create"
     - Update connection string to use `todo-evolution` instead of `neondb`

---

### STEP 0.2: Backend Environment Configuration (5 minutes)

**1. Create `.env` file**:
   ```bash
   cd backend
   cp .env.example .env
   ```

**2. Edit `backend/.env`** with your values:
   ```bash
   # Paste your Neon connection string here
   DATABASE_URL=postgresql://neondb_owner:xxxxx@ep-cool-name-12345.us-east-1.aws.neon.tech/neondb?sslmode=require

   # Use the generated secrets (already provided below)
   BETTER_AUTH_SECRET=HgkFzYWVxdJjobxlsZRKcSypijaYRuGmXL9Ck+RyNfg=
   JWT_SECRET=jIfhrD71meAWGP2mUim8M3R83udusoW03Tkch9iPQ+E=

   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000

   # Environment
   ENVIRONMENT=development
   ```

**3. Save the file**

**IMPORTANT**: Never commit `backend/.env` to git (it's already in `.gitignore`)

---

### STEP 0.3: Verify Setup (2 minutes)

**1. Test DATABASE_URL Format**:
   Your connection string should have this format:
   ```
   postgresql://[username]:[password]@[host]/[database]?sslmode=require
   ```

**2. Verify Secrets Are Set**:
   ```bash
   # On Linux/Mac:
   cat backend/.env | grep SECRET

   # On Windows PowerShell:
   Get-Content backend\.env | Select-String SECRET
   ```

   You should see both `BETTER_AUTH_SECRET` and `JWT_SECRET` populated.

---

## ✅ Checkpoint: STEP 0.1-0.3 Complete

You should now have:
- ✅ Neon PostgreSQL project created
- ✅ Connection string copied
- ✅ `backend/.env` file created with:
  - DATABASE_URL (your Neon connection string)
  - BETTER_AUTH_SECRET (generated)
  - JWT_SECRET (generated)

---

## 🔄 Next Steps

✅ **STEP 0 Complete!** All environment setup tasks finished:
- ✅ STEP 0.1-0.3: Manual setup (Neon PostgreSQL, .env configuration)
- ✅ STEP 0.4-0.5: Research (FastAPI + Next.js 16 + Better Auth patterns documented in `specs/003-phase-ii-web-app/research.md`)
- ✅ STEP 0.6: Database migration strategy (documented in `specs/003-phase-ii-web-app/data-model.md`)
- ✅ STEP 0.7: Alembic setup (configured, dependencies installed, guide created in `backend/ALEMBIC_SETUP.md`)

**Ready to proceed to STEP 1: Backend Foundation** 🚀

---

## 📚 Resources

- **Neon Docs**: https://neon.tech/docs
- **Neon Console**: https://console.neon.tech
- **PostgreSQL Connection Strings**: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING

---

## ⚠️ Troubleshooting

**Issue**: Can't access Neon website
- **Solution**: Check your internet connection, try different browser

**Issue**: Connection string doesn't work
- **Solution**: Ensure `?sslmode=require` is at the end, verify username/password are correct

**Issue**: Lost my connection string
- **Solution**: Go to Neon dashboard → Click your project → "Connection Details"

---

## 🎉 What's Next After STEP 0?

After completing all of STEP 0 (T001-T023), we'll move to:
- **STEP 1**: Backend Foundation (12-16 hours) - Build FastAPI, models, migrations, API endpoints
- **STEP 2**: Backend Testing (8-10 hours) - Unit & integration tests, ≥80% coverage
- **STEP 3**: Frontend Foundation (12-16 hours) - Next.js 16 + Shadcn/ui (Slate theme)
- And so on...

**Total Phase II**: 46.5 hours (6 days)
