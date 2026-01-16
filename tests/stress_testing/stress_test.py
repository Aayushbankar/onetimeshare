"""
Day 22 Stress Testing Suite - Rebuilt using Day 20 Proven Pattern
==================================================================
Simple, reliable stress testing that actually works.
"""

import time
import requests
import statistics
import random
import string
import threading
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Configuration
TARGET_URL = os.getenv("TARGET_URL", "http://localhost:5000")

# Pre-generate 1MB payload to reduce test client CPU overhead
def generate_random_data(size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=size)).encode('utf-8')

PAYLOAD_1MB = generate_random_data(1024 * 1024)

# ============================================
# TIER 1: BASELINE (10, 20, 30 users)
# ============================================

def benchmark_upload(session, payload):
    """Performs: GET / -> POST /upload"""
    start_time = time.time()
    try:
        # 1. GET Landing Page
        r1 = session.get(TARGET_URL, timeout=10)
        if r1.status_code != 200:
            return False, 0, r1.status_code
            
        # 2. POST Upload
        files = {'file': ('test_load.txt', payload, 'text/plain')}
        r2 = session.post(f"{TARGET_URL}/upload", files=files, timeout=30)
        
        elapsed = time.time() - start_time
        return r2.status_code in (200, 201), elapsed, r2.status_code
    except Exception as e:
        return False, 0, str(e)


def run_tier1_pass(users, num_requests, pass_name):
    """Run a single Tier 1 baseline pass."""
    print(f"\n{'='*60}")
    print(f"🧪 {pass_name}")
    print(f"{'='*60}")
    print(f"  Users: {users} | Requests: {num_requests}")
    print(f"  Target: {TARGET_URL}")
    
    latencies = []
    success_count = 0
    errors = {}
    
    start_total = time.time()
    
    with ThreadPoolExecutor(max_workers=users) as executor:
        sessions = [requests.Session() for _ in range(num_requests)]
        tasks = [executor.submit(benchmark_upload, session, PAYLOAD_1MB) for session in sessions]
        
        for future in as_completed(tasks):
            success, latency, status = future.result()
            if success:
                success_count += 1
                latencies.append(latency)
            else:
                errors[str(status)] = errors.get(str(status), 0) + 1

    duration = time.time() - start_total
    
    # Metrics
    rps = success_count / duration if duration > 0 else 0
    avg_lat = statistics.mean(latencies) if latencies else 0
    p50_lat = statistics.median(latencies) if latencies else 0
    p95_lat = statistics.quantiles(latencies, n=20)[18] if len(latencies) > 20 else (max(latencies) if latencies else 0)
    p99_lat = statistics.quantiles(latencies, n=100)[98] if len(latencies) >= 100 else p95_lat
    error_rate = (num_requests - success_count) / num_requests * 100
    
    print(f"\n📊 RESULTS")
    print(f"  Total Time:   {duration:.2f}s")
    print(f"  Successful:   {success_count}/{num_requests}")
    print(f"  Error Rate:   {error_rate:.2f}%")
    print(f"  RPS:          {rps:.2f} req/s")
    print(f"  Avg Latency:  {avg_lat*1000:.0f}ms")
    print(f"  P50 Latency:  {p50_lat*1000:.0f}ms")
    print(f"  P95 Latency:  {p95_lat*1000:.0f}ms")
    if errors:
        print(f"  ⚠️  Errors: {errors}")
    
    # Grade
    if error_rate < 1 and rps > 30:
        grade = "A"
    elif error_rate < 5 and rps > 20:
        grade = "B"
    elif error_rate < 10:
        grade = "C"
    else:
        grade = "D"
    print(f"  Grade: {grade}")
    
    return {
        "pass": pass_name,
        "users": users,
        "requests": num_requests,
        "duration": duration,
        "successful": success_count,
        "rps": rps,
        "error_rate": error_rate,
        "latency": {"avg": avg_lat*1000, "p50": p50_lat*1000, "p95": p95_lat*1000, "p99": p99_lat*1000},
        "grade": grade,
        "errors": errors
    }


def run_tier1():
    """Run all Tier 1 passes."""
    print("\n" + "="*60)
    print("🏁 TIER 1: BASELINE LOAD TESTING")
    print("="*60)
    
    results = []
    
    # Pass 1.1: Light Load
    results.append(run_tier1_pass(users=10, num_requests=200, pass_name="TIER 1 - Pass 1.1 (10 users)"))
    time.sleep(3)
    
    # Pass 1.2: Moderate Load
    results.append(run_tier1_pass(users=20, num_requests=300, pass_name="TIER 1 - Pass 1.2 (20 users)"))
    time.sleep(3)
    
    # Pass 1.3: Normal Production
    results.append(run_tier1_pass(users=30, num_requests=400, pass_name="TIER 1 - Pass 1.3 (30 users)"))
    
    return results


# ============================================
# TIER 2: PEAK PRODUCTION (50, 75, 100 users)
# ============================================

def run_tier2():
    """Run all Tier 2 passes."""
    print("\n" + "="*60)
    print("🏁 TIER 2: PEAK PRODUCTION LOAD TESTING")
    print("="*60)
    
    results = []
    
    # Pass 2.1: High Load
    results.append(run_tier1_pass(users=50, num_requests=500, pass_name="TIER 2 - Pass 2.1 (50 users)"))
    time.sleep(5)
    
    # Pass 2.2: Very High Load
    results.append(run_tier1_pass(users=75, num_requests=600, pass_name="TIER 2 - Pass 2.2 (75 users)"))
    time.sleep(5)
    
    # Pass 2.3: Peak Production
    results.append(run_tier1_pass(users=100, num_requests=800, pass_name="TIER 2 - Pass 2.3 (100 users)"))
    
    return results


# ============================================
# TIER 3: DDoS SIMULATION (150, 200, 300 users)
# ============================================

def run_tier3():
    """Run all Tier 3 passes - find the breaking point."""
    print("\n" + "="*60)
    print("🏁 TIER 3: DDoS SIMULATION (FIND BREAKING POINT)")
    print("="*60)
    print("⚠️  WARNING: Expect errors - that's the goal!")
    
    results = []
    
    # Pass 3.1: Stress Test
    results.append(run_tier1_pass(users=150, num_requests=750, pass_name="TIER 3 - Pass 3.1 (150 users)"))
    time.sleep(10)
    
    # Check if system is already broken
    if results[-1]["error_rate"] > 50:
        print("\n❌ System reached breaking point. Stopping further tests.")
        return results
    
    # Pass 3.2: Extreme Load
    results.append(run_tier1_pass(users=200, num_requests=800, pass_name="TIER 3 - Pass 3.2 (200 users)"))
    time.sleep(10)
    
    if results[-1]["error_rate"] > 50:
        print("\n❌ System reached breaking point. Stopping further tests.")
        return results
    
    # Pass 3.3: DDoS Simulation
    results.append(run_tier1_pass(users=300, num_requests=900, pass_name="TIER 3 - Pass 3.3 (300 users)"))
    
    return results


# ============================================
# MAIN RUNNER
# ============================================

def run_full_suite():
    """Run complete 9-pass stress test suite."""
    print("\n" + "="*70)
    print("🚀 DAY 22: COMPREHENSIVE STRESS TESTING SUITE")
    print("="*70)
    
    start_time = time.time()
    all_results = {"tier1": [], "tier2": [], "tier3": []}
    
    # Tier 1
    all_results["tier1"] = run_tier1()
    print("\n⏳ Cooling down for 10 seconds...\n")
    time.sleep(10)
    
    # Tier 2
    all_results["tier2"] = run_tier2()
    print("\n⏳ Cooling down for 15 seconds...\n")
    time.sleep(15)
    
    # Tier 3
    all_results["tier3"] = run_tier3()
    
    total_time = time.time() - start_time
    
    # Final Summary
    print("\n" + "="*70)
    print("🏆 FINAL STRESS TEST REPORT")
    print("="*70)
    print(f"Total Duration: {total_time/60:.1f} minutes")
    print("\n📊 RESULTS SUMMARY")
    print(f"{'Pass':<35} {'Users':<8} {'RPS':<10} {'Error%':<10} {'Grade'}")
    print("-"*70)
    
    for tier_name, tier_results in all_results.items():
        for r in tier_results:
            print(f"{r['pass']:<35} {r['users']:<8} {r['rps']:<10.2f} {r['error_rate']:<10.2f} {r['grade']}")
    
    # Find performance ceiling
    print("\n🎯 PERFORMANCE CEILING")
    stable_users = 0
    max_rps = 0
    for tier_results in all_results.values():
        for r in tier_results:
            if r["error_rate"] < 5:
                stable_users = max(stable_users, r["users"])
                max_rps = max(max_rps, r["rps"])
    
    print(f"  ✅ Stable at: {stable_users} concurrent users")
    print(f"  📈 Max stable RPS: {max_rps:.2f}")
    
    # Save report
    os.makedirs("results", exist_ok=True)
    report_file = f"results/day22_stress_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_duration_seconds": total_time,
            "performance_ceiling": {"stable_users": stable_users, "max_rps": max_rps},
            "results": all_results
        }, f, indent=2)
    print(f"\n💾 Report saved to: {report_file}")
    
    return all_results


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        tier = sys.argv[1]
        if tier == "tier1":
            run_tier1()
        elif tier == "tier2":
            run_tier2()
        elif tier == "tier3":
            run_tier3()
        elif tier == "full":
            run_full_suite()
        else:
            print("Usage: python stress_test.py [tier1|tier2|tier3|full]")
    else:
        run_full_suite()
