from app import index, by_id

MIN_SCORE = 1.5
K = 3

# (sawal, sahi file) -- None ka matlab: docs me iska jawab hai hi nahi
TESTS = [
    ("How many vacation days do I get?", "leave_policy.txt"),
    ("How do I request time off?", "leave_policy.txt"),
    ("How many sick days are allowed?", "leave_policy.txt"),
    ("How long is parental leave for new parents?", "leave_policy.txt"),
    ("What is the deadline to submit receipts?", "expense_policy.txt"),
    ("How much can I spend on meals while traveling?", "expense_policy.txt"),
    ("Is alcohol reimbursed?", "expense_policy.txt"),
    ("Do I need approval for expensive flights?", "expense_policy.txt"),
    ("How often do engineers carry the pager?", "oncall_guide.txt"),
    ("What happens if I do not acknowledge an alert in 15 minutes?", "oncall_guide.txt"),
    ("When must a postmortem be written?", "oncall_guide.txt"),
    ("How often are API keys rotated?", "security_basics.txt"),
    ("What should I do if I lose my laptop?", "security_basics.txt"),
    ("Do I need two-factor authentication?", "security_basics.txt"),
    # mushkil sawal: alag shabd, wahi matlab
    ("Can I get reimbursed for beer?", "expense_policy.txt"),
    ("How long is maternity leave?", "leave_policy.txt"),
    ("What if my phone gets stolen?", "security_basics.txt"),
    # mushkil: sawal me docs wale shabd nahi hain
    ("How soon must I respond when my beeper goes off?", "oncall_guide.txt"),
    ("What is the maximum I can claim for dinner on a business trip?", "expense_policy.txt"),
    ("Where are secret credentials kept?", "security_basics.txt"),
    ("Can I get paid back for a plane ticket?", "expense_policy.txt"),
    ("What happens if nobody answers the alarm?", "oncall_guide.txt"),
    # jawab docs me hai hi nahi
    ("Who won the cricket world cup?", None),
    ("What is the CEO salary?", None),
    ("How many days of leave do contractors get?", None),
]


def retrieve_sources(question):
    results = index.search(question, k=K)
    return [by_id[cid]["source"] for cid, s in results if s >= MIN_SCORE]


answerable = [t for t in TESTS if t[1] is not None]
unanswerable = [t for t in TESTS if t[1] is None]

hits = 0
for q, expected in answerable:
    ok = expected in retrieve_sources(q)
    hits += ok
    if not ok:
        print(f"MISS  : {q}   (chahiye: {expected})")

refused = 0
for q, _ in unanswerable:
    got = retrieve_sources(q)
    ok = len(got) == 0
    refused += ok
    if not ok:
        print(f"BHATKA: {q}   (dhoondha: {sorted(set(got))})")

print()
print(f"Sahi file mili      : {hits}/{len(answerable)} = {100 * hits / len(answerable):.0f}%")
print(f"Sahi 'pata nahi'    : {refused}/{len(unanswerable)} = {100 * refused / len(unanswerable):.0f}%")
