import os
import shutil

# Caminho para a pasta onde estão os arquivos .bin
directory = r"C:\Users\vinic\Downloads\Megaman\DAT"

# Lista de arquivos que serão ignorados
exclude_files = [
    "ST01.BIN",
    "ST02_00.BIN", "ST02_01.BIN", "ST02_02.BIN", "ST02.BIN",
    "ST03B.BIN", "ST03.BIN",
    "ST04B.BIN", "ST04.BIN",
    "ST05_01C.BIN", "ST05.BIN",
    "ST06_02C.BIN", "ST06_03.BIN", "ST06.BIN",
    "ST07_00.BIN", "ST07_05B.BIN", "ST07_05.BIN", "ST07.BIN",
    "ST08.BIN",
    "ST09_02.BIN", "ST09.BIN",
    "ST0A.BIN",
    "ST0B_00D.BIN", "ST0B_00E.BIN", "ST0B_01B.BIN", "ST0B_01.BIN", "ST0B.BIN",
    "ST0D_02.BIN", "ST0D_03.BIN", "ST0D.BIN",
    "ST0F.BIN",
    "ST10B.BIN", "ST10.BIN",
    "ST11B.BIN", "ST11.BIN",
    "ST12.BIN",
    "ST13.BIN",
    "ST15_00.BIN", "ST15.BIN",
    "ST16_00B.BIN", "ST16_00.BIN", "ST16.BIN",
    "ST17B.BIN", "ST17C.BIN",
    "ST18_00.BIN", "ST18.BIN",
    "ST19B.BIN", "ST19C.BIN", "ST19_00.BIN",
    "ST1A.BIN",
    "ST1B.BIN",
    "ST1D_00.BIN",
    "ST00.BIN",
    "ST00_04.BIN",
    "ST00_03.BIN",
    "ST00_00.BIN",
    "ST1D_01.BIN",
    "ST1D_02.BIN",
    "ST1E_06.BIN",
    "ST1E.BIN"
]


# Tabela de tradução fornecida
base_table = {
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
}
patterns = [
    (b'\xa0\x1E\x00\x9b\x83\x00', '<END>'),
    (b'\xa0\x14\x00', '<PAUSE>'),
    (b'\x87\x06\x00', '<SHORTPAUSE>'),
    (b'\x9b\x83\x04\x00\xbb\x00\xe4\x00\x00', '<END2>'),
    (b'\x9b\x83\x04\x00', '<NEXT>'),
    (b'\x88\x52\x00\x30\x00\x0D\x03\x8f\x00\x08\x86\x00\x00', '<BLUE>'),
    (b'\xe9\x92\x01\x11\xe9', '<YoN>'),
    (b'\x9c\x20\x00\x92\x01\x00\xe9', '<Yes>'),
    (b'\x86\x01\x00\x93\x80', '<NO>'),
    (b'\x00\x80\xFF\x88\x40\x00\x24\x00\x10\x03\x8F\x00', '<DIALOG>'),
    (b'\x88\x40\x00\xA2\x00\x10\x03\x8F\x00\x08\x4E', '<DIALOG2>')
]

def adjust_table(base_table, new_e_position=0x33):
    adjusted_table = {}
    for key, value in base_table.items():
        if 'e' in value:
            offset = new_e_position - key
            break
    for key, value in base_table.items():
        adjusted_key = key + offset
        if 0 <= adjusted_key <= 255:
            adjusted_table[adjusted_key] = value
    return adjusted_table

def translate_bytes(data, table):
    result = []
    i = 0
    while i < len(data):
        matched = False
        for pattern, tag in patterns:
            if data[i:i + len(pattern)] == pattern:
                result.append(tag)
                i += len(pattern)
                matched = True
                break
        if matched:
            continue

        if i + 7 < len(data) and data[i:i+2] == b'\x8f\x00' and data[i + 2] in (0x00, 0x08) and data[i + 3] == 0x8B and data[i + 5:i + 8] == b'\x00\x00\x00':
            hex_value = f"0x{data[i + 4]:02X}"
            if data[i + 2] == 0x08:
                result.append(f'<MSG.8.{hex_value}>')
            elif data[i + 2] == 0x00:
                result.append(f'<MSG.0.{hex_value}>')
            i += 8
        else:
            char = table.get(data[i], f"[{hex(data[i])}]")
            result.append(char)
            i += 1

    return ''.join(result)

def refind(txt_directory):
    not_found_directory = os.path.join(txt_directory, "not_found")
    os.makedirs(not_found_directory, exist_ok=True)
    
    for txt_file in os.listdir(txt_directory):
        if txt_file.endswith(".txt"):
            txt_path = os.path.join(txt_directory, txt_file)
            with open(txt_path, "r", encoding="utf-8") as file:
                content = file.read()
            # Verificar se o conteúdo contém as tags desejadas
            if not any(tag in content for tag in ("<END>", "<NEXT>", "<MSG.")):
                print(f"Movendo {txt_file} para a pasta 'not_found'")
                shutil.move(txt_path, os.path.join(not_found_directory, txt_file))

def process_files_in_directory(directory):
    if not os.path.exists(directory):
        print(f"O diretório especificado não existe: {directory}")
        return

    # Listar todos os arquivos que começam com ST e terminam em .BIN
    files = [f for f in os.listdir(directory) if f.startswith("ST") and f.endswith(".BIN")]
    if not files:
        print(f"Nenhum arquivo STXXX.BIN encontrado no diretório: {directory}")
        return

    # Ordenar para garantir que ST00.BIN seja processado primeiro
    files = sorted(files)
    
    adjusted_table = adjust_table(base_table, new_e_position=0x33)

    txt_directory = directory  # Diretório onde os arquivos .txt serão salvos
    for file in files:
        # Ignorar arquivos na lista de exclusão
        if file in exclude_files:
            print(f"Ignorando arquivo: {file}")
            continue

        file_path = os.path.join(directory, file)
        print(f"Processando arquivo: {file_path}")

        try:
            with open(file_path, "rb") as f:
                data = f.read()
                translated_text = translate_bytes(data, adjusted_table)
                strings = [s for s in translated_text.split('\0') if len(s) > 3]
                if strings:
                    output_file = os.path.join(txt_directory, f"{os.path.splitext(file)[0]}_strings.txt")
                    with open(output_file, "w", encoding="utf-8") as out_file:
                        out_file.write("\n".join(strings))
                    print(f"Strings encontradas e salvas em: {output_file}")
                else:
                    print(f"Nenhuma string legível encontrada no arquivo: {file}")
        except Exception as e:
            print(f"Erro ao processar o arquivo {file}: {e}")
    
    # Chamar refind para verificar os arquivos gerados
    refind(txt_directory)

if __name__ == "__main__":
    process_files_in_directory(directory)
