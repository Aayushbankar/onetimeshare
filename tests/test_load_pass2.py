import threading
import time
import requests
import statistics
import sys
import random
import string
from concurrent.futures import ThreadPoolExecutor

# Configuration
TARGET_URL = "http://localhost:5000"
SCENARIOS = [
    {"name": "Light Load (10 users, 100kb)", "users": 10, "requests": 200, "size": 100 * 1024},
    {"name": "Heavy Load (50 users, 1MB)",   "users": 50, "requests": 500, "size": 1 * 1024 * 1024},
    # {"name": "Stress Test (100 users, 10KB)", "users": 100, "requests": 1000, "size": 10 * 1024}, # Optional
]

def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode('utf-8')

def benchmark_request(session, payload):
    """Performs a single request flow: GET / -> POST /upload"""
    start_time = time.time()
    try:
        # 1. GET Landing Page (simulate browsing)
        r1 = session.get(TARGET_URL)
        if r1.status_code != 200:
            return False, 0, r1.status_code
            
        # 2. POST Upload
        files = {'file': ('test_load.txt', payload, 'text/plain')}
        r2 = session.post(f"{TARGET_URL}/upload", files=files)
        
        elapsed = time.time() - start_time
        return r2.status_code in (200, 201), elapsed, r2.status_code
    except Exception as e:
        return False, 0, str(e)

def run_scenario(scenario):
    print(f"\n🚀 Running Scenario: {scenario['name']}")
    print(f"   Users: {scenario['users']} | Requests: {scenario['requests']} | Payload: {scenario['size']/1024:.0f}KB")
    
    # Pre-generate payload to avoid CPU bottleneck during test
    payload = generate_random_data(scenario['size'])
    
    latencies = []
    success_count = 0
    errors = {}
    
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=scenario['users']) as executor:
        sessions = [requests.Session() for _ in range(scenario['requests'])]
        # Distribute payload ref to all tasks
        tasks = [executor.submit(benchmark_request, session, payload) for session in sessions]
        
        for future in tasks:
            success, latency, status = future.result()
            if success:
                success_count += 1
                latencies.append(latency)
            else:
                errors[status] = errors.get(status, 0) + 1

    duration = time.time() - start_total
    
    # Metrics
    rps = success_count / duration
    avg_lat = statistics.mean(latencies) if latencies else 0
    p50_lat = statistics.median(latencies) if latencies else 0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if latencies else 0
    p99_lat = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else p95_lat
    
    print(f"   ✅ Complete in {duration:.2f}s")
    print(f"   -------- Stats --------")
    print(f"   RPS:       {rps:.2f} req/s")
    print(f"   Avg Lat:   {avg_lat:.3f}s")
    print(f"   P50 (Med): {p50_lat:.3f}s")
    print(f"   P95:       {p95_lat:.3f}s")
    print(f"   P99:       {p99_lat:.3f}s")
    if errors:
        print(f"   ⚠️ Errors: {errors}")
        
    return {
        "scenario": scenario['name'],
        "rps": rps,
        "avg": avg_lat,
        "p95": p95_lat,
        "success_rate": (success_count / scenario['requests']) * 100
    }

def main():
    results = []
    print("🔥 Starting Load Test Pass 2 (Verification)")
    print("-------------------------------------------")
    
    for scenario in SCENARIOS:
        res = run_scenario(scenario)
        results.append(res)
        time.sleep(2) # Cooldown
        
    print("\n📝 Final Summary")
    print("=================")
    for r in results:
        print(f"🔹 {r['scenario']:<25} | RPS: {r['rps']:<6.2f} | P95: {r['p95']:.3f}s | Success: {r['success_rate']:.0f}%")

if __name__ == "__main__":
    main()
