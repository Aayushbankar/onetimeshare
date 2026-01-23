# Day 14 Social Posts — Week 2 Wrap & Mid-Point

**Date**: January 7, 2026 (Wednesday)  
**Post Time**: 6:30 PM IST  

---

## 🚀 Post 1: The Daily Log (Security Disaster Class)
**Schedule**: Today (Wednesday), 7:00 PM IST

▼▼▼ COPY BELOW THIS LINE ▼▼▼

🔥 I Accidentally Built the "Account Lockout" Bug... but on Steroids.

━━━━━━━━━━━━━

Day 14/30. I tried to patch a small security hole.
Instead, I built a feature that allowed anyone to delete anything.

Narrator: "He skipped the 'Logic' chapter of the Security Handbook. Bold move."

━━━━━━━━━━━━━

THE ORIGINAL BUG (Pass 1):

I found a vulnerability: If you guessed the password wrong 5 times, the file locked... but you could just refresh the page to try again.

Infinite brute-force attempts. 

Narrator: "Ah yes. Security via 'Please Do Not Refresh'. Very polite."

━━━━━━━━━━━━━

THE "FIX" (The Disaster):

I decided to be ruthless.
"If they hit 5 wrong attempts? NUKE IT. Delete the file."

I felt like an admin god. "This will teach them."
I deployed it.

Then I realized what I had actually done.

If *I* can delete a file by entering "password123" 5 times...
So can a script.
So can a bored teenager.

I didn't fix security. I re-invented the classic **"Account Lockout DoS"**—but instead of just locking you out, I burned your house down.

It's a textbook **Business Logic Vulnerability**. I handed the internet a "Delete" button for files they don't own.

Narrator: "He basically built the Self-Destruct button from Doofenshmirtz Evil Incorporated. But put it on the outside of the building."

━━━━━━━━━━━━━

THE REAL FIX (Pass 3):

Reverted the nuclear option.
Now, it soft-locks the file. 

- Attacker: "I'll brute force it!" -> Server: "Lol no."
- Owner: "Is my file safe?" -> Server: "Yes, just locked."
- Me: "Am I fired?" -> Narrator: "If this wasn't a solo project, HR would be waiting in the lobby."

━━━━━━━━━━━━━

THE LESSON:

Availability is a security metric (the 'A' in CIA triad).
If your "defense" destroys the user's data, you haven't secured it. You've just done the hacker's job for them.

Narrator: "He's still sad he can't use the delete button. He loves the delete button."

━━━━━━━━━━━━━

Now Working:
✅ Retry limits that don't nuke the database
✅ IDOR/Logic protections (finally)
✅ Zero-Knowledge privacy
✅ End-to-end encryption (Week 3!)

🔗 Roast my code here: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

What's the most dangerous "Security Feature" you've ever accidentally built? 👇

Narrator: "Be honest. You've definitely created an admin/admin login. We all saw it."

#BuildInPublic #CyberSecurity #DoS #Log4Shell #InfoSec #OneTimeShare30 #CodingFails #WebDev #Flask #Redis #SoftwareEngineering #Debugging #DeveloperLife #TechHumor

▲▲▲ COPY ABOVE THIS LINE ▲▲▲

---

## 📊 Post 2: Week 2 Summary (From "Hello World" to Enterprise)
**Schedule**: Friday, 6:00 PM IST

▼▼▼ COPY BELOW THIS LINE ▼▼▼

🔥 Week 2 Report: I Accidentally Built an Enterprise App for One Person.

━━━━━━━━━━━━━

Day 14/30 of #OneTimeShare30.
I started with "simple file upload."
I ended up with Zero-Knowledge Privacy, Admin Dashboards, and rate-limited auth.

It escalated quickly.

Narrator: "Because he has zero chill. Zero."

━━━━━━━━━━━━━

WHAT WE "SHIPPED" (Days 8-14):

🔐 **Security (The Good)**:
- Bcrypt password hashing (Salted, Hashed, Fried)
- Retry lockouts (Soft locks, not self-destructs... anymore)
- Blind Admin Mode (I can't see your filenames, NSA style)

🚀 **The "Overkill" Features (The Bad)**:
- Real-time Analytics Dashboard (For... me?)
- Config-based Authentication (Replaced a SQL DB I didn't need)
- Auto-logout mechanisms (Because I don't trust myself)
- Redis persistence tuning

🐛 **The Damage Report (The Ugly)**:
- 26 bugs squashed
- 1 DoS vulnerability created & patched (The "4Chan Button")
- 1 Major pivot (SQLAlchemy -> .env)

Narrator: "He spent 3 hours debating database schema for a single user. That user was him. He lost the debate."

━━━━━━━━━━━━━

THE BIG PIVOT (Day 13):

I was building a complex SQL User system. For one admin.
I deleted 200 lines of code. Replaced it with 2 lines of config.

Result: Faster. Safer. Simpler.
Pain: 10/10.

Narrator: "Deleting code is the only time he feels something."

━━━━━━━━━━━━━

COMING UP (Week 3):

- Encryption-at-rest (The big one)
- Rate Limiting (Flask-Limiter)
- Finally fixing the UI (It looks like 1998 called)

Goal: A file sharing service that knows NOTHING about your files.

🔗 Code + Mistakes Log: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

What's the most "Overkill" feature you've ever built? 👇

Narrator: "Besides your dating profile requirements. Keep it technical."

#BuildInPublic #WeeklyUpdate #SaaS #Python #Flask #WebDev #OneTimeShare30 #Progress #MVP #Startup #IndieHacker #Coding #SoftwareDev

▲▲▲ COPY ABOVE THIS LINE ▲▲▲

---

## 🏁 Post 3: Halfway Point (The Truth About "Building in Public")
**Schedule**: Saturday, 7:00 PM IST

▼▼▼ COPY BELOW THIS LINE ▼▼▼

🔥 Halfway Through a 30-Day Build. The "Honeymoon Phase" is Dead. 🪦

━━━━━━━━━━━━━

Day 14/30.
The dopamine of "Day 1" is gone.
Now, it's just me, a Redis container, and my poor life choices.

This is the messy middle.

Narrator: "He misses 'Hello World'. Simpler times."

━━━━━━━━━━━━━

THE REALITY CHECK:

running_on_caffeine = True
sanity_level = "Critical"

Day 1-7 (The Dream):
"Wow, Flask is fast! Redis is magic!"
• Built everything in hours
• Felt like a 10x engineer

Day 8-14 (The Reality):
"Why is Docker DNS failing? What is a race condition? Why did I do this?"
• Edge cases everywhere
• Security holes
• Admin tools

Narrator: "Day 15-21 Prediction: Crying over encryption algorithms."

━━━━━━━━━━━━━

BIGGEST LESSON SO FAR:

Code is easy. Making *decisions* is exhausting.
- "DB or No DB?" (Wasted 3 hours)
- "Delete or Lock?" (Created a security CVE)
- "React or Jinja?" (Stuck with ugly HTML because I respect myself)

Everything is a trade-off. And every trade-off hurts.

Narrator: "He's being dramatic. He loves it."

━━━━━━━━━━━━━

CURRENT STATUS:

✅ Core Engine: 100%
✅ Security: 85% (Patched the 4chan hole)
✅ UI/UX: 40% (It works if you squint)
✅ Encryption: 0% (Starting tomorrow. Pray for me.)

We are on track. Somehow.

🔗 Follow the disaster: github.com/Aayushbankar/onetimeshare

━━━━━━━━━━━━━

How do you push through the "Middle of the Project" slump? 👇

Narrator: "Coffee. Spite. And fear of public failure. Mostly spite."

#OneTimeShare30 #BuildInPublic #HalfwayPoint #IndieDev #SaaS #WebDevelopment #Python #CodingJourney #Developer #Tech #Motivation #Discipline #100DaysOfCode

▲▲▲ COPY ABOVE THIS LINE ▲▲▲
