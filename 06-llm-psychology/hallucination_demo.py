import requests

HF_TOKEN = "your_hf_token_here"  # get a free token at huggingface.co/settings/tokens
MODEL = "gpt2"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

PROMPT = "Orson Kovats is a famous"

print(f"Asking: '{PROMPT}...' — 3 times\n")
print("=" * 50)

for i in range(1, 4):
    response = requests.post(
        API_URL,
        headers=HEADERS,
        json={
            "inputs": PROMPT,
            "parameters": {"max_new_tokens": 80, "temperature": 0.9, "do_sample": True}
        }
    )
    result = response.json()
    if isinstance(result, list):
        answer = result[0]["generated_text"]
    elif "error" in result:
        answer = f"Error: {result['error']}"
    else:
        answer = str(result)
    print(f"\nAttempt {i}:\n{answer}")
    print("-" * 50)
