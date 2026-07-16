# Assignment 2 Progress Report: TinyLang Front-End Implementation

## Status Update

The TinyLang compiler front end has been completed for Assignment 2. The current implementation includes a lexical analyzer, syntax analyzer, and Abstract Syntax Tree construction layer. The lexer recognizes keywords, identifiers, integer literals, floating-point literals, arithmetic operators, comparison operators, assignment, parentheses, braces, and semicolons. The parser accepts declarations, assignments, arithmetic expressions, conditionals, while loops, and print statements.

The parser returns a `Program` AST root node. Each AST node includes a `display()` method so that the syntactic structure of a TinyLang program can be inspected visually. This is useful for debugging and for demonstrating how the compiler transforms raw source text into an intermediate representation.

## Methodology and Tools

The implementation uses Python 3 and PLY, which provides Lex and Yacc-style compiler construction tools in Python. The project is organized into four core modules. `lexer.py` defines the token set and regular expressions. `parser.py` defines the Context-Free Grammar rules and constructs AST nodes. `ast_nodes.py` defines the tree representation. `main.py` acts as the driver program that reads a `.tiny` file, invokes the parser, and displays the AST.

The grammar was designed to keep the front-end phase focused and modular. Semantic concerns such as undeclared variables, duplicate declarations, and type compatibility are intentionally excluded from this phase. Those checks will be added during Semantic Analysis.

## Challenges Faced

The first major challenge was enforcing arithmetic precedence correctly. Without explicit precedence declarations, expressions such as `a + 5 * 3` may be parsed incorrectly or generate parser conflicts. This was resolved through PLY's `precedence` tuple. Multiplication and division are assigned higher precedence than addition and subtraction, while comparison operators are placed at a lower precedence level than arithmetic operators. Parenthesized expressions are handled with a separate grammar rule, allowing programmers to override default precedence.

The second challenge was the classic dangling-else ambiguity. In nested conditional statements, an `else` could theoretically match more than one unmatched `if`. The implementation resolves this shift/reduce conflict using an artificial precedence marker named `IFX`. The `if` production without `else` is assigned lower precedence than the `ELSE` token, causing PLY to attach each `else` to the nearest unmatched `if`, which matches the behavior of most imperative programming languages.

## Roadmap for Remaining Phases

The next phase is Semantic Analysis. It will introduce a symbol table for variable declarations, detect duplicate declarations, report use of undeclared identifiers, and verify type compatibility for assignments and expressions. It should also validate that conditions used in `if` and `while` statements are meaningful comparison expressions or numeric expressions according to the TinyLang type rules.

After Semantic Analysis, the project will move to intermediate code generation. The planned target is Three-Address Code (TAC). Arithmetic expressions will be lowered into temporary variables, control-flow statements will generate labels and conditional jumps, and print statements will emit simple output instructions. This design keeps the compiler pipeline clear: source code is tokenized, parsed into an AST, checked semantically, and then translated into an intermediate representation suitable for later optimization or interpretation.
