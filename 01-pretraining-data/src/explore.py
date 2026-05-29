from datasets import load_dataset

# Stream FineWeb — this doesn't download all 44TB.
# Streaming means it fetches one sample at a time, on demand.
dataset = load_dataset(
    "HuggingFaceFW/fineweb",
    name="sample-10BT",   # a 10-billion-token slice of the full 15T dataset
    split="train",
    streaming=True,        # don't download everything, just fetch as we go
)

print("=" * 60)
print("FINEWEB — RAW PRETRAINING DATA")
print("This is the actual data LLMs like Llama 3 train on.")
print("=" * 60)

for i, sample in enumerate(dataset):
    if i >= 10:  # look at 10 samples
        break

    print(f"\n--- Sample {i + 1} ---")
    print(f"URL    : {sample['url']}")
    print(f"Length : {len(sample['text'])} characters")
    print(f"Text   :\n{sample['text'][:500]}")  # first 500 characters
    print()

print("=" * 60)
print("That's what 44TB of filtered internet text looks like up close.")
print("Ordinary web articles, back to back, for 15 trillion tokens.")
