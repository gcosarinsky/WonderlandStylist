import nltk
import time


def chunk_with_nltk(file_path, target_sentences=5):
    with open(file_path, 'r', encoding='cp1252') as f:
        lines = f.readlines()
    text = "".join(lines[29:]) # Saltamos las primeras 29 líneas 
    # Divide el texto en una lista de oraciones
    sentences = nltk.tokenize.sent_tokenize(text, language='spanish')
    
    # Filtramos y agrupamos
    sentences = [s.replace('\n', ' ').strip() for s in sentences if len(s) > 20]
    
    return [" ".join(sentences[i:i+target_sentences]) 
            for i in range(0, len(sentences), target_sentences)]


if __name__ == "__main__":
    nltk.download('punkt')
    nltk.download('punkt_tab')
    filename = r'raw\\Carroll, Lewis - Alicia En El País De Las Maravillas.txt'
    print("Chunking the file:", filename)
    start = time.perf_counter()
    chunks = chunk_with_nltk(filename, target_sentences=3)
    elapsed = time.perf_counter() - start
    print(f"Tiempo de chunking: {elapsed:.3f} s")
    print(f"Total de chunks creados: {len(chunks)}")
    # Imprime los primeros 3 chunks como ejemplo
    for i, chunk in enumerate(chunks[:5]):
        print(f"--- Chunk {i+1} ---\n{chunk}\n")
    # guardar los chunks en un archivo
    with open('chunks_nltk.txt', 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(chunk + '\n\n') # separa los chunks con una línea en blanco
    print(f"Chunks guardados en 'chunks_nltk.txt'")