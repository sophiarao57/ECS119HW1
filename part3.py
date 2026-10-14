"""
Part 3: Short Exercises on the Shell

For the third and last part of this homework,
we will complete a few tasks related to shell programming
and shell commands, particularly, with relevance to how
the shell is used in data science.

Please note:
The "project proposal" portion will be postponed to part of Homework 2.

===== Questions 1-5: Setup Scripting =====

1. For this first part, let's write a setup script
that downloads a dataset from the web,
clones a GitHub repository, and runs the Python script
contained in `script.py` on the dataset in question.

For the download portion, we have written a helper
download_file(url, filename) which downloads the file
at `url` and saves it in `filename`.

You should use Python subprocess to run all of these operations.

To test out your script, and as your answer to this part,
run the following:
    setup(
        "https://github.com/DavisPL-Teaching/119-hw1",
        "https://raw.githubusercontent.com/DavisPL-Teaching/119-hw1/refs/heads/main/data/test-input.txt",
        "test-script.py"
    )

Then read the output of `output/test-output.txt`,
convert it to an integer and return it. You should get "12345".

Note:
Running this question will leave an extra repo 119-hw1 lying around in your repository.
We recommend adding this to your .gitignore file so it does not
get uploaded when you submit.
"""

import os
import subprocess
import sys

# You may need to conda install requests or pip3 install requests
import requests

def download_file(url, filename):
    r = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(r.content)

def repo_directory(repo_url):
    # The folder that `git clone` creates, e.g. ".../119-hw1" -> "119-hw1"
    return os.path.basename(repo_url.rstrip("/")).removesuffix(".git")

def clone_repo(repo_url):
    # Don't clone again if the repository is already there.
    if os.path.isdir(repo_directory(repo_url)):
        return
    subprocess.run(["git", "clone", repo_url], check=True)

def run_script(script_path, data_path):
    # Run the script with the same Python interpreter that runs this file.
    # (The script reads its input from data_path and writes into output/.)
    subprocess.run([sys.executable, script_path, data_path], check=True)

def setup(repo_url, data_url, script_path):
    # Get the code
    clone_repo(repo_url)
    # Get the data
    os.makedirs("data", exist_ok=True)
    data_path = os.path.join("data", os.path.basename(data_url))
    download_file(data_url, data_path)
    # Run the script from the cloned repository on the data
    os.makedirs("output", exist_ok=True)
    cloned_script = os.path.join(repo_directory(repo_url), script_path)
    run_script(cloned_script, data_path)

def q1():
    # Call setup as described in the prompt
    setup(
        "https://github.com/DavisPL-Teaching/119-hw1",
        "https://raw.githubusercontent.com/DavisPL-Teaching/119-hw1/refs/heads/main/data/test-input.txt",
        "test-script.py"
    )
    # Read the file test-output.txt to a string
    with open("output/test-output.txt") as f:
        output = f.read()
    # Return the integer value of the output
    return int(output)

"""
2.
Suppose you are on a team of 5 data scientists working on
a project; every 2 weeks you need to re-run your scripts to
fetch the latest data and produce the latest analysis.

a. When might you need to use a script like setup() above in
this scenario?

=== ANSWER Q2a BELOW ===

You need a setup script like setup() whenever the pipeline has to be
re-run from scratch on a machine where the code or the data is missing or out
of date: for each biweekly re-run, to fetch the newest data, to pull the latest
version of the team's code, and run the analysis in the same way every time.
It is also needed when a new team member joins, or when the analysis runs
unattended on a server or in a scheduled job that has no state from a previous run.

=== END OF Q2a ANSWER ===

Do you see an alternative to using a script like setup()?

=== ANSWER Q2b BELOW ===

Yes. Alternatives are: a workflow/build tool (make, Snakemake, Airflow or
a cron job/CI pipeline) which tracks dependencies and only re-runs what changed;
a shared, versioned data store or database that everyone reads the latest data from,
instead of downloading it by script; or packaging the whole environment
in a container (Docker) or notebook environment so that everyone runs the same
setup. Having the code as a proper installable package, and versioned
data (git-lfs/DVC), also removes most of the need for an ad-hoc script.

=== END OF Q2b ANSWER ===

3.
Now imagine we have to re-think our script to
work on a brand-new machine, without any software installed.
(For example, this would be the case if you need to run
your pipeline inside an Amazon cloud instance or inside a
Docker instance -- to be more specific you would need
to write something like a Dockerfile, see here:
https://docs.docker.com/reference/dockerfile/
which is basically a list of shell commands.)

Don't worry, we won't test your code for this part!
I just want to see that you are thinking about how
shell commands can be used for setup and configuration
necessary for data processing pipelines to work.

Think back to HW0. What sequence of commands did you
need to run?
Write a function setup_for_new_machine() that would
be able to run on a brand-new machine and set up
everything that you need.

Assume that you need your script to work on all of the packages
that we have used in HW1 (that is, any `import` statements
and any other software dependencies).

Assume that the new server machine is identical
in operating system and architecture to your own,
but it doesn't have any software installed.
It has Python 3.12
and conda or pip3 installed to get needed packages.

Hint: use subprocess again!

Hint: search for "import" in parts 1-3. Did you miss installing
any packages?
"""

def setup_for_new_machine():
    # Assumes macOS with Python 3.12 and pip3 installed (git comes with
    # the Xcode command line tools: `xcode-select --install`).
    # Every package that is imported in parts 1-3 which is not part
    # of the standard library (matplotlib, numpy and requests are needed
    # even though they are not installed together with pandas/pytest).
    packages = ["pandas", "numpy", "matplotlib", "pytest", "requests"]
    subprocess.run(["pip3", "install"] + packages, check=True)
    # Get the homework code and make sure the folders it writes to exist.
    subprocess.run(["git", "clone", "https://github.com/DavisPL-Teaching/119-hw1"], check=True)
    os.makedirs("119-hw1/output", exist_ok=True)

def q3():
    # As your answer, return a string containing
    # the operating system name that you assumed the
    # new machine to have.
    return "macOS"

"""
4. This question is open ended :)
It won't be graded for correctness.

What percentage of the time do you think real data scientists
working in larger-scale projects in industry have to write
scripts like setup() and setup_for_new_machine()
in their day-to-day jobs?

=== ANSWER Q4 BELOW ===

I would guess that it varies a lot, but probably something like 10-20% of the
time for a typical data scientist; more for a data engineer or an ML engineer
(maybe 30-50%) since they often work on pipelines, deployment and environments,
and much less (a few %) for analysts who work mostly in notebooks on data that
is given to them. In larger projects a lot of this is done once, by a few
people, and then reused by everybody, so scripts like these are written
rarely but are used constantly.

=== END OF Q4 ANSWER ===

5.
Copy your setup_for_new_machine() function from Q3
(remove the other code in this file)
to a new script and run it on a friend's machine who
is not in this class. Did it work? What problems did you run into?

Only answer this if you actually did the above.
Paste the output you got when running the script on the
new machine:

If you don't have a friend's machine, please speculate about
what might happen if you tried. You can guess.

=== ANSWER Q5 BELOW ===

I did not have a friend's machine to try this on, so this is a
speculation. I would expect the script to mostly work but run into
problems like: pip3 pointing at a different Python version than python3
(so the packages are installed for the wrong interpreter); git not being installed;
no permission to install packages system-wide (needing --user or a
virtual environment); missing compiler or build tools if a package needs to
be built from source; no network access or a firewall; and the folder
119-hw1 already existing, which makes git clone fail. A Windows machine
would also fail on the shell-specific parts.

=== END OF Q5 ANSWER ===

===== Questions 6-9: A comparison of shell vs. Python =====

The shell can also be used to process data.

This series of questions will be in the same style as part 2.
Let's import the part2 module:
"""

import part2
import pandas as pd

"""
Write two versions of a script that takes in the population.csv
file and produces as output the number of rows in the file.
The first version should use shell commands and the second
should use Pandas.

For technical reasons, you will need to use
os.popen instead of subprocess.run for the shell version.
Example:
    os.popen("echo hello").read()

Runs the command `echo hello` and returns the output as a string.

Hints:
    1. Given a file, you can print it out using
        cat filename

    2. Given a shell command, you can use the `tail` command
        to skip the first line of the output. Like this:

    (shell command that spits output) | tail -n +2

    Note: if you are curious why +2 is required here instead
        of +1, that is an odd quirk of the tail command.
        See here: https://stackoverflow.com/a/604871/2038713

    3. Given a shell command, you can use the `wc` command
        to count the number of lines in the output

   (shell command that spits output) | wc -l

NOTE:
The shell commands above require that population.csv
has a newline at the end of the file.
Otherwise, it will give an off-by-one error
FYI, if this were not the case you can replace
    cat filename
with:
    (cat filename ; echo)
.
"""

def pipeline_shell():
    # skip the header line, then count the remaining lines
    output = os.popen("cat data/population.csv | tail -n +2 | wc -l").read()
    return int(output)

def pipeline_pandas():
    df = pd.read_csv("data/population.csv")
    return len(df)

def q6():
    # As your answer to this part, check that both
    # integers are the same and return one of them.
    shell_rows = pipeline_shell()
    pandas_rows = pipeline_pandas()
    assert shell_rows == pandas_rows
    return shell_rows

"""
Let's do a performance comparison between the two methods.

Use use your ThroughputHelper and LatencyHelper classes
from part 2 to get answers for both pipelines.

Additionally, generate a plot and save it in
    output/part3-q7.png

7. Throughput
"""

# Number of rows in population.csv (the number of rows both pipelines output)
POPULATION_ROWS = pipeline_pandas()

def q7():
    # Return a list of two floats
    # [throughput for shell, throughput for pandas]
    # (in rows per second)
    h = part2.ThroughputHelper()
    h.add_pipeline("shell", POPULATION_ROWS, pipeline_shell)
    h.add_pipeline("pandas", POPULATION_ROWS, pipeline_pandas)
    throughputs = h.compare_throughput()
    h.generate_plot("output/part3-q7.png")
    return throughputs

"""
8. Latency

For latency, remember that we should create a version of the
pipeline that processes only a single row! (As in Part 2).
However, for this question only, it is OK if you choose to run
latency on the entire pipeline instead.

Additionally, generate a plot and save it in
    output/part3-q8.png
"""

def q8():
    # Return a list of two floats
    # [latency for shell, latency for pandas]
    # (in milliseconds)
    # (we run the entire pipeline here, instead of a single-row version)
    h = part2.LatencyHelper()
    h.add_pipeline("shell", pipeline_shell)
    h.add_pipeline("pandas", pipeline_pandas)
    latencies = h.compare_latency()
    h.generate_plot("output/part3-q8.png")
    return latencies

"""
9. Which method is faster?
Comment on anything else you notice below.

=== ANSWER Q9 BELOW ===

The Pandas version is faster for both throughput and latency in my run:
about 2-3.4 million rows/s for Pandas vs. about 0.3-0.6 million rows/s for the
shell pipeline, and about 17-20 ms vs. about 100-110 ms latency (the exact
numbers vary between runs). This is somewhat surprising since `wc -l` is a very
simple tool, and counting lines should be cheaper than parsing a CSV in
Pandas. The shell version has to start a new shell and three processes (cat, tail, wc)
for each run, and pipe the whole file through them, and
this process startup cost shows up in the latency. Also note that the two pipelines
do not do exactly the same thing: Pandas parses the file into columns and
types, while the shell just counts newline characters (which also means the shell
version would be wrong for fields that contain newlines in quotes).

=== END OF Q9 ANSWER ===
"""

import pytest

def test_q6_pipelines_agree():
    assert pipeline_shell() == pipeline_pandas() == 59177

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part3-answers.txt"
UNFINISHED = 0

def log_answer(name, func, *args):
    try:
        answer = func(*args)
        print(f"{name} answer: {answer}")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},{answer}\n')
            print(f"Answer saved to {ANSWER_FILE}")
    except NotImplementedError:
        print(f"Warning: {name} not implemented.")
        with open(ANSWER_FILE, 'a') as f:
            f.write(f'{name},Not Implemented\n')
        global UNFINISHED
        UNFINISHED += 1

def PART_3_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    # 2a: commentary
    # 2b: commentary
    log_answer("q3", q3)
    # 4: commentary
    # 5: commentary
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    # 9: commentary

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 3 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 3", PART_3_PIPELINE)
