# Day 20 Social Posts (The "Fight Club" Edition)

## 👔 LinkedIn: The "Violence" Post (FINAL)

🔥 Today, I chose violence. And lost. 🥊

Day 20 of building OneTimeShare.
I woke up and decided to destroy everything I love.

I call it "Load Testing."
Real engineers call it "DDOSing yourself because you have trust issues."

Narrator: "He woke up and chose chaos. The chaos wasn't interested."

━━━━━━━━━━━━━

THE EXPERIMENT

I fired up a script to simulate 100 angry users hitting the "Upload" button simultaneously.
I wanted fire. I wanted explosions. I wanted error 500s.

THE RESULT:

• 218 Requests/Second (Peak)
• 0.00% Error Rate
• Latency: < 400ms

The app didn't flinch. Gunicorn ate the traffic like it was a light snack.
I failed to break my own code.

Narrator: "He's visibly disappointed that his server didn't catch fire. He bought marshmallows."

━━━━━━━━━━━━━

THE SHAME

It wasn't all perfect.
I hit a "429 Too Many Requests" error immediately.
I thought I broke the internet.

Turns out, I just forgot to disable my own rate limiter.

Narrator: "He built a security system so good, it locked him out of his own house. Genius."

━━━━━━━━━━━━━

THE NERD STATS

• Previous: Flask Dev Server (90 RPS, sweating profusely)
• Current: Gunicorn + 4 Workers + 2 Threads (218 RPS, bored)

We are officially ready for the chaos of the internet.

Narrator: "He printed a certificate that says 'Not Garbage'. It's on the fridge."

━━━━━━━━━━━━━

Why share the failures?

Because "perfect" software is a lie.
Behind every "Production Ready" app is a developer who locked themselves out 5 times.

Narrator: "Or six. We stopped counting."

━━━━━━━━━━━━━

Now working:
✅ Gunicorn WSGI Server (Optimized)
✅ Redis Rate Limiting (Re-enabled)
✅ Argon2id Encryption (Streaming)

🔗 GitHub: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

What's the dumbest way you've broken your own app?

Narrator: "If you say 'recursive loop in production', you win a hug."

#BuildInPublic #OneTimeShare30 #LoadTesting #DevOps #Python #Flask #Redis #WebDevelopment #DebuggingHell #CodingFails #SoftwareEngineering #BackendDevelopment #100DaysOfCode #TechHumor #DeveloperLife #CodeNewbie #Programming #LearnToCode #WebDev #TechTwitter

---

### 💬 First Comment (Post Immediately)

🔗 Complete breakdown: github.com/Aayushbankar/onetimeshare

All 3 Load Test Passes documented in docs/Day_20_Load_Testing_Report.md

The 3 things that saved us:
→ Gunicorn Worker/Thread tuning
→ Redis atomic locks
→ Ignoring my own inability to configure permissions

Narrator: "If this saved you from the same pain, drop a star ⭐"

---

## 🐦 Twitter/X: The "Indestructible" Tweet

I spent 5 hours trying to murder my own app today. 🔪
100 concurrent users. 1MB encrypted uploads. 218 RPS.

It survived.
0% Error Rate.

I have never been so happy to be a failure.
OneTimeShare 1, Developer 0. 🏳️

Narrator: "He's crying in the corner. It's a mix of pride and exhaustion."

#Day20 #IndieDev #Python #LoadTesting #BuildInPublic
