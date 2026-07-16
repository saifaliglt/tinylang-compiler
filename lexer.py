"""PLY lexer for the TinyLang programming language.

The lexer converts raw source code into a stream of tokens. Tokens are the
smallest meaningful units of the language, such as identifiers, keywords,
operators, and numeric literals.
"""

from __future__ import annotations

import ply.lex as lex


lexical_error_count = 0


reserved = {
    "int": "INT_TYPE",
    "float": "FLOAT_TYPE",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "print": "PRINT",
}


tokens = [
    "ID",
    "INT_LITERAL",
    "FLOAT_LITERAL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "ASSIGN",
    "EQ",
    "NE",
    "LT",
    "GT",
    "LPAREN",
    "RPAREN",
    "LBRACE",
    "RBRACE",
    "SEMICOLON",
] + list(reserved.values())


t_PLUS = r"\+"
t_MINUS = r"-"
t_TIMES = r"\*"
t_DIVIDE = r"/"
t_EQ = r"=="
t_NE = r"!="
t_ASSIGN = r"="
t_LT = r"<"
t_GT = r">"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_SEMICOLON = r";"


t_ignore = " \t\r"


def t_FLOAT_LITERAL(token):
    r"(\d+\.\d*|\.\d+)"
    token.value = float(token.value)
    return token


def t_INT_LITERAL(token):
    r"\d+"
    token.value = int(token.value)
    return token


def t_ID(token):
    r"[A-Za-z_][A-Za-z0-9_]*"
    token.type = reserved.get(token.value, "ID")
    return token


def t_COMMENT(token):
    r"//.*"
    pass


def t_newline(token):
    r"\n+"
    token.lexer.lineno += len(token.value)


def t_error(token):
    """Report illegal characters and continue scanning."""
    global lexical_error_count
    lexical_error_count += 1
    token.lexer.error_count = getattr(token.lexer, "error_count", 0) + 1
    print(
        f"Lexical error: illegal character {token.value[0]!r} "
        f"at line {token.lexer.lineno}"
    )
    token.lexer.skip(1)


def build_lexer(**kwargs):
    """Create and return a fresh PLY lexer instance."""
    lexer_instance = lex.lex(**kwargs)
    lexer_instance.error_count = 0
    return lexer_instance


def reset_lexical_error_count() -> None:
    """Reset the module-level lexical error counter before a parse run."""
    global lexical_error_count
    lexical_error_count = 0


def get_lexical_error_count() -> int:
    """Expose lexical errors so main.py can halt before semantic analysis."""
    return lexical_error_count


lexer = build_lexer()
