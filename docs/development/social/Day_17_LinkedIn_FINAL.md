🚀 Day 17/30: The "Stop Hitting Refresh" Update

Narrator: "So after encrypting everything yesterday, our hero woke up thinking: 'You know what this app needs? A bouncer.'"

Started the day reading Flask-Limiter docs. The plan was simple:
• 5 uploads per hour (who needs 6 cat photos in 60 minutes?)
• 60 downloads per minute  
• Redis-backed storage

Narrator: "Little did he know, Flask-Limiter 3.x had broken up with the storage_uri parameter like a bad Tinder match."

━━━━━━━━━━━━━

THE REDIS TRILOGY

Bug #1: Hardcoded localhost IP
Docker containers were NOT amused.

Bug #2: Wrong key pattern in cleanup script
Looking for LIMITER:* when Flask uses LIMITS:LIMITER*

Bug #3: Missing 429 error handler route
Users got generic 500 errors instead of "slow down, buddy"

Narrator: "At this point, the rate limiter was limiting… itself. Beautiful irony."

━━━━━━━━━━━━━

THE BREAKTHROUGH

After 2 hours of Redis CLI spelunking and Docker log archaeology, the limiter FINALLY worked.

One test upload… two… three… WHAM. HTTP 429.

Narrator: "Success! The app now rejects users. What a milestone."

Added real-time "Limit Hits" tracking to the admin dashboard. Now I can watch bots get blocked in real-time. Oddly satisfying.

Also standardized error pages to match the theme. Because if you're gonna fail, fail with style.

━━━━━━━━━━━━━

FINAL STATS

• Lines of code: +487
• Rate limit rules: 2
• Error templates redesigned: 9
• Bugs fixed: 6
• Times I tested by spamming my own app: 23

Narrator: "He built a rate limiter to stop abuse. Then immediately abused it himself for testing. The cycle of tech."

━━━━━━━━━━━━━

KEY LESSONS

1. Flask-Limiter 3.x uses app.config, not init params
2. Check actual Redis key patterns before cleanup scripts
3. Design systems = applying them EVERYWHERE
4. Don't rate-limit your own health checks

━━━━━━━━━━━━━

TOMORROW: Mobile check. If screws don't look good on phones, what's the point?

Tech: Flask-Limiter | Redis | Jinja2 | CSS

━━━━━━━━━━━━━

Should a 404 page match your brand, or is "Page Not Found" enough?

Narrator: "He's asking for validation on screw placement. This is where we are."

#BuildInPublic #Python #Flask #Redis #WebDevelopment #RateLimiting #UIDesign #100DaysOfCode #DebuggingHell #SoftwareEngineering #BackendDevelopment #TechHumor #DeveloperLife #CodeNewbie #Programming #LearnToCode #WebDev #CodingFails #OneTimeShare30
