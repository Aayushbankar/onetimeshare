# OneTimeShare Architecture

## System Overview

```mermaid
flowchart TB
    subgraph Client["Client Layer"]
        Browser["🌐 Browser"]
        CLI["💻 CLI (Blocked)"]
    end

    subgraph Gateway["Gateway Layer"]
        Nginx["Nginx/Render Proxy"]
        RateLimit["⚡ Rate Limiter"]
        SecurityHeaders["🛡️ Security Headers"]
    end

    subgraph Application["Application Layer"]
        Flask["🐍 Flask App"]
        Gunicorn["⚙️ Gunicorn (4 workers)"]
        
        subgraph Routes["Routes"]
            Upload["/upload"]
            Download["/d/:token"]
            Verify["/verify/:token"]
            Admin["/auth/*"]
        end
        
        subgraph Services["Services"]
            RedisService["RedisService"]
            Encryption["EncryptionUtils"]
            Password["PasswordUtils"]
        end
    endmermaid 

    subgraph Data["Data Layer"]
        Redis[("🔴 Redis\n(Metadata + TTL)")]
        Disk[("💾 Disk\n(Encrypted Files)")]
    end

    Browser --> Nginx
    CLI -.->|"406 Blocked"| Nginx
    Nginx --> RateLimit
    RateLimit --> SecurityHeaders
    SecurityHeaders --> Gunicorn
    Gunicorn --> Flask
    Flask --> Routes
    Routes --> Services
    RedisService --> Redis
    Encryption --> Disk
```

---

## Request Flow: Upload

```mermaid
sequenceDiagram
    participant U as User
    participant F as Flask
    participant E as EncryptionUtils
    participant R as Redis
    participant D as Disk

    U->>F: POST /upload (file, password?)
    F->>F: Validate file (size, type)
    F->>F: Generate UUID token
    
    alt Password Protected
        F->>E: derive_key(password, salt)
    else No Password
        F->>E: generate_key()
    end
    
    F->>E: encrypt_file_chunked()
    E->>D: Write encrypted file
    F->>R: Store metadata + TTL
    R-->>F: OK
    F-->>U: {token, metadata}
```

---

## Request Flow: Download

```mermaid
sequenceDiagram
    participant U as User
    participant F as Flask
    participant R as Redis
    participant E as EncryptionUtils
    participant D as Disk

    U->>F: GET /d/{token}
    F->>F: Check User-Agent (block CLI)
    F->>R: Get metadata
    R-->>F: metadata
    
    alt Protected File
        F-->>U: Render password.html
        U->>F: POST /verify/{token}
        F->>R: Check attempts < 5
        F->>E: derive_key(password, salt)
        F->>E: decrypt_file_chunked()
    else Unprotected
        F->>E: decrypt_file_chunked()
    end
    
    E->>D: Read encrypted file
    D-->>E: Encrypted bytes
    E-->>F: Decrypted stream
    F->>R: Delete metadata
    F->>D: Delete file
    F-->>U: File download
```

---

## Security Layers

```mermaid
flowchart LR
    subgraph L1["Layer 1: Network"]
        HTTPS["🔒 HTTPS/TLS"]
        Headers["Security Headers"]
    end
    
    subgraph L2["Layer 2: Application"]
        RateLimit["Rate Limiting"]
        CLIBlock["CLI Blocking"]
        Auth["Admin Auth"]
    end
    
    subgraph L3["Layer 3: Data"]
        Encrypt["ChaCha20 Encryption"]
        Argon2["Argon2id KDF"]
        TTL["Redis TTL"]
    end
    
    subgraph L4["Layer 4: Physical"]
        Atomic["Atomic Delete"]
        Cleanup["Orphan Cleanup"]
    end
    
    L1 --> L2 --> L3 --> L4
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
