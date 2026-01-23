# Day 5 Social Media Posts — FINAL VERSION

---

## 📘 LinkedIn Post (COPY-PASTE NOW)

3 and a half hours. 13 mistakes. One discovery that broke me.

Let me tell you about the dumbest debugging session of my life.

—

11 AM. Monday. I'm ready.

"Download endpoint. Should take 30 minutes. Maybe an hour if I'm slow."

I write the route. I write the function. I test it.

Backend logs: "File sent ✅"

Open browser. Click link.

...nothing happens.

—

I check the code. Looks fine.
I check Redis. Token exists.
I check the file. It's there.

So I do what any developer does.

I start changing things.

—

Here's where it gets stupid.

Change 1: Renamed the route from /download to /dl.
Forgot to update the frontend. Now BOTH are broken.

Change 2: Deleted some imports "to clean up."
Deleted send_from_directory. The function I needed.

Change 3: Wrote a second function with the same name.
Python silently killed the first one. No warning. Just gone.

Change 4: Made the function call itself.
Infinite loop. Crashed.

In 30 minutes, I went from "almost working" to "nothing works and I don't know why."

—

By noon, I was just staring at my screen.

The code looked right.
The logic made sense.
I had fixed everything.

WHY. WON'T. IT. DOWNLOAD.

I opened the file in the browser.
Refreshed everything.
Cleared cache.

Nothing.

—

Then it hit me.

I looked at my terminal.

Flask hadn't restarted.

I was running code from 2 hours ago.

Every fix I made? Not loaded.
Every test I ran? Testing OLD code.

I was debugging the future while the server was stuck in the past.

—

One restart.

The file downloaded instantly.

—

I sat there for a minute.

13 mistakes.
3 and a half hours.
The fix: restart the server.

That's it. That's the whole story.

—

What I actually built today:

→ /download/<token> shows the file info page
→ /d/<token> serves the actual file
→ send_from_directory() = safe from path attacks
→ Original filename preserved in download

The complete upload → link → download flow works now.

—

Tomorrow: Self-destruct.

Files delete themselves after download.
The "one-time" part of one-time share.

github.com/aayushbankar/onetimeshare

Have you ever spent HOURS debugging something that wasn't even broken?

Tell me your worst "forgot to restart" moment.
I need to know I'm not alone.

#BuildInPublic #Python #SoftwareEngineering #Coding #WebDevelopment #OneTimeShare30