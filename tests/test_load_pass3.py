import time
import requests
import statistics
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
TARGET_URL = "http://localhost:5000"

# Test Phases
PHASES = [
    {"name": "Warmup",    "duration": 5,  "users": 10,  "desc": "Warming up JVM/Gunicorn workers"},
    {"name": "Endurance", "duration": 20, "users": 30,  "desc": "Sustained moderate load (30 concurrent)"},
    {"name": "Spike",     "duration": 5,  "users": 100, "desc": "Sudden burst to 100 concurrent users"},
    {"name": "Cooldown",  "duration": 5,  "users": 10,  "desc": "Return to baseline"},
]

def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode('utf-8')

# Pre-generate 1MB payload to reduce test client CPU overhead
PAYLOAD_1MB = generate_random_data(1024 * 1024)

def user_session(duration, stop_event):
    """Simulates a single user performing actions for a set duration."""
    session = requests.Session()
    stats = []
    
    while not stop_event.is_set():
        # Action 1: Browse Home (20% chance)
        if random.random() < 0.2:
            start = time.time()
            try:
                r = session.get(TARGET_URL, timeout=5)
                stats.append(("GET_HOME", r.status_code, time.time() - start))
            except Exception as e:
                stats.append(("GET_HOME", "ERR", 0))

        # Action 2: Upload File (80% chance)
        else:
            start = time.time()
            try:
                files = {'file': ('pass3.txt', PAYLOAD_1MB, 'text/plain')}
                r = session.post(f"{TARGET_URL}/upload", files=files, timeout=30)
                stats.append(("POST_UPLOAD", r.status_code, time.time() - start))
            except Exception as e:
                stats.append(("POST_UPLOAD", "ERR", 0))
        
        # Simulate think time
        time.sleep(random.uniform(0.1, 0.5))
        
    return stats

def run_phase(phase):
    print(f"\n🏃 Starting Phase: {phase['name'].upper()}")
    print(f"   ℹ️  {phase['desc']}")
    print(f"   ⏱️  Duration: {phase['duration']}s | 👥 Users: {phase['users']}")
    
    stop_event = threading.Event()
    
    with ThreadPoolExecutor(max_workers=phase['users']) as executor:
        # Launch users
        futures = [executor.submit(user_session, phase['duration'], stop_event) for _ in range(phase['users'])]
        
        # Let them run for duration
        time.sleep(phase['duration'])
        
        # Signal stop
        stop_event.set()
        
        # Collect results
        phase_results = []
        for f in as_completed(futures):
            phase_results.extend(f.result())
            
    return process_results(phase_results, phase['name'])

def process_results(raw_data, phase_name):
    total_reqs = len(raw_data)
    if total_reqs == 0:
        return None
        
    # Filter by type
    uploads = [x for x in raw_data if x[0] == "POST_UPLOAD" and isinstance(x[1], int) and x[1] in (200, 201)]
    errors = [x for x in raw_data if x[1] not in (200, 201)]
    
    # Latency Stats (Uploads only)
    latencies = [x[2] for x in uploads]
    avg_lat = statistics.mean(latencies) if latencies else 0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if latencies else 0
    
    # Throughput
    # Note: RPS here is approximate (Total Reqs / Duration is managed by caller printing)
    
    return {
        "phase": phase_name,
        "total_requests": total_reqs,
        "successful_uploads": len(uploads),
        "errors": len(errors),
        "avg_latency": avg_lat,
        "p95_latency": p95_lat,
        "error_details": [x[1] for x in errors[:5]] # Sample errors
    }

def main():
    print("🛡️  ONE_TIME_SHARE SYSTEM STRESS TEST - PASS 3")
    print("==============================================")
    
    global_stats = []
    
    start_time = time.time()
    
    for phase in PHASES:
        p_stats = run_phase(phase)
        p_stats["duration"] = phase["duration"]
        p_stats["rps"] = p_stats["total_requests"] / phase["duration"]
        global_stats.append(p_stats)
        
        print(f"   ✅ Finished {phase['name']}")
        print(f"      RPS: {p_stats['rps']:.2f} | P95 Latency: {p_stats['p95_latency']:.3f}s | Errors: {p_stats['errors']}")
        
        time.sleep(2) # Phase transition cooldown
        
    total_duration = time.time() - start_time
    total_reqs = sum(x["total_requests"] for x in global_stats)
    total_errors = sum(x["errors"] for x in global_stats)
    
    print("\n📝 PASS 3 CERTIFICATION SUMMARY")
    print("================================")
    print(f"Total Duration: {total_duration:.2f}s")
    print(f"Total Requests: {total_reqs}")
    print(f"Total Errors:   {total_errors}")
    print("\nPhase Breakdown:")
    print(f"{'Phase':<15} | {'RPS':<8} | {'P95 (s)':<8} | {'Status'}")
    print("-" * 50)
    for s in global_stats:
        status = "✅ PASS" if s['errors'] == 0 else "⚠️ WARN"
        print(f"{s['phase']:<15} | {s['rps']:<8.2f} | {s['p95_latency']:<8.3f} | {status}")

if __name__ == "__main__":
    main()
