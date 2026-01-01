#!/usr/bin/env python3
"""
OneTimeShare Concurrent Download Tests
Day 8: Testing Atomic One-Time Downloads

Usage:
    python test_concurrent_downloads.py

Requirements:
    - Flask app running on localhost:5000
    - Redis running
    - requests library installed
"""

import threading
import time
import os
import sys
import requests

# Configuration
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5000')
TEST_FILE_CONTENT = f"Test file created at {time.time()}"


def create_test_file():
    """Create a temporary test file."""
    test_path = '/tmp/test_upload.txt'
    with open(test_path, 'w') as f:
        f.write(TEST_FILE_CONTENT)
    return test_path


def upload_file(file_path):
    """Upload a file and return the token."""
    try:
        with open(file_path, 'rb') as f:
            response = requests.post(
                f"{BASE_URL}/upload",
                files={'file': ('test.txt', f, 'text/plain')},
                timeout=30
            )
        
        if response.status_code == 201:
            data = response.json()
            metadata = data.get('metadata', {})
            token = metadata.get('token')
            return token
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"❌ Upload exception: {e}")
        return None


def download_file(token, results, index, thread_name):
    """Attempt to download a file, store result."""
    start_time = time.time()
    try:
        response = requests.get(f"{BASE_URL}/d/{token}", timeout=30)
        elapsed = time.time() - start_time
        results[index] = {
            'thread': thread_name,
            'status_code': response.status_code,
            'elapsed': round(elapsed, 3),
            'success': response.status_code == 200
        }
    except Exception as e:
        elapsed = time.time() - start_time
        results[index] = {
            'thread': thread_name,
            'status_code': 'ERROR',
            'error': str(e),
            'elapsed': round(elapsed, 3),
            'success': False
        }


def test_sequential_downloads():
    """Test 1: Verify basic sequential download works and second fails."""
    print("\n" + "=" * 60)
    print("TEST 1: Sequential Downloads")
    print("=" * 60)
    
    # Upload a file
    test_file = create_test_file()
    token = upload_file(test_file)
    
    if not token:
        print("❌ FAILED: Could not upload test file")
        return False
    
    print(f"📤 Uploaded file, token: {token}")
    
    # First download - should succeed
    response1 = requests.get(f"{BASE_URL}/d/{token}")
    print(f"📥 Download 1: HTTP {response1.status_code}")
    
    # Second download - should fail with 410 Gone
    response2 = requests.get(f"{BASE_URL}/d/{token}")
    print(f"📥 Download 2: HTTP {response2.status_code}")
    
    # Verify
    if response1.status_code == 200 and response2.status_code == 410:
        print("✅ PASSED: First download succeeded, second got 410 Gone")
        return True
    else:
        print(f"❌ FAILED: Expected (200, 410), got ({response1.status_code}, {response2.status_code})")
        return False


def test_concurrent_downloads(num_threads=5):
    """Test 2: Verify only ONE of N concurrent downloads succeeds."""
    print("\n" + "=" * 60)
    print(f"TEST 2: Concurrent Downloads ({num_threads} threads)")
    print("=" * 60)
    
    # Upload a file
    test_file = create_test_file()
    token = upload_file(test_file)
    
    if not token:
        print("❌ FAILED: Could not upload test file")
        return False
    
    print(f"📤 Uploaded file, token: {token}")
    
    # Prepare threads
    results = [None] * num_threads
    threads = []
    
    for i in range(num_threads):
        thread_name = f"Thread-{i+1}"
        t = threading.Thread(
            target=download_file,
            args=(token, results, i, thread_name)
        )
        threads.append(t)
    
    # Start all threads as close together as possible
    print(f"🚀 Starting {num_threads} concurrent downloads...")
    start_time = time.time()
    
    for t in threads:
        t.start()
    
    # Wait for all to complete
    for t in threads:
        t.join()
    
    elapsed = time.time() - start_time
    print(f"⏱️ All downloads completed in {elapsed:.3f}s")
    
    # Analyze results
    print("\n📊 Results:")
    success_count = 0
    fail_count = 0
    
    for r in results:
        if r:
            status = "✅ SUCCESS" if r['success'] else "❌ FAILED"
            print(f"  {r['thread']}: HTTP {r['status_code']} ({status}) - {r['elapsed']}s")
            if r['success']:
                success_count += 1
            elif r['status_code'] == 410:
                fail_count += 1
    
    print(f"\n📈 Summary:")
    print(f"  Successful downloads (200): {success_count}")
    print(f"  Rejected downloads (410):   {fail_count}")
    
    # Verify exactly ONE succeeded
    if success_count == 1 and fail_count == num_threads - 1:
        print(f"\n✅ PASSED: Exactly 1 download succeeded, {num_threads - 1} got 410 Gone")
        return True
    elif success_count == 0:
        print(f"\n❌ FAILED: No downloads succeeded (something else is broken)")
        return False
    else:
        print(f"\n❌ FAILED: {success_count} downloads succeeded (RACE CONDITION DETECTED!)")
        return False


def test_rapid_concurrent_downloads():
    """Test 3: Stress test with rapid concurrent requests."""
    print("\n" + "=" * 60)
    print("TEST 3: Rapid Concurrent Downloads (10 threads)")
    print("=" * 60)
    
    return test_concurrent_downloads(num_threads=10)


def run_all_tests():
    """Run all concurrent download tests."""
    print("=" * 60)
    print("OneTimeShare Concurrent Download Test Suite")
    print(f"Target: {BASE_URL}")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Server is responding (HTTP {response.status_code})")
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please start the Flask app first: docker-compose up")
        sys.exit(1)
    
    results = []
    
    # Run tests
    results.append(("Sequential Downloads", test_sequential_downloads()))
    results.append(("Concurrent Downloads (5)", test_concurrent_downloads(5)))
    results.append(("Rapid Concurrent (10)", test_rapid_concurrent_downloads()))
    
    # Summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
        if result:
            passed += 1
    
    print(f"\n{passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Atomic downloads working correctly.")
        return 0
    else:
        print("\n⚠️ Some tests failed! Check implementation for race conditions.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
