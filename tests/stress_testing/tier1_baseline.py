"""
Day 22 Stress Testing Suite - Tier 1: Baseline
================================================
Tests: Pass 1.1 (10 users), Pass 1.2 (20 users), Pass 1.3 (30 users)

This tests normal production load to establish baseline metrics.
"""

import threading
import time
import requests
import statistics
import sys
import os
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:5000")
TEST_FILE_PATH = "tests/stress_testing/test_1mb.txt"

# Pass configurations
PASS_CONFIGS = {
    "1.1": {"users": 10, "requests_per_user": 20, "duration": 60},
    "1.2": {"users": 20, "requests_per_user": 15, "duration": 60},
    "1.3": {"users": 30, "requests_per_user": 15, "duration": 120},
}


def create_test_file():
    """Create 1MB test file if it doesn't exist."""
    os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
    if not os.path.exists(TEST_FILE_PATH):
        with open(TEST_FILE_PATH, "wb") as f:
            f.write(os.urandom(1024 * 1024))  # 1MB random data
        print(f"✓ Created test file: {TEST_FILE_PATH}")
    return TEST_FILE_PATH


def upload_file(session, file_path):
    """Upload a file and return the token."""
    try:
        with open(file_path, "rb") as f:
            response = session.post(
                f"{TARGET_URL}/upload",
                files={"file": ("test.txt", f, "text/plain")},
                timeout=30
            )
        if response.status_code in (200, 201):
            data = response.json()
            # Token can be at data['token'] or data['metadata']['token']
            return data.get("token") or data.get("metadata", {}).get("token")
    except Exception as e:
        print(f"Upload error: {e}")
    return None


def download_info(session, token):
    """Get file info (simulates download page visit)."""
    try:
        start = time.time()
        response = session.get(f"{TARGET_URL}/info/{token}", timeout=30)
        latency = time.time() - start
        return response.status_code == 200, latency
    except Exception as e:
        return False, 0


def mixed_workload(session, tokens, file_path, results):
    """Perform mixed workload: 70% downloads, 30% uploads."""
    import random
    
    # Decide action
    action = random.choices(["download", "upload"], weights=[70, 30])[0]
    
    start = time.time()
    try:
        if action == "download" and tokens:
            token = random.choice(tokens)
            response = session.get(f"{TARGET_URL}/info/{token}", timeout=30)
            success = response.status_code == 200
        else:
            with open(file_path, "rb") as f:
                response = session.post(
                    f"{TARGET_URL}/upload",
                    files={"file": ("test.txt", f, "text/plain")},
                    timeout=30
                )
            success = response.status_code in (200, 201)
            if success:
                data = response.json()
                new_token = data.get("token") or data.get("metadata", {}).get("token")
                if new_token:
                    tokens.append(new_token)
        
        latency = time.time() - start
        results.append({"success": success, "latency": latency, "action": action})
        
    except Exception as e:
        results.append({"success": False, "latency": 0, "action": action, "error": str(e)})


def run_tier1_pass(pass_id):
    """Run a single Tier 1 pass."""
    config = PASS_CONFIGS[pass_id]
    users = config["users"]
    requests_per_user = config["requests_per_user"]
    duration = config["duration"]
    total_requests = users * requests_per_user
    
    print(f"\n{'='*60}")
    print(f"🧪 TIER 1 - PASS {pass_id}: BASELINE TEST")
    print(f"{'='*60}")
    print(f"  Users:     {users}")
    print(f"  Requests:  {total_requests} ({requests_per_user}/user)")
    print(f"  Duration:  {duration}s target")
    print(f"  Target:    {TARGET_URL}")
    print(f"{'='*60}\n")
    
    # Setup
    file_path = create_test_file()
    
    # Pre-create tokens for downloads
    print("📤 Pre-uploading files for download pool...")
    session = requests.Session()
    tokens = []
    for i in range(min(10, users)):
        token = upload_file(session, file_path)
        if token:
            tokens.append(token)
    print(f"  ✓ Created {len(tokens)} tokens for download pool\n")
    
    # Run benchmark
    print("🔥 Starting load test...")
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=users) as executor:
        futures = []
        for _ in range(total_requests):
            sess = requests.Session()
            future = executor.submit(mixed_workload, sess, tokens, file_path, results)
            futures.append(future)
            # Small delay to spread requests
            time.sleep(duration / total_requests)
        
        # Wait for completion
        for future in futures:
            try:
                future.result(timeout=60)
            except:
                pass
    
    total_time = time.time() - start_time
    
    # Calculate metrics
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    latencies = [r["latency"] for r in successful if r["latency"] > 0]
    
    downloads = [r for r in results if r.get("action") == "download"]
    uploads = [r for r in results if r.get("action") == "upload"]
    
    metrics = {
        "pass_id": f"1.{pass_id}",
        "tier": 1,
        "timestamp": datetime.now().isoformat(),
        "config": {
            "users": users,
            "total_requests": total_requests,
            "target_duration": duration
        },
        "results": {
            "total_requests": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "error_rate": len(failed) / len(results) * 100 if results else 0,
            "total_time": total_time,
            "rps": len(successful) / total_time if total_time > 0 else 0,
            "latency": {
                "avg": statistics.mean(latencies) * 1000 if latencies else 0,
                "p50": statistics.median(latencies) * 1000 if latencies else 0,
                "p95": statistics.quantiles(latencies, n=20)[18] * 1000 if len(latencies) > 20 else 0,
                "p99": statistics.quantiles(latencies, n=100)[98] * 1000 if len(latencies) > 100 else 0,
            },
            "breakdown": {
                "downloads": len(downloads),
                "uploads": len(uploads),
                "download_success": len([d for d in downloads if d.get("success")]),
                "upload_success": len([u for u in uploads if u.get("success")]),
            }
        }
    }
    
    # Print results
    print(f"\n{'='*60}")
    print(f"📊 PASS {pass_id} RESULTS")
    print(f"{'='*60}")
    print(f"  Total Time:      {total_time:.2f}s")
    print(f"  Requests:        {len(successful)}/{len(results)} successful")
    print(f"  Error Rate:      {metrics['results']['error_rate']:.2f}%")
    print(f"  RPS:             {metrics['results']['rps']:.2f} req/s")
    print(f"  Avg Latency:     {metrics['results']['latency']['avg']:.0f}ms")
    print(f"  P50 Latency:     {metrics['results']['latency']['p50']:.0f}ms")
    print(f"  P95 Latency:     {metrics['results']['latency']['p95']:.0f}ms")
    print(f"{'='*60}\n")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    result_file = f"results/tier1_pass{pass_id.replace('.', '_')}.json"
    with open(result_file, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"💾 Results saved to: {result_file}")
    
    # Grade
    if metrics['results']['error_rate'] < 1 and metrics['results']['rps'] > 30:
        grade = "A"
    elif metrics['results']['error_rate'] < 5 and metrics['results']['rps'] > 20:
        grade = "B"
    elif metrics['results']['error_rate'] < 10:
        grade = "C"
    else:
        grade = "D"
    
    print(f"🎯 GRADE: {grade}")
    
    return metrics


def run_all_tier1():
    """Run all Tier 1 passes."""
    print("\n" + "="*60)
    print("🏁 TIER 1: BASELINE LOAD TESTING")
    print("="*60)
    
    all_results = []
    for pass_id in ["1.1", "1.2", "1.3"]:
        result = run_tier1_pass(pass_id)
        all_results.append(result)
        print("\n⏳ Cooling down for 5 seconds...\n")
        time.sleep(5)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TIER 1 SUMMARY")
    print("="*60)
    print(f"{'Pass':<10} {'Users':<8} {'RPS':<10} {'Error%':<10} {'P95 (ms)':<10}")
    print("-"*60)
    for r in all_results:
        print(f"{r['pass_id']:<10} {r['config']['users']:<8} {r['results']['rps']:<10.2f} {r['results']['error_rate']:<10.2f} {r['results']['latency']['p95']:<10.0f}")
    print("="*60)
    
    return all_results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass_id = sys.argv[1]
        if pass_id in PASS_CONFIGS:
            run_tier1_pass(pass_id)
        elif pass_id == "all":
            run_all_tier1()
        else:
            print(f"Unknown pass: {pass_id}. Use 1.1, 1.2, 1.3, or 'all'")
    else:
        run_all_tier1()
