# Tests Directory Structure

## Current Organization

```
tests/
├── stress_testing/          # Day 22: Comprehensive stress tests
│   ├── README.md
│   ├── run_all.py          # Main runner (all 9 passes)
│   ├── tier1_baseline.py   # Baseline: 10, 20, 30 users
│   ├── tier2_peak.py       # Peak: 50, 75, 100 users
│   └── tier3_ddos.py       # DDoS: 150, 200, 300+ users
│
├── day20_legacy/            # Day 20: Original (superseded) tests
│   ├── README.md
│   ├── test_load.py
│   ├── test_load_pass2.py
│   └── test_load_pass3.py
│
├── test_encryption.py       # Unit tests: ChaCha20 encryption
├── test_concurrent_downloads.py  # Unit tests: Race conditions
└── performance/             # Additional performance tests
```

## Test Categories

### Unit Tests (pytest)
- `test_encryption.py` - Encryption/decryption unit tests
- `test_concurrent_downloads.py` - Thread safety tests

Run with: `pytest tests/test_*.py -v`

### Stress Tests (standalone)
- `stress_testing/` - Full load testing suite

Run with: `python -m tests.stress_testing.run_all full`

### Legacy (archived)
- `day20_legacy/` - Original ad-hoc tests, kept for reference
