path = "eval.py"
src = open(path).read()
marker = "    # jawab docs me hai hi nahi\n"
new = '''    # mushkil: sawal me docs wale shabd nahi hain
    ("How soon must I respond when my beeper goes off?", "oncall_guide.txt"),
    ("What is the maximum I can claim for dinner on a business trip?", "expense_policy.txt"),
    ("Where are secret credentials kept?", "security_basics.txt"),
    ("Can I get paid back for a plane ticket?", "expense_policy.txt"),
    ("What happens if nobody answers the alarm?", "oncall_guide.txt"),
'''
if "mushkil: sawal me docs wale shabd nahi hain" in src:
    print("Mushkil sawal pehle se jude hain.")
elif marker not in src:
    print("Marker nahi mila. eval.py me '# jawab docs me hai hi nahi' wali line check karo.")
else:
    open(path, "w").write(src.replace(marker, new + marker))
    print("5 mushkil sawal jud gaye.")
