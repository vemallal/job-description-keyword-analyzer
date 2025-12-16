import re
import csv
from collections import Counter

# A small list of common "stop words" to ignore (you can add more later)
STOP_WORDS = {
    "a","an","the","and","or","to","of","in","on","for","with","as","by","is","are","be",
    "this","that","it","from","at","you","we","our","your","they","their","will","can",
    "must","may","etc","not","but","into","than","then"
}

# Optional: skill phrases to look for (resume-friendly)
SKILL_PHRASES = [
    "python", "sql", "excel", "tableau", "power bi", "data analysis", "data analytics",
    "machine learning", "statistics", "communication", "project management",
    "pandas", "numpy", "scikit-learn", "visualization", "dashboards", "etl",
    "aws", "azure", "git", "linux", "cybersecurity"
]

def clean_text(text: str) -> str:
    text = text.lower()
    # replace non-letters/numbers with spaces
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    words = text.split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 2]

def phrase_counts(text: str, phrases):
    counts = {}
    for p in phrases:
        # match whole phrase boundaries loosely
        pattern = r"\b" + re.escape(p) + r"\b"
        counts[p] = len(re.findall(pattern, text))
    return counts

def main():
    print("\n=== Job Description Keyword Analyzer ===\n")
    print("Paste a job description below. When you're done, type END on a new line.\n")

    lines = []
    while True:
        line = input()
        if line.strip() == "END":
            break
        lines.append(line)

    raw_text = "\n".join(lines)
    if not raw_text.strip():
        print("\nNo text pasted. Exiting.\n")
        return

    cleaned = clean_text(raw_text)

    # word frequency
    tokens = tokenize(cleaned)
    word_freq = Counter(tokens)

    # phrase frequency
    skill_freq = phrase_counts(cleaned, SKILL_PHRASES)

    print("\nTop 20 keywords:\n")
    for word, count in word_freq.most_common(20):
        print(f"{word:20} {count}")

    print("\nSkill phrase matches:\n")
    for skill, count in sorted(skill_freq.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"{skill:20} {count}")

    # export to CSV
    out_file = "keyword_results.csv"
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["type", "keyword", "count"])
        for word, count in word_freq.most_common():
            writer.writerow(["word", word, count])
        for skill, count in skill_freq.items():
            writer.writerow(["skill_phrase", skill, count])

    print(f"\nSaved results to: {out_file}")
    print("You can open it with Excel/Google Sheets.\n")

if __name__ == "__main__":
    main()

