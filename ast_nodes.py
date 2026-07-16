"""Abstract Syntax Tree node definitions for TinyLang.

The parser constructs objects from this module instead of directly executing
program statements. This separation is important in compiler design: the AST is
an intermediate representation that later phases can inspect for semantic
analysis, optimization, and code generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Union


def print_indented(indent: int, text: str) -> None:
    """Print one line using two spaces per indentation level."""
    print(f"{'  ' * indent}{text}")


class ASTNode:
    """Base class for all AST nodes."""

    def display(self, indent: int = 0) -> None:
        """Display a readable tree representation of the node."""
        raise NotImplementedError("Subclasses must implement display().")


@dataclass
class Program(ASTNode):
    """Root node containing all top-level statements."""

    statements: List[ASTNode]

    def display(self, indent: int = 0) -> None:
        print_indented(indent, "Program")
        for statement in self.statements:
            statement.display(indent + 1)


@dataclass
class VarDecl(ASTNode):
    """Variable declaration node, optionally with initialization."""

    var_type: str
    name: str
    initializer: Optional[ASTNode] = None

    def display(self, indent: int = 0) -> None:
        print_indented(indent, f"VarDecl(type={self.var_type}, name={self.name})")
        if self.initializer is not None:
            print_indented(indent + 1, "Initializer")
            self.initializer.display(indent + 2)


@dataclass
class Assign(ASTNode):
    """Assignment statement node."""

    name: str
    value: ASTNode

    def display(self, indent: int = 0) -> None:
        print_indented(indent, f"Assign(name={self.name})")
        self.value.display(indent + 1)


@dataclass
class BinOp(ASTNode):
    """Binary operation node for arithmetic and comparison expressions."""

    operator: str
    left: ASTNode
    right: ASTNode

    def display(self, indent: int = 0) -> None:
        print_indented(indent, f"BinOp(operator={self.operator})")
        print_indented(indent + 1, "Left")
        self.left.display(indent + 2)
        print_indented(indent + 1, "Right")
        self.right.display(indent + 2)


@dataclass
class Number(ASTNode):
    """Numeric literal node for integer and floating-point values."""

    value: Union[int, float]

    def display(self, indent: int = 0) -> None:
        print_indented(indent, f"Number(value={self.value})")


@dataclass
class Identifier(ASTNode):
    """Identifier reference node."""

    name: str

    def display(self, indent: int = 0) -> None:
        print_indented(indent, f"Identifier(name={self.name})")


@dataclass
class If(ASTNode):
    """Conditional statement node with optional else branch."""

    condition: ASTNode
    then_branch: List[ASTNode]
    else_branch: Optional[List[ASTNode]] = None

    def display(self, indent: int = 0) -> None:
        print_indented(indent, "If")
        print_indented(indent + 1, "Condition")
        self.condition.display(indent + 2)
        print_indented(indent + 1, "Then")
        for statement in self.then_branch:
            statement.display(indent + 2)
        if self.else_branch is not None:
            print_indented(indent + 1, "Else")
            for statement in self.else_branch:
                statement.display(indent + 2)


@dataclass
class While(ASTNode):
    """While-loop node."""

    condition: ASTNode
    body: List[ASTNode]

    def display(self, indent: int = 0) -> None:
        print_indented(indent, "While")
        print_indented(indent + 1, "Condition")
        self.condition.display(indent + 2)
        print_indented(indent + 1, "Body")
        for statement in self.body:
            statement.display(indent + 2)


@dataclass
class Print(ASTNode):
    """Print statement node."""

    expression: ASTNode

    def display(self, indent: int = 0) -> None:
        print_indented(indent, "Print")
        self.expression.display(indent + 1)
