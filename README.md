# math-parser
This small project allows math expressions to be parsed and evaluated.
It supports basic arithmetic operations with floating-point numbers and some pre-defined constants. 
Some trigonometric functions and more advanced operations using parentheses are also supported. 

### Disclaimer
This implementation does not intend to be a robust or complete math parser and evaluator. 
This is a proof of concept rather than a production code. 
Therefore, it has limitations and critical applications should not rely on it.
For advanced scenarios scenarios consider [SymPy](https://docs.sympy.org/latest/index.html). 

### How it works
Expressions are entered as a string and sanitized. Implicit operations are expanded to simplify the next steps. 
We could have used a [context-free grammar](https://en.wikipedia.org/wiki/Context-free_grammar), described using [EBNF](https://en.wikipedia.org/wiki/Extended_Backus–Naur_form)
but that would add some complexity that would go beyond the purpose of this implementation. 
So instead, we aught to use a very simplistic (and limited) char-by-char tokenizer but that fits our needs.

After the expression is scanned, it creates a list of tokens and variables. 
The parsed expression is feed to be converted into the [Reverse Polish notation](https://en.wikipedia.org/wiki/Reverse_Polish_notation)
using an extended version of the [Shunting-yard algorithm](https://en.wikipedia.org/wiki/Shunting-yard_algorithm).

The RPN expression is then evaluated and the result is produced.

### Supported features

The following operators are supported:

| Symbol | Operation      | 
|:------:|----------------|
|+       | addition       |
|-       | subtraction    |
|*       | multiplication |
|/       | division       |
|!       | factorial      |
|^       | exponentiation |

The following functions are supported:

| Symbol | Function           | 
|:------:|--------------------|
|sqrt    | square root        |
|cbrt    | cubic root         |
|sin     | sine               |
|cos     | cosine             |
|tan     | tangent            |
|radians | degrees to radians |
|degrees | radians to degrees |

The following constants are supported:

| Symbol | Constant          | 
|:------:|-------------------|
|pi      | 3.141592653589793 |
|phi     | 1.618033988749894 |
|e       | 2.718281828459045 |

Alphabetic sequences that do not match any of the functions or constants will be treated as variables.
Decimal places should be separated by dot (`.`) on floating-point numbers.

### Examples

#### Simple addition
```
e = Expression('1+1')
print(e.evaluate()) # Output: 2
```

#### Simple subtraction
```
e = Expression('1-2')
e.evaluate() # Output: -1
```

#### Simple multiplication
```
e = Expression('1*2')
e.evaluate() # Output: 2
```

#### Simple division
```
e = Expression('1/2')
e.evaluate() # Output: 0.5
```