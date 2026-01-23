# Day 10 Social Media Posts — OneTimeShare

**Date**: January 3, 2026  
**Topic**: Password Verification - Maximum Sarcasm Narrator Edition
**Character Count**: 2,718 ✅

---

## 📱 LINKEDIN POST (COPY THIS EXACTLY)

**COPY FROM HERE:**

🔥 Day 10/30: 30 Minutes Staring at a Counter That Wouldn't Count. Then Another 30 Finding ONE Missing Line.

Day 10. Password verification. Should've taken 2 hours.

Narrator: "Spoiler: It did not. Our hero is adorably optimistic."

Took 4.5. With 26 bugs. Existential crisis over a counter that refused to count.

Narrator: "He thought he knew what he was doing. He was so, so wrong."

━━━━━━━━━━━━━

THE COUNTER FROM HELL:

cnt = 0
When password wrong:
    cnt += 1

Wrong password → "Attempt 1 of 5"
Wrong password → "Attempt 1 of 5"  
Wrong password → "Attempt 1 of 5"

15 tests. FIFTEEN.

Narrator: "The counter had no feelings. Unlike our protagonist, who is feeling EVERYTHING."

Restarted Redis. Flask. LAPTOP. Still at 1.

Then: HTTP has no memory. "cnt = 0" runs EVERY REQUEST.

Narrator: "He's fighting HTTP's core design. Like arguing with gravity. Adorable, but futile."

━━━━━━━━━━━━━

THE "FIX" THAT WASN'T:

attempts = redis.get('counter')
attempts += 1
redis.save('counter', attempts)

Narrator: "Look at him. So confident. Precious."

Still stuck. 20 minutes later:

def store_file_metadata():
    save: filename
    save: password_hash
    # password_attempts? ← MISSING

Narrator: "Updating Python memory while Redis sat there, sipping tea, unaware. Beautiful."

━━━━━━━━━━━━━

THEN REDIS EXPLODED:

BOOM. WRONGTYPE error.

Called hgetall() on strings, sets, everything.

Narrator: "Called hgetall() on a string. That's like opening a PDF with a hammer. Wildly incorrect."

━━━━━━━━━━━━━

EARLIER CARNAGE:

• Deleted files BEFORE checking passwords
• Read POST from GET
• Compared bcrypt with ==

Narrator: "Pass 1 was performance art in how NOT to secure anything."

━━━━━━━━━━━━━

WHAT WORKED:

✅ Three routes
✅ Persistent retry limits
✅ Bcrypt security

Narrator: "Only took 26 bugs and what doctors call 'mild trauma.'"

━━━━━━━━━━━━━

BRUTAL TRUTH:

Web apps are distributed systems cosplaying as simple apps.

Every page load has amnesia. Variables? Ghosts. Databases? The only adults.

Narrator: "HTTP is that friend who asks your name every time. For 10 years."

━━━━━━━━━━━━━

TAKEAWAYS:

1️⃣ HTTP is stateless and will gaslight you
2️⃣ Local variables are comforting fiction
3️⃣ If you don't save it, it never existed
4️⃣ Manual testing finds 3 AM bugs

━━━━━━━━━━━━━

Why share?

"Build in Public" showing only wins? Fantasy.

Reality: 26 bugs. 3 rage-quits. 1 developer Googling "is farming hard"

Narrator: "He persisted. Like Sisyphus. Or a moth with an attractive flame."

━━━━━━━━━━━━━

Now working:
✅ Bcrypt verification
✅ Retry limits that COUNT
✅ Files that lock

🔗 GitHub: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

What bug made you question your profession? 👇

#BuildInPublic #Python #Flask #Redis #WebDevelopment #OneTimeShare30 #Debugging #100DaysOfCode

---

**STOP COPYING HERE**

---

## 📝 FIRST COMMENT

```
Narrator: "If this disaster resonated, the repo awaits: github.com/Aayushbankar/onetimeshare"

All 26 bugs documented. The 3 that broke him:
→ Counter stuck (HTTP statelessness)
→ Missing line in store_file_metadata()
→ WRONGTYPE from hgetall() on wrong types
```

---

**READY TO PUBLISH** 🚀  
**POST TIME**: Saturday 7:00 PM IST  
**TARGETS**: 2K+ impressions | 80+ reactions | Maximum Saturday engagement
