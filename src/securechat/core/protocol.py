def max_twenty_c(pseudo: str) -> bool:
    return len(pseudo) > 20

def bar_in_pseudo(pseudo: str) -> bool:
    return "|" in pseudo

def is_empty(line: str):
    return line.strip() == ""

def encode(pseudo: str, text: str) -> bytes:

    if max_twenty_c(pseudo):
        raise ValueError("pseudo trop long")        
    if bar_in_pseudo(pseudo):
        raise ValueError("| dans le pseudo")
    if is_empty(pseudo):
        raise ValueError("pseudo vide")
    if is_empty(text):
        raise ValueError("texte vide")

    ligne = f"{pseudo}|{text}\n"
    return ligne.encode('utf-8')
        

def parse(line: bytes) -> tuple[str, str]:  

    p = line.strip().decode('utf-8').split("|", 1)

    if len(p) != 2:
        raise ValueError("pas de séparateur |")     
    if max_twenty_c(p[0]):
        raise ValueError("pseudo trop long") 
    if bar_in_pseudo(p[0]):
        raise ValueError("| dans le pseudo")
    if is_empty(p[0]):
        raise ValueError("pseudo vide")
    if is_empty(p[1]):
        raise ValueError("texte vide")

    return tuple(p)