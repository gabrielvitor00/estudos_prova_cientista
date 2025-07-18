import os

# Caminho da pasta onde estão os arquivos .mp3
folder = os.path.dirname(os.path.abspath(__file__))

# Listar e apagar todos os arquivos .mp3
for file in os.listdir(folder):
    if file.endswith('.mp3'):
        file_path = os.path.join(folder, file)
        print(f'Removendo: {file}')
        os.remove(file_path)

print('Todos os arquivos .mp3 foram removidos!')
