# Day 02 Social Media Posts - OneTimeShare 30-Day Build Challenge

---

## 📘 LinkedIn Post (Long-Form)

**Title/Hook**: 🔥 Day 2/30: I Failed 4 Times Before My File Upload Worked

---

Day 2 of #OneTimeShare30.

I went from 58% working code to 95% in 3 hours.
But those 3 hours? Pure chaos.

**Quick recap**: I'm building a one-time secure file sharing app in 30 days.
Upload a file → Get a link → They view it once → It's **deleted forever**.

---

**What I tried to build today:**
- Accept file uploads via API
- Save files with UUID filenames (for security)
- Store metadata in Redis with auto-expiration
- Validate file extensions and size

Sounds simple. It wasn't.

---

**Here's what actually happened:**

🔴 **Try 1 (58%)**
I mixed up `import config` vs `from config import Config`.
Python doesn't warn you when you shadow a module with a variable. It just breaks.

🔴 **Try 2 (70%)**
Got "Error connecting to redis:6379. Name or service not known."
*Facepalm moment*: I was running Flask locally, not in Docker. `redis` isn't a valid hostname on my machine.

🔴 **Try 3 (85%)**
File upload returned success. I checked the uploads folder.
**It was empty.**
I had *deleted* the `os.makedirs()` line while refactoring. The folder didn't exist.

🟢 **Try 4 (95%)**
```json
{
  "status": "success",
  "filename": "5872fbb3-564a-4c18-be92-5b02e979d9f8.txt",
  "token": "5872fbb3-564a-4c18-be92-5b02e979d9f8.txt"
}
```
It works. File saved. Metadata in Redis. TTL set. Extension validation active.

---

**The hardest lesson today:**

Understanding concepts is easy.
Integration is hard.

I *understood* how Flask handles uploads.
I *understood* how UUIDs work.
I *understood* how Redis hashes work.

But putting them together? That's where the real learning happens.

---

**Today's Key Takeaways :**

1️⃣ `import module` ≠ `from module import Class`
   Know this cold. It will bite you.

2️⃣ Never return "success" for operations that didn't happen
   My code returned success while `file.save()` was commented out. That's how production bugs are born.

3️⃣ `os.makedirs(folder, exist_ok=True)` is not optional
   Before writing to a folder, make sure it exists. Every. Single. Time.

4️⃣ `decode_responses=True` in Redis
   Without it, you get `{b'key': b'value'}` instead of `{"key": "value"}`.

---

**Tech progress:**
- ✅ UUID-based file naming
- ✅ Extension validation (pdf, txt, png, jpg, gif)
- ✅ File size limits (20MB)
- ✅ Redis metadata with 5-hour TTL
- ✅ `/upload`, `/info/<token>`, `/list-files` endpoints

**GitHub**: github.com/aayushbankar/onetimeshare

---

💬 **Question for you:**
Have you ever spent hours debugging something that turned out to be a missing `os.makedirs()`?

What's your dumbest-but-most-educational bug?

Drop it in the comments. I'll share mine. 👇

#BuildInPublic #Python #Flask #Redis #Docker #WebDev #DeveloperLife #OneTimeShare30 #30DayChallenge #LearningInPublic

---

## 🐦 X (Twitter) Thread

**Tweet 1 (Hook):**
🔥 Day 2/30: OneTimeShare

Went from 58% working → 95% working in 3 hours.

But I failed 4 times to get there.

Here's every mistake I made (so you don't have to) ⬇️

---

**Tweet 2 (Context):**
Building a one-time file sharing app:
Upload → View once → Deleted forever.

Today's goal:
✓ Accept file uploads
✓ Save with UUID names
✓ Store metadata in Redis
✓ Add TTL (auto-expiration)

Sounds simple. It wasn't.

---

**Tweet 3 (Mistake 1):**
Mistake 1: Import Shadowing

```python
import config
config = Config()  # Wait... what?
```

I imported the MODULE, then tried to use a CLASS that doesn't exist.

Fix: `from config import Config`

Python doesn't warn you. It just breaks.

---

**Tweet 4 (Mistake 2):**
Mistake 2: The Localhost Trap (Again)

"Error connecting to redis:6379. Name not known."

I was running Flask locally.
`redis` is only a valid hostname *inside* Docker.

Fix: Use env vars with fallback:
`os.environ.get('REDIS_HOST', 'localhost')`

---

**Tweet 5 (Mistake 3):**
Mistake 3: The Silent Failure

API returned: "success" ✅
I checked the uploads folder: **Empty** ❌

The crime: `file.save()` was commented out.

Lesson: Never return success for operations that didn't happen.

This is how production bugs are born.

---

**Tweet 6 (Mistake 4):**
Mistake 4: The Missing Folder

```json
{"error": "No such file or directory: 'uploads/abc.txt'"}
```

I deleted `os.makedirs()` while refactoring.

The line that creates folders before writing to them?

Yeah, that one's important.

---

**Tweet 7 (Victory):**
Try 4: Finally.

```json
{
  "status": "success",
  "filename": "5872fbb3-564a...txt"
}
```

File saved. Metadata in Redis. TTL set.

3 hours. 4 tries. 37% improvement.

That's the game.

---

**Tweet 8 (Insight):**
The hardest lesson from today:

Understanding is easy.
Integration is hard.

I *understood* Flask uploads.
I *understood* UUIDs.
I *understood* Redis hashes.

But putting them together?
That's where the real learning happens.

---

**Tweet 9 (CTA):**
Day 3 plan:
• Download endpoint `/d/<token>`
• One-time view enforcement
• Delete file after first access

💬 What's your dumbest-but-most-educational bug?

Follow for 30 days of #BuildInPublic

GitHub: github.com/aayushbankar/onetimeshare

#OneTimeShare30 #Python #Flask #Redis

---

## 📌 Short LinkedIn Update (Alternative - Quick Version)

**🔥 Day 2/30: OneTimeShare**

4 tries to get file upload working.

The mistakes:
❌ Import shadowing (`import x` vs `from x import Y`)
❌ Forgot `os.makedirs()` — folder didn't exist
❌ Missing `decode_responses=True` in Redis
❌ Returned "success" while `file.save()` was commented out

The wins:
✅ UUID-based file naming
✅ Extension & size validation
✅ Redis metadata with 5-hour TTL
✅ Working `/upload` and `/info/<token>` endpoints

Progress: 58% → 95% in 3 hours.

Today's biggest lesson:
> "Understanding concepts is easy. Integration is hard."

Tomorrow: Download endpoint + one-time view enforcement.

#BuildInPublic #Python #Flask #OneTimeShare30

---

## 📸 Instagram/Carousel Post (Visual Ideas)

**Slide 1 (Hook):**
Day 2: I Failed 4 Times Before It Worked
🔴🔴🔴🟢
OneTimeShare 30-Day Challenge

**Slide 2 (The Goal):**
Today's Mission:
• Accept file uploads
• UUID-based security
• Redis metadata + TTL
• Extension validation

**Slide 3 (Mistake 1):**
❌ Mistake 1: Import Confusion
`import config` ≠ `from config import Config`
Python doesn't warn you. It just breaks.

**Slide 4 (Mistake 2):**
❌ Mistake 2: Missing Folder
`os.makedirs()` is NOT optional.
You can't write to a folder that doesn't exist.

**Slide 5 (Mistake 3):**
❌ Mistake 3: Silent Failure
API returned "success"
Folder was empty.
`file.save()` was commented out.
🤦

**Slide 6 (Victory):**
✅ Try 4: SUCCESS
File uploaded. Metadata stored. TTL set.
58% → 95% in 3 hours.

**Slide 7 (Lesson):**
"Understanding is easy.
Integration is hard."
— Every developer, always

**Slide 8 (CTA):**
Follow for 30 days of building in public.
GitHub in bio.
#OneTimeShare30

---

## 🎯 Hashtag Strategy

**Primary (Always Use):**
#BuildInPublic #OneTimeShare30 #Python #Flask

**Secondary (Rotate):**
#Redis #Docker #WebDev #DeveloperLife #30DayChallenge #LearningInPublic #CodeNewbie #Programming #SoftwareEngineering

**LinkedIn Specific:**
#OpenToWork #CareerGrowth #TechJourney

---

## 💡 Engagement Tips for This Post

1. **Ask a question**: "What's your dumbest-but-most-educational bug?" gets replies.

2. **Be vulnerable**: Showing failures builds authenticity and trust.

3. **Teach something**: The import shadowing + os.makedirs lessons are shareable knowledge.

4. **Show progress**: "58% → 95%" gives readers a measurable journey.

5. **End with CTA**: "Follow for 30 days" converts readers into followers.
