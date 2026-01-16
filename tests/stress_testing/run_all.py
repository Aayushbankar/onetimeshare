"""
Day 22 Stress Testing Suite - Main Runner
==========================================
Runs all 9 passes across 3 tiers and generates final report.
"""

import sys
import os
import json
import time
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stress_testing.tier1_baseline import run_all_tier1
from stress_testing.tier2_peak import run_all_tier2
from stress_testing.tier3_ddos import run_all_tier3


def generate_final_report(tier1_results, tier2_results, tier3_results):
    """Generate comprehensive final report."""
    
    all_results = tier1_results + tier2_results + tier3_results
    
    report = {
        "report_date": datetime.now().isoformat(),
        "total_passes": len(all_results),
        "tiers": {
            "tier1": {
                "name": "Baseline",
                "passes": len(tier1_results),
                "max_users": max(r["config"]["users"] for r in tier1_results) if tier1_results else 0,
                "avg_rps": sum(r["results"]["rps"] for r in tier1_results) / len(tier1_results) if tier1_results else 0,
                "max_error_rate": max(r["results"]["error_rate"] for r in tier1_results) if tier1_results else 0,
            },
            "tier2": {
                "name": "Peak Production",
                "passes": len(tier2_results),
                "max_users": max(r["config"]["users"] for r in tier2_results) if tier2_results else 0,
                "avg_rps": sum(r["results"]["rps"] for r in tier2_results) / len(tier2_results) if tier2_results else 0,
                "max_error_rate": max(r["results"]["error_rate"] for r in tier2_results) if tier2_results else 0,
            },
            "tier3": {
                "name": "DDoS Simulation",
                "passes": len(tier3_results),
                "max_users": max(r["config"]["users"] for r in tier3_results) if tier3_results else 0,
                "peak_rps": max(r["results"]["rps"] for r in tier3_results) if tier3_results else 0,
                "breaking_point_error_rate": tier3_results[-1]["results"]["error_rate"] if tier3_results else 0,
            }
        },
        "performance_ceiling": {
            "stable_users": 0,
            "degraded_users": 0,
            "failing_users": 0,
            "max_stable_rps": 0,
        },
        "all_passes": all_results
    }
    
    # Find performance ceiling
    for r in all_results:
        error_rate = r["results"]["error_rate"]
        users = r["config"]["users"]
        rps = r["results"]["rps"]
        
        if error_rate < 5:
            report["performance_ceiling"]["stable_users"] = users
            report["performance_ceiling"]["max_stable_rps"] = max(
                report["performance_ceiling"]["max_stable_rps"], rps
            )
        elif error_rate < 20:
            report["performance_ceiling"]["degraded_users"] = users
        else:
            if report["performance_ceiling"]["failing_users"] == 0:
                report["performance_ceiling"]["failing_users"] = users
    
    return report


def print_final_summary(report):
    """Print beautiful final summary."""
    print("\n")
    print("=" * 70)
    print("🏆 FINAL STRESS TEST REPORT - OneTimeShare")
    print("=" * 70)
    print(f"Date: {report['report_date']}")
    print(f"Total Passes: {report['total_passes']}")
    print("=" * 70)
    
    print("\n📊 TIER SUMMARY")
    print("-" * 70)
    print(f"{'Tier':<25} {'Users':<10} {'Avg RPS':<12} {'Max Error%':<12}")
    print("-" * 70)
    
    for tier_name, tier_data in report["tiers"].items():
        if tier_data["passes"] > 0:
            avg_rps = tier_data.get("avg_rps", tier_data.get("peak_rps", 0))
            max_err = tier_data.get("max_error_rate", tier_data.get("breaking_point_error_rate", 0))
            print(f"{tier_data['name']:<25} {tier_data['max_users']:<10} {avg_rps:<12.2f} {max_err:<12.2f}")
    
    print("-" * 70)
    
    ceiling = report["performance_ceiling"]
    print("\n🎯 PERFORMANCE CEILING")
    print("-" * 70)
    print(f"  ✅ Stable at:          {ceiling['stable_users']} concurrent users")
    print(f"  ⚠️  Degraded at:        {ceiling['degraded_users']} concurrent users")
    print(f"  ❌ Failing at:         {ceiling['failing_users']} concurrent users")
    print(f"  📈 Max Stable RPS:     {ceiling['max_stable_rps']:.2f} requests/second")
    print("-" * 70)
    
    # Certification
    print("\n🏅 CERTIFICATION")
    print("-" * 70)
    if ceiling["stable_users"] >= 100:
        cert = "🏆 PLATINUM - Production Ready (100+ users stable)"
    elif ceiling["stable_users"] >= 50:
        cert = "🥇 GOLD - High Capacity (50+ users stable)"
    elif ceiling["stable_users"] >= 30:
        cert = "🥈 SILVER - Standard Capacity (30+ users stable)"
    else:
        cert = "🥉 BRONZE - Limited Capacity (needs optimization)"
    
    print(f"  {cert}")
    print("=" * 70)


def run_full_suite():
    """Run the complete stress testing suite."""
    print("\n")
    print("=" * 70)
    print("🚀 DAY 22: COMPREHENSIVE STRESS TESTING SUITE")
    print("=" * 70)
    print("Running 9 passes across 3 tiers...")
    print("This will take approximately 20-30 minutes.")
    print("=" * 70)
    
    start_time = time.time()
    
    # Tier 1
    print("\n\n" + "=" * 70)
    print("PHASE 1/3: TIER 1 - BASELINE")
    print("=" * 70)
    tier1_results = run_all_tier1()
    print("\n✅ Tier 1 Complete. Cooling down for 10 seconds...")
    time.sleep(10)
    
    # Tier 2
    print("\n\n" + "=" * 70)
    print("PHASE 2/3: TIER 2 - PEAK PRODUCTION")
    print("=" * 70)
    tier2_results = run_all_tier2()
    print("\n✅ Tier 2 Complete. Cooling down for 15 seconds...")
    time.sleep(15)
    
    # Tier 3
    print("\n\n" + "=" * 70)
    print("PHASE 3/3: TIER 3 - DDoS SIMULATION")
    print("=" * 70)
    tier3_results = run_all_tier3()
    print("\n✅ Tier 3 Complete.")
    
    total_time = time.time() - start_time
    
    # Generate report
    report = generate_final_report(tier1_results, tier2_results, tier3_results)
    report["total_test_duration_seconds"] = total_time
    
    # Save report
    os.makedirs("results", exist_ok=True)
    report_file = f"results/day22_final_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n💾 Full report saved to: {report_file}")
    
    # Print summary
    print_final_summary(report)
    
    print(f"\n⏱️  Total Test Duration: {total_time/60:.1f} minutes")
    
    return report


if __name__ == "__main__":
    if len(sys.argv) > 1:
        tier = sys.argv[1]
        if tier == "tier1":
            run_all_tier1()
        elif tier == "tier2":
            run_all_tier2()
        elif tier == "tier3":
            run_all_tier3()
        elif tier == "full":
            run_full_suite()
        else:
            print("Usage: python run_all.py [tier1|tier2|tier3|full]")
    else:
        run_full_suite()
