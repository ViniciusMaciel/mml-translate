import os
import json

# Caminho para o diretório onde estão os arquivos .txt
txt_directory = os.path.join(os.getcwd(), "txt")

def extract_original_content(content):
    """Procura a primeira tag iniciando com '<' e retorna o conteúdo a partir daí."""
    start_index = content.find('<')
    if start_index != -1:
        return content[start_index:].strip()
    return ""  # Retorna vazio se nenhuma tag for encontrada

def txt_to_json_custom(txt_directory):
    # Verifica se o diretório existe
    if not os.path.exists(txt_directory):
        print(f"O diretório especificado não existe: {txt_directory}")
        return

    # Lista todos os arquivos que terminam com _strings.txt
    txt_files = [f for f in os.listdir(txt_directory) if f.endswith("_strings.txt")]
    if not txt_files:
        print(f"Nenhum arquivo _strings.txt encontrado no diretório: {txt_directory}")
        return

    # Processa cada arquivo _strings.txt
    for txt_file in txt_files:
        # Extrai o nome base da BIN
        bin_name = os.path.splitext(txt_file)[0].replace("_strings", "") + ".BIN"
        txt_path = os.path.join(txt_directory, txt_file)
        json_path = os.path.join(txt_directory, bin_name.replace(".BIN", ".json"))
        
        try:
            # Lê o conteúdo do arquivo _strings.txt
            with open(txt_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Extrai o texto a partir da primeira tag '<'
            original_content = extract_original_content(content)

            # Cria a estrutura de dicionário no formato solicitado
            json_data = {
                "name": bin_name,
                "original": original_content,
                "new": original_content,  # Adiciona o mesmo conteúdo em "new"
            }

            # Salva o conteúdo no arquivo .json
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)

            print(f"Arquivo JSON gerado: {json_path}")
        except Exception as e:
            print(f"Erro ao processar o arquivo {txt_file}: {e}")

if __name__ == "__main__":
    txt_to_json_custom(txt_directory)
