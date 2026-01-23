# How I Built an End-to-End Encrypted File Sharing App in 30 Days Using Flask, Redis, and ChaCha20

From empty Git repo to 218 RPS. The complete technical breakdown, the 6 critical vulnerabilities I caught on launch day, and why one final audit saved me from shipping a brute-force bypass.

---

**December 24th, 2025.** I made a public commitment: build a production-ready, secure file sharing application in 30 days.

Not a tutorial. Not a "clone this and customize." A real product, from an empty directory to deployed, encrypted, and battle-tested.

**The result:** OneTimeShare — upload a file, get a link, share it, and watch it *permanently delete* after one download. ChaCha20-Poly1305 encryption. Argon2id password hashing. Atomic Redis operations. Zero-knowledge architecture.

This post is the complete technical breakdown.

**Try the live demo:** https://onetimeshare.onrender.com

**Full source code:** https://github.com/Aayushbankar/onetimeshare

---

# Part I: The "Why" — Defining the Problem Space

## The Inciting Incident

Every developer has done it: shared an API key in Slack. Sent a `.env` file over WhatsApp. Pasted credentials into a Discord DM.

These messages live forever. They're indexed. They're searchable. They're a breach waiting to happen.

I wanted a tool where:

1. Files are encrypted at rest (the server can't read them).
2. Files delete themselves after one download.
3. Password protection is zero-knowledge (the key is derived client-side).

Existing tools either store your data indefinitely, require accounts, or are designed for enterprise budgets. I wanted something simple, open-source, and uncompromisingly secure.

## The Stack Decision

**Backend:** Flask (Python 3.13) — Lightweight, flexible, I know it well

**Database:** Redis — Perfect for ephemeral data with TTL auto-expiry

**Encryption:** ChaCha20-Poly1305 — Constant-time, used by Signal, no AES-NI dependency

**KDF:** Argon2id — Memory-hard, GPU-resistant

**Deployment:** Docker + Render — Free tier, horizontal scaling, Gunicorn-ready

The choice of ChaCha20 over AES-GCM was deliberate. AES-GCM performance varies dramatically based on hardware (AES-NI presence). ChaCha20-Poly1305 is software-optimized and maintains constant-time properties regardless of the environment — critical for a containerized deployment where hardware is unpredictable.

---

# Part II: The "How" — 30 Days in the Crucible

## Week 1: Building the Foundation (Days 1–7)

The first week was about getting the skeleton right.

**Day 1:** Flask application factory, Dockerfile, docker-compose.yml with Redis.

**Day 2:** Core upload endpoint. UUID-based filenames (preventing path traversal), extension validation, 20MB limit.

**Day 3:** The first "graveyard" moment. I built an entire `RedisService` class. Flask silently ignored it.

**The bug:** Missing `__init__.py` in the services directory. Two hours, zero bytes of actual code change.

**Day 6:** Implemented atomic self-destruct using Redis `WATCH/MULTI/EXEC`. This was the first real architectural decision — ensuring that concurrent downloads couldn't result in duplicate file access.

```python
# Atomic read-and-delete pattern
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

## Week 2: The Security Core (Days 8–14)

This is where the real engineering started — and where 80% of the bugs lived.

### Day 10: The HTTP Statelessness Disaster

I implemented password retry limits. Simple, right?

```python
# THE BUG: This resets every request
attempts = 0
if attempts > 5:
    block_user()
attempts += 1
```

**26 bugs in one day.** All stemming from the same root cause: I forgot that HTTP is stateless. Local Python variables don't persist across requests. The retry counter had to live in Redis.

The lesson was humiliating but essential: *every persistent state must be externalized.*

### Day 14: The DoS Vulnerability I Built

My "security" feature: delete the file after 5 wrong password attempts.

The attack vector I didn't consider: an attacker could grief any user by sending 5 wrong passwords to any file. File gone. Availability destroyed.

**The fix:** Lock files on max retries, don't delete them. Deletion creates a denial-of-service vector; locking preserves data availability while still preventing brute-force.

---

## Week 3: Encryption and Hardening (Days 15–21)

### Day 16: Implementing ChaCha20-Poly1305 Streaming

The naive approach to file encryption: read the entire file into memory, encrypt, write back.

The problem: A 500MB file would require 500MB+ of RAM. On a container with 512MB allocated, this is an OOM kill waiting to happen.

**The solution:** Chunked streaming encryption with 64KB blocks.

```python
def encrypt_file_chunked(input_path, output_path, key):
    base_nonce = os.urandom(12)  # Unique per file
    cipher = ChaCha20Poly1305(key)
    
    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
        chunk_num = 0
        while chunk := infile.read(64 * 1024):
            chunk_nonce = increment_nonce(base_nonce, chunk_num)
            encrypted = cipher.encrypt(chunk_nonce, chunk, None)
            outfile.write(len(encrypted).to_bytes(4, 'big') + encrypted)
            chunk_num += 1
    return base_nonce
```

**Critical detail:** The nonce for each chunk is derived as `base_nonce + chunk_number` using arithmetic addition (not XOR). This prevents nonce reuse while maintaining deterministic decryption order.

### Day 20: Load Testing

Ran Locust stress tests across 3 tiers:

- **Tier 1 (30 users):** 174 RPS, 355ms p95 latency
- **Tier 2 (100 users):** 116 RPS, 1.3s p95 latency
- **Tier 3 (300 users):** 97 RPS, 3.5s p95 latency

**Result:** Grade A across all tiers with 0% error rate. The system was production-ready.

---

## Week 4: The Launch Sprint (Days 22–30)

**Days 22–25:** CI/CD with GitHub Actions, Playwright end-to-end tests, security headers (CSP, HSTS, X-Frame-Options).

**Day 29:** Deep security audit. Found and fixed nonce generation edge cases, added constant-time comparison for password verification.

**Day 30:** The audit that almost didn't happen.

---

# Part III: The "So What" — Day 30 and the Final Audit

At 9 PM on launch day, everything was ready. Tests green. Docker building. README polished.

I almost shipped.

Then I ran one more security pass.

## Critical Vulnerability #1: The Race Condition

```python
# THE BUG
attempts = int(metadata.get('attempt_to_unlock', 0))
attempts += 1
metadata['attempt_to_unlock'] = str(attempts)
redis_service.store_file_metadata(token, metadata)
```

**The attack:** 50 parallel requests hit this endpoint simultaneously.

1. All 50 read `attempts = 0`
2. All 50 compute `attempts = 1`
3. All 50 write `attempts = 1`

**Result:** 50 password guesses for the price of 1. My "5 attempt limit" was fiction.

**The fix:** Atomic increment using Redis `HINCRBY`.

```python
# THE FIX: Atomic operation
def increment_file_attempt(self, token: str) -> int:
    return self.redis_client.hincrby(token, "attempt_to_unlock", 1)
```

`HINCRBY` is atomic. Redis serializes the operations. No race condition possible.

## Critical Vulnerability #2: Missing CSRF

The admin login form had no CSRF token. I thought, "It's just a login page."

**The attack:** Login CSRF. An attacker could force a victim to log into the attacker's account, then monitor activity.

**The fix:** Flask-WTF. 15 minutes of implementation.

## The Final Count

- **Days:** 30
- **Commits:** 60
- **Bugs Fixed:** 100+
- **Critical Vulnerabilities (Day 30):** 6
- **Lines of Code:** ~5,000

---

# The Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT                               │
│  Browser → Drag/Drop Upload → Password (Optional)           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      FLASK + GUNICORN                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │   Routes    │  │  Services   │  │   Utils     │          │
│  │ (HTTP I/O)  │──│ (Business)  │──│ (Crypto)    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│         REDIS           │     │      ENCRYPTED DISK         │
│  - Metadata (TTL: 5h)   │     │  - Files (ChaCha20-Poly1305)│
│  - Atomic Counters      │     │  - UUID Filenames           │
│  - Rate Limit State     │     │  - 64KB Chunks              │
└─────────────────────────┘     └─────────────────────────────┘
```

---

# Key Learnings

**1. "Read-Modify-Write" is a race condition.**

If you're incrementing anything in a distributed system, use atomic operations. I don't care how simple it looks.

**2. Security is a logic problem, not a library problem.**

I had ChaCha20. I had Argon2. I still had a brute-force bypass hiding in the application logic.

**3. The final audit is non-negotiable.**

If I'd shipped on Day 29, I would be writing an incident report, not a launch post.

**4. Build in public works.**

The pressure of knowing people were watching made me do the extra audit. That audit caught the race condition.

---

# What's Next

OneTimeShare v1.0.0 is live. The challenge is complete.

**Roadmap:**
- S3 integration for files > 20MB
- Public API for CLI access
- Mobile-optimized UI

**Try it now:** https://onetimeshare.onrender.com

**Inspect the code:** https://github.com/Aayushbankar/onetimeshare

---

*If you learned something from this breakdown, I'd appreciate a follow. I build in public and document everything — including the failures.*

*Questions about the architecture, the encryption, or the bugs? Drop them in the comments.*
