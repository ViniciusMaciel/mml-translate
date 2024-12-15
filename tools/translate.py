import os
import json

# Caminho para a pasta onde estão os arquivos .BIN e JSON
base_directory = r"C:\Megaman\mml-renew\RAW\DAT"
json_directory = os.path.join(os.getcwd(), "txt")

# Tabela base de tradução invertida para converter caracteres e tags em hexadecimal
reverse_base_table = {v: k for k, v in {
    0x01: '1', 0x02: '2', 0x03: '3', 0x04: '4', 0x05: '5', 0x06: '6', 0x07: '7',
    0x08: '8', 0x09: '9', 0x0A: ' ', 0x0B: ',', 0x0C: '0',  0x0E: '?',
    0x10: '.', 0x13: ':', 0x15: 'A', 0x16: 'B', 0x17: 'C', 0x18: 'D', 0x19: 'E',
    0x1A: 'F', 0x1B: 'G', 0x1C: 'H', 0x1D: 'I', 0x1E: 'J', 0x1F: 'K', 0x20: 'L',
    0x21: 'M', 0x22: 'N', 0x23: 'O', 0x24: 'P', 0x25: 'Q', 0x26: 'R', 0x27: 'S',
    0x28: 'T', 0x29: 'U', 0x2A: 'V', 0x2B: 'W', 0x2C: 'X', 0x2D: 'Y', 0x2E: 'Z',
    0x2F: 'a', 0x30: 'b', 0x31: 'c', 0x32: 'd', 0x33: 'e', 0x34: 'f', 0x35: 'g',
    0x36: 'h', 0x37: 'i', 0x38: 'j', 0x39: 'k', 0x3A: 'l', 0x3B: 'm', 0x3C: 'n',
    0x3D: 'o', 0x3E: 'p', 0x3F: 'q', 0x40: 'r', 0x41: 's', 0x42: 't', 0x43: 'u',
    0x44: 'v', 0x45: 'w', 0x46: 'x', 0x47: 'y', 0x48: 'z', 0x4D: "'", 0x82: "\n",
    0x50: "-", 0x4E: '"', 0x0D: "!"
}.items()}

# Tabela de padrões para as tags
tags_table = {
    "<END>": b'\xa0\x1E\x00\x9b\x83\x00',
    "<NEXT>": b'\x9b\x83\x04\x00',
    "<MSG.8.": lambda x: b'\x8f\x00\x08\x8B' + bytes([int(x, 16)]) + b'\x00\x00\x00',
    "<MSG.0.": lambda x: b'\x8f\x00\x00\x8B' + bytes([int(x, 16)]) + b'\x00\x00\x00',
    "<BLUE>": b'\x88\x52\x00\x30\x00\x0D\x03\x8f\x00\x08\x86\x00\x00',
    "<YoN>": b'\xe9\x92\x01\x11\xe9',
    "<Yes>": b'\x9c\x20\x00\x92\x01\x00\xe9',
    "<NO>": b'\x86\x01\x00\x93\x80',
    "<DIALOG>": b'\x00\x80\xFF\x88\x40\x00\x24\x00\x10\x03\x8F\x00',
    "<DIALOG2>": b'\x88\x40\x00\xA2\x00\x10\x03\x8F\x00\x08\x4E',
}

# Função para converter texto em hexadecimal
def text_to_hexadecimal(text, reverse_table, tags_table):
    hex_values = bytearray()
    i = 0
    while i < len(text):
        if text[i] == "<":
            end_tag_index = text.find(">", i)
            if end_tag_index != -1:
                tag = text[i:end_tag_index + 1]
                if tag.startswith("<MSG.8.") or tag.startswith("<MSG.0."):
                    prefix, hex_value = tag[0:7], tag[7:-1]
                    if prefix in tags_table:
                        hex_values.extend(tags_table[prefix](hex_value))
                        i = end_tag_index + 1
                        continue
                elif tag in tags_table:
                    hex_values.extend(tags_table[tag])
                    i = end_tag_index + 1
                    continue
                else:
                    raise ValueError(f"Tag não reconhecida: {tag}")
        elif text[i] == "[":
            end_bracket_index = text.find("]", i)
            if end_bracket_index != -1:
                hex_value = text[i + 1:end_bracket_index]
                if hex_value.startswith("0x"):
                    hex_values.append(int(hex_value, 16))
                    i = end_bracket_index + 1
                    continue
                else:
                    raise ValueError(f"Formato hexadecimal inválido: {hex_value}")
        if text[i] in reverse_table:
            hex_values.append(reverse_table[text[i]])
        else:
            raise ValueError(f"Caractere não mapeado: {text[i]}")
        i += 1

    return hex_values

# Função para processar o JSON e substituir o conteúdo no arquivo BIN
def process_json_and_bin(json_directory, base_directory):
    json_file = os.path.join(json_directory, "ST00_01.json")
    
    if not os.path.exists(json_file):
        print(f"Arquivo JSON não encontrado: {json_file}")
        return

    try:
        with open(json_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        bin_name = data.get("name", "").strip()
        original_content = data.get("original", "")
        new_content = data.get("new", "")

        if not bin_name or not original_content or not new_content:
            print("JSON não possui os campos 'name', 'original' ou 'new' válidos.")
            return

        bin_path = os.path.join(base_directory, bin_name)
        if not os.path.exists(bin_path):
            print(f"Arquivo BIN não encontrado: {bin_path}")
            return

        # Converte o conteúdo 'original' para hexadecimal
        original_hex = text_to_hexadecimal(original_content, reverse_base_table, tags_table)
        # Converte o conteúdo 'new' para hexadecimal
        new_hex = text_to_hexadecimal(new_content, reverse_base_table, tags_table)

        # Lê o conteúdo do arquivo BIN
        with open(bin_path, "rb") as bin_file:
            bin_data = bytearray(bin_file.read())

        # Procura a sequência hexadecimal no arquivo BIN
        position = bin_data.find(original_hex)
        if position != -1:
            print(f"found at position {position}")
            # Substitui o conteúdo original pelo novo no arquivo BIN
            bin_data[position:position + len(original_hex)] = new_hex
            # Salva as alterações no arquivo BIN
            with open(bin_path, "wb") as bin_file:
                bin_file.write(bin_data)
            print("Conteúdo substituído com sucesso.")
        else:
            print("not found")
    except Exception as e:
        print(f"Erro ao processar: {e}")

if __name__ == "__main__":
    process_json_and_bin(json_directory, base_directory)
