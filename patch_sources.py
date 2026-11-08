path = "app.py"
src = open(path).read()

if "cited = sorted" in src:
    print("Fix pehle se laga hua hai.")
else:
    old_sources = '''    sources = [f'[{i + 1}] {c["source"]}' for i, c in enumerate(contexts)]
    return answer, sources'''
    new_sources = '''    # sirf wahi sources dikhao jinka number jawab me likha hai, jaise [1]
    cited = sorted({int(n) for n in re.findall(r"\\[(\\d+)\\]", answer) if 1 <= int(n) <= len(contexts)})
    if not cited:
        cited = list(range(1, len(contexts) + 1))
    sources = [f'[{n}] {contexts[n - 1]["source"]}' for n in cited]
    return answer, sources'''
    if old_sources not in src or not src.startswith("from loader import build_chunks"):
        print("app.py ka format alag hai. Patch nahi lagaya.")
    else:
        src = src.replace(old_sources, new_sources)
        src = "import re\n" + src
        open(path, "w").write(src)
        print("Fix lag gaya.")
