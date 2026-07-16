# TinyLang Assignment 2: Front-End Implementation

TinyLang is a small imperative teaching language for a mini-compiler term project. This phase implements the compiler front end: lexical analysis, syntax analysis, and Abstract Syntax Tree (AST) construction using Python 3 and PLY.

## Features

- Integer and floating-point declarations: `int x;`, `float y = 3.5;`
- Arithmetic expressions with BODMAS/PEMDAS precedence: `+`, `-`, `*`, `/`
- Comparison expressions: `==`, `!=`, `<`, `>`
- Assignment statements
- `if` / `else` conditional statements
- `while` loops
- `print(...)` commands
- AST visualization through `display()`

## Project Structure

```text
.
├── ast_nodes.py
├── lexer.py
├── parser.py
├── main.py
├── requirements.txt
├── tests/
│   ├── arithmetic.tiny
│   ├── control_flow.tiny
│   └── loops.tiny
└── progress_report.md
```

## Prerequisites

- Python 3.8 or newer
- PLY

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install PLY directly:

```bash
pip install ply
```

## Running the Compiler Front End

Run `main.py` with a TinyLang source file:

```bash
python main.py tests/arithmetic.tiny
python main.py tests/control_flow.tiny
python main.py tests/loops.tiny
```

The program prints the generated AST. This assignment does not yet perform semantic analysis or code generation.

## TinyLang Syntax Example

```c
int counter = 0;
int limit = 3;

while (counter < limit) {
    print(counter);
    counter = counter + 1;
}
```

## Test Case 1: Arithmetic

Source: `tests/arithmetic.tiny`

Expected AST:

```text
Program
  VarDecl(type=int, name=a)
    Initializer
      Number(value=10)
  VarDecl(type=float, name=b)
    Initializer
      Number(value=2.5)
  Assign(name=a)
    BinOp(operator=+)
      Left
        Identifier(name=a)
      Right
        BinOp(operator=*)
          Left
            Number(value=5)
          Right
            Number(value=3)
  Assign(name=b)
    BinOp(operator=/)
      Left
        BinOp(operator=+)
          Left
            Identifier(name=b)
          Right
            Number(value=1.5)
      Right
        Number(value=2)
  Print
    Identifier(name=a)
  Print
    Identifier(name=b)
```

## Test Case 2: Control Flow

Source: `tests/control_flow.tiny`

Expected AST:

```text
Program
  VarDecl(type=int, name=score)
    Initializer
      Number(value=75)
  If
    Condition
      BinOp(operator=>)
        Left
          Identifier(name=score)
        Right
          Number(value=50)
    Then
      Print
        Identifier(name=score)
    Else
      Assign(name=score)
        BinOp(operator=+)
          Left
            Identifier(name=score)
          Right
            Number(value=10)
      Print
        Identifier(name=score)
```

## Test Case 3: Loops

Source: `tests/loops.tiny`

Expected AST:

```text
Program
  VarDecl(type=int, name=counter)
    Initializer
      Number(value=0)
  VarDecl(type=int, name=limit)
    Initializer
      Number(value=3)
  While
    Condition
      BinOp(operator=<)
        Left
          Identifier(name=counter)
        Right
          Identifier(name=limit)
    Body
      Print
        Identifier(name=counter)
      Assign(name=counter)
        BinOp(operator=+)
          Left
            Identifier(name=counter)
          Right
            Number(value=1)
```

## Notes for Future Phases

The AST is deliberately simple and phase-friendly. Semantic analysis can traverse it to build a symbol table and enforce type rules. Code generation can later traverse the same tree to emit Three-Address Code.
