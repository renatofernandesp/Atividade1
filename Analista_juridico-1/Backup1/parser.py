import json
import csv
import io

def parse_arquivo(conteudo_bytes: bytes, nome_arquivo: str) -> list[str]:
    ext = nome_arquivo.lower().split(".")[-1]
    conteudo = conteudo_bytes.decode("utf-8", errors="replace")

    if ext == "json":
        return _parse_json(conteudo)
    elif ext == "csv":
        return _parse_csv(conteudo)
    else:
        return _parse_txt(conteudo)

def _parse_json(conteudo: str) -> list[str]:
    data = json.loads(conteudo)
    textos = []
    if isinstance(data, list):
        for item in data:
            if isinstance(item, str):
                textos.append(item)
            elif isinstance(item, dict):
                # Concatena todos os valores string do objeto
                texto = " | ".join(str(v) for v in item.values() if v)
                textos.append(texto)
    elif isinstance(data, dict):
        texto = " | ".join(str(v) for v in data.values() if v)
        textos.append(texto)
    return [t for t in textos if t.strip()]

def _parse_csv(conteudo: str) -> list[str]:
    textos = []
    reader = csv.DictReader(io.StringIO(conteudo))
    for row in reader:
        texto = " | ".join(f"{k}: {v}" for k, v in row.items() if v and v.strip())
        if texto.strip():
            textos.append(texto)
    return textos

def _parse_txt(conteudo: str) -> list[str]:
    # Divide por linhas em branco (parágrafos) ou por linha
    blocos = [b.strip() for b in conteudo.split("\n\n") if b.strip()]
    if len(blocos) <= 1:
        blocos = [l.strip() for l in conteudo.splitlines() if l.strip()]
    return blocos
