# 🔒 OneTimeShare

> **Secure, self-destructing file sharing** — Files are automatically deleted after one download.

![Docker Pulls](https://img.shields.io/docker/pulls/legion4041/onetimeshare?style=flat-square)
![Docker Image Size](https://img.shields.io/docker/image-size/legion4041/onetimeshare/latest?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 🚀 Quick Start

```bash
docker run -d \
  -p 5000:5000 \
  -e SECRET_KEY=your-secret-key \
  -e ADMIN_PASSWORD=your-admin-password \
  legion4041/onetimeshare:latest
```

Then open **http://localhost:5000** 🎉

---

## 🐳 Docker Compose (Recommended)

```yaml
version: '3.8'
services:
  web:
    image: legion4041/onetimeshare:latest
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=change-me-in-production
      - ADMIN_PASSWORD=change-me
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - uploads:/app/uploads

  redis:
    image: redis:alpine
    volumes:
      - redis_data:/data

volumes:
  uploads:
  redis_data:
```

```bash
docker-compose up -d
```

---

## ✨ Features

| Feature                     | Description                        |
| --------------------------- | ---------------------------------- |
| 🔥 **Self-Destruct**         | Files deleted after first download |
| 🔐 **Password Protection**   | Optional bcrypt-hashed passwords   |
| 🔒 **End-to-End Encryption** | ChaCha20-Poly1305 + Argon2id       |
| ⏰ **Auto-Expiry**           | 5-hour TTL (configurable)          |
| 📊 **Admin Dashboard**       | Monitor uploads, downloads, stats  |
| 🐳 **Redis-Backed**          | Fast, ephemeral storage            |

---

## 🔧 Environment Variables

| Variable         | Required | Default                    | Description           |
| ---------------- | -------- | -------------------------- | --------------------- |
| `SECRET_KEY`     | ✅        | -                          | Flask session secret  |
| `ADMIN_PASSWORD` | ✅        | -                          | Admin panel password  |
| `ADMIN_USERNAME` | ❌        | `admin`                    | Admin username        |
| `REDIS_URL`      | ❌        | `redis://localhost:6379/0` | Redis connection      |
| `MAX_FILE_SIZE`  | ❌        | `20`                       | Max upload size (MB)  |
| `REDIS_TTL`      | ❌        | `18000`                    | File expiry (seconds) |

---

## 🌐 Endpoints

| URL           | Description   |
| ------------- | ------------- |
| `/`           | Upload page   |
| `/d/<token>`  | Download file |
| `/auth/login` | Admin login   |
| `/stats`      | Public stats  |

---

## 📖 Full Documentation

**GitHub**: [github.com/Aayushbankar/onetimeshare](https://github.com/Aayushbankar/onetimeshare)

---

## 📄 License

MIT License — Use freely for personal and commercial projects.
