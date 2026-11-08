import os
import shutil

DROP_SOURCES = {
    "hiring/_index.md",
    "finance/growth-and-development/_index.md",
    "finance/financial-planning-and-analysis/gtm-analytics-hub.md",
    "leadership/emotional-intelligence/psychological-safety.md",
    "hiring/interviewing/technical.md",
    "people-group/general-onboarding/_index.md",
    "people-group/people-ops-tech-analytics/_index.md",
    "people-policies/india-ltd/india-sexual-harassment-policy.md",
}

if not os.path.exists("testset_raw.tsv"):
    shutil.copy("testset.tsv", "testset_raw.tsv")

with open("testset.tsv", encoding="utf-8") as f:
    rows = [line.rstrip("\n").split("\t") for line in f if "\t" in line]

final, seen, dropped = [], set(), 0
for q, s in rows:
    if s in DROP_SOURCES or "/readmes/" in s or q.lower() in seen:
        dropped += 1
        continue
    seen.add(q.lower())
    final.append((q, s))

with open("testset.tsv", "w", encoding="utf-8") as f:
    for q, s in final:
        f.write(f"{q}\t{s}\n")
print(f"{len(rows)} me se {dropped} hataye, {len(final)} sawal bache. (Asli list testset_raw.tsv me safe hai)")
