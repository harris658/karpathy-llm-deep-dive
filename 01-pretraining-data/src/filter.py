from datasets import load_dataset
from langdetect import detect, LangDetectException

# --- The 5-step filter pipeline from Karpathy's video ---

# Step 1: URL filter — blocklist of bad domain patterns
URL_BLOCKLIST = [
    "porn", "xxx", "adult", "spam", "malware",
    "casino", "viagra", "login", "signin", "signup",
    "profile.cgi",   # forum profile pages (no real content)
]

def passes_url_filter(url):
    url_lower = url.lower()
    for bad in URL_BLOCKLIST:
        if bad in url_lower:
            return False, f"URL blocklist ({bad})"
    return True, None


# Step 2: Text extraction quality — did we actually get prose?
# (FineWeb already strips HTML, but some pages are still just tables/menus)
def passes_text_filter(text):
    if len(text.strip()) < 200:
        return False, "too short (< 200 chars)"
    return True, None


# Step 3: Language filter — keep only pages that are clearly English
# Karpathy's FineWeb uses >65% English as the threshold
def passes_language_filter(text):
    try:
        lang = detect(text[:1000])  # check the first 1000 chars
        if lang != "en":
            return False, f"wrong language ({lang})"
    except LangDetectException:
        return False, "language undetectable"
    return True, None


# Step 4: Deduplication — skipped here (needs comparing across all docs)
# In production this uses MinHash across millions of documents.
# We'll just note where it would apply.

# Step 5: Repetition filter — a simple proxy for spam/low-quality pages
# If the same sentence appears 3+ times, it's likely boilerplate or spam
def passes_repetition_filter(text):
    sentences = [s.strip() for s in text.split(".") if len(s.strip()) > 20]
    seen = {}
    for s in sentences:
        seen[s] = seen.get(s, 0) + 1
        if seen[s] >= 3:
            return False, f"repeated sentence: '{s[:60]}...'"
    return True, None


def run_pipeline(sample):
    text = sample["text"]
    url = sample["url"]

    checks = [
        ("URL filter",         passes_url_filter(url)),
        ("Text filter",        passes_text_filter(text)),
        ("Language filter",    passes_language_filter(text)),
        ("Repetition filter",  passes_repetition_filter(text)),
    ]

    for step, (passed, reason) in checks:
        if not passed:
            return False, step, reason

    return True, None, None


# --- Run it ---

dataset = load_dataset(
    "HuggingFaceFW/fineweb",
    name="sample-10BT",
    split="train",
    streaming=True,
)

kept = 0
dropped = 0
drop_reasons = {}

print("=" * 60)
print("RUNNING THE FILTER PIPELINE")
print("=" * 60)

for i, sample in enumerate(dataset):
    if i >= 50:  # test on 50 samples
        break

    passed, failed_step, reason = run_pipeline(sample)

    if passed:
        kept += 1
        status = "KEPT"
        detail = ""
    else:
        dropped += 1
        status = "DROPPED"
        detail = f"  → {failed_step}: {reason}"
        drop_reasons[failed_step] = drop_reasons.get(failed_step, 0) + 1

    # print every sample's result
    print(f"[{status}] {sample['url'][:70]}{detail}")

print("\n" + "=" * 60)
print(f"Results across 50 samples:")
print(f"  Kept    : {kept} ({kept/50*100:.0f}%)")
print(f"  Dropped : {dropped} ({dropped/50*100:.0f}%)")
print(f"\nDrop reasons:")
for step, count in sorted(drop_reasons.items(), key=lambda x: -x[1]):
    print(f"  {step}: {count}")
print("=" * 60)
