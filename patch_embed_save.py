path = "embed.py"
src = open(path).read()
if "n_batches" in src:
    print("Patch pehle se laga hua hai.")
else:
    old = '''    for start in range(0, len(missing), BATCH):
        batch = missing[start:start + BATCH]
        for t, v in zip(batch, _call_ollama(batch)):
            _cache[_key(t)] = v
        _save()
'''
    new = '''    n_batches = (len(missing) + BATCH - 1) // BATCH
    for b, start in enumerate(range(0, len(missing), BATCH)):
        batch = missing[start:start + BATCH]
        for t, v in zip(batch, _call_ollama(batch)):
            _cache[_key(t)] = v
        if b % 10 == 9 or b == n_batches - 1:      # har 10 batch par aur aakhir me save
            _save()
'''
    if old not in src:
        print("embed.py ka format alag hai. Patch nahi lagaya.")
    else:
        open(path, "w").write(src.replace(old, new))
        print("Patch lag gaya.")
