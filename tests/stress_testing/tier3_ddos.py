"""
Day 22 Stress Testing Suite - Tier 3: DDoS Simulation
======================================================
Tests: Pass 3.1 (150 users), Pass 3.2 (200 users), Pass 3.3 (300+ users until break)

This pushes the system to absolute failure to find the breaking point.
"""

import threading
import time
import requests
import statistics
import sys
import os
import json
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:5000")
TEST_FILE_PATH = "tests/stress_testing/test_1mb.bin"

# Pass configurations - DDoS Simulation
PASS_CONFIGS = {
    "3.1": {"users": 150, "requests_per_user": 5, "duration": 120},
    "3.2": {"users": 200, "requests_per_user": 4, "duration": 120},
    "3.3": {"users": 300, "requests_per_user": 3, "duration": 180},
}


def create_test_file():
    """Create 1MB test file if it doesn't exist."""
    os.makedirs(os.path.dirname(TEST_FILE_PATH), exist_ok=True)
    if not os.path.exists(TEST_FILE_PATH):
        with open(TEST_FILE_PATH, "wb") as f:
            f.write(os.urandom(1024 * 1024))
        print(f"✓ Created test file: {TEST_FILE_PATH}")
    return TEST_FILE_PATH


def upload_file(session, file_path):
    """Upload a file and return the token."""
    try:
        with open(file_path, "rb") as f:
            response = session.post(
                f"{TARGET_URL}/upload",
                files={"file": ("test.txt", f, "text/plain")},
                timeout=10
            )
        if response.status_code == 200:
            return response.json().get("token")
    except:
        pass
    return None


def aggressive_workload(session, tokens, file_path, results, error_tracker):
    """
    Aggressive DDoS simulation workload.
    No wait times - fire as fast as possible.
    """
    action = random.choices(
        ["download", "upload", "stats"],
        weights=[60, 30, 10]
    )[0]
    
    start = time.time()
    success = False
    error = None
    error_type = None
    
    try:
        if action == "download" and tokens:
            token = random.choice(list(tokens)) if tokens else None
            if token:
                response = session.get(f"{TARGET_URL}/info/{token}", timeout=30)
                success = response.status_code == 200
                if not success:
                    error_type = f"HTTP_{response.status_code}"
            
        elif action == "upload":
            with open(file_path, "rb") as f:
                response = session.post(
                    f"{TARGET_URL}/upload",
                    files={"file": ("test.txt", f, "text/plain")},
                    timeout=30
                )
            success = response.status_code == 200
            if success:
                new_token = response.json().get("token")
                if new_token and len(tokens) < 100:  # Cap token pool
                    tokens.add(new_token)
            else:
                error_type = f"HTTP_{response.status_code}"
                        
        elif action == "stats":
            response = session.get(f"{TARGET_URL}/stats-json", timeout=30)
            success = response.status_code == 200
            if not success:
                error_type = f"HTTP_{response.status_code}"
        
        latency = time.time() - start
        
    except requests.exceptions.Timeout:
        latency = time.time() - start
        error = "Timeout"
        error_type = "Timeout"
    except requests.exceptions.ConnectionError as e:
        latency = time.time() - start
        error = "Connection refused"
        error_type = "ConnectionRefused"
    except Exception as e:
        latency = time.time() - start
        error = str(e)
        error_type = type(e).__name__
    
    # Track error types
    if error_type:
        error_tracker[error_type] = error_tracker.get(error_type, 0) + 1
    
    results.append({
        "success": success,
        "latency": latency,
        "action": action,
        "error": error,
        "error_type": error_type
    })


def run_tier3_pass(pass_id):
    """Run a single Tier 3 pass."""
    config = PASS_CONFIGS[pass_id]
    users = config["users"]
    requests_per_user = config["requests_per_user"]
    duration = config["duration"]
    total_requests = users * requests_per_user
    
    print(f"\n{'='*60}")
    print(f"💥 TIER 3 - PASS {pass_id}: DDoS SIMULATION")
    print(f"{'='*60}")
    print(f"  Users:     {users} (AGGRESSIVE)")
    print(f"  Requests:  {total_requests} ({requests_per_user}/user)")
    print(f"  Duration:  {duration}s max")
    print(f"  Target:    {TARGET_URL}")
    print(f"  Mode:      MAXIMUM AGGRESSION")
    print(f"{'='*60}\n")
    
    # Setup
    file_path = create_test_file()
    
    # Pre-create tokens (thread-safe set)
    print("📤 Pre-uploading files for download pool...")
    session = requests.Session()
    tokens = set()
    
    for i in range(min(30, users // 5)):
        try:
            token = upload_file(session, file_path)
            if token:
                tokens.add(token)
        except:
            pass
    
    print(f"  ✓ Created {len(tokens)} tokens for download pool\n")
    
    # Run aggressive benchmark
    print("💥 LAUNCHING DDoS SIMULATION...")
    print("   (Expect errors - that's the goal!)\n")
    
    results = []
    error_tracker = {}
    start_time = time.time()
    
    # Minimum delay between requests (aggressive)
    delay = duration / total_requests / 2  # Even faster than target
    
    with ThreadPoolExecutor(max_workers=min(users, 200)) as executor:
        futures = []
        
        for i in range(total_requests):
            sess = requests.Session()
            future = executor.submit(
                aggressive_workload, sess, tokens, file_path, results, error_tracker
            )
            futures.append(future)
            
            # Minimal delay - fire rapidly
            if delay > 0:
                time.sleep(delay)
            
            # Progress indicator
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start_time
                current_rps = (i + 1) / elapsed if elapsed > 0 else 0
                error_count = sum(1 for r in results if not r.get("success"))
                print(f"   [{i+1}/{total_requests}] RPS: {current_rps:.1f} | Errors: {error_count}")
        
        # Wait for completion with timeout
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
    
    metrics = {
        "pass_id": f"3.{pass_id}",
        "tier": 3,
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
            "peak_rps": len(results) / total_time if total_time > 0 else 0,  # All requests
            "latency": {
                "avg": statistics.mean(latencies) * 1000 if latencies else 0,
                "p50": statistics.median(latencies) * 1000 if latencies else 0,
                "p95": statistics.quantiles(latencies, n=20)[18] * 1000 if len(latencies) > 20 else 0,
                "p99": statistics.quantiles(latencies, n=100)[98] * 1000 if len(latencies) > 100 else 0,
                "max": max(latencies) * 1000 if latencies else 0,
            },
            "error_breakdown": error_tracker
        },
        "breaking_point_analysis": {
            "system_held": len(failed) / len(results) < 0.1 if results else False,
            "degraded": 0.1 <= len(failed) / len(results) < 0.3 if results else False,
            "failing": len(failed) / len(results) >= 0.3 if results else True,
            "primary_failure_mode": max(error_tracker, key=error_tracker.get) if error_tracker else "None"
        }
    }
    
    # Print results
    print(f"\n{'='*60}")
    print(f"📊 PASS {pass_id} RESULTS")
    print(f"{'='*60}")
    print(f"  Total Time:      {total_time:.2f}s")
    print(f"  Requests:        {len(successful)}/{len(results)} successful")
    print(f"  Error Rate:      {metrics['results']['error_rate']:.2f}%")
    print(f"  Successful RPS:  {metrics['results']['rps']:.2f} req/s")
    print(f"  Peak RPS:        {metrics['results']['peak_rps']:.2f} req/s")
    print(f"  Avg Latency:     {metrics['results']['latency']['avg']:.0f}ms")
    print(f"  P95 Latency:     {metrics['results']['latency']['p95']:.0f}ms")
    print(f"  Max Latency:     {metrics['results']['latency']['max']:.0f}ms")
    
    print(f"\n  ⚠️  Error Breakdown:")
    for error_type, count in sorted(error_tracker.items(), key=lambda x: -x[1]):
        pct = count / len(results) * 100 if results else 0
        print(f"    {error_type}: {count} ({pct:.1f}%)")
    
    # Analysis
    analysis = metrics['breaking_point_analysis']
    print(f"\n  🔍 Breaking Point Analysis:")
    if analysis['system_held']:
        status = "✅ SYSTEM HELD - Error rate < 10%"
    elif analysis['degraded']:
        status = "⚠️  DEGRADED - Error rate 10-30%"
    else:
        status = "❌ FAILING - Error rate > 30%"
    print(f"    Status: {status}")
    print(f"    Primary Failure: {analysis['primary_failure_mode']}")
    
    print(f"{'='*60}\n")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    result_file = f"results/tier3_pass{pass_id.replace('.', '_')}.json"
    with open(result_file, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"💾 Results saved to: {result_file}")
    
    return metrics


def run_all_tier3():
    """Run all Tier 3 passes."""
    print("\n" + "="*60)
    print("🏁 TIER 3: DDoS SIMULATION (FIND THE CEILING)")
    print("="*60)
    print("⚠️  WARNING: This will stress the system to failure!")
    print("="*60)
    
    all_results = []
    for pass_id in ["3.1", "3.2", "3.3"]:
        result = run_tier3_pass(pass_id)
        all_results.append(result)
        
        # Check if system is already broken
        if result['results']['error_rate'] > 50:
            print("\n❌ System reached breaking point. Stopping further tests.")
            break
        
        print("\n⏳ Cooling down for 15 seconds (let system recover)...\n")
        time.sleep(15)
    
    # Summary
    print("\n" + "="*60)
    print("📊 TIER 3 SUMMARY - BREAKING POINT ANALYSIS")
    print("="*60)
    print(f"{'Pass':<10} {'Users':<8} {'RPS':<10} {'Error%':<10} {'Status':<15}")
    print("-"*60)
    for r in all_results:
        error_rate = r['results']['error_rate']
        if error_rate < 10:
            status = "✅ Stable"
        elif error_rate < 30:
            status = "⚠️  Degraded"
        else:
            status = "❌ Failing"
        print(f"{r['pass_id']:<10} {r['config']['users']:<8} {r['results']['rps']:<10.2f} {error_rate:<10.2f} {status:<15}")
    print("="*60)
    
    # Find ceiling
    for r in all_results:
        if r['results']['error_rate'] >= 10:
            print(f"\n🎯 PERFORMANCE CEILING DETECTED:")
            print(f"   System degrades at ~{r['config']['users']} concurrent users")
            print(f"   Maximum stable RPS: ~{r['results']['rps']:.0f}")
            break
    else:
        print(f"\n✅ System held up to {all_results[-1]['config']['users']} users!")
        print(f"   Peak RPS: {max(r['results']['rps'] for r in all_results):.0f}")
    
    return all_results


if __name__ == "__main__":
    if len(sys.argv) > 1:
        pass_id = sys.argv[1]
        if pass_id in PASS_CONFIGS:
            run_tier3_pass(pass_id)
        elif pass_id == "all":
            run_all_tier3()
        else:
            print(f"Unknown pass: {pass_id}. Use 3.1, 3.2, 3.3, or 'all'")
    else:
        run_all_tier3()
