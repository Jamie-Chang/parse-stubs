# parse-stubs

These are public type stubs for [parse](https://github.com/r1chardj0n3s/parse) as specified in [PEP 561](https://peps.python.org/pep-0561/#stub-only-packages).

## Why?
Parse is a fantanstic library that allows you do process strings effortlessly, but it doesn't always play well with type checkers, for example:

```python
parse("Bring me a {}", "Bring me a shrubbery")
```

returns a `Result`, but

```
parse("Bring me a {}", "Bring me a shrubbery", evaluate_result=False)
```

returns a `Match` instance.
