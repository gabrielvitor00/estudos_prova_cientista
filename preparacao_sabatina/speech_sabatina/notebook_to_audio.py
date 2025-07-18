import os
import nbformat
import asyncio
import edge_tts

# Caminho da pasta com os notebooks
notebooks_dir = os.path.dirname(os.path.abspath(__file__))

# Listar todos os arquivos .ipynb na pasta
notebooks = [f for f in os.listdir(notebooks_dir) if f.endswith('.ipynb')]




# Função assíncrona para converter texto em áudio usando edge-tts
async def notebook_to_audio():
    import string
    import re
    for nb_file in notebooks:
        nb_path = os.path.join(notebooks_dir, nb_file)
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
        # Extrair textos de todas as células markdown
        texts = []
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                texts.append(cell.source)
        # Concatenar todo o texto
        full_text = '\n'.join(texts)
        # Substituir vírgulas, pontos e quebras de linha por pausas para naturalidade
        text_pause = full_text
        text_pause = re.sub(r',', ' ...', text_pause)  # Pausa curta
        text_pause = re.sub(r'\.', ' ...', text_pause)  # Pausa média
        text_pause = re.sub(r'\n+', ' ...... ', text_pause)  # Pausa longa para parágrafos
        # Remover asteriscos e pontuações desnecessárias
        exclude = set(string.punctuation)
        exclude.update({'*', '’', '“', '”', '–', '—', '…'})
        exclude.discard(',')
        exclude.discard('.')
        table = str.maketrans('', '', ''.join(exclude))
        text_pause = text_pause.translate(table)
        # Nome do arquivo de áudio de saída
        audio_file = nb_file.replace('.ipynb', '.mp3')
        audio_path = os.path.join(notebooks_dir, audio_file)
        print(f'Gerando áudio para: {nb_file} -> {audio_file}')
        # Usar voz neural brasileira (ex: "pt-BR-AntonioNeural" ou "pt-BR-FranciscaNeural")
        communicate = edge_tts.Communicate(text_pause, voice="pt-BR-AntonioNeural")
        await communicate.save(audio_path)
    print('Conversão concluída!')

if __name__ == "__main__":
    asyncio.run(notebook_to_audio())
