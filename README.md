# HackClubTerra_Functional_Programming_Language
This is a repository for my submission to the Hack Club Terra programming competition

My submission is creating my own functional programming language, with time-travel features (by treating time as a sinusoidal wave, rather than linear), allowing for programs to revert time, and quantum features, allowing for parallel features

## Niche
Tau acts as a speculative "what-if" engine for decisions, due to its time travelling and multi-branch processing. It can be used for simulating real-world scenarios, e.g. how closing a road will affect the traffic elsewhere, as multiple factors and parameters can be fed into the machine, as they can vary across timelines, and only the winner will be output. 

## Try it
Live playground link
https://maanavnagda.github.io/HackClubTerra_Functional_Programming_Language/

## Run locally
python main.py
^^ runs the repl

python main.py examples/hello.tau
^^ Runs an example program in the Tau language. 
Also lambdas.tau, numbers.tau, conditionals.py, and piplines.py for extra example programs

## What Tau is today
Tau is a functional programming language written entirely in python. It features a lexer, recursive-descent parser, and two evaluators. It has the original naive tree walk evaluator, and a CEK style step machine where the whole evaluation state (control, env, kont) is plain data - this is what powers the step-forward, and rewind-time travel controls in the playground today, and full machine learning integrated speculation later. Both engines are proven equivalent through the oracle test series in the test_cek.py test suite. It currently supports let bindings, arithmetic with BODMAS precedence and floats, if/elseif/else conditionals, comparisons and booleans, comments (through the ;; operator), strings with backslash escapes, and mixed type + coercion, heterogeneous lists with the ++ append operator, named functions with closures and recursion, anonymous lambdas, -> application and |> pipelines. It can run in the web playground (which runs on the CEK machine for the latest features), as an interactive REPL, and file execution with the --engine naive or --engine machine choosing the evaluator and --step for choosing to run it step by step (and have the ability to go forward or backwards step by step) instead of the default run



## Timeline so far

Week 1:
- Let bindings
- Arithmetic
- BODMAS
- Everything is an expression, and env is immutable
- Example block
- Conditionals
- Comparisons
- Booleans
- ;; comments
- Web playground

Week 2:
- Named functions (fn name(x){...}), -> application, closures, recursion
- Anonymous lambdas (fn(x){..}) which are useable anywhere a value is
- Currying - multi-argument functions as chains of single-argument ones
- |> pipelines, which desugars into a function call
- CEK step machine, where control/env/kont state is plain, printable data (CEK machine necessary for time travel capabilities)
- oracle tests asserting both engines produce the same output
- --engine flag to pick which evaluator is chosen when running locally; the playground runs fully on the CEK machine

Week 3:
- print builtin - env bojnd value that returns its arguments so pipelines can keep flowing
- builtin names are now reserved and  cannot be overwritten by user bindings
- more example programs
- step through functionality added to web playground and main cli (currently broken)
- Swapped out basic text field  for Code mirror with syntax highlighting

Week 4:
- NEWLINE token - top level newlines now separate statements (fixes lines starting with unary minus from merging into previous expression); (), [], {} still allow mult-line expressions
- Rewind - playground button allows you to step BACKWARDS through the code as well as forward, cli flags let you do the same locally, the first stage of time travel
- Step-through is now fixed, as the python helpers were moved from inline JS template strings to their own separate file, which is imported with the other files. This makes the code clearer, cleaner, and makes it easier to see errors, as well as keeping python in python files and not in html files
- Strings - added strings datatype, accessible with double quotes(""), + feature allows cross-datatype concatenation
- Lists - added lists datatype, accessible using square brackets ([]), heterogeneous by design, allowing multiple datatypes to exist in the same list
- Added appending feature to lists, through the appending (++) operator. This is for appending in general, as well as to concatenate lists with other lists, as well as other types
- consolidated apply_op, to remove duplicated code & functions, so it is now a shared operator function between evaluator, CEK machine, and RPN 
- Added floats as a datatype, so if a float is returned, it doesn't automatically crash