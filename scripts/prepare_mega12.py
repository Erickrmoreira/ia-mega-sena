import re
import csv

# Cole seus dados brutos da Mega Sena aqui como string
dados_brutos = """
20/12/2025	
1
9
37
39
42
44
18/12/2025	
5
10
24
25
47
54
16/12/2025
1
20
45
48
51
58
"""  # ... cole todo o restante aqui

# Regex para encontrar datas e números
padrão = r'(\d{2}/\d{2}/\d{4})\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)'
matches = re.findall(padrão, dados_brutos, re.MULTILINE)

# Escreve CSV
with open("mega_12_meses.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Data","N1","N2","N3","N4","N5","N6"])
    for m in matches:
        # Converte data para YYYY/MM/DD
        dia, mes, ano = m[0].split('/')
        data_formatada = f"{ano}/{mes}/{dia}"
        numeros = m[1:]
        writer.writerow([data_formatada] + list(numeros))

print("CSV gerado com sucesso!")
