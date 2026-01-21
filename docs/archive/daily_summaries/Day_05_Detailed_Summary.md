# Day 5 Detailed Summary — Download/View Endpoint

## Overview

**Date**: December 29, 2025  
**Duration**: ~2 hours 15 minutes  
**Final Grade**: A- (90%)  
**Core Achievement**: Implemented actual file download functionality

---

## What Was Built

### Two-Route Download Architecture

```
User Journey:
  1. Upload file → get link: /download/abc.pdf
  2. Visit link → see info page with file details
  3. Click DOWNLOAD button → triggers /d/abc.pdf
  4. File downloads with original filename
```

### Route 1: `/download/<token>` — Info Page
- Renders `dl.html` template
- Shows file metadata (name, type, token)
- Displays warnings ("This link works ONCE")
- Contains DOWNLOAD button

### Route 2: `/d/<token>` — File Server
- Uses `send_from_directory()` for security
- Sets `download_name` to original filename
- Returns binary file to browser

---

## Files Created/Modified

### New Files
| File                        | Purpose                           |
| --------------------------- | --------------------------------- |
| `app/static/js/download.js` | Click handler for download button |
| `docs/development/notes/Day_05/*.md`      | 6 textbook chapters               |

### Modified Files
| File                    | Changes                                                        |
| ----------------------- | -------------------------------------------------------------- |
| `app/routes.py`         | Added `/d/<token>` route, renamed `/download/<token>` function |
| `app/templates/dl.html` | Added download button, linked JS                               |
| `app/static/js/app.js`  | Fixed link generation to `/download/`                          |
| `app/utils/get_uuid.py` | Kept file extension in UUID                                    |

---

## Key Code Additions

### routes.py — Download File Route
```python
@bp.route('/d/<token>', methods=['GET'])
def download_file(token):
    metadata = redis_service.get_file_metadata(token)
    if not metadata:
        return jsonify({"error": "File not found"}), 404
    
    return send_from_directory(
        directory=Config.UPLOAD_FOLDER,
        path=metadata['filename'],
        as_attachment=True,
        download_name=metadata['real_filename']
    )
```

### routes.py — Info Page Route
```python
@bp.route('/download/<token>', methods=['GET'])
def render_download_page(token):
    metadata = redis_service.get_file_metadata(token)
    if not metadata:
        return jsonify({"error": "File not found"}), 404
    return render_template('dl.html', metadata=metadata, token=token)
```

---

## Learning Journey

### Pass 1 (1.5 hours) — Grade: C+ (65%)
- Attempted to implement download in `/download/` route
- Made 6 mistakes including route naming confusion
- Backend logic worked but frontend broken

### Pass 2 (30 mins) — Grade: D (40%)
- Tried to fix by reorganizing code
- Made 6 more mistakes including deleting required imports
- Infinite recursion, undefined variables

### Pass 3 (15 mins) — Grade: A- (90%)
- Fresh start with clear two-route architecture
- All code correct but forgot to restart Flask
- Once restarted: everything working!

---

## Mistakes Summary

**13 total mistakes** across 3 passes:

| Category      | Count | Examples                                    |
| ------------- | ----- | ------------------------------------------- |
| Import/syntax | 3     | Deleted `send_from_directory` import        |
| Architecture  | 4     | Two functions same name, infinite recursion |
| Naming/paths  | 3     | Route mismatch, regex rejecting dots        |
| Environment   | 3     | Forgot to restart Flask, unreachable code   |

---

## Key Lessons

1. **Restart your server** after code changes
2. **Two routes for download**: info page → file serve
3. **Save Redis results**: `metadata = redis_service.get(...)` not just check
4. **Test incrementally**: one change → one test
5. **Check DevTools Network tab** to debug URL issues

---

## Technical Concepts Learned

### send_from_directory() vs send_file()
- `send_from_directory()` prevents path traversal attacks
- Use for user-influenced file paths
- `send_file()` only for trusted, hardcoded paths

### Content-Disposition Header
- `as_attachment=True` → Forces download dialog
- `download_name` → Shows original filename to user

### Flask Route Architecture
- Separate concerns: display routes vs action routes
- Function names must be unique (Python overwrites duplicates)

---

## What's Next (Day 6)

**Self-Destruct Mechanism:**
- Delete file from disk after successful download
- Delete Redis key (metadata cleanup)
- Handle race conditions if same file accessed twice
- TTL fallback for files never downloaded
