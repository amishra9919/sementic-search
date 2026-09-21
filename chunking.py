def chunk_text(
        text,
        chunk_size=100,
        overlap=20
):
        words = text.split()

        chunks = []

        step = chunk_size - overlap

        for start in range(0, len(words), step):

                chunk_words = words[start:start + chunk_size]

                if not chunk_words:
                        break

                chunks.append(" ".join(chunk_words))

        return chunks