from langchain.text_splitter import RecursiveCharacterTextSplitter


def generate_chunks(texto: str): #colocar tipo de retorno
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,       # tamanho do chunk (em caracteres)
        chunk_overlap=50,     # sobreposição entre chunks
        separators=["\n\n", "\n", ".", " ", ""]  # tentará quebrar nessa ordem
    )

    chunks = splitter.split_text(texto)

    return chunks