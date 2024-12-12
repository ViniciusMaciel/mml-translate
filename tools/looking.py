import os

# Caminho para a pasta onde estão os arquivos .bin
directory = r"C:\Users\vinic\Downloads\Megaman\DAT"

# Calcula a diferença entre os caracteres consecutivos da string alvo
def calculate_char_differences(target_phrase):
    return [ord(target_phrase[i+1]) - ord(target_phrase[i]) for i in range(len(target_phrase) - 1)]

# Busca pela frase calculando as diferenças entre os caracteres consecutivos
def search_phrase_by_difference(directory, target_phrase="eaverbots"):
    if not os.path.exists(directory):
        print(f"O diretório especificado não existe: {directory}")
        return

    # Calcula a diferença de valores dos caracteres da frase-alvo
    target_differences = calculate_char_differences(target_phrase)
    print(f"Diferenças entre caracteres de '{target_phrase}': {target_differences}")
    
    found_any = False  # Variável para indicar se a frase foi encontrada em algum arquivo

    for root, _, files in os.walk(directory):
        for file in files:
            if file.startswith("ST") and file.endswith(".BIN"):  # Apenas arquivos ST*.BIN
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                        # Percorre os bytes e verifica as diferenças
                        for i in range(len(data) - len(target_differences)):
                            differences = [
                                data[i + j + 1] - data[i + j]
                                for j in range(len(target_differences))
                            ]
                            if differences == target_differences:
                                found_any = True
                                print(f"\nA frase '{target_phrase}' foi encontrada no arquivo: {file_path}")
                                print(f"Posição inicial do 'e' (hexadecimal): {hex(i)}")
                                print(f"Valores hexadecimais encontrados: {[hex(data[i + k]) for k in range(len(target_phrase))]}")
                except Exception as e:
                    print(f"Erro ao processar o arquivo {file_path}: {e}")

    if not found_any:
        print(f"\nA frase '{target_phrase}' não foi encontrada em nenhum arquivo ST*.BIN no diretório: {directory}")

# Chamada principal
if __name__ == "__main__":
    search_phrase_by_difference(directory, target_phrase="looking")
