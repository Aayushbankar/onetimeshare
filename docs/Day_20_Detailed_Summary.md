# Day 20: Performance Testing & Optimization (Detailed Summary)

## 🏁 The Finish Line of Week 3
Day 20 marked the transition from "Building" to "Hardening". We focused exclusively on ensuring the application can stand up to the rigors of the real world.

## 🔑 Key Achievements

### 1. The Gunicorn Migration
We replaced the development server (Werkzeug) with **Gunicorn**, a production-grade WSGI server.
- **Why**: Werkzeug is single-threaded and insecure for public exposure.
- **Config**: 4 Workers (Parallelism) + 2 Threads (I/O Handling).
- **Result**: The server can now handle concurrent uploads without blocking other users.

### 2. Platinum-Certified Load Testing
We conducted three rigorous passes of load testing:
- **Pass 1 (Baseline)**: Established the limits of the Dev Server (90 RPS, but unstable).
- **Pass 2 (Verification)**: Confirmed Gunicorn stability (169 RPS on heavy load).
- **Pass 3 (Stress)**:
  - **Endurance**: Sustained 30 users for 20s.
  - **Spike**: Survived a burst of 100 users, peaking at **218 RPS**.
  - **Error Rate**: 0.00% across 3,296 requests.

### 3. "The Root Trap" Resolved
We encountered and fixed a classic Docker permission issue where volumes created by `root` were unwritable by our new secure `appuser`. A quick Alpine-based `chown` operation restored order.

## 📊 Metrics That Matter
| Metric             | Day 1 (Baseline)    | Day 20 (Actual) |
| :----------------- | :------------------ | :-------------- |
| **Concurrency**    | 1 User (Sequential) | 100+ Concurrent |
| **Latency (1MB)**  | Varied              | < 400ms (P95)   |
| **Security Score** | F                   | A+ (Verified)   |

## 🔮 What's Next?
Week 4: Launch & Documentation.
- **Day 21**: Rest & Reflection (or Buffer).
- **Day 22**: Production Deployment Setup.
