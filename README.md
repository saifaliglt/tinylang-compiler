# TinyLang — A Mini Compiler

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![PLY](https://img.shields.io/badge/PLY-3.11-green)](https://www.dabeaz.com/ply/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

**TinyLang** is a small imperative teaching language built to explore the full compiler pipeline — from raw source text to Three-Address Code (TAC) — as a term project for a Compiler Construction course. It's implemented from scratch in Python 3 using [PLY](https://www.dabeaz.com/ply/) (Python Lex-Yacc), covering lexical analysis, syntax analysis, AST construction, semantic analysis, and intermediate code generation.

> Term project for BSCS Compiler Construction, Karakoram International University (6th Semester).

---

## Table of Contents

- [Features](#features)
- [Compiler Pipeline](#compiler-pipeline)
- [Project Structure](#project-structure)
- [Prerequisites & Installation](#prerequisites--installation)
- [Usage](#usage)
- [TinyLang Syntax](#tinylang-syntax)
- [Example: Source to TAC](#example-source-to-tac)
- [Test Cases](#test-cases)
- [Design Highlights](#design-highlights)
- [Limitations & Future Work](#limitations--future-work)
- [References](#references)

---

## Features

- Integer and floating-point variable declarations: `int x;`, `float y = 3.5;`
- Arithmetic expressions with correct BODMAS/PEMDAS precedence: `+`, `-`, `*`, `/`
- Comparison expressions: `==`, `!=`, `<`, `>`
- Assignment statements
- `if` / `else` conditional statements (dangling-else resolved)
- `while` loops
- `print(...)` statements
- Single-line comments (`//`)
- AST visualization via `display()`
- Symbol-table-backed semantic analysis (undeclared-variable detection, type checking)
- Three-Address Code (TAC) generation for all supported constructs
- Clear, located error messages at every compilation stage

## Compiler Pipeline

```
 Source (.tiny)
      │
      ▼
 ┌───────────┐     ┌────────┐     ┌─────────────────┐     ┌────────────────────┐
 │  Lexer    │ ──▶ │ Parser │ ──▶ │ Semantic Analyzer │ ──▶ │  TAC Generator     │
 │ (lexer.py)│     │(parser.│     │(semantic_analyzer│     │ (tac_generator.py) │
 │           │     │  .py)  │     │      .py)         │     │                    │
 └───────────┘     └────────┘     └─────────────────┘     └────────────────────┘
      │                 │                  │                        │
   Tokens              AST          Validated AST /            Three-Address
                                     Semantic Errors                 Code
```

## Project Structure

```text
.
├── ast_nodes.py            # AST node class definitions + display()
├── lexer.py                # PLY lexer: tokens, keywords, operators
├── parser.py                # PLY yacc parser: grammar rules, AST construction
├── semantic_analyzer.py     # Symbol table, type checking, semantic errors
├── tac_generator.py         # Three-Address Code generation
├── main.py                  # CLI entry point (full pipeline)
├── requirements.txt
├── README.md
├── progress_report.md
└── tests/
    ├── arithmetic.tiny
    ├── control_flow.tiny
    ├── loops.tiny
    ├── semantic_error_undeclared.tiny
    ├── semantic_error_type_mismatch.tiny
    └── tac_full_program.tiny
```

## Prerequisites & Installation

- Python 3.8 or newer

```bash
git clone https://github.com/<your-username>/tinylang-compiler.git
cd tinylang-compiler
pip install -r requirements.txt
```

Or install PLY directly:

```bash
pip install ply
```

## Usage

Run the full pipeline (lex → parse → AST → semantic check → TAC) on any `.tiny` file:

```bash
python main.py tests/arithmetic.tiny
python main.py tests/control_flow.tiny
python main.py tests/loops.tiny
```

On success, the program prints the AST and the generated TAC, and writes the TAC to a matching `.tac` file next to the source.

To see semantic error handling in action:

```bash
python main.py tests/semantic_error_undeclared.tiny
python main.py tests/semantic_error_type_mismatch.tiny
```

## TinyLang Syntax

```c
int counter = 0;
int limit = 3;

while (counter < limit) {
    print(counter);
    counter = counter + 1;
}
```

## Example: Source to TAC

**Input**

```c
int a = 10;
int b = 5;
if (a > b) {
    print(a);
} else {
    print(b);
}
```

**Generated TAC**

```text
a = 10
b = 5
t1 = a > b
if t1 goto L1
goto L2
L1:
print a
goto L3
L2:
print b
L3:
```

## Test Cases

| Test | Purpose |
|---|---|
| `arithmetic.tiny` | Declarations, operator precedence, parenthesized expressions |
| `control_flow.tiny` | `if`/`else`, comparisons, branch-scoped assignment |
| `loops.tiny` | `while` loops, loop-condition evaluation, in-loop updates |
| `semantic_error_undeclared.tiny` | Use of an undeclared identifier |
| `semantic_error_type_mismatch.tiny` | Assigning an incompatible type |
| `tac_full_program.tiny` | End-to-end program exercising every TAC instruction pattern |

## Design Highlights

- **Operator precedence** is handled declaratively via PLY's `precedence` tuple rather than grammar restructuring.
- **Dangling-else ambiguity** is resolved using an artificial `IFX` precedence marker, favoring the nearest unmatched `if`.
- **Semantic analysis** uses the visitor pattern to walk the AST, backed by a symbol table that tracks each variable's declared type and declaration line.
- **TAC generation** reuses the same AST and visitor structure, emitting sequential temporaries (`t1, t2, ...`) and labels (`L1, L2, ...`) for control flow.

## Limitations & Future Work

- No functions, arrays, or user-defined types
- No code optimization passes on the generated TAC
- No target-machine code generation (TAC is the final output)
- Single global scope only (no nested block scoping)

## References

1. A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman, *Compilers: Principles, Techniques, and Tools*, 2nd ed. Pearson Education, 2006.
2. K. D. Cooper and L. Torczon, *Engineering a Compiler*, 2nd ed. Morgan Kaufmann, 2011.
3. D. Beazley, *PLY (Python Lex-Yacc) Documentation*, v3.11. https://www.dabeaz.com/ply/
4. A. Aiken, *Stanford CS143: Compilers — Course Materials*. https://web.stanford.edu/class/cs143/

---

*Term project for the Compiler Construction course, Department of Computer Science, Karakoram International University.*