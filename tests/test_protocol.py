import pytest
from securechat.core.protocol import encode, parse, check_pseudo

def test_check_pseudo_valide_normal():
    # check_pseudo("fares") -> pas d’erreur
    assert check_pseudo("fares") is None

def test_check_pseudo_valide_longueur_max():
    # check_pseudo("x" * 20) -> pas d’erreur
    assert check_pseudo("x" * 20) is None

def test_check_pseudo_invalide_trop_long():
    # check_pseudo("x" * 21) -> ValueError
    with pytest.raises(ValueError, match="pseudo trop long"):
        check_pseudo("x" * 21)

def test_check_pseudo_invalide_vide():
    # check_pseudo("") -> ValueError
    with pytest.raises(ValueError, match="pseudo vide"):
        check_pseudo("")

def test_check_pseudo_invalide_espaces():
    # check_pseudo(" ") -> ValueError
    with pytest.raises(ValueError, match="pseudo vide"):
        check_pseudo(" ")

def test_check_pseudo_invalide_separateur():
    # check_pseudo("a|b") -> ValueError
    with pytest.raises(ValueError, match="\| dans le pseudo"):
        check_pseudo("a|b")

# --- TESTS DES CAS VALIDES ---

def test_parse_sans_retour_ligne():
    # parse(b"fares|Salut") (sans \n) → ("fares", "Salut")
    assert parse(b"fares|Salut") == ("fares", "Salut")


def test_parse_retour_ligne_windows():
    # parse(b"fares|Salut\r\n") → ("fares", "Salut")
    assert parse(b"fares|Salut\r\n") == ("fares", "Salut")


def test_parse_plusieurs_pipes():
    # parse(b"fares|a|b\n") → ("fares", "a|b")
    assert parse(b"fares|a|b\n") == ("fares", "a|b")


def test_parse_caracteres_accentues():
    # parse("é|ça va ?\n".encode()) → ("é", "ça va ?")
    assert parse("é|ça va ?\n".encode("utf-8")) == ("é", "ça va ?")


def test_encode_limite_exacte_vingt_caracteres():
    # Limite : encode("x" * 20, "Salut") valide
    # On vérifie que cela retourne bien les bytes attendus sans lever d'erreur
    assert encode("x" * 20, "Salut") == b"x" * 20 + b"|Salut\n"


# --- TESTS DES CAS INVALIDES (Avec pytest.raises) ---

def test_parse_sans_separateur_invalide():
    # parse(b"Salut\n") → ValueError
    with pytest.raises(ValueError):
        parse(b"Salut\n")


def test_encode_pseudo_vide_invalide():
    # encode("", "Salut") → ValueError
    with pytest.raises(ValueError):
        encode("", "Salut")


def test_encode_texte_espace_invalide():
    # encode("fares", " ") → ValueError
    with pytest.raises(ValueError):
        encode("fares", " ")


def test_parse_texte_espace_invalide():
    # parse(b"fares| \n") → ValueError
    with pytest.raises(ValueError):
        parse(b"fares| \n")


def test_parse_pseudo_vingt_et_un_caracteres_invalide():
    # parse d’un pseudo de 21 caractères → ValueError
    # On crée une ligne valide syntaxiquement (avec |) mais dont le pseudo fait 21 caractères
    ligne_invalide = b"x" * 21 + b"|Salut\n"
    with pytest.raises(ValueError):
        parse(ligne_invalide)
