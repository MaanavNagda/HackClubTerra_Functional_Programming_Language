#
import subprocess
import sys
import os
from pathlib import Path
import pytest


#helper functions
MAIN = Path(__file__).parent.parent/ "main.py"

def run_cli(args, input=""):
    #runs "python main.py" followed by args, captures output, and then returns the process object
    return subprocess.run(
        [sys.executable, str(MAIN)] + args,
        input = input, capture_output = True, text=True
    ) 

def last_line(text):
    #splits into lines, drops empty ones, and returns the final line
    lines = [l for l in text.split("\n") if l.strip()]
    return lines[-1]


#Main program tests
#Follownng test ran on 9.11.26
#All failed on 9.11.26 @2.29am
def test_file_mode_default_engine():
    #no --engine flag,  as using the naive evaluator; numbers_test.tau prints every |> print, so the program result is the LAST line of stdout (which is 7)
    r = run_cli(["examples/numbers_test.tau"])
    assert r.returncode == 0
    assert last_line(r.stdout) == "7"

def test_engine_machine_matches_naive():
    #oracle cehck, as both engines mustproduce byte-identical stdout
    naive = run_cli(["examples/numbers_test.tau"])
    machine = run_cli(["--engine", "machine", "examples/numbers_test.tau"])
    assert naive.stdout == machine.stdout
    assert last_line(machine.stdout) == "7"

def test_engine_naive_explicit():
    #--engine naive spelled out behaves the same as the default
    r  = run_cli(["--engine", "naive", "examples/numbers_test.tau"])
    assert r.returncode == 0 
    assert last_line(r.stdout) == "7"

def test_step_prints_state_blocks():
    #every state renders as control:/env:/lont: lines, blcoks separated by blank lines
    r = run_cli(["--step", "examples/numbers_test.tau"])
    assert r.returncode== 0
    assert "env:" in r.stdout and "kont:" in r.stdout
    assert "control: halt" in r.stdout               #final state is the halt marker
    assert  "result:" in r.stdout                    #halt state shows the result
    assert "\n\n" in r.stdout                        # states  are  separated by blank lines


#Following tests ran on 9.11.26
#All successfully passed on 9.11.26 @ 2.29am
def test_step_ignores_engine_flag():
    # --step always runs the machine trace; --engine, especially naive, must not change the output
    plain = run_cli(["--step", "examples/numbers_test.tau"])
    with_eng = run_cli(["--step", "--engine", "naive", "examples/numbers_test.tau"])
    assert plain.stdout == with_eng.stdout

def test_step_trace_length_for_tiny_program(tmp_path):
    # "14 + 11" takes exactly 4 states: body ->  BinOp ->  value 25 -> halt
    prog = tmp_path / "tiny.tau"
    prog.write_text("14 + 11\n")
    r = run_cli(["--step", str(prog)])
    assert r.returncode ==  0
    assert r.stdout.count("control:") == 4
    assert "result:25" in r.stdout or "result: 25" in r.stdout

def test_step_on_error_program(tmp_path):
    #a program that fails mid run throuhh the Error: path, not a traceback
    prog = tmp_path / "bad.tau"
    prog.write_text("y+1\n")  #y is undefined and so the machine raises mid tracey
    r = run_cli(["--step", str(prog)])
    assert "Error:" in r.stdout

def test_missing_file():
    r = run_cli(["does_not_exist.tau"])
    assert "File does_not_exist.tau not found" in r.stdout

def test_repl_still_works():
    # no file argument so its the interactive REPL, feed it exit on stdin
    r = run_cli([], "exit\n")
    assert "Tau REPL" in r.stdout
    assert "Goodbye" in r.stdout
