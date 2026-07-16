"""TinyLang compiler pipeline entry point.

This module connects all implemented compiler phases:

1. Lexical analysis with PLY lex.
2. Syntax analysis with PLY yacc and AST construction.
3. Semantic analysis.
4. Three-Address Code generation.

Usage:
    python main.py path/to/source.tiny
"""

from __future__ import annotations

import argparse
from pathlib import Path

from lexer import get_lexical_error_count
from parser import get_syntax_error_count, parse
from semantic_analyzer import analyze
from tac_generator import generate


def read_source_file(file_path: Path) -> str:
    """Read a TinyLang source file as UTF-8 text."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"Error: source file not found: {file_path}") from exc
    except OSError as exc:
        raise SystemExit(f"Error: could not read source file: {exc}") from exc


def write_tac_file(source_file: Path, instructions: list[str]) -> Path:
    """Write TAC instructions beside the source file using a .tac suffix."""
    tac_file = source_file.with_suffix(".tac")
    tac_file.write_text("\n".join(instructions) + "\n", encoding="utf-8")
    return tac_file


def main() -> None:
    """Run parsing, semantic analysis, and TAC generation."""
    argument_parser = argparse.ArgumentParser(
        description="TinyLang compiler: parser, semantic analyzer, and TAC generator."
    )
    argument_parser.add_argument(
        "source_file",
        type=Path,
        help="Path to a .tiny source file.",
    )
    args = argument_parser.parse_args()

    source_code = read_source_file(args.source_file)
    ast_root = parse(source_code)

    if get_lexical_error_count() or get_syntax_error_count():
        raise SystemExit("Compilation halted due to lexical/syntax errors.")

    if ast_root is None:
        raise SystemExit("Parsing failed. No AST was generated.")

    print("Abstract Syntax Tree")
    print("====================")
    ast_root.display()

    semantic_errors = analyze(ast_root, source_code)
    if semantic_errors:
        print()
        print("Semantic Analysis Errors")
        print("========================")
        for error in semantic_errors:
            print(error)
        raise SystemExit("Compilation halted because semantic errors were found.")

    tac_instructions = generate(ast_root)
    tac_file = write_tac_file(args.source_file, tac_instructions)

    print()
    print("Three-Address Code")
    print("==================")
    for instruction in tac_instructions:
        print(instruction)
    print()
    print(f"TAC written to: {tac_file}")


if __name__ == "__main__":
    main()
