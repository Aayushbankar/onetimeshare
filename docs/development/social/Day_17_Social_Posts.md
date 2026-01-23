# Day 17 Social Media Post

## LinkedIn Post

🚀 **30-Day Build Challenge | Day 17/30: The "Stop Hitting Refresh" Update**

**What Got Built:**
✅ Rate Limiting Engine (Flask-Limiter + Redis)
✅ 9 Error Pages Redesigned (404, 500, 429, etc.)
✅ Real-time Abuse Analytics Dashboard
✅ 6 Production Bugs Squashed

---

**The Saga:**

*Narrator: "So after encrypting everything yesterday, our hero woke up thinking: 'You know what this app needs? A bouncer.'"*

Started the day reading Flask-Limiter docs like a detective looking for clues. The plan was simple:
- 5 uploads per hour (because who needs to share 6 cat photos in 60 minutes?)
- 60 downloads per minute (generous, but not insane)
- Redis-backed storage (because memory is… temporary)

*Narrator: "Little did he know, Flask-Limiter 3.x had broken up with the `storage_uri` parameter like a bad Tinder match."*

**Bug #1-3: The Redis Trilogy**
- Hardcoded localhost IP ❌ (Docker containers were NOT amused)
- Wrong key pattern in cleanup script ❌ (Looking for `LIMITER:*` when Flask uses `LIMITS:LIMITER*`)
- Missing 429 error handler route ❌ (Users got generic server errors instead of "slow down, buddy")

*Narrator: "At this point, the rate limiter was limiting… itself. Beautiful irony."*

After 2 hours of Redis CLI spelunking and Docker log archaeology, the limiter FINALLY worked. One test upload… two… three… WHAM. HTTP 429.

*Narrator: "Success! The app now rejects users. What a milestone."*

But then I looked at the 429 error page.

It was… Bootstrap default.
Plain white.
Times New Roman.
Comic Sans vibes.

*Narrator: "He had built a dark, industrial, screw-laden masterpiece, and the error pages looked like a 2005 WordPress blog."*

**The Great Redesign:**
Spent the next hour applying the "Industrial Dark" theme to EVERY error page:
- 400 (Bad Request)
- 401 (Unauthorized)
- 403 (Forbidden)
- 404 (Not Found)
- 410 (Gone)
- 429 (Rate Limit)
- 500 (Server Error)
- 503 (Unavailable)
- 504 (Timeout)

All with the signature screws, containment cards, and shadows. Because even your errors should look good.

*Narrator: "He spent 45 minutes debating screw placement on a 429 page. Let that sink in."*

Added real-time "Limit Hits" tracking to the admin dashboard. Now I can watch bots get blocked in real-time. It's oddly satisfying.

**Final Stats:**
- Lines of code: +487
- Rate limit rules: 2
- Error templates redesigned: 9
- Bugs fixed: 6
- Times I tested by spamming my own app: 23
- Apologies to my Docker container: 1

*Narrator: "He built a rate limiter to stop abuse. Then immediately abused it himself for testing. The cycle of tech."*

**Tomorrow's Plan:**
Mobile responsiveness check. Because if these screws don't look good on a phone, what's even the point?

---

**Tech Stack:**
`Flask-Limiter` | `Redis` | `Jinja2` | `CSS Variables` | `Pure Spite`

---

**What I Learned:**
1. Flask-Limiter 3.x uses `app.config['RATELIMIT_STORAGE_URI']`, not `init` params
2. Always check actual Redis key patterns before writing cleanup scripts
3. Design systems are only systems if you apply them EVERYWHERE
4. Rate limiting your own health check probes is… not ideal

*Narrator: "Day 17: Complete. The app now has a bouncer, a theme, and trust issues."*

---

💬 What's your take: Should a 404 page match your brand identity, or is "Page Not Found" good enough?

---

#100DaysOfCode #WebDev #Flask #Python #Redis #RateLimiting #UIDesign #BuildInPublic #SoftwareEngineering #30DayChallenge

---

## Thread Version (Twitter/X)

🧵 Day 17/30: Built a rate limiter, then spent an hour making sure the "Too Many Requests" error page had perfectly aligned decorative screws.

Priorities? Questionable. Results? *chef's kiss*

1/8 🧵

---

Started with Flask-Limiter docs. Goal: Stop people from uploading their entire hard drive in one sitting.

5 uploads/hour. 60 downloads/min. Redis backend.

Simple, right? 

(Narrator: It was not simple.)

2/8

---

Bug #1: Hardcoded Redis host to localhost
Docker containers: "LOL no"

Bug #2: Wrong key cleanup pattern
Redis: "I have no idea what you're looking for"

Bug #3: Forgot to register 429 error handler
Users: *gets generic 500 error*

Me: 🤦‍♂️

3/8

---

2 hours later, rate limiting WORKS.

Upload count hits 6 → BOOM. HTTP 429.

*Narrator: "He was so excited to see his own app reject him. Character development."*

4/8

---

Then I saw the 429 error page.

White background.
Default font.
Zero personality.

It looked like it time-traveled from 2005.

My beautifully dark, industrial app... serving Times New Roman errors.

Unacceptable.

5/8

---

Redesigned ALL 9 error pages (400, 401, 403, 404, 410, 429, 500, 503, 504) with:
- Industrial dark theme
- Containment cards
- Corner screws (obviously)
- Consistent spacing

Because if you're gonna fail, fail with STYLE.

6/8

---

Added "Limit Hits" counter to admin dashboard.

Now I can watch bots get blocked in real-time.

It's like a firewall, but with more dopamine.

7/8

---

Day 17 Stats:
✅ Rate limiter: Working
✅ Error pages: Gorgeous
✅ Bugs fixed: 6
✅ Times I rate-limited myself testing: 23

*Narrator: "He became the very thing he sought to destroy."*

Tomorrow: Mobile responsiveness audit.

8/8

---

#BuildInPublic #100DaysOfCode #Flask #WebDev

---

## Instagram Caption

🚀 Day 17/30: Rate Limiting & The Great Error Page Redesign

Today's vibe: Building a bouncer for my app, then spending an hour making sure the "you're blocked" message looks aesthetically pleasing.

✨ What Got Done:
• Flask-Limiter integration (5 uploads/hr limit)
• Redesigned 9 error pages with dark industrial theme
• Added real-time abuse tracking dashboard
• Fixed 6 bugs (most of them self-inflicted)

🎭 The Drama:
Started with Flask docs → Hit breaking changes → Spent 2hrs debugging Redis → Finally got rate limiting working → Realized error pages looked like 2005 → Redesigned everything

My favorite part? Debating screw placement on a 429 error page for 45 minutes. Because DETAILS MATTER.

🎯 Lesson: Design systems aren't systems if you don't apply them everywhere. Even your error pages deserve love.

Tomorrow: Making sure those screws look good on mobile 📱

---

#30DayChallenge #WebDevelopment #Flask #Python #Redis #UIDesign #BuildInPublic #CodeLife #TechStack #RateLimiting

---

## Reddit Post (r/webdev or r/flask)

**[Day 17/30] Built rate limiting, then obsessed over error page aesthetics for an hour**

Hey r/webdev! Continuing my 30-day build challenge for a secure file-sharing app.

**Today's Goal:** Add rate limiting to prevent abuse

**What Actually Happened:**
1. Implemented Flask-Limiter with Redis backend
2. Hit 3 separate bugs related to Flask-Limiter 3.x breaking changes
3. Got it working after 2 hours of Redis CLI debugging
4. Looked at the default 429 error page
5. Had an existential crisis
6. Spent the rest of the day redesigning ALL 9 error pages to match my dark industrial theme

**The Bugs:**
- Hardcoded Redis host (Docker wasn't having it)
- Wrong key pattern for cleanup script (`LIMITER:*` vs `LIMITS:LIMITER*`)
- Forgot to register 429 error handler route

**The Redesign:**
Standardized these error pages: 400, 401, 403, 404, 410, 429, 500, 503, 504

Applied:
- Dark theme with CSS variables
- Containment card structure
- Corner screw decorations (my signature)
- Consistent spacing/typography

**Tech Stack:**
- Flask-Limiter 3.x
- Redis for storage
- Jinja2 templates
- Pure CSS (no frameworks)

**Lessons Learned:**
1. Flask-Limiter 3.x requires `app.config['RATELIMIT_STORAGE_URI']` (can't pass to `init_app`)
2. Always verify actual Redis key patterns before writing cleanup code
3. Design consistency matters even (especially?) on error pages

**Question for the community:**
Do you bother styling error pages to match your brand, or is the default "Page Not Found" good enough? Genuinely curious about different perspectives.

GitHub: [Will share at Day 30]
Stack: Flask, Redis, Docker, Cryptography

---

*P.S. Yes, I spent 45 minutes adjusting screw position on a 429 page. No, I'm not sorry.*

---
