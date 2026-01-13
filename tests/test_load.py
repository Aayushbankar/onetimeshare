import threading
import time
import requests
import statistics
import sys
from concurrent.futures import ThreadPoolExecutor

# Configuration
TARGET_URL = "http://localhost:5000"
NUM_REQUESTS = 500
CONCURRENCY = 20
UPLOAD_FILE_SIZE = 1024 * 1024  # 1MB

def benchmark_request(session):
    """Performs a single request flow: GET / -> POST /upload"""
    start_time = time.time()
    try:
        # 1. GET Landing Page
        r1 = session.get(TARGET_URL)
        if r1.status_code != 200:
            print(f"Connection failed: {r1.status_code}")
            return False, 0
            
        # 2. POST Upload (1MB dummy data)
        files = {'file': ('test_load.txt', 'A' * UPLOAD_FILE_SIZE, 'text/plain')}
        r2 = session.post(f"{TARGET_URL}/upload", files=files)
        
        elapsed = time.time() - start_time
        if r2.status_code not in (200, 201):
            print(f"Failed with {r2.status_code}: {r2.text[:200]}")
        return r2.status_code in (200, 201), elapsed
    except Exception as e:
        print(f"Error: {e}")
        return False, 0

def run_benchmark():
    print(f"🚀 Starting Benchmark: {NUM_REQUESTS} requests, {CONCURRENCY} threads...")
    print(f"Target: {TARGET_URL} | Payload: {UPLOAD_FILE_SIZE/1024:.0f}KB")
    
    latencies = []
    success_count = 0
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:
        # Create a session per thread (approximated by just passing new sessions)
        sessions = [requests.Session() for _ in range(NUM_REQUESTS)]
        results = list(executor.map(benchmark_request, sessions))
        
    duration = time.time() - start_total
    
    for success, latency in results:
        if success:
            success_count += 1
            latencies.append(latency)
            
    # Calculate Metrics
    rps = success_count / duration
    avg_latency = statistics.mean(latencies) if latencies else 0
    p95_latency = statistics.quantiles(latencies, n=20)[18] if latencies else 0
    
    print("\n📊 RESULTS")
    print(f"Total Time:     {duration:.2f}s")
    print(f"Successful:     {success_count}/{NUM_REQUESTS}")
    print(f"RPS:            {rps:.2f} req/s")
    print(f"Avg Latency:    {avg_latency:.3f}s")
    print(f"P95 Latency:    {p95_latency:.3f}s")
    
    if success_count < NUM_REQUESTS:
        print(f"⚠️  Failures: {NUM_REQUESTS - success_count}")

if __name__ == "__main__":
    run_benchmark()
