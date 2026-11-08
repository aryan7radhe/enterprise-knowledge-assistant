import os
import re


def split_front_matter(raw):
    """Hugo markdown ke upar jo metadata block hota hai (--- ... ---) usse title nikalo aur hata do.
    Return: (title, baaki_text)"""
    for pattern in (r"^\s*---\s*\n(.*?)\n---\s*(?:\n|$)", r"^\s*\+\+\+\s*\n(.*?)\n\+\+\+\s*(?:\n|$)"):
        m = re.match(pattern, raw, re.S)
        if m:
            meta, body = m.group(1), raw[m.end():]
            t = re.search(r'^title\s*[:=]\s*["\']?(.*?)["\']?\s*$', meta, re.M)
            return (t.group(1).strip() if t else ""), body
    return "", raw


def clean_markdown(text):
    """Kachra saaf karo: shortcodes, HTML comments, images, links ka URL."""
    text = re.sub(r"\{\{[<%].*?[>%]\}\}", " ", text, flags=re.S)   # {{< shortcode >}}
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)            # <!-- comment -->
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", text)              # ![image](url)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)           # [text](url) -> text
    return text


def load_documents(folder="docs"):
    """Folder (aur uske andar ke saare folders) ki .txt/.md files padho.
    Return: [(file_ka_path, text), ...]"""
    docs = []
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        for name in sorted(files):
            if name.endswith(".txt") or name.endswith(".md"):
                path = os.path.join(root, name)
                with open(path, encoding="utf-8", errors="ignore") as f:
                    docs.append((os.path.relpath(path, folder), f.read()))
    return docs


def chunk_text(text, size=40, overlap=10):
    """Lambe text ko chhote tukdo (chunks) me todo.
    Har tukda 'size' shabd ka, aur agle tukde me pichle ke 'overlap' shabd dobara aate hain."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        chunks.append(" ".join(words[start:start + size]))
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks


def build_chunks(folder="docs", size=40, overlap=10, min_words=0):
    """Har chunk ki parchi: id, source (file ka path), dept (pehla folder), title, text."""
    all_chunks = []
    for path, raw in load_documents(folder):
        title, body = split_front_matter(raw)
        body = clean_markdown(body)
        if len(body.split()) < min_words:
            continue                                   # bahut chhoti/khaali file chhod do
        parts = path.split(os.sep)
        dept = parts[0] if len(parts) > 1 else ""
        for i, piece in enumerate(chunk_text(body, size, overlap)):
            text = f"{title}\n{piece}" if title else piece
            all_chunks.append({"id": f"{path}#{i}", "source": path, "dept": dept, "title": title, "text": text})
    return all_chunks
