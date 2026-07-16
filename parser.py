"""PLY parser for TinyLang.

The parser recognizes TinyLang's context-free grammar and constructs an
Abstract Syntax Tree (AST). Semantic checks, such as type compatibility and
undeclared-variable detection, are intentionally left for later project phases.
"""

from __future__ import annotations

import ply.yacc as yacc

from ast_nodes import Assign, BinOp, Identifier, If, Number, Print, Program, VarDecl, While
from lexer import build_lexer, tokens


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
    p[0] = Program(p[1])


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
    p[0] = VarDecl(p[1], p[2])


def p_var_decl_with_initializer(p):
    """var_decl : type_specifier ID ASSIGN expression SEMICOLON"""
    p[0] = VarDecl(p[1], p[2], p[4])


def p_type_specifier(p):
    """type_specifier : INT_TYPE
                      | FLOAT_TYPE"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : ID ASSIGN expression SEMICOLON"""
    p[0] = Assign(p[1], p[3])


def p_if_statement_without_else(p):
    """if_statement : IF LPAREN expression RPAREN block %prec IFX"""
    p[0] = If(p[3], p[5])


def p_if_statement_with_else(p):
    """if_statement : IF LPAREN expression RPAREN block ELSE block"""
    p[0] = If(p[3], p[5], p[7])


def p_while_statement(p):
    """while_statement : WHILE LPAREN expression RPAREN block"""
    p[0] = While(p[3], p[5])


def p_print_statement(p):
    """print_statement : PRINT LPAREN expression RPAREN SEMICOLON"""
    p[0] = Print(p[3])


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
    p[0] = BinOp(p[2], p[1], p[3])


def p_expression_grouped(p):
    """expression : LPAREN expression RPAREN"""
    p[0] = p[2]


def p_expression_number(p):
    """expression : INT_LITERAL
                  | FLOAT_LITERAL"""
    p[0] = Number(p[1])


def p_expression_identifier(p):
    """expression : ID"""
    p[0] = Identifier(p[1])


def p_error(p):
    """Handle syntax errors without exposing a Python traceback."""
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
    return parser.parse(source_code, lexer=build_lexer())
