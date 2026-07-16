"""Semantic analysis for TinyLang.

This phase walks the AST after parsing and checks meaning-oriented rules that
the grammar alone cannot enforce, such as declaration-before-use and assignment
type compatibility.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from ast_nodes import Assign, BinOp, Identifier, If, Number, Print, Program, VarDecl, While


ARITHMETIC_OPERATORS = {"+", "-", "*", "/"}
COMPARISON_OPERATORS = {"==", "!=", "<", ">"}
UNKNOWN_LINE = 0


@dataclass
class Symbol:
    """Stores compile-time information known about one variable."""

    var_type: str
    declaration_line: int


class SymbolTable:
    """Dictionary-backed symbol table for the current TinyLang scope."""

    def __init__(self) -> None:
        self.symbols: dict[str, Symbol] = {}

    def declare(self, name: str, var_type: str, line: int) -> bool:
        """Register a new variable and reject same-scope redeclarations."""
        if name in self.symbols:
            return False
        self.symbols[name] = Symbol(var_type, line)
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        """Return symbol information for a declared variable, if present."""
        return self.symbols.get(name)


class SourceLineResolver:
    """Best-effort source line resolver used without modifying AST classes.

    Assignment 2 AST nodes do not store token line numbers. To obey Assignment
    3 reporting requirements while keeping the AST unchanged, this helper scans
    the source text for declaration, assignment, and identifier occurrences.
    """

    def __init__(self, source_code: str | None) -> None:
        self.source_lines = source_code.splitlines() if source_code else []

    def declaration_line(self, name: str) -> int:
        pattern = re.compile(rf"^\s*(?:int|float)\s+{re.escape(name)}\b")
        return self._find_line(pattern)

    def assignment_line(self, name: str) -> int:
        pattern = re.compile(rf"^\s*{re.escape(name)}\s*=")
        return self._find_line(pattern)

    def identifier_line(self, name: str) -> int:
        pattern = re.compile(rf"\b{re.escape(name)}\b")
        return self._find_line(pattern)

    def _find_line(self, pattern: re.Pattern[str]) -> int:
        for line_number, line in enumerate(self.source_lines, start=1):
            if pattern.search(line):
                return line_number
        return UNKNOWN_LINE


class SemanticAnalyzer:
    """Visitor-based semantic checker for TinyLang AST nodes."""

    def __init__(self, source_code: str | None = None) -> None:
        self.symbol_table = SymbolTable()
        self.errors: list[str] = []
        self.line_resolver = SourceLineResolver(source_code)

    def analyze(self, ast_root: Program) -> list[str]:
        """Analyze the AST and return all discovered semantic errors."""
        self.visit(ast_root)
        return self.errors

    def visit(self, node):
        """Dispatch to a node-specific visitor method."""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name)
        return visitor(node)

    def add_error(self, line: int, message: str) -> None:
        """Record an error while continuing analysis to find more issues."""
        self.errors.append(f"Semantic Error at line {line}: {message}")

    def visit_Program(self, node: Program) -> None:
        """Check each top-level statement in program order."""
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDecl(self, node: VarDecl) -> None:
        """Add declarations to the symbol table before checking initializers."""
        line = self.line_resolver.declaration_line(node.name)
        declared = self.symbol_table.declare(node.name, node.var_type, line)

        if not declared:
            original = self.symbol_table.lookup(node.name)
            original_line = original.declaration_line if original else UNKNOWN_LINE
            self.add_error(
                line,
                f"Variable '{node.name}' is already declared at line {original_line}.",
            )

        if node.initializer is not None:
            initializer_type = self.visit(node.initializer)
            self.check_assignment_compatibility(
                node.var_type,
                initializer_type,
                line,
                f"Cannot initialize '{node.name}'",
            )

    def visit_Assign(self, node: Assign) -> None:
        """Verify that assignments target declared variables with safe types."""
        line = self.line_resolver.assignment_line(node.name)
        symbol = self.symbol_table.lookup(node.name)
        value_type = self.visit(node.value)

        if symbol is None:
            self.add_error(line, f"Variable '{node.name}' used before declaration.")
            return

        self.check_assignment_compatibility(
            symbol.var_type,
            value_type,
            line,
            f"Cannot assign to '{node.name}'",
        )

    def visit_BinOp(self, node: BinOp) -> str:
        """Infer expression types and enforce arithmetic/comparison rules."""
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type == "error" or right_type == "error":
            return "error"

        if node.operator in ARITHMETIC_OPERATORS:
            if left_type in {"int", "float"} and right_type in {"int", "float"}:
                return "float" if "float" in {left_type, right_type} else "int"
            self.add_error(
                UNKNOWN_LINE,
                f"Operator '{node.operator}' requires numeric operands.",
            )
            return "error"

        if node.operator in COMPARISON_OPERATORS:
            if left_type in {"int", "float"} and right_type in {"int", "float"}:
                return "bool"
            self.add_error(
                UNKNOWN_LINE,
                f"Comparison '{node.operator}' requires numeric operands.",
            )
            return "error"

        self.add_error(UNKNOWN_LINE, f"Unknown operator '{node.operator}'.")
        return "error"

    def visit_Number(self, node: Number) -> str:
        """Classify numeric literals as int or float."""
        return "float" if isinstance(node.value, float) else "int"

    def visit_Identifier(self, node: Identifier) -> str:
        """Resolve identifier references against the symbol table."""
        symbol = self.symbol_table.lookup(node.name)
        if symbol is None:
            line = self.line_resolver.identifier_line(node.name)
            self.add_error(line, f"Variable '{node.name}' used before declaration.")
            return "error"
        return symbol.var_type

    def visit_If(self, node: If) -> None:
        """Require boolean-producing conditions before checking both branches."""
        condition_type = self.visit(node.condition)
        if condition_type != "bool" and condition_type != "error":
            self.add_error(
                UNKNOWN_LINE,
                "If condition must be a comparison expression that produces bool.",
            )

        for statement in node.then_branch:
            self.visit(statement)
        if node.else_branch is not None:
            for statement in node.else_branch:
                self.visit(statement)

    def visit_While(self, node: While) -> None:
        """Require boolean loop conditions before checking the loop body."""
        condition_type = self.visit(node.condition)
        if condition_type != "bool" and condition_type != "error":
            self.add_error(
                UNKNOWN_LINE,
                "While condition must be a comparison expression that produces bool.",
            )

        for statement in node.body:
            self.visit(statement)

    def visit_Print(self, node: Print) -> None:
        """Check printed expressions so undeclared identifiers are reported."""
        self.visit(node.expression)

    def check_assignment_compatibility(
        self,
        target_type: str,
        value_type: str,
        line: int,
        context: str,
    ) -> None:
        """Reject unsafe narrowing while allowing int-to-float promotion."""
        if value_type == "error":
            return
        if target_type == value_type:
            return
        if target_type == "float" and value_type == "int":
            return
        self.add_error(
            line,
            f"{context}: cannot store {value_type} value in {target_type} variable.",
        )


def analyze(ast_root: Program, source_code: str | None = None) -> list[str]:
    """Convenience entry point for main.py."""
    return SemanticAnalyzer(source_code).analyze(ast_root)
