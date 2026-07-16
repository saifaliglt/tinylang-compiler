"""Three-Address Code generation for TinyLang.

TAC is a simple intermediate representation in which complex expressions are
lowered into small instructions using temporary variables and explicit labels.
"""

from __future__ import annotations

from ast_nodes import Assign, BinOp, Identifier, If, Number, Print, Program, VarDecl, While


class TACGenerator:
    """Visitor-based Three-Address Code generator."""

    def __init__(self) -> None:
        self.instructions: list[str] = []
        self.temp_counter = 0
        self.label_counter = 0

    def generate(self, ast_root: Program) -> list[str]:
        """Generate ordered TAC instructions from a semantically valid AST."""
        self.visit(ast_root)
        return self.instructions

    def new_temp(self) -> str:
        """Create a fresh temporary for an intermediate expression value."""
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    def new_label(self) -> str:
        """Create a fresh label for structured control-flow lowering."""
        self.label_counter += 1
        return f"L{self.label_counter}"

    def emit(self, instruction: str) -> None:
        """Append one TAC instruction to the output stream."""
        self.instructions.append(instruction)

    def visit(self, node):
        """Dispatch to a node-specific TAC generation method."""
        method_name = f"visit_{node.__class__.__name__}"
        visitor = getattr(self, method_name)
        return visitor(node)

    def visit_Program(self, node: Program) -> None:
        """Lower each source statement into TAC in original program order."""
        for statement in node.statements:
            self.visit(statement)

    def visit_VarDecl(self, node: VarDecl) -> None:
        """Reserve declared names conceptually and emit initializer code."""
        if node.initializer is not None:
            value_place = self.visit(node.initializer)
            self.emit(f"{node.name} = {value_place}")

    def visit_Assign(self, node: Assign) -> None:
        """Lower assignment by evaluating the right side before storing it."""
        value_place = self.visit(node.value)
        self.emit(f"{node.name} = {value_place}")

    def visit_BinOp(self, node: BinOp) -> str:
        """Lower a binary expression into one temporary-producing TAC line."""
        left_place = self.visit(node.left)
        right_place = self.visit(node.right)
        result_place = self.new_temp()
        self.emit(f"{result_place} = {left_place} {node.operator} {right_place}")
        return result_place

    def visit_Number(self, node: Number) -> str:
        """Represent numeric literals directly as TAC operands."""
        return str(node.value)

    def visit_Identifier(self, node: Identifier) -> str:
        """Represent variable references directly as TAC operands."""
        return node.name

    def visit_If(self, node: If) -> None:
        """Lower if/else into conditional branches and labels."""
        condition_place = self.visit(node.condition)
        true_label = self.new_label()
        false_label = self.new_label()
        end_label = self.new_label()

        self.emit(f"if {condition_place} goto {true_label}")
        self.emit(f"goto {false_label}")
        self.emit(f"{true_label}:")
        for statement in node.then_branch:
            self.visit(statement)
        self.emit(f"goto {end_label}")
        self.emit(f"{false_label}:")
        if node.else_branch is not None:
            for statement in node.else_branch:
                self.visit(statement)
        self.emit(f"{end_label}:")

    def visit_While(self, node: While) -> None:
        """Lower while loops into a start label, guard, body, and back edge."""
        start_label = self.new_label()
        end_label = self.new_label()

        self.emit(f"{start_label}:")
        condition_place = self.visit(node.condition)
        self.emit(f"ifFalse {condition_place} goto {end_label}")
        for statement in node.body:
            self.visit(statement)
        self.emit(f"goto {start_label}")
        self.emit(f"{end_label}:")

    def visit_Print(self, node: Print) -> None:
        """Lower print statements after evaluating their expression operand."""
        value_place = self.visit(node.expression)
        self.emit(f"print {value_place}")


def generate(ast_root: Program) -> list[str]:
    """Convenience entry point for main.py."""
    return TACGenerator().generate(ast_root)
