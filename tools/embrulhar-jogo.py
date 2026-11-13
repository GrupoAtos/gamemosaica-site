#!/usr/bin/env python3
"""Copia o jogo (mosaica.html do Artifact, sem esqueleto) para jogar/index.html.
Uso: python3 tools/embrulhar-jogo.py /mnt/project-files/mosaica/mosaica.html
Só acrescenta doctype/meta e troca o Google Fonts pelas fontes locais; não altera o jogo."""
import sys, os, re
src = open(sys.argv[1], encoding="utf-8").read()
src2 = re.sub(r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\s*<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">',
              '<link rel="stylesheet" href="/fonts/fonts.css">', src, count=1)
assert src2 != src, "link do Google Fonts não encontrado"
assert "googleapis" not in src2
head = '''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#14163a">
<meta name="description" content="Jogue Mosaica no navegador: estratégia por turnos em ilhas, 12 clãs, 32 turnos.">
<link rel="icon" href="/img/favicon.png">
<link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
'''
out = os.path.join(os.path.dirname(__file__), "..", "jogar", "index.html")
open(out, "w", encoding="utf-8").write(head + src2 + "\n</html>\n")
print("ok", len(src2))
