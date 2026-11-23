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
Tau is a functional programming language written entirely in python. It is made up of a lexer, a recursive-descent parser, and two eavluators. It has the original naive tree walk evalutor, and a CEK style step machine where the whole evaluation state (control, env, kont) is plain data - this is what powers the step-forward, and rewind-time travel controls in the playground (currently) and full machine learning integrated speculation (in the future). Both engines are proven equivalent through the oracle test series in the test_cek test suite. It currently supports let bindings, arithmetic with BODMAS precendece, float literals, if/elseif/else conditionals, comparisons and booleans, comments (through the ;; operator), strings with backslash escapes and mixed type with coercion, heterogeneous lists with the ++ append operator, named functions with closures and recursions, anonymous lambdas, -> application and |>piprelines, checkpoint/rewind, primitives that snapshot and restore the environment mid-program, an effect vocabulary where scenario actions are described rather than performed (dispatch!/reroute!/page!/write!/ return Effect values, and commit! performs them), a . operator for applying functions and builtins to other functions/lists/sets (but NOT expressions), and for floats (x.name, 13 respectively for example), and the map/filter list builtins which only exist in the .map and .filter forms, as they are only applicable to functions. It can run in the web playground (which runs on the CEK machine for the latest features), an interactive REPL, and standard file execution with different flags (like --engine naive or --step) that can be used to alter the different modes (what type of engine backend is being used, if it is running in stepped mode or not etc).



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

Week 5:
- checkpoint/rewind language primitives - snapshot and restore the environment mid-program, a persistent trail, with a 100 checkpoint cap (hard coded for now, may later be allowed to be user-configurable), works in both evaluators
- Effect vocabulary - dispatch!, reroute!, page!, write! commands that are like a todo list. They are commands which can be stored, and their results seen by the rest of the branch, but they will not be executed until the very end. This is so if there are multiple competing branches, only the final branch's todo list should be run, as it produces the optimal output, and we can only figure this out at the end
- . operator - this is for a) floats, as it is used to show decimals (e.g. 13.14), and for b) function/builtin upon function acting, where you can use function.builtin or function.function (also works for lists, sets etc), where it indicates that the builtin/function is acting on a another function.
- Map builtin - allows for a function to be easily applied to an entire list. As it requires a function, only exists as a .map, and cannot use -> or |>
- Filter builtin - allows to discard all elements from a list that cause the assigned function to evaluate to false, and keeps all the elements from the list that cause the evaluated function to evaluate to true. Once again, as there must be a function involved, filter only exists in the .filter form, and cannot use -> or |>