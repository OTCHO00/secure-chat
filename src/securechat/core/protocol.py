def check_pseudo(pseudo: str) -> None:

    if len(pseudo) > 20:
        raise ValueError("pseudo trop long")
    if "|" in pseudo:
        raise ValueError("| dans le pseudo")
    if pseudo.strip() == "":
        raise ValueError("pseudo vide")

def check_text(text: str) -> None:

    if len(text.strip()) == 0:
        raise ValueError("texte vide")
    
def encode(pseudo: str, text: str) -> bytes:

    check_pseudo(pseudo)
    check_text(text)

    ligne = f"{pseudo}|{text}\n"
    return ligne.encode('utf-8')
    
def parse(line: bytes) -> tuple[str, str]:  

    p = line.strip().decode('utf-8').split("|", 1)

    if len(p) != 2:
        raise ValueError("pas de séparateur |")     
    
    check_text(p[1])
    check_pseudo(p[0])

    return tuple(p)