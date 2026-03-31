import requests
import time

url = "http://localhost:8000/api/knowledge/upload-file"
filename = "beebot_test.txt"
file_content = b"BeeBot is an amazing AI assistant that integrates seamlessly with Pinecone."

files = {
    "file": (filename, file_content, "text/plain")
}
data = {
    "business_id": "test-business-2",
    "source_id": "api-call-test-source"
}

print(f"Uploading {filename} to {url}")
try:
    response = requests.post(url, files=files, data=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Failed: {e}")

time.sleep(3)

print("\nTesting Chat generation...")
chat_url = "http://localhost:8000/api/chat"
chat_data = {
    "query": "Does BeeBot integrate with Pinecone?",
    "business_id": "test-business-2"
}
try:
    chat_resp = requests.post(chat_url, json=chat_data, timeout=10)
    print(f"Chat Status: {chat_resp.status_code}")
    print(f"Chat Response: {chat_resp.json()}")
except Exception as e:
    print(f"Chat Failed: {e}")
