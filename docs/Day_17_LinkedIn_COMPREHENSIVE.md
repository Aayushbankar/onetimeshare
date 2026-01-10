� Day 17/30: Built a Bouncer for My App. Then Rate-Limited My Own Health Checks.

Yesterday: Encrypted everything. Signal-level security.
Today: "Let's add rate limiting. Easy."

Narrator: "Day 16 had 25 bugs. He thought Day 17 would be better. Optimism."

━━━━━━━━━━━━━

THE PLAN (11:39 AM):

Flask-Limiter docs open. Strategy simple:
• 5 uploads/hour (cats have upload limits now)
• 60 downloads/min (generous but not insane)
• Redis persistence (memory dies, Redis remembers)

Narrator: "Flask-Limiter 3.x dumped the storage_uri parameter. Like his ex dumped him. No warning. Just gone."

━━━━━━━━━━━━━

BUG #1: THE LOCALHOST BETRAYAL

limiter = Limiter(storage_uri="redis://localhost:6379")

Works locally? ✅  Works in Docker? ❌

Localhost is INSIDE the container. Not the host.

Fixed: Config.REDIS_HOST from env vars.

━━━━━━━━━━━━━

BUG #2: THE REDIS KEY MYSTERY

Wrote cleanup script:
redis-cli KEYS "LIMITER:*"

Returns: Nothing.

Actual keys? "LIMITS:LIMITER:*"

Flask changed prefixes between versions.

Narrator: "He read yesterday's breach reports. Missed today's release notes."

━━━━━━━━━━━━━

BUG #3: THE PHANTOM 500

Rate limit hit → HTTP 500 error.

Not 429. Not "Too Many Requests."
Generic server explosion.

Why? Forgot to register the error handler.

@app.errorhandler(429)
def rate_limit_error(e):
    # THIS FUNCTION EXISTED
    # JUST... NOT REGISTERED

Narrator: "Like writing a will. Then not signing it. Technically complete. Legally useless. Also like his dating profile. Complete but unregistered."

━━━━━━━━━━━━━

THE BREAKTHROUGH (2 hours in):

Fixed Redis config. Fixed key patterns. Fixed handler.

Test upload #1 → 200 OK
Test upload #2 → 200 OK
Test upload #3 → 200 OK
...
Test upload #6 → HTTP 429 ✅

FINALLY.

Narrator: "He was excited to watch his own app reject him. Character development via self-sabotage."

Added real-time abuse tracking to admin dashboard. Now I can watch bots get blocked live. Oddly satisfying.

━━━━━━━━━━━━━

FINAL DAMAGE:

Bugs found today: 6
Files modified: 8
Redis keys debugged: ALL OF THEM
Times I blocked myself: 23
Sanity: Rate-limited

Narrator: "Day 10: 26 bugs. Day 16: 25 bugs. Day 17: 6 bugs. He's either learning or running out of ways to break things."

━━━━━━━━━━━━━

Now working:
✅ 5 uploads/hour limit
✅ 60 downloads/min limit
✅ Redis-backed rate tracking
✅ Admin analytics dashboard
✅ Exempt health endpoints

Tech: Flask-Limiter | Redis | Python

━━━━━━━━━━━━━

What feature did you build that immediately bit you?

Narrator: "17 days in. Most people quit by Day 3. Or they're smarter. Hard to tell."

#BuildInPublic #Python #Flask #Redis #RateLimiting #WebDevelopment #OneTimeShare30 #100DaysOfCode #DebuggingHell #SoftwareEngineering #BackendDevelopment #TechHumor #DeveloperLife #Programming #LearnToCode
