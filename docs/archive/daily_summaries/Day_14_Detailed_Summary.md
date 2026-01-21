# Day 14 Detailed Summary: Week 2 Testing & Security Fixes

**Date**: January 7, 2026  
**Time Invested**: ~50 minutes  
**Focus**: Integration Testing, Critical Security Fixes  
**Final Grade**: A  
**Status**: ✅ COMPLETE

---

## What Was Done

Comprehensive testing of all Week 2 features with critical bug discovery and fixing.

### Testing Completed (9 Flows)
1. ✅ Upload flow (regular file)
2. ✅ Upload flow (password-protected)
3. ✅ Download flow (unprotected)
4. ✅ Download flow (protected + verify)
5. ✅ Retry limit enforcement
6. ✅ Self-destruct verification
7. ✅ Admin login/logout
8. ✅ Admin dashboard + stats
9. ✅ Auto-logout security

---

## Bugs Found & Fixed

| Bug                                   | Severity   | Fix                     |
| ------------------------------------- | ---------- | ----------------------- |
| Redis DNS startup failure             | 🟡 MEDIUM   | Added retry logic       |
| Retry counter bypass (URL revisit)    | 🔴 CRITICAL | Check at route entry    |
| File not deleted on max retries       | 🔴 HIGH     | Implement file locking  |
| DoS Vulnerability (Pass 2 regression) | 🔴 CRITICAL | Reverted deletion logic |

---

## Pass Breakdown

### Pass 1: Investigation (15:14-15:30)
**Grade**: A

- Found critical retry bypass bug
- Created flowcharts (Broken vs Expected)
- Identified Redis DNS timing issue

### Pass 2: Security Fixes (15:34-15:40)
**Grade**: C- (introduced regression)

- Fixed retry bypass
- **MISTAKE**: Added file deletion on max retries → DoS vulnerability

### Pass 3: DoS Fix (15:43+)  
**Grade**: A+

- Reverted file deletion
- Implemented file locking instead
- Documented the mistake

---

## Critical Lesson: The DoS Mistake

**What Happened**: 
- Pass 2 "fix" deleted files when max retries exceeded
- This allowed ANYONE to delete ANY password-protected file

**Why It's Wrong**:
- Violates CIA Triad (Availability)
- Attacker can grief users by exhausting retries

**The Fix**:
- Lock the file instead of deleting
- Only owner can still access with correct password

---

## Key Learnings

1. **Availability = Security** — Deleting to "secure" violates CIA Triad
2. **Think Like an Attacker** — "Can I grief the user?"
3. **Locking > Deleting** — Soft locks before hard destruction

---

## Files Modified

| Type         | Files                                            |
| ------------ | ------------------------------------------------ |
| **Created**  | 3 notes in `notes_ai/Day_14/`                    |
| **Modified** | `routes.py`, `__init__.py`, `docker-compose.yml` |
| **Assets**   | 2 flowchart diagrams (PNG)                       |

---

## Related Documents

- [01_Pass_1_Findings.md](file:///mnt/shared_data/projects/onetimeshare/notes_ai/Day_14/01_Pass_1_Findings.md)
- [03_Pass_2_Mistakes_and_Correction.md](file:///mnt/shared_data/projects/onetimeshare/notes_ai/Day_14/03_Pass_2_Mistakes_and_Correction.md)

---

**Day 14 Status**: ✅ COMPLETE  
**Final Grade**: A (after Pass 3 correction)
