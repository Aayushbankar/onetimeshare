---
title: How I Built an End-to-End Encrypted File Sharing App with Flask and ChaCha20 in 30 Days
published: true
description: From empty Git repo to 218 RPS. The complete build log, 6 critical vulnerabilities caught on launch day, and why atomic Redis operations saved me from shipping a brute-force bypass.
tags: showdev, python, webdev, security
cover_image: https://raw.githubusercontent.com/Aayushbankar/onetimeshare/main/docs/images/ui/home.png
---

![OneTimeShare Demo](https://raw.githubusercontent.com/Aayushbankar/onetimeshare/main/docs/images/ui/upload_success.png)

**TL;DR:** I built a self-destructing file sharing app in 30 days. Files are encrypted with ChaCha20-Poly1305, passwords are hashed with Argon2id, and everything deletes after one download. On launch day, I found a race condition that would have let attackers bypass my password limit. Here's the full story.

{% github Aayushbankar/onetimeshare %}

---

## The Problem

Every developer has done it.

Shared an API key in Slack. Sent a `.env` file over WhatsApp. Pasted credentials into a Discord DM.

These messages live forever. They're indexed. They're searchable. They're a breach waiting to happen.

I wanted a tool where:
1. Files are encrypted at rest (the server can't read them)
2. Files delete themselves after one download
3. Password protection is zero-knowledge (the key never touches the server)

Existing tools either store data indefinitely, require accounts, or cost enterprise money.

So I built my own. In 30 days. In public.

---

## The Stack

| Component      | Choice              | Why                                             |
| -------------- | ------------------- | ----------------------------------------------- |
| **Backend**    | Flask (Python 3.13) | Lightweight, flexible, I know it                |
| **Database**   | Redis               | TTL auto-expiry = perfect for ephemeral data    |
| **Encryption** | ChaCha20-Poly1305   | Constant-time, used by Signal, no AES-NI needed |
| **KDF**        | Argon2id            | Memory-hard, GPU-resistant                      |
| **Deployment** | Docker + Render     | Free tier, Gunicorn-ready                       |

**Why ChaCha20 over AES-GCM?**

AES-GCM performance varies based on hardware (AES-NI). ChaCha20-Poly1305 is software-optimized and constant-time everywhere — critical for containerized deployments where you don't control the CPU.

---

## The Build: Week by Week

### Week 1: Foundation (Days 1-7)

**Day 1:** Flask application factory, Dockerfile, docker-compose with Redis.

**Day 2:** Core upload endpoint. UUID filenames (path traversal prevention), extension validation, 20MB limit.

**Day 3:** The first "graveyard" moment.

I built an entire `RedisService` class. Flask ignored it completely.

**The bug:** Missing `__init__.py`.

Two hours. Zero bytes of actual code.

**Day 6:** Atomic self-destruct with Redis `WATCH/MULTI/EXEC`:

```python
pipeline.watch(token)
metadata = redis_client.hgetall(token)
if metadata:
    pipeline.multi()
    pipeline.delete(token)
    pipeline.execute()
    return metadata
```

**Week 1 Bug Count:** 29

---

### Week 2: The Security Core (Days 8-14)

This is where 80% of the bugs lived.

**Day 10: The HTTP Statelessness Disaster**

I implemented password retry limits:

```python
# THE BUG
attempts = 0
if attempts > 5:
    block_user()
attempts += 1
```

**26 bugs in one day.**

All from the same root cause: I forgot that HTTP is stateless. Python variables don't persist across requests. The retry counter had to live in Redis.

The lesson: *Every persistent state must be externalized.*

**Day 14: The DoS I Built**

My "security" feature: delete files after 5 wrong passwords.

The attack I didn't consider: anyone could delete anyone's file by sending 5 wrong passwords.

**The fix:** Lock files, don't delete them. Deletion = DoS vector.

---

### Week 3: Encryption and Hardening (Days 15-21)

**Day 16: Streaming Encryption**

The naive approach: read entire file into memory, encrypt, write back.

The problem: 500MB file = 500MB RAM = OOM kill.

**The solution:** 64KB streaming chunks:

```python
def encrypt_file_chunked(input_path, output_path, key):
    base_nonce = os.urandom(12)  # Unique per file
    cipher = ChaCha20Poly1305(key)
    
    with open(input_path, 'rb') as infile:
        with open(output_path, 'wb') as outfile:
            chunk_num = 0
            while chunk := infile.read(64 * 1024):
                chunk_nonce = increment_nonce(base_nonce, chunk_num)
                encrypted = cipher.encrypt(chunk_nonce, chunk, None)
                outfile.write(len(encrypted).to_bytes(4, 'big'))
                outfile.write(encrypted)
                chunk_num += 1
    return base_nonce
```

**Critical detail:** Nonce = `base_nonce + chunk_number` using arithmetic addition. XOR would cause collisions.

**Day 20: Load Testing**

Ran Locust across 3 tiers:

- **Tier 1 (30 users):** 174 RPS, 355ms p95
- **Tier 2 (100 users):** 116 RPS, 1.3s p95
- **Tier 3 (300 users):** 97 RPS, 3.5s p95

**Result:** Grade A, 0% error rate. Production-ready.

---

### Week 4: Launch (Days 22-30)

**Days 22-25:** CI/CD (GitHub Actions), Playwright E2E tests, security headers (CSP, HSTS, X-Frame-Options).

**Day 29:** Deep security audit. Fixed nonce edge cases, added constant-time comparison.

**Day 30:** The audit that almost didn't happen.

---

## The Day 30 Crisis

9 PM. Launch day. Everything ready.

I almost shipped.

Then I ran one more pass.

### Critical Bug #1: Race Condition

```python
# THE BUG
attempts = int(metadata.get('attempt_to_unlock', 0))
attempts += 1
metadata['attempt_to_unlock'] = str(attempts)
redis_service.store_file_metadata(token, metadata)
```

**The attack:** 50 parallel requests hit this simultaneously.

1. All 50 read `attempts = 0`
2. All 50 compute `attempts = 1`
3. All 50 write `attempts = 1`

**Result:** 50 password guesses for the price of 1. My "5 attempt limit" was fiction.

**The fix:** Atomic increment:

```python
# THE FIX
def increment_file_attempt(self, token: str) -> int:
    return self.redis_client.hincrby(token, "attempt_to_unlock", 1)
```

`HINCRBY` is atomic. Redis serializes operations. No race condition possible.

### Critical Bug #2: Missing CSRF

Admin login had no CSRF token.

**The attack:** Login CSRF. Attacker forces victim to log into attacker's account.

**The fix:** Flask-WTF. 15 minutes.

---

## The Architecture

```
┌─────────────────────────────────────────────────────┐
│                     CLIENT                           │
│  Browser → Drag/Drop → Password (Optional)          │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│                 FLASK + GUNICORN                     │
│  Routes (HTTP) → Services (Logic) → Utils (Crypto)  │
└─────────────────────────────────────────────────────┘
                          │
           ┌──────────────┼──────────────┐
           ▼                             ▼
┌──────────────────────┐    ┌─────────────────────────┐
│       REDIS          │    │    ENCRYPTED DISK       │
│  Metadata (TTL: 5h)  │    │  ChaCha20-Poly1305      │
│  Atomic Counters     │    │  UUID Filenames         │
│  Rate Limit State    │    │  64KB Chunks            │
└──────────────────────┘    └─────────────────────────┘
```

---

## Final Stats

| Metric                  | Value  |
| ----------------------- | ------ |
| Days                    | 30     |
| Commits                 | 60     |
| Bugs Fixed              | 100+   |
| Critical Vulns (Day 30) | 6      |
| Lines of Code           | ~5,000 |

---

## Key Lessons

**1. Read-Modify-Write = Race Condition**

If you're incrementing anything in a distributed system, use atomic operations. Always.

**2. Security is Logic, Not Libraries**

I had ChaCha20. I had Argon2. I still had a brute-force bypass in the application logic.

**3. The Final Audit is Non-Negotiable**

If I'd shipped on Day 29, I'd be writing an incident report.

**4. Build in Public Works**

The pressure of knowing people were watching made me do the extra audit. That audit caught the race condition.

---

## Future Roadmap

- [ ] S3 integration for files > 20MB
- [ ] Public API for CLI access
- [ ] Mobile-optimized UI

---

## Try It

**Live Demo:** [onetimeshare.onrender.com](https://onetimeshare.onrender.com)

**Source Code:** [github.com/Aayushbankar/onetimeshare](https://github.com/Aayushbankar/onetimeshare)

---

*If you learned something, I'd appreciate a follow. I build in public and document everything — including the failures.*

**What's the scariest bug you've found on launch day?** 👇
