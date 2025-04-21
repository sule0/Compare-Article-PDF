# embeddings/embedding_generator.py
import re
def metni_paragraflara_bol(metin):
    paragraflar = [p.strip() for p in metin.split("\n") if len(p.strip()) > 30]
    return paragraflar

def paragraflari_embed_et(model, paragraflar):
    embeddings = model.encode(paragraflar, convert_to_tensor=True)
    return embeddings
def bol_maddelere_ayir(metin):
    """
    Word dosyasındaki maddeleri (1. 2. 3. ...) tespit edip ayırır.
    """
    bolumler = re.split(r'(?=\n?\d+\.\s)', metin)
    return [b.strip() for b in bolumler if len(b.strip()) > 30]