# 🚀 One-Time Secure File/Text Sharing App
> **30-Day Build Challenge**

![Status](https://img.shields.io/badge/Status-Planning-blue?style=flat-square)
![Language](https://img.shields.io/badge/Language-Python-yellow?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🧐 The Problem
> *Sharing sensitive information (API keys, passwords, configuration files) via email, Discord, or WhatsApp is insecure. Third-party services like Pastebin or WeTransfer store your data on their servers, creating a privacy risk.*

## 💡 The Solution
**Build a lightweight, containerized Python web application** that allows you to:
1. Upload a file or text snippet.
2. Generate a unique, secure link.
3. **Permanently delete** the data from the server immediately after it is viewed once (or after a short timer expires).

---

## � 30-Day Build Roadmap

### Week 1: Foundation (Dec 24 - Dec 31) 🏗️
- [x] **Day 0** (Dec 24): Inception & Foundation - Project defined, Tech Stack confirmed (Flask/Redis), Repo created.
- [ ] **Day 1** (Dec 25): Skeleton & Prototype - Flask/Docker setup, Basic Upload endpoint.
- [ ] **Day 2** (Dec 26): Core Logic - Secure file saving, Metadata structure.
- [ ] **Day 3** (Dec 27): Link Generation - UUIDs, Redis abstraction layer.
- [ ] **Day 4** (Dec 28): Basic UI - Bootstrap setup, Upload Interface.
- [ ] **Day 5** (Dec 29): Download/View - Lookup logic, Download route.
- [ ] **Day 6** (Dec 30): Self-Destruct - Delete-after-read logic, Redis TTL.
- [ ] **Day 7** (Dec 31): Recap & Refactor - Manual testing, Documentation v0.1.

### Week 2: Core Features (Jan 1 - Jan 7) ⚙️
- [ ] **Day 8** (Jan 1): Atomic Limits - Strict one-time use enforcement.
- [ ] **Day 9** (Jan 2): Password UI - Add protection field to upload.
- [ ] **Day 10** (Jan 3): Password Backend - Hashing and verification.
- [ ] **Day 11** (Jan 4): Access Gate - Password entry page.
- [ ] **Day 12** (Jan 5): Validation - File limits, Extensions.
- [ ] **Day 13** (Jan 6): Error Handling - 404/500 pages.
- [ ] **Day 14** (Jan 7): Testing - Week 2 bug fixes.

### Week 3: Security & Polish (Jan 8 - Jan 14) 🔒
- [ ] **Day 15** (Jan 8): Encryption Research - Select AES/Fernet.
- [ ] **Day 16** (Jan 9): Encryption at Rest - Encrypt before save.
- [ ] **Day 17** (Jan 10): Decryption on Fly - Decrypt on download.
- [ ] **Day 18** (Jan 11): Rate Limiting - Flask-Limiter setup.
- [ ] **Day 19** (Jan 12): UI Polish - Animations, Mobile responsive.
- [ ] **Day 20** (Jan 13): Security Audit - Vuln scan, Secret check.
- [ ] **Day 21** (Jan 14): Performance - Week 3 Wrap-up.

### Week 4: Launch & Documentation (Jan 15 - Jan 24) 🚀
- [ ] **Day 22** (Jan 15): Production Docker - Gunicorn setup.
- [ ] **Day 23** (Jan 16): CI/CD - GitHub Actions (Pytest).
- [ ] **Day 24** (Jan 17): Unit Tests - Core logic coverage.
- [ ] **Day 25** (Jan 18): Deployment Prep - Nginx/Proxy config.
- [ ] **Day 26** (Jan 19): Dry Run - VPS/Cloud test.
- [ ] **Day 27** (Jan 20): Documentation - Finalize README/API docs.
- [ ] **Day 28** (Jan 21): Polish - Analytics/Feedback placeholders.
- [ ] **Day 29** (Jan 22): Launch Prep - Demo video, Assets.
- [ ] **Day 30** (Jan 24): **PUBLIC LAUNCH** - Release v1.0.0.

---

## 📝 Daily Adaptation Template

Copy this into your daily log to track progress and blockers.

```markdown
### Evening Review Questions (Answer daily):
- **What surprised me today?** (Technical or feedback)
  - 
- **What's blocking progress?**
  - 
- **What feedback should I act on immediately?**
  - 
- **What can I simplify tomorrow?**
  - 
- **What should I learn tonight to unblock tomorrow?**
  - 

### Morning Planning Questions:
- **Based on yesterday, what needs to change today?**
  - 
- **What's the most valuable single thing I can complete?**
  - 
- **Who can help me with today's challenges?**
  - 
- **What's the simplest implementation that works?**
  - 
- **How can I share today's progress compellingly?**
  - 
```