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
Tau is a functional programming language written entirely in python. It features a lexer, a recursive-descent parser, and two evaluators. It has the original naive tree walk evaluator, and a CEK style step machine where the whole evaluation state (control, env, kont) is plain data - this is what makes the upcoming time-travel feature possible, and both engines are proven equivalent through the oracle test suite. It currently supports let bindings, arithmetic with BODMAS precedence, if/elseif/else conditionals, comparisons and booleans, ;; comments, named functions with closures and recursion, anonymous lambdas, -> application and |> pipelines. It can run in the web playground (which runs on the CEK machine), as an interactive REPL, and file execution, with --engine naive or --engine machine choosing the evaluator

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
- Swapped out basic text field  for Code mirror with pretty print