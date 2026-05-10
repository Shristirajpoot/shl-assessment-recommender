import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    print("Testing /health...")
    resp = requests.get(f"{BASE_URL}/health")
    print(resp.status_code, resp.json())

def test_chat():
    print("\nTesting /chat (Turn 1: vague query)...")
    payload1 = {
        "messages": [
            {"role": "user", "content": "I am hiring a Java developer"}
        ]
    }
    resp1 = requests.post(f"{BASE_URL}/chat", json=payload1)
    res_data1 = resp1.json()
    print("Turn 1 Response:")
    print(json.dumps(res_data1, indent=2))
    
    print("\nTesting /chat (Turn 2: providing context)...")
    payload2 = {
        "messages": [
            {"role": "user", "content": "I am hiring a Java developer"},
            {"role": "assistant", "content": res_data1['reply']},
            {"role": "user", "content": "Mid-level. And I need a personality test focusing on teamwork."}
        ]
    }
    resp2 = requests.post(f"{BASE_URL}/chat", json=payload2)
    res_data2 = resp2.json()
    print("Turn 2 Response:")
    print(json.dumps(res_data2, indent=2))

    print("\nTesting /chat (Turn 3: comparing tests)...")
    payload3 = {
        "messages": [
            {"role": "user", "content": "I am hiring a Java developer"},
            {"role": "assistant", "content": res_data1['reply']},
            {"role": "user", "content": "Mid-level. And I need a personality test focusing on teamwork."},
            {"role": "assistant", "content": res_data2['reply']},
            {"role": "user", "content": "What is the difference between OPQ32r and GSA?"}
        ]
    }
    resp3 = requests.post(f"{BASE_URL}/chat", json=payload3)
    res_data3 = resp3.json()
    print("Turn 3 Response:")
    print(json.dumps(res_data3, indent=2))

if __name__ == "__main__":
    test_health()
    test_chat()

