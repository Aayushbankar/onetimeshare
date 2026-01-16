"""
Day 22 Stress Testing Suite - Tier 2: Peak Production
======================================================
Tests: Pass 2.1 (50 users), Pass 2.2 (75 users), Pass 2.3 (100 users)

This simulates heavy but realistic production traffic.
"""

import threading
import time
import requests
import statistics
import sys
import os
import json
import random
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:5000")
TEST_FILE_PATH = "tests/stress_testing/test_1mb.bin"

# Pass configurations - Peak Production
PASS_CONFIGS = {
    "2.1": {"users": 50, "requests_per_user": 10, "duration": 120},
    "2.2": {"users": 75, "requests_per_user": 8, "duration": 120},
    "2.3": {"users": 100, "requests_per_user": 8, "duration": 180},
}


def create_test_file():
    """Create 1MB test file if it doesn't exist."""
    os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
    if not os.path.exists(TEST_FILE_PATH):
        with open(TEST_FILE_PATH, "wb") as f:
            f.write(os.urandom(1024 * 1024))
        print(f"✓ Created test file: {TEST_FILE_PATH}")
    return TEST_FILE_PATH


def upload_file(session, file_path, password=None):
    """Upload a file, optionally with password."""
    try:
        with open(file_path, "rb") as f:
            data = {"password": password} if password else {}
            response = session.post(
                f"{TARGET_URL}/upload",
                files={"file": ("test.txt", f, "text/plain")},
                data=data,
                timeout=30
            )
        if response.status_code == 200:
            result = response.json()
            return result.get("token"), password
    except Exception as e:
        pass
    return None, None


def peak_workload(session, tokens, password_tokens, file_path, results):
    """
    Peak production workload:
    - 50% regular downloads
    - 20% password-protected downloads
    - 20% uploads
    - 10% stats check
    """
    action = random.choices(
        ["download", "password_download", "upload", "stats"],
        weights=[50, 20, 20, 10]
    )[0]
    
    start = time.time()
    success = False
    error = None
    
    try:
        if action == "download" and tokens:
            token = random.choice(tokens)
            response = session.get(f"{TARGET_URL}/info/{token}", timeout=30)
            success = response.status_code == 200
            
        elif action == "password_download" and password_tokens:
            item = random.choice(password_tokens)
            # First get the info page
            session.get(f"{TARGET_URL}/d/{item['token']}", timeout=30)
            # Then verify password
            response = session.post(
                f"{TARGET_URL}/verify/{item['token']}",
                data={"password": item["password"]},
                timeout=30
            )
            success = response.status_code in (200, 302)
            
        elif action == "upload":
            with open(file_path, "rb") as f:
                use_password = random.random() < 0.3  # 30% of uploads use password
                data = {"password": "testpass123"} if use_password else {}
                response = session.post(
                    f"{TARGET_URL}/upload",
                    files={"file": ("test.txt", f, "text/plain")},
                    data=data,
                    timeout=30
                )
            success = response.status_code == 200
            if success:
                new_token = response.json().get("token")
                if new_token:
                    if use_password:
                        password_tokens.append({"token": new_token, "password": "testpass123"})
                    else:
                        tokens.append(new_token)
                        
        elif action == "stats":
            response = session.get(f"{TARGET_URL}/stats-json", timeout=30)
            success = response.status_code == 200
        
        else:
            # Fallback - just hit homepage
            response = session.get(TARGET_URL, timeout=30)
            success = response.status_code == 200
            action = "fallback"
        
        latency = time.time() - start
        
    except Exception as e:
        latency = time.time() - start
        error = str(e)
    
    results.append({
        "success": success,
        "latency": latency,
        "action": action,
        "error": error
    })


def run_tier2_pass(pass_id):
    """Run a single Tier 2 pass."""
    config = PASS_CONFIGS[pass_id]
    users = config["users"]
    requests_per_user = config["requests_per_user"]
    duration = config["duration"]
    total_requests = users * requests_per_user
    
    print(f"\n{'='*60}")
    print(f"🔥 TIER 2 - PASS {pass_id}: PEAK PRODUCTION TEST")
    print(f"{'='*60}")
    print(f"  Users:     {users}")
    print(f"  Requests:  {total_requests} ({requests_per_user}/user)")
    print(f"  Duration:  {duration}s target")
    print(f"  Target:    {TARGET_URL}")
    print(f"{'='*60}\n")
    
    # Setup
    file_path = create_test_file()
    
    # Pre-create tokens
    print("📤 Pre-uploading files for download pool...")
    session = requests.Session()
    tokens = []
    password_tokens = []
    
    # Regular tokens
    for i in range(min(20, users)):
        token, _ = upload_file(session, file_path)
        if token:
            tokens.append(token)
    
    # Password-protected tokens
    for i in range(min(10, users // 5)):
        token, pwd = upload_file(session, file_path, password="testpass123")
        if token:
            password_tokens.append({"token": token, "password": pwd})
    
    print(f"  ✓ Created {len(tokens)} regular tokens")
    print(f"  ✓ Created {len(password_tokens)} password-protected tokens\n")
    
    # Run benchmark
    print("🔥 Starting peak production load test...")
    results = []
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=users) as executor:
        futures = []
        delay = duration / total_requests
        
        for _ in range(total_requests):
            sess = requests.Session()
            future = executor.submit(
                peak_workload, sess, tokens, password_tokens, file_path, results
            )
            futures.append(future)
            time.sleep(delay)
        
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
    
    # By action
    actions = {}
    for r in results:
        action = r.get("action", "unknown")
        if action not in actions:
            actions[action] = {"total": 0, "success": 0, "latencies": []}
        actions[action]["total"] += 1
        if r.get("success"):
            actions[action]["success"] += 1
            actions[action]["latencies"].append(r["latency"])
    
    metrics = {
        "pass_id": f"2.{pass_id}",
        "tier": 2,
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
            "by_action": {
                name: {
                    "total": data["total"],
                    "success": data["success"],
                    "success_rate": data["success"] / data["total"] * 100 if data["total"] > 0 else 0,
                    "avg_latency_ms": statistics.mean(data["latencies"]) * 1000 if data["latencies"] else 0
                }
                for name, data in actions.items()
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
    print(f"  P95 Latency:     {metrics['results']['latency']['p95']:.0f}ms")
    print(f"\n  📋 By Action:")
    for action, data in metrics['results']['by_action'].items():
        print(f"    {action}: {data['success']}/{data['total']} ({data['success_rate']:.0f}%) @ {data['avg_latency_ms']:.0f}ms avg")
    print(f"{'='*60}\n")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    result_file = f"results/tier2_pass{pass_id.replace('.', '_')}.json"
    with open(result_file, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"💾 Results saved to: {result_file}")
    
    # Grade
    if metrics['results']['error_rate'] < 2 and metrics['results']['rps'] > 80:
        grade = "A"
    elif metrics['results']['error_rate'] < 5 and metrics['results']['rps'] > 50:
        grade = "B"
    elif metrics['results']['error_rate'] < 10:
        grade = "C"
    else:
        grade = "D"
    
    print(f"🎯 GRADE: {grade}")
    
    return metrics


def run_all_tier2():
    """Run all Tier 2 passes."""
    print("\n" + "="*60)
    print("🏁 TIER 2: PEAK PRODUCTION LOAD TESTING")
    print("="*60)
    
    all_results = []
    for pass_id in ["2.1", "2.2", "2.3"]:
        result = run_tier2_pass(pass_id)
        all_results.append(result)
        print("\n⏳ Cooling down for 10 seconds...\n")
        time.sleep(10)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TIER 2 SUMMARY")
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
            run_tier2_pass(pass_id)
        elif pass_id == "all":
            run_all_tier2()
        else:
            print(f"Unknown pass: {pass_id}. Use 2.1, 2.2, 2.3, or 'all'")
    else:
        run_all_tier2()
