# OneTimeShare Architecture

## System Overview

```
+-----------------------------------------------------------+
|                       Client Layer                        |
|                                                           |
|   +-------------------+       +-----------------------+   |
|   |    🌐 Browser     |       |   💻 CLI (Blocked)    |   |
|   +---------+---------+       +-----------+-----------+   |
|             |                             |               |
+-------------|-----------------------------|---------------+
              |                             |
              v                             v
+-----------------------------------------------------------+
|                      Gateway Layer                        |
|                                                           |
|   +-------------------+       +-----------------------+   |
|   | Nginx/Render Proxy|<------| "406 Not Acceptable"  |   |
|   +---------+---------+       +-----------------------+   |
|             |                                             |
|             v                                             |
|   +-------------------+                                   |
|   |  ⚡ Rate Limiter  |                                   |
|   +---------+---------+                                   |
|             |                                             |
|             v                                             |
|   +-------------------+                                   |
|   |🛡️ SecurityHeaders|                                   |
|   +---------+---------+                                   |
|             |                                             |
+-------------|---------------------------------------------+
              |
              v
+-----------------------------------------------------------+
|                    Application Layer                      |
|                                                           |
|        +-----------------------------------------+        |
|        |       ⚙️ Gunicorn (4 workers)           |        |
|        +--------------------+--------------------+        |
|                             |                             |
|                             v                             |
|        +--------------------+--------------------+        |
|        |             🐍 Flask App                |        |
|        |                                         |        |
|        |   +---------------------------------+   |        |
|        |   |             Routes              |   |        |
|        |   |  /upload, /d/:token, /auth/*    |   |        |
|        |   +----------------+----------------+   |        |
|        |                    |                    |        |
|        |                    v                    |        |
|        |   +---------------------------------+   |        |
|        |   |            Services             |   |        |
|        |   | RedisService, EncryptionUtils   |   |        |
|        |   +----------------+-------+--------+   |        |
+--------|--------------------|-------|-------------|-------+
         |                    |       |             |
         v                    v       v             v
+------------------+    +------------------+  +-------------+
|    Data Layer    |    |    Data Layer    |  | File System |
|                  |    |                  |  |             |
| +--------------+ |    | +--------------+ |  | +---------+ |
| |   🔴 Redis   | |    | |   🔴 Redis   | |  | | 💾 Disk | |
| |(Metadata+TTL)| |    | |(Metadata+TTL)| |  | |(Encrypt)| |
| +--------------+ |    | +--------------+ |  | +---------+ |
+------------------+    +------------------+  +-------------+
```

---

## Request Flow: Upload

```
User                Flask App           EncryptionUtils          Redis                Disk
 |                      |                      |                   |                   |
 |--- POST /upload ---->|                      |                   |                   |
 | (file, password?)    |                      |                   |                   |
 |                      |---- Validate File -->|                   |                   |
 |                      |                      |                   |                   |
 |                      |--- Generate UUID --->|                   |                   |
 |                      |                      |                   |                   |
 |                      |-- Derive/Gen Key --->|                   |                   |
 |                      |                      |                   |                   |
 |                      |--- Encrypt Chunk --->|                   |                   |
 |                      |                      |-------------------------------------->|
 |                      |                      |                   | Write Encrypted   |
 |                      |                      |                   |                   |
 |                      |--- Store Metadata ---------------------->|                   |
 |                      |                      |                   |                   |
 |<-- {token, meta} ----|                      |                   |                   |
 |                      |                      |                   |                   |
```

---

## Request Flow: Download

```
User                Flask App           Redis                EncryptionUtils          Disk
 |                      |                  |                        |                   |
 |---- GET /d/{token} ->|                  |                        |                   |
 |                      |-- Check Agent -> |                        |                   |
 |                      |                  |                        |                   |
 |                      |-- Get Metadata ->|                        |                   |
 |                      |<- {metadata} ----|                        |                   |
 |                      |                  |                        |                   |
 | [If Protected]       |                  |                        |                   |
 |<-- 401 Password HTML-|                  |                        |                   |
 |--- POST /verify ---->|                  |                        |                   |
 |                      |-- Check Tries -->|                        |                   |
 |                      |                  |                        |                   |
 |                      |-- Derive Key --->|                        |                   |
 |                      |                  |                        |                   |
 | [Decrypt Stream]     |                  |                        |                   |
 |                      |                  |--- Decrypt Chunk <------------------------|
 |                      |                  |                        |  Read Encrypted  |
 |<-- File Stream ------|                  |                        |                   |
 |                      |                  |                        |                   |
 | [Cleanup]            |                  |                        |                   |
 |                      |-- Delete Key --->|                        |                   |
 |                      |                  |                        |                   |
 |                      |------------------------------------------------------------->|
 |                      |                  |                        |    Delete File    |
```

---

## Security Layers

```
+-------------------+       +-------------------+       +-------------------+       +-------------------+
| Layer 1: Network  | ----> | Layer 2: App      | ----> | Layer 3: Data     | ----> | Layer 4: Physical |
+-------------------+       +-------------------+       +-------------------+       +-------------------+
| 🔒 HTTPS/TLS      |       | ⚡ Rate Limiting  |       | 🔑 ChaCha20 Keys  |       | 💥 Atomic Delete  |
| 🛡️ Sec Headers    |       | 🚫 CLI Blocking   |       | 🛡️ Argon2id KDF   |       | 🧹 Orphan Cleanup |
|                   |       | 👮 Admin Auth     |       | ⏲️ Redis TTL      |       |                   |
+-------------------+       +-------------------+       +-------------------+       +-------------------+
```

---

## Technology Stack

| Layer          | Technology                      |
| -------------- | ------------------------------- |
| **Frontend**   | HTML, CSS, JavaScript           |
| **Backend**    | Python 3.13, Flask 3.x          |
| **WSGI**       | Gunicorn                        |
| **Database**   | Redis (ephemeral)               |
| **Encryption** | ChaCha20-Poly1305, Argon2id     |
| **Auth**       | Flask-Login, Flask-JWT-Extended |
| **Testing**    | pytest, Playwright              |
| **CI/CD**      | GitHub Actions                  |
| **Deployment** | Render (Docker)                 |
