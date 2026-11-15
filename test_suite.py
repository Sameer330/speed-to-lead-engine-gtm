import json
import time
from starlette.testclient import TestClient
from app import app

client = TestClient(app)

def run_test_suite():
    print("=" * 80)
    print("⚡ ANTHROPIC ENTERPRISE SPEED-TO-LEAD ENGINE: AUTOMATED TEST SUITE")
    print("=" * 80)

    with open("data/test_leads.json", "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    results = []

    for idx, test in enumerate(test_cases, 1):
        lead_payload = test["payload"]
        expected = test["expected_tier"]
        desc = test["description"]

        print(f"\n[Test {idx}/{len(test_cases)}] {lead_payload.get('first_name')} {lead_payload.get('last_name')} @ {lead_payload.get('company_name')}")
        print(f"Context: {desc}")
        print(f"Expected: {expected}")

        start_time = time.time()
        response = client.post("/webhook/inbound-lead", json=lead_payload)
        elapsed = round(time.time() - start_time, 2)

        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            continue

        data = response.json()
        actual_tier = data["evaluation"]["tier"]
        actual_action = data["evaluation"]["suggested_action"]
        crawl_status = data["profile"]["crawl_status"]

        # Check if actual tier matches or contains expected
        passed = expected.lower() in actual_tier.lower()
        status_flag = "✅ PASS" if passed else "⚠️ VARIANCE"

        print(f"Result: {status_flag} | Actual: {actual_tier} | Latency: {elapsed}s | Crawl: {crawl_status}")
        print(f"Action: {actual_action}")

        results.append({
            "company": lead_payload.get("company_name"),
            "email": lead_payload.get("email"),
            "expected": expected,
            "actual": actual_tier,
            "status": status_flag,
            "latency": f"{elapsed}s",
            "action": actual_action
        })

    # Summary Table
    print("\n" + "=" * 80)
    print("📊 EXECUTIVE BENCHMARK SUMMARY")
    print("=" * 80)
    print(f"{'Company':<15} | {'Email':<28} | {'Expected':<12} | {'Actual':<12} | {'Latency':<8} | {'Status'}")
    print("-" * 80)
    for r in results:
        print(f"{r['company']:<15} | {r['email']:<28} | {r['expected']:<12} | {r['actual']:<12} | {r['latency']:<8} | {r['status']}")
    print("=" * 80)

if __name__ == "__main__":
    run_test_suite()
