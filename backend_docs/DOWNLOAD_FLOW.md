# Download Flow Diagram

**Purpose**: Visual guide to file download process

---

## 🔄 Complete Download Flow

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          DOWNLOAD SEQUENCE                                   │
└──────────────────────────────────────────────────────────────────────────────┘

  USER                /d/<token>           REDIS            serve_and_delete()
   │                      │                  │                      │
   │  GET /d/abc123       │                  │                      │
   │─────────────────────▶│                  │                      │
   │                      │  get_metadata()  │                      │
   │                      │─────────────────▶│                      │
   │                      │                  │                      │
   │                      │◀─────────────────│                      │
   │                      │   metadata       │                      │
   │                      │                  │                      │
   │                      │                  │                      │
   │   ┌──────────────────┴──────────────────┴──────┐               │
   │   │            DECISION POINT                  │               │
   │   └────────────────────────────────────────────┘               │
   │                      │                                         │
   │         ┌────────────┼────────────┬────────────┐               │
   │         ▼            ▼            ▼            ▼               │
   │    NOT FOUND     LOCKED     PROTECTED    UNPROTECTED          │
   │         │            │            │            │               │
   │         ▼            ▼            │            │               │
   │◀──410 Gone     ◀──403 Locked      │            │               │
   │                                   ▼            │               │
   │                           password.html        │               │
   │                                   │            │               │
   │   POST /verify/<token>            │            │               │
   │─────────────────────────────────▶ │            │               │
   │                                   │            │               │
   │         ┌─────────────────────────┤            │               │
   │         ▼                         ▼            │               │
   │     CORRECT                    WRONG           │               │
   │         │                         │            │               │
   │         │                         ▼            │               │
   │         │                 increment attempts   │               │
   │         │                         │            │               │
   │         │                   ┌─────┴─────┐      │               │
   │         │                   ▼           ▼      │               │
   │         │               UNDER      LIMIT       │               │
   │         │               LIMIT      REACHED     │               │
   │         │                   │           │      │               │
   │         │                   ▼           ▼      │               │
   │         │        ◀──"X remaining"  ◀──403      │               │
   │         │                                      │               │
   │         └───────────────────┬──────────────────┘               │
   │                             │                                  │
   │                             ▼                                  │
   │                    serve_and_delete()─────────────────────────▶│
   │                                                                │
   │◀───────────────────────STREAM FILE─────────────────────────────│
   │                                                                │
   │                                              DELETE file + meta│
   │                                                                │
```

---

## 🚦 Decision Points

### 1. At `/d/<token>`

```
                    ┌───────────────┐
                    │  /d/<token>   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Metadata      │
                    │ exists?       │
                    └───────┬───────┘
                      │           │
                     NO          YES
                      │           │
                      ▼           ▼
               ┌──────────┐ ┌──────────────┐
               │ 410 Gone │ │ attempts >= 5?│
               └──────────┘ └──────┬───────┘
                              │          │
                             YES        NO
                              │          │
                              ▼          ▼
                       ┌──────────┐ ┌──────────────┐
                       │403 Locked│ │is_protected? │
                       └──────────┘ └──────┬───────┘
                                      │          │
                                     YES        NO
                                      │          │
                                      ▼          ▼
                               ┌──────────┐ ┌──────────────┐
                               │ password │ │serve_and_    │
                               │ form     │ │delete()      │
                               └──────────┘ └──────────────┘
```

### 2. At `/verify/<token>`

```
                    ┌────────────────────┐
                    │ /verify/<token>    │
                    │ POST password      │
                    └────────┬───────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │ Password       │
                    │ provided?      │
                    └────────┬───────┘
                       │          │
                      NO         YES
                       │          │
                       ▼          ▼
                ┌──────────┐ ┌────────────────┐
                │400 Error │ │Password correct?│
                └──────────┘ └────────┬───────┘
                               │            │
                              YES          NO
                               │            │
                               ▼            ▼
                        ┌──────────┐ ┌──────────────┐
                        │ Reset    │ │ Increment    │
                        │ counter  │ │ counter      │
                        └────┬─────┘ └──────┬───────┘
                             │              │
                             ▼              ▼
                      ┌────────────┐ ┌──────────────┐
                      │serve_and_  │ │attempts >= 5?│
                      │delete()    │ └──────┬───────┘
                      └────────────┘   │          │
                                      YES        NO
                                       │          │
                                       ▼          ▼
                                ┌──────────┐ ┌──────────┐
                                │403 Locked│ │Show error│
                                └──────────┘ │+ retry   │
                                             └──────────┘
```

---

## 📁 File Lifecycle

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   UPLOAD    │     │   STORED    │     │  DELETED    │
│             │────▶│             │────▶│             │
│  encrypted  │     │  in Redis   │     │  forever    │
│  to disk    │     │  + disk     │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  DOWNLOAD   │
                    │  decrypt +  │
                    │  stream     │
                    └─────────────┘
```

---

## 🔐 Security Flow

```
┌───────────────────────────────────────────────────────────────────────────┐
│                              UPLOAD PHASE                                 │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   File ──▶ Generate Key ──▶ Encrypt (ChaCha20) ──▶ Store encrypted       │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         ▼                                                     ▼
┌─────────────────────────────────┐     ┌─────────────────────────────────┐
│     IF PASSWORD PROVIDED        │     │     IF NO PASSWORD              │
├─────────────────────────────────┤     ├─────────────────────────────────┤
│                                 │     │                                 │
│  Password ──▶ Argon2id          │     │  Random key stored in Redis    │
│           ──▶ Derive key        │     │  (expires with file)           │
│           ──▶ Store SALT only   │     │                                 │
│                                 │     │                                 │
│  ⚠️ Key NEVER stored!           │     │                                 │
│  (Zero-knowledge)               │     │                                 │
│                                 │     │                                 │
└─────────────────────────────────┘     └─────────────────────────────────┘
                                    │
                                    ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                             DOWNLOAD PHASE                                │
├───────────────────────────────────────────────────────────────────────────┤
│                                                                           │
│   Password ──▶ Re-derive key ──▶ Decrypt ──▶ Stream ──▶ Delete ALL       │
│   (from user)   (using salt)     (ChaCha20)                              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## ⚠️ Error Paths

| Condition            | Route             | Response                |
| -------------------- | ----------------- | ----------------------- |
| Token not in Redis   | `/d/<token>`      | 410 Gone                |
| File not on disk     | `/d/<token>`      | 404 → cleanup metadata  |
| Max retries reached  | `/d/<token>`      | 403 Locked              |
| No password provided | `/verify/<token>` | 400 + form              |
| Wrong password       | `/verify/<token>` | 403 + retry count       |
| Redis down           | Any               | 503 Service Unavailable |
