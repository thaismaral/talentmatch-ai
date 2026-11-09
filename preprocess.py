import re

def limpar_texto(t: str) -> str:
    t = str(t).lower()
    t = re.sub(r"http\S+|www\S+", " ", t)
    t = re.sub(r"\S+@\S+", " ", t)
    t = re.sub(r"[^a-zA-ZÀ-ÿ\s+#.]", " ", t)
    return re.sub(r"\s+", " ", t).strip()
