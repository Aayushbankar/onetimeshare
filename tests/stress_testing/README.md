# Day 22 Stress Testing Suite

Comprehensive 3-tier, 9-pass stress testing for OneTimeShare.

## Structure

```
stress_testing/
├── run_all.py           # Main runner (all 9 passes)
├── tier1_baseline.py    # Baseline: 10, 20, 30 users
├── tier2_peak.py        # Peak: 50, 75, 100 users
├── tier3_ddos.py        # DDoS: 150, 200, 300+ users
└── test_1mb.bin         # Auto-generated test file
```

## Usage

### Run Full Suite (Recommended)
```bash
cd /mnt/shared_data/projects/onetimeshare
python -m tests.stress_testing.run_all full
```

### Run Individual Tiers
```bash
python -m tests.stress_testing.run_all tier1
python -m tests.stress_testing.run_all tier2
python -m tests.stress_testing.run_all tier3
```

### Run Single Pass
```bash
python -m tests.stress_testing.tier1_baseline 1.1
python -m tests.stress_testing.tier2_peak 2.3
python -m tests.stress_testing.tier3_ddos 3.2
```

## Prerequisites

1. Docker running: `docker compose up -d`
2. Rate limiting disabled (for accurate benchmarks)
3. ~30 minutes for full suite

## Results

Results saved to `results/` directory:
- `tier1_pass1_1.json`, `tier1_pass1_2.json`, etc.
- `day22_final_report_YYYYMMDD_HHMMSS.json`

## Metrics Captured

- RPS (Requests Per Second)
- Latency: P50, P95, P99, Max
- Error Rate
- Error Breakdown (by type)
- Breaking Point Analysis
