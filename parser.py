"""PLY parser for TinyLang.

The parser recognizes TinyLang's context-free grammar and constructs an
Abstract Syntax Tree (AST). Semantic checks, such as type compatibility and
undeclared-variable detection, are intentionally left for later project phases.
"""

from __future__ import annotations

import ply.yacc as yacc

from ast_nodes import Assign, BinOp, Identifier, If, Number, Print, Program, VarDecl, While
from lexer import build_lexer, reset_lexical_error_count, tokens


syntax_error_count = 0


# Precedence is listed from lowest to highest. The artificial IFX precedence
# gives an if-without-else lower precedence than ELSE, which resolves the
# classic dangling-else ambiguity by attaching else to the nearest if.
precedence = (
    ("nonassoc", "IFX"),
    ("nonassoc", "ELSE"),
    ("nonassoc", "EQ", "NE", "LT", "GT"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
)


def p_program(p):
    """program : statement_list"""
    first_line = p[1][0].line if p[1] else 1
    p[0] = Program(p[1], line=first_line)


def p_statement_list_multiple(p):
    """statement_list : statement_list statement"""
    p[0] = p[1] + [p[2]]


def p_statement_list_single(p):
    """statement_list : statement"""
    p[0] = [p[1]]


def p_statement(p):
    """statement : var_decl
                 | assignment
                 | if_statement
                 | while_statement
                 | print_statement"""
    p[0] = p[1]


def p_var_decl_without_initializer(p):
    """var_decl : type_specifier ID SEMICOLON"""
    var_type, line = p[1]
    p[0] = VarDecl(var_type, p[2], line=line)


def p_var_decl_with_initializer(p):
    """var_decl : type_specifier ID ASSIGN expression SEMICOLON"""
    var_type, line = p[1]
    p[0] = VarDecl(var_type, p[2], p[4], line=line)


def p_type_specifier(p):
    """type_specifier : INT_TYPE
                      | FLOAT_TYPE"""
    # Preserve the original keyword line through this nonterminal.
    p[0] = (p[1], p.lineno(1))


def p_assignment(p):
    """assignment : ID ASSIGN expression SEMICOLON"""
    p[0] = Assign(p[1], p[3], line=p.lineno(1))


def p_if_statement_without_else(p):
    """if_statement : IF LPAREN expression RPAREN block %prec IFX"""
    p[0] = If(p[3], p[5], line=p.lineno(1))


def p_if_statement_with_else(p):
    """if_statement : IF LPAREN expression RPAREN block ELSE block"""
    p[0] = If(p[3], p[5], p[7], line=p.lineno(1))


def p_while_statement(p):
    """while_statement : WHILE LPAREN expression RPAREN block"""
    p[0] = While(p[3], p[5], line=p.lineno(1))


def p_print_statement(p):
    """print_statement : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = Print(p[3], line=p.lineno(1))


def p_block(p):
    """block : LBRACE statement_list RBRACE"""
    p[0] = p[2]


def p_expression_binary(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NE expression
                  | expression LT expression
                  | expression GT expression"""
    # The operator token line is the most precise location for expression
    # type errors such as invalid operands.
    p[0] = BinOp(p[2], p[1], p[3], line=p.lineno(2))


def p_expression_grouped(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : INT_LITERAL
                  | FLOAT_LITERAL"""
    p[0] = Number(p[1], line=p.lineno(1))


def p_expression_identifier(p):
    """expression : ID"""
    p[0] = Identifier(p[1], line=p.lineno(1))


def p_error(p):
    """Handle syntax errors without exposing a Python traceback."""
    global syntax_error_count
    syntax_error_count += 1
    if p is None:
        print("Syntax error: unexpected end of input.")
        return

    print(
        f"Syntax error: unexpected token {p.type}({p.value!r}) "
        f"at line {p.lineno}."
    )


parser = yacc.yacc(debug=False, write_tables=False)


def parse(source_code: str):
    """Parse source code and return the root Program node."""
    global syntax_error_count
    syntax_error_count = 0
    reset_lexical_error_count()
    return parser.parse(source_code, lexer=build_lexer())


def get_syntax_error_count() -> int:
    """Expose syntax errors so main.py can halt before semantic analysis."""
    return syntax_error_count
