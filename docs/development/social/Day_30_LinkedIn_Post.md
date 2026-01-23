Day 30: The Launch — LinkedIn Post

---

🔥 30 days ago, I started building a secure file sharing app from scratch.

Tonight, I launched v1.0.0.

It’s deployed. It’s open source. It’s working.

Here is the technical retrospective of the build.

━━━━━━━━━━━━━

THE PROBLEM

I needed a way to share sensitive files (env vars, keys) that:
1. Encrypts data at rest (server cannot read it).
2. Guarantees deletion after one download.
3. Does not persist the decryption key.

Existing tools were either closed source or required accounts. I wanted a stateless, anonymous, secure alternative.

━━━━━━━━━━━━━

THE ARCHITECTURE

• Encryption: ChaCha20-Poly1305.
  Chosen over AES-GCM for consistent performance on containerized hardware without AES-NI.

• Key Derivation: Argon2id.
  Memory-hard hashing prevents GPU brute-forcing of password-protected files.

• Storage: Redis + Ephemeral Disk.
  Redis handles atomic locking and metadata. Files are streamed to disk in 64KB chunks to maintain O(1) memory usage.

• Concurrency: Atomic Redis Operations.
  Use WATCH/MULTI/EXEC transactions to ensure a file can only be downloaded once, even under parallel race conditions.

━━━━━━━━━━━━━

THE DEVELOPMENT REALITY

This wasn't a smooth tutorial. It was 30 days of engineering trade-offs.

• Day 10 (State Management):
  Attempted to track retry limits in application memory.
  Failure: HTTP is stateless. Gunicorn workers don't share memory.
  Fix: Moved state to Redis with atomic counters.

• Day 14 (Availability):
  Implemented "Delete after 5 failures."
  Failure: Created a Denial of Service vector (attackers could delete any file).
  Fix: Changed to "Lock after 5 failures."

• Day 30 (Race Condition):
  Found a read-modify-write race condition in the retry logic during final audit.
  Fix: Replaced logic with Redis HINCRBY (atomic increment).

━━━━━━━━━━━━━

PERFORMANCE

Benchmarked locally (mimicking production constraints) using Locust:

• Throughput: 218 RPS sustained.
• Latency: 355ms p95 at 30 users.
• Efficiency: RAM usage remained flat (<100MB) even while processing 500MB files due to streaming architecture.

━━━━━━━━━━━━━

THE OUTCOME

OneTimeShare is production-ready.

It is not a "hobby script." It is a structured Flask application with:
- Factory pattern architecture
- Service layer abstraction
- 90% test coverage (Pytest + Playwright)
- CI/CD pipelines via GitHub Actions

I am a diploma student. I built this to bridge the gap between theory and production engineering.

━━━━━━━━━━━━━

LINKS

• Live Demo: https://onetimeshare.onrender.com
• Source Code: https://github.com/Aayushbankar/onetimeshare (Stars appreciated if you find the code useful)
• Technical Writeup: Links in comments.

If you are an engineer or hiring manager, I welcome your code review on the repository.

#BuildInPublic #SystemDesign #CyberSecurity #Python #BackendDevelopment #100DaysOfCode #OpenSource

---

First Comment:

Full Technical Breakdown:

I wrote detailed engineering logs for those interested in the implementation details:

• Dev.to (The Build Log): https://dev.to/aayushbankar/how-i-built-an-end-to-end-encrypted-file-sharing-app-with-flask-and-chacha20-in-30-days-9k8
• Medium (The Narrative): https://aayushbankar42.medium.com/how-i-built-an-end-to-end-encrypted-file-sharing-app-in-30-days-using-flask-redis-and-chacha20-069613da2ba7

Feedback on the architecture is welcome.
