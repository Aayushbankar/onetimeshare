# Day 25 LinkedIn Post: The "Savage" Return

**Based on Day 10 & 24 Success Formula**
**Status**: Ready to Roast.

---

🔥 Day 25: I Crashed Production trying to "Optimize" a 5-Line Feature.

I needed to add Security Headers.
I *should* have used `app.after_request`.
I decided to write a custom WSGI wrapper instead.

Narrator: "He decided to punch himself in the face. For efficiency."

━━━━━━━━━━━━━

THE CRASH:

I wrapped the app. I intercepted the response.
I tried to inject headers directly into the WSGI iterable.

`AttributeError: 'list' object has no attribute 'headers'`

The server died instantly.
I forgot that WSGI apps return a list of bytes, not a Flask Response object.
I was trying to set HTTP headers on a Python list.

Narrator: "He successfully protected the server... by turning it off. 10/10 Security."

I stared at the logs for 15 minutes.
I questioned my career choices.
I considered becoming a goat farmer.

━━━━━━━━━━━━━

THE FIX:

I deleted my 45 lines of "clever" code.
I opened the Flask docs (radical, I know).

```python
@app.after_request
def secure(response):
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

5 lines.
Zero crashes.
Works perfectly.

Narrator: "He discovered that the framework developers might be smarter than him. Shocking."

━━━━━━━━━━━━━

THE CLI WAR:

Earlier, `curl` was bypassing my UI flow to steal files.
I implemented a User-Agent block (HTTP 406).

Now, if you aren't a browser, you get rejected.
"406 Not Acceptable."

Narrator: "It's the digital equivalent of 'You can't sit with us.'"

━━━━━━━━━━━━━

THE LESSON:

1.  **Complexity is the enemy.** If you are writing a custom wrapper for a standard feature, you are wrong.
2.  **Read the docs.** Flask has hooks. Use them.
3.  **Fail Secure.** If the frontend hides it, the backend must block it.

Narrator: "He will forget these lessons by tomorrow. Tune in for Day 26."

━━━━━━━━━━━━━

Now working:
✅ HSTS & CSP Headers (A+ Rating)
✅ CLI Tools Blocked (406)
✅ My humility (Restored)

🔗 GitHub: github.com/Aayushbankar/onetimeshare

Drop a 🤡 if you've ever over-engineered a crash.
Drop a 🐐 if you're ready to join my farm.

#BuildInPublic #Python #Flask #CodingFails #WebSec #Debugging #OneTimeShare30 #SoftwareEngineering #DeveloperLife #100DaysOfCode #TechHumor

---

## 💬 First Comment Plan

🔗 **Full Breakdown**: [GitHub Link]

**The Stack**:
→ Flask (The thing I fought)
→ WSGI (The thing that beat me)
→ Redis (The thing that watched)

Narrator: "Star the repo if you want to see what else he breaks."
