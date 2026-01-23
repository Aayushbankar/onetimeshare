# Day 11 Social Post (Saturday Version)

**Date**: January 4, 2026 (Saturday)  
**Post Time**: 7:00 PM IST (optimal for Saturday)  
**Platform**: LinkedIn  
**Character Count**: TBD (verify with `wc -m`)

---

## 📱 Main Post

🔥 Day 11/30: My Stats Counter Was Haunted. By Yesterday's Data.

Day 11. Built analytics dashboard. Everything worked.

Rebuilt the container. Fresh start.

Narrator: "Spoilers: It wasn't fresh."

Stats showed: 6 uploads. 3 downloads.

I uploaded 0 files. Downloaded 0.

━━━━━━━━━━━━━

THE GHOST IN THE MACHINE:

Rebuilt container → old data appeared
Restarted Redis → still there
Deleted uploads folder → STILL THERE

Narrator: "The data was coming from inside the house."

Then I saw it in the logs:

"BGSAVE done, 11 keys saved"

Redis saves data to disk on shutdown. By default.

Narrator: "Redis doesn't forget. Unlike your ex. At least Redis is consistent."

━━━━━━━━━━━━━

BUT THAT WASN'T THE FIRST BUG:

Before the ghost, there was the typo.

redis.set("uploads", 0)
redis.get("upload")  ← missing 's'

Counter: 0. Files uploaded: 6.

Narrator: "One letter. 20 minutes. His IDE has autocomplete. He has trust issues with it."

I felt stupid.

Narrator: "Growth starts with humiliation. He's growing fast."

━━━━━━━━━━━━━

AND THE STRING DISASTER:

value = redis.get("downloads")
return value  # "3" ← string

JSON API returned: "downloads": "3"

Narrator: "Quotes around a number. That's not data. That's a cry for help."

Fix: return int(value) if value else 0

Narrator: "Page 1 of the docs. Literally page 1. He skipped it like terms and conditions."

━━━━━━━━━━━━━

EARLIER CARNAGE:

• Module-level code resetting counters on reload
• Tracking page VIEWS instead of actual DOWNLOADS
• Counter names with SPACES in them

Narrator: "Three bugs. Three categories of pain. Call it a trilogy nobody asked for."

━━━━━━━━━━━━━

WHAT WORKED:

✅ 8 analytics counters
✅ Stats dashboard (real-time)
✅ Protected badge on uploads
✅ Reset counters on startup (ghosts exorcised)

Narrator: "Finally. Working code. Took him 2 hours. The chimp at the zoo types faster."

━━━━━━━━━━━━━

TAKEAWAYS:

1️⃣ Redis persists by default. Check your config.
2️⃣ Counter names must match EXACTLY
3️⃣ Redis returns strings. Always decode.
4️⃣ Module-level code = pain

━━━━━━━━━━━━━

Why share?

"Build in Public" with only wins? That's Instagram for devs.

Narrator: \"Posting failures for engagement. It's not masochism, it's... okay it's a little masochism.\"

━━━━━━━━━━━━━

Now working:
✅ Analytics that COUNT
✅ Data that DIES (on restart)
✅ Pride (damaged but functional)

🔗 GitHub: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

Ever had data haunt you after a restart? 👇

Narrator: "Redis remembers. Your code doesn't. Choose your battles."

#BuildInPublic #Python #Flask #Redis #WebDevelopment #OneTimeShare30 #Debugging #DebuggingHell #CodingFails #SoftwareEngineering #BackendDevelopment #Analytics #TechHumor #DeveloperLife #RedisPersistence #Programming #LearnToCode #WebDev #100DaysOfCode #TechTwitter

---

## 💬 First Comment (Post Within 60 Seconds)

🔗 Full breakdown: github.com/Aayushbankar/onetimeshare

All 5 passes documented in notes_ai/Day_11/

The 3 bugs that broke me:
→ Counter names didn't match (get vs set)
→ Redis returns strings, not integers
→ Persistence kept old data alive

Tech stack:
→ Flask 3 (routes + stats endpoint)
→ Redis (counters + persistence)
→ Jinja2 (stats dashboard)

Narrator: "If this saved you from the same pain, drop a star ⭐"

---

## 📊 Post Metrics Target

| Metric        | Target |
| ------------- | ------ |
| Impressions   | 2,000+ |
| Reactions     | 80+    |
| Comments      | 20+    |
| Saves         | 10+    |
| GitHub clicks | 15+    |

---

## ✅ Pre-Post Checklist

- [ ] Character count under 2,800 (`wc -m`)
- [ ] NO markdown code blocks
- [ ] Visual separators included
- [ ] Savage narrator commentary (5 lines)
- [ ] First-person emotional content
- [ ] Specific numbers (5 passes, 2h 15m, 11 bugs)
- [ ] GitHub link in first comment
- [ ] 20 hashtags included
- [ ] Engaging question at end
- [ ] Post at 7 PM IST Saturday

---

**Character Count Check**:
```bash
# Run before posting
wc -m posts/Day_11_Social_Posts.md
```

**Status**: Ready for posting!
