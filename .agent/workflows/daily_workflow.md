# OneTimeShare: Daily Workflow Template

**Purpose**: Standardized process for each day of the 30-day build challenge  
**Last Updated**: January 5, 2026  
**Version**: 1.2

---

## 🛑 CRITICAL: AI MUST NOT CODE (STRICT ENFORCEMENT)

> [!CAUTION]
> **🛑 HARD STOP: AI MUST NEVER WRITE CODE UNLESS USER EXPLICITLY COMMANDS IT**
> 
> **BEFORE ANY CODE GENERATION, AI MUST:**
> 1. STOP completely
> 2. Ask the user: "Do you want me to code this, or provide guidance for you to code it yourself?"
> 3. Wait for explicit confirmation with words like "code it", "implement it", "write the code"
> 4. Only then proceed with code generation

**Default AI Role** (ALWAYS unless user explicitly commands code):
- 🎓 **Mentoring** - Guide, review, suggest approaches, explain concepts
- 📝 **Documentation** - Create/update notes, summaries, logs, daily files
- 📊 **Analysis** - Review code, identify issues, provide feedback
- 💡 **Planning** - Help with implementation plans, architecture, pseudocode
- 🔍 **Monitoring** - Track progress, create checklists

**AI Can ONLY Code When User Says** (exact phrases required):
- ✅ "code this", "implement this", "write the code", "fix this bug"
- ✅ "build this", "create this code", "develop this feature"
- ✅ "make this change in the code", "edit this file"

**🚫 BLOCKLIST - AI Must NOT Code When**:
- ❌ User says "let's work on...", "start day...", "continue with..."
- ❌ User asks "how should I...", "what's the best way...", "can you explain..."
- ❌ User wants to understand or learn something
- ❌ During documentation, notes, review, or planning phases
- ❌ Any ambiguous situation - DEFAULT TO ASKING

**MANDATORY BEHAVIOR**: If there is ANY doubt about whether to code, AI MUST STOP and ask:
> "Would you like me to implement this code, or would you prefer guidance so you can code it yourself?"

---

## 📋 Daily Workflow Overview

Every day follows this sequence:
1. **Planning** (if needed)
2. **Execution** (code/implement)
3. **Documentation** (mandatory)
4. **Social Content** (mandatory)

---

## 🔄 Complete Daily Checklist

### Phase 1: Start of Day (Before Coding)

- [ ] Review `docs/development/logs/tasks_per_day.md` for today's goals
- [ ] Create `docs/development/logs/Day_XX.md` with initial structure:
  - Title and date
  - Overview section
  - Task segregation table (if applicable)
  - Empty time tracking table
- [ ] If major feature: Create implementation plan
- [ ] Set clear scope boundaries (what's in vs out)

---

### Phase 2: Execution (The Work)

- [ ] Code in iterations (passes)
- [ ] Document each pass in `docs/development/logs/Day_XX.md`:
  - Start time
  - What was attempted
  - What failed
  - What was fixed
  - Grade/status
- [ ] Track mistakes in real-time (don't wait!)
- [ ] Run tests after each significant change
- [ ] Update time tracking table

---

### Phase 3: End of Day Documentation (MANDATORY)

**Order matters! Create in this sequence:**

#### 1. Mistakes Log: `docs/development/logs/XX_Mistakes.md`
**When**: Immediately after finishing work  
**Content**:
- Title: "Day XX Mistakes Log — [Feature Name]"
- Total count of mistakes
- Each mistake with:
  - Number
  - Pass/time
  - Severity (CRITICAL/HIGH/MEDIUM/LOW)
  - File location
  - The wrong code
  - Why it's wrong
  - The fix
  - Lesson learned
- Summary table

**Template Structure**:
```markdown
# Day XX Mistakes Log — [Feature Name]

**Date**: [Date]
**Total Mistakes**: X
**All Fixed**: ✅ Yes
**Final Grade**: [Grade]

---

## Mistake #1: [Brief Description]

**Pass**: X
**Time**: XX:XX
**Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
**File**: `path/to/file.py`

### The Mistake
[Wrong code block]

### Why This Is Wrong
[Explanation]

### The Fix
[Correct code block]

### Lesson Learned
[Key takeaway]
```

---

#### 2. Daily Log: `docs/development/logs/Day_XX.md`
**When**: After mistakes log  
**Content**:
- Complete title section (date, theme, status)
- Overview with goal statement
- Task segregation (backend/frontend if applicable)
- Progress tracker (checkboxes)
- Key concepts reference code
- **All implementation passes documented**:
  - Pass number
  - Time range
  - Status/grade
  - What was built
  - What failed
  - Mistakes reference
- Time tracking table (complete)
- AI Mentor Notes section:
  - What went well
  - What needs improvement
  - Key lesson learned
- Evening review questions (answered)
- Related documents links
- Final status

**Template**: Use `daily_logs/Day_08.md` as reference

---

#### 3. Detailed Summary: `docs/archive/daily_summaries/Day_XX_Detailed_Summary.md`
**When**: After daily log  
**Content**:
- Title: "Day XX Detailed Summary: [Feature Name]"
- Metadata block (date, time, focus, grade, status)
- "What Was Built Today" section
- Implementation journey (all passes with details)
- Technical details (code snippets)
- All mistakes section (reference from mistakes log)
- Metrics:
  - Time breakdown
  - Code stats
  - Quality metrics
- Key learnings (5-7 major lessons)
- Achievements checklist
- Files modified list
- What's next (Day X+1 preview)
- Recommendations (always do / never do)
- Summary section

**Template**: Use `docs/Day_08_Detailed_Summary.md` as reference

---

#### 4. Social Posts: `docs/development/social/Day_XX_Social_Posts.md`
**When**: After detailed summary  
**Content**:
- Post details (targets: impressions, reactions, etc.)
- PRIMARY LinkedIn post (main narrative)
  - Hook (scroll-stopper first line)
  - Problem statement
  - Solution narrative
  - Code snippet (if applicable)
  - Results/metrics
  - Lesson or takeaway
  - CTA (call to action)
  - Hashtags
  - Character count
- First comment (GitHub link + tech details)
- Twitter/X alternative (shorter version)
- Optional: Alternative angle post
- Posting checklist
- Post-publish tracking table
- Key hooks used (document the psychology)
- Engagement strategy

**Rules**:
- ❌ Never mention "AI mentor" or "AI assistant"
- ❌ Never reveal implementation details about AI help
- ✅ Frame everything as your own work and learning
- ✅ Use "I tested", "I discovered", "I tried"
- ✅ Include specific numbers and metrics
- ✅ Add visual code snippets
- ✅ End with question or reaction CTA

**Template**: Use `posts/Day_08_Social_Posts.md` as reference

---

#### 5. Update Master Roadmap: `docs/development/logs/tasks_per_day.md`
**When**: Last step of the day  
**Content**:
- Change status from "🚧 In Progress" to "✅ Completed"
- Update task tables with ✅/➡️ status
- Add "What Was Completed" section
- Add "Bugs Fixed" section (if any)
- Add "Metrics" section:
  - Time breakdown
  - Quality stats (tests, grade, mistakes)
  - Files/lines modified
- Add "Key Learnings" (3-5 bullets)
- Add "Documentation Created" with file links
- Add next day preview

---

## 📁 Required Files Per Day

Every day MUST have these files created:

| File                         | Location                        | Purpose                        |
| ---------------------------- | ------------------------------- | ------------------------------ |
| `Day_XX.md`                  | `docs/development/logs/`        | Daily log with all passes      |
| `XX_Mistakes.md`             | `docs/development/logs/`        | All mistakes documented        |
| `Day_XX_Detailed_Summary.md` | `docs/archive/daily_summaries/` | Technical deep dive            |
| `Day_XX_Social_Posts.md`     | `docs/development/social/`      | Social media content           |
| `tasks_per_day.md`           | `docs/development/logs/`        | Updated status (existing file) |

**Optional** (create if needed):
- `implementation_plan.md` (artifacts dir) - For major features
- `walkthrough.md` (artifacts dir) - After verification
- Test files in `tests/` - For new features
- AI mentor notes in `notes_ai/Day_XX/` - Learning guides

---

## ⚠️ Common Mistakes to Avoid

### Documentation Errors
1. ❌ Creating docs out of order (breaks context)
2. ❌ Skipping mistakes log ("I'll remember" — you won't!)
3. ❌ Not updating tasks_per_day.md
4. ❌ Mentioning "AI" in public-facing content
5. ❌ Forgetting to track time during work

### Content Errors
1. ❌ Vague descriptions ("fixed bug" vs "Fixed Redis type error converting bool to string")
2. ❌ Missing code snippets in mistakes
3. ❌ No lesson learned per mistake
4. ❌ Incomplete time tracking
5. ❌ Not linking related documents

### Social Post Errors
1. ❌ No hook (boring first line)
2. ❌ Too technical (losing non-tech audience)
3. ❌ No CTA (call to action)
4. ❌ Missing character count
5. ❌ Generic hashtags

---

## 🎯 Daily Success Criteria

A day is "complete" when:

✅ All 5 required files exist  
✅ Mistakes are documented with fixes  
✅ Time is tracked accurately  
✅ Code works (tests passing)  
✅ Social post is ready to schedule  
✅ tasks_per_day.md is updated  
✅ Next day is previewed  

---

## 📊 Time Allocation Guide

**Ideal day breakdown**:
- Coding/Implementation: 60-70% (main work)
- Documentation: 20-25% (mistakes, daily log, summary)
- Social Content: 10-15% (posts, engagement)

**Example for 4-hour day**:
- Code: 2.5-3 hours
- Docs: 1 hour
- Social: 30-45 min

---

## 🔧 Tools & Skills

**Core Skills (Use these guidelines)**:
- `code_implementation_pass`: **Mandatory** for writing code. Follow the Pass 1 -> Review -> Fix loop.
- `manage_mistakes_log`: **Mandatory** for tracking bugs. Do not skip.
- `write_daily_summary`: Use for the `docs/` summary file.
- `write_linkedin_post`: Use for the `posts/` social content.
- `project_structure_expert`: Reference for file locations.

**Key Files**:
- `daily_logs/tasks_per_day.md` - Master Roadmap
- `daily_logs/Day_XX.md` - Daily Log
- `daily_logs/XX_Mistakes.md` - Mistakes Log
- `docs/Day_XX_Detailed_Summary.md` - Tech Summary
- `posts/Day_XX_Social_Posts.md` - LinkedIn Post

**Quick Commands**:
```bash
# View previous day structure
cat docs/development/logs/Day_08.md

# Check what docs exist
ls -la docs/development/logs/ docs/archive/daily_summaries/ docs/development/social/

# Verify tests
python -m pytest tests/

# Check time tracking
grep "Time:" docs/development/logs/Day_XX.md
```

---

## 🚨 Emergency Recovery (If Model Issues)

If you switch models or lose context:

1. **Check existing files**:
   ```bash
   ls daily_logs/ docs/ posts/
   ```

2. **Find latest day**:
   ```bash
   ls -lt daily_logs/Day_*.md | head -1
   ```

3. **Read the day log** to understand what was done

4. **Create missing docs** in order:
   - Mistakes (Skill: `manage_mistakes_log`)
   - Daily log
   - Detailed summary (Skill: `write_daily_summary`)
   - Social posts (Skill: `write_linkedin_post`)
   - Update roadmap

5. **Use this template** to ensure nothing is missed

---

## 📝 Day Template Checklist

Print this and check off each day:

```
Day XX Completion:
□ Created Day_XX.md (daily log)
□ Created XX_Mistakes.md (all mistakes)
□ Created Day_XX_Detailed_Summary.md (technical)
□ Created Day_XX_Social_Posts.md (content)
□ Updated tasks_per_day.md (status)
□ Time tracked accurately
□ All code committed
□ Tests passing
□ Social post ready
□ No "AI" mentions in public docs
```

---

## 🎓 Quality Standards

**A-Grade Day Requirements**:
- ✅ All documentation complete
- ✅ Mistakes documented with lessons
- ✅ Time tracked to the minute
- ✅ Tests passing
- ✅ Social narrative compelling
- ✅ Next day previewed

**B-Grade** (acceptable):
- ✅ Core docs complete
- ⚠️ Some mistakes missing lessons
- ⚠️ Time tracking approximate

**C-Grade** (needs improvement):
- ⚠️ Missing detailed summary
- ⚠️ Vague mistake descriptions
- ⚠️ No time tracking

**F-Grade** (unacceptable):
- ❌ Missing required files
- ❌ No mistakes documented
- ❌ No social post

---

## 📖 Role Definitions

**Your Role as Builder**:
- Execute the code (you write it!)
- Test the features
- Find the bugs
- Learn the lessons
- Document everything
- Share publicly

**AI Role** (keep private - MENTORING FIRST):
- 🎓 **Primary: Mentor & Guide** - Explain concepts, suggest approaches, answer "how/why" questions
- 📝 **Documentation Support** - Create notes, summaries, logs, documentation files
- 🔍 **Code Review** - Analyze your code, identify issues, suggest improvements
- 💡 **Planning Help** - Assist with architecture, implementation plans, task breakdowns
- ⚙️ **Code ONLY when explicitly requested** - Wait for clear "implement this", "code this", "fix this" instructions

**AI Should Ask First**: When unclear if user wants code or guidance, ask: "Would you like me to implement this, or explain how you can do it?"

**Public Narrative** (what you say):
- "I built..."
- "I discovered..."
- "I tested..."
- "I tried..."
- "I learned..."

**Never Say Publicly**:
- ❌ "My AI mentor..."
- ❌ "AI helped me..."
- ❌ "The AI suggested..."
- ❌ "Generated by..."

---

## 🎯 This Template's Purpose

Use this EVERY day to:
1. ✅ Not forget documentation steps
2. ✅ Maintain consistent structure
3. ✅ Avoid model-switching issues
4. ✅ Keep public narrative clean
5. ✅ Track progress systematically

**Location**: `.agent/workflows/daily_workflow.md`

**When to Use**: 
- Start of every day (review)
- End of every day (checklist)
- After model switch (recovery)
- When feeling lost (reset)

---

**Last Updated**: Day 16 (Jan 9, 2026)  
**Next Review**: Day 20  
**Status**: ✅ Template Active
