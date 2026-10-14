"""
Part 2: Performance Comparisons

In this part, we will explore comparing the performance
of different pipelines.
First, we will set up some helper classes.
Then we will do a few comparisons
between two or more versions of a pipeline
to report which one is faster.
"""

import time
from contextlib import redirect_stdout
from io import StringIO

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # we only save figures; no display needed
import matplotlib.pyplot as plt

import part1

"""
=== Questions 1-5: Throughput and Latency Helpers ===

We will design and fill out two helper classes.

The first is a helper class for throughput (Q1).
The class is created by adding a series of pipelines
(via .add_pipeline(name, size, func))
where name is a title describing the pipeline,
size is the number of elements in the input dataset for the pipeline,
and func is a function that can be run on zero arguments
which runs the pipeline (like def f()).

The second is a similar helper class for latency (Q3).

1. Throughput helper class

Fill in the add_pipeline, eval_throughput, and generate_plot functions below.
"""

# Number of times to run each pipeline in the following results.
# You may modify this as you go through the file if you like, but make sure
# you set it back to 10 at the end before you submit.
NUM_RUNS = 10

class ThroughputHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline input sizes
        self.sizes = []

        # Pipeline throughputs
        # This is set to None, but will be set to a list after throughputs
        # are calculated.
        self.throughputs = None

    def add_pipeline(self, name, size, func):
        self.names.append(name)
        self.sizes.append(size)
        self.pipelines.append(func)

    def compare_throughput(self):
        # Run each pipeline NUM_RUNS times; the throughput is the total
        # number of items processed divided by the total time taken.
        self.throughputs = []
        for size, func in zip(self.sizes, self.pipelines):
            start = time.perf_counter()
            for _ in range(NUM_RUNS):
                func()
            elapsed = time.perf_counter() - start
            self.throughputs.append(size * NUM_RUNS / elapsed)
        return self.throughputs

    def generate_plot(self, filename):
        # A bar chart, one bar (and legend entry) per pipeline.
        bar_chart(self.names, self.throughputs, filename,
                  ylabel="throughput (items per second)",
                  title="Throughput of each pipeline")

def bar_chart(names, values, filename, ylabel, title):
    # Shared by both helper classes: one labeled bar per pipeline.
    fig, ax = plt.subplots(figsize=(max(6, 1.5 * len(names)), 5))
    colors = plt.cm.tab10.colors
    bars = ax.bar(range(len(names)), values,
                  color=[colors[i % len(colors)] for i in range(len(names))],
                  label=names)
    ax.bar_label(bars, fmt="%.3g", fontsize=8)
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=30, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(bars, names, fontsize=8)
    fig.tight_layout()
    fig.savefig(filename)
    plt.close(fig)

"""
As your answer to this part,
return the name of the method you decided to use in
matplotlib.

(Example: "boxplot" or "scatter")
"""

def q1():
    # Return plot method (as a string) from matplotlib
    return "bar"

"""
2. A simple test case

To make sure your monitor is working, test it on a very simple
pipeline that adds up the total of all elements in a list.

We will compare three versions of the pipeline depending on the
input size.
"""

LIST_SMALL = [10] * 100
LIST_MEDIUM = [10] * 100_000
LIST_LARGE = [10] * 100_000_000

def add_list(l):
    total = 0
    for x in l:
        total += x
    return total

def q2a():
    # Create a ThroughputHelper object
    h = ThroughputHelper()
    # Add the 3 pipelines.
    h.add_pipeline("small", len(LIST_SMALL), lambda: add_list(LIST_SMALL))
    h.add_pipeline("medium", len(LIST_MEDIUM), lambda: add_list(LIST_MEDIUM))
    h.add_pipeline("large", len(LIST_LARGE), lambda: add_list(LIST_LARGE))
    # Run the comparison and save the plot.
    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-q2a.png")
    # Finally, return the throughputs as a list.
    return throughputs

"""
2b.
Which pipeline has the highest throughput?
Is this what you expected?

=== ANSWER Q2b BELOW ===

In my run the medium list had the highest throughput (about 47 million items/s),
followed by small (about 41 million) and large (about 20 million).
(Exact numbers change from run to run.)
I expected all three to be roughly the same, since the work per item is
the same, and I did expect small to be slightly lower because the fixed cost of
calling the function is spread over only 100 items. The large list was about
2x slower per item, which I did not expect: a list of 100 million
elements takes about 800 MB, so it does not fit in cache and the loop has to
stream it from main memory.

=== END OF Q2b ANSWER ===
"""

"""
3. Latency helper class.

Now we will create a similar helper class for latency.

The helper should assume a pipeline that only has *one* element
in the input dataset.

It should use the NUM_RUNS variable as with throughput.
"""

LIST_ONE_ITEM = [10]

class LatencyHelper:
    def __init__(self):
        # Initialize the object.
        # Pipelines: a list of functions, where each function
        # can be run on no arguments.
        # (like: def f(): ... )
        self.pipelines = []

        # Pipeline names
        # A list of names for each pipeline
        self.names = []

        # Pipeline latencies
        # This is set to None, but will be set to a list after latencies
        # are calculated.
        self.latencies = None

    def add_pipeline(self, name, func):
        self.names.append(name)
        self.pipelines.append(func)

    def compare_latency(self):
        # Run each pipeline (on a single item) NUM_RUNS times and
        # report the average time of one run, in milliseconds.
        self.latencies = []
        for func in self.pipelines:
            start = time.perf_counter()
            for _ in range(NUM_RUNS):
                func()
            elapsed = time.perf_counter() - start
            self.latencies.append(elapsed / NUM_RUNS * 1000)
        return self.latencies

    def generate_plot(self, filename):
        bar_chart(self.names, self.latencies, filename,
                  ylabel="latency (milliseconds)",
                  title="Latency of each pipeline")

"""
As your answer to this part,
return the number of input items that each pipeline should
process if the class is used correctly.
"""

def q3():
    # Return the number of input items in each dataset,
    # for the latency helper to run correctly.
    return 1

"""
4. To make sure your monitor is working, test it on
the simple pipeline from Q2.

For latency, all three pipelines would only process
one item. Therefore instead of using
LIST_SMALL, LIST_MEDIUM, and LIST_LARGE,
for this question run the same pipeline three times
on a single list item.
"""

LIST_SINGLE_ITEM = [10] # Note: a list with only 1 item

def q4a():
    # Create a LatencyHelper object
    h = LatencyHelper()
    # Add the single pipeline three times.
    for i in range(1, 4):
        h.add_pipeline(f"copy {i}", lambda: add_list(LIST_SINGLE_ITEM))
    # Run the comparison and save the plot.
    latencies = h.compare_latency()
    h.generate_plot("output/part2-q4a.png")
    # Finally, return the latencies as a list.
    return latencies

"""
4b.
How much did the latency vary between the three copies of the pipeline?
Is this more or less than what you expected?

=== ANSWER Q4b BELOW ===

The three latencies were about 0.37, 0.25 and 0.23 ms; the first copy was
the slowest by about 0.1 ms, and the other two almost the same. The three pipelines are
identical, so I expected no difference; the variation is small in absolute terms
and comes from warm-up effects (cold caches/first call) and
noise from the OS at the sub-millisecond scale. It is more than I expected in relative
terms (first run ~50% slower), but not meaningful in absolute terms.

=== END OF Q4b ANSWER ===
"""

"""
Now that we have our helpers, let's do a simple comparison.

NOTE: you may add other helper functions that you may find useful
as you go through this file.

5. Comparison on Part 1

Finally, use the helpers above to calculate the throughput and latency
of the pipeline in part 1.

Remember that for latency you should use a version of the pipeline with only one input row!
You may need to write a new version of the pipeline for this to work.
"""

# You will need these:
# part1.load_input
# part1.PART_1_PIPELINE

# Number of input rows in the part 1 pipeline: 100 universities per year,
# 3 years.
PART_1_NUM_ROWS = 300

def part1_pipeline():
    # The part 1 pipeline prints a lot; keep the output quiet while timing.
    with redirect_stdout(StringIO()):
        part1.PART_1_PIPELINE()

def part1_pipeline_single_row():
    # A version of part 1 that processes a single input row per year
    # (the questions in part 1 which need all 100 rows are left out).
    with redirect_stdout(StringIO()):
        dfs = [df.head(1).copy() for df in part1.load_input()]
        part1.q1(dfs)
        part1.q2(dfs)
        part1.q3(dfs)
        part1.q7(dfs)
        part1.q9(dfs)
        avg_2021 = part1.q10_helper(dfs)
        part1.q11(avg_2021)

def q5a():
    # Return the throughput of the pipeline in part 1.
    h = ThroughputHelper()
    h.add_pipeline("part 1 pipeline", PART_1_NUM_ROWS, part1_pipeline)
    return h.compare_throughput()[0]

def q5b():
    # Return the latency of the pipeline in part 1.
    h = LatencyHelper()
    h.add_pipeline("part 1 pipeline (one row)", part1_pipeline_single_row)
    return h.compare_latency()[0]

"""
===== Questions 6-10: Performance Comparison 1 =====

For our first performance comparison,
let's look at the cost of getting input from a file, vs. in an existing DataFrame.

6. We will use the same population dataset
that we used in lecture 3.

Load the data using load_input() given the file name.

- Make sure that you clean the data by removing
  continents and world data!
  (World data is listed under OWID_WRL)

Then, set up a simple pipeline that computes summary statistics
for the following:

- *Year over year increase* in population, per country

    (min, median, max, mean, and standard deviation)

How you should compute this:

- For each country, we need the maximum year and the minimum year
in the data. We should divide the population difference
over this time by the length of the time period.

- Make sure you throw out the cases where there is only one year
(if any).

- We should at this point have one data point per country.

- Finally, as your answer, return a list of the:
    min, median, max, mean, and standard deviation
  of the data.

Hints:
You can use the describe() function in Pandas to get these statistics.
You should be able to do something like
df.describe().loc["min"]["colum_name"]

to get a specific value from the describe() function.

You shouldn't use any for loops.
See if you can compute this using Pandas functions only.
"""

def load_input(filename):
    # Return a dataframe containing the population data
    df = pd.read_csv(filename)
    df = df.rename(columns={"Population (historical)": "population"})
    # Continents and other aggregates have no country code,
    # and world data is listed under OWID_WRL.
    df = df[df["Code"].notna() & (df["Code"] != "OWID_WRL")]
    return df

def population_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation

    # First and last observation for each country
    # (sort_values returns a new dataframe so the input is not modified).
    by_country = df.sort_values(["Entity", "Year"]).groupby("Entity")
    first = by_country[["Year", "population"]].first()
    last = by_country[["Year", "population"]].last()

    # Year over year increase in population, throwing out
    # countries with only one year of data.
    years = last["Year"] - first["Year"]
    increase = (last["population"] - first["population"])[years > 0] / years[years > 0]

    stats = increase.describe()
    return [stats["min"], stats["50%"], stats["max"], stats["mean"], stats["std"]]

def q6():
    # As your answer to this part,
    # call load_input() and then population_pipeline()
    # Return a list of min, median, max, mean, and standard deviation
    df = load_input("data/population.csv")
    return [float(x) for x in population_pipeline(df)]

"""
7. Varying the input size

Next we want to set up three different datasets of different sizes.

Create three new files,
    - data/population-small.csv
      with the first 600 rows
    - data/population-medium.csv
      with the first 6000 rows
    - data/population-single-row.csv
      with only the first row
      (for calculating latency)

You can edit the csv file directly to extract the first rows
(remember to also include the header row)
and save a new file.

Make four versions of load input that load your datasets.
(The _large one should use the full population dataset.)
Each should return a dataframe.

The input CSV file will have 600 rows, but the DataFrame (after your cleaning) may have less than that.
"""

def load_input_small():
    return load_input("data/population-small.csv")

def load_input_medium():
    return load_input("data/population-medium.csv")

def load_input_large():
    return load_input("data/population.csv")

def load_input_single_row():
    # This is the pipeline we will use for latency.
    return load_input("data/population-single-row.csv")

def q7():
    # Don't modify this part
    s = load_input_small()
    m = load_input_medium()
    l = load_input_large()
    x = load_input_single_row()
    return [len(s), len(m), len(l), len(x)]

"""
8.
Create baseline pipelines

First let's create our baseline pipelines.
Create four pipelines,
    baseline_small
    baseline_medium
    baseline_large
    baseline_latency

based on the three datasets above.
Each should call your population_pipeline from Q6.

Your baseline_latency function will not be very interesting
as the pipeline does not produce any meaningful output on a single row!
You may choose to instead run an example with two rows,
or you may fill in this function in any other way that you choose
that you think is meaningful.
"""

def baseline_small():
    return population_pipeline(load_input_small())

def baseline_medium():
    return population_pipeline(load_input_medium())

def baseline_large():
    return population_pipeline(load_input_large())

def baseline_latency():
    # A single row has no year-over-year increase (the output is all NaN),
    # but this still measures the fixed cost of loading and running.
    return population_pipeline(load_input_single_row())

def q8():
    # Don't modify this part
    _ = baseline_medium()
    return ["baseline_small", "baseline_medium", "baseline_large", "baseline_latency"]

"""
9.
Finally, let's compare whether loading an input from file is faster or slower
than getting it from an existing Pandas dataframe variable.

Create four new dataframes (constant global variables)
directly in the script.
Then use these to write 3 new pipelines:
    fromvar_small
    fromvar_medium
    fromvar_large
    fromvar_latency

These pipelines should produce the same answers as in Q8.

As your answer to this part;
a. Generate a plot in output/part2-q9a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, fromvar_small, fromvar_medium, fromvar_large
b. Generate a plot in output/part2-q9b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, fromvar_latency
"""

POPULATION_SMALL = load_input_small()
POPULATION_MEDIUM = load_input_medium()
POPULATION_LARGE = load_input_large()
POPULATION_SINGLE_ROW = load_input_single_row()

def fromvar_small():
    return population_pipeline(POPULATION_SMALL)

def fromvar_medium():
    return population_pipeline(POPULATION_MEDIUM)

def fromvar_large():
    return population_pipeline(POPULATION_LARGE)

def fromvar_latency():
    return population_pipeline(POPULATION_SINGLE_ROW)

def q9a():
    # Add all 6 pipelines for a throughput comparison
    h = ThroughputHelper()
    h.add_pipeline("baseline_small", len(POPULATION_SMALL), baseline_small)
    h.add_pipeline("baseline_medium", len(POPULATION_MEDIUM), baseline_medium)
    h.add_pipeline("baseline_large", len(POPULATION_LARGE), baseline_large)
    h.add_pipeline("fromvar_small", len(POPULATION_SMALL), fromvar_small)
    h.add_pipeline("fromvar_medium", len(POPULATION_MEDIUM), fromvar_medium)
    h.add_pipeline("fromvar_large", len(POPULATION_LARGE), fromvar_large)
    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-q9a.png")
    return throughputs

def q9b():
    # Add 2 pipelines for a latency comparison
    h = LatencyHelper()
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("fromvar_latency", fromvar_latency)
    latencies = h.compare_latency()
    h.generate_plot("output/part2-q9b.png")
    return latencies

"""
10.
Comment on the plots above!
How dramatic is the difference between the two pipelines?
Which differs more, throughput or latency?
What does this experiment show?

===== ANSWER Q10 BELOW =====

The difference is substantial for throughput: reading from a variable was
about 1.6x faster for the small dataset, 2.3x for medium and about 4x for the large dataset
(for example, about 1.6 million rows/s from file vs. 6 million rows/s from the
variable). For latency the difference was smaller: about 3.1 ms from file vs.
2.0 ms from the variable (about 1.5x). So the throughput differs more than
latency. The reason is that parsing the CSV is a cost per row, so it is
spread over every row and grows with the size of the input, whereas for a
single row the latency is dominated by fixed overhead of starting pandas
operations (groupby, describe etc.), which is the same in both pipelines.
The experiment shows that if you process the same data many times (or many rows),
you should load it once and keep it in memory; file I/O and parsing are a
big part of the cost of the pipeline.

===== END OF Q10 ANSWER =====
"""

"""
===== Questions 11-14: Performance Comparison 2 =====

Our second performance comparison will explore vectorization.

Operations in Pandas use Numpy arrays and vectorization to enable
fast operations.
In particular, they are often much faster than using for loops.

Let's explore whether this is true!

11.
First, we need to set up our pipelines for comparison as before.

We already have the baseline pipelines from Q8,
so let's just set up a comparison pipeline
which uses a for loop to calculate the same statistics.

Your pipeline should produce the same answers as in Q6 and Q8.

Create a new pipeline:
- Iterate through the dataframe entries. You can assume they are sorted.
- Manually compute the minimum and maximum year for each country.
- Compute the same answers as in Q6.
- Manually compute the summary statistics for the resulting list (min, median, max, mean, and standard deviation).
"""

def for_loop_pipeline(df):
    # Input: the dataframe from load_input()
    # Return a list of min, median, max, mean, and standard deviation

    # For each country: [min year, population then, max year, population then]
    extremes = {}
    for entity, year, population in zip(df["Entity"], df["Year"], df["population"]):
        if entity not in extremes:
            extremes[entity] = [year, population, year, population]
            continue
        entry = extremes[entity]
        if year < entry[0]:
            entry[0], entry[1] = year, population
        if year > entry[2]:
            entry[2], entry[3] = year, population

    # Year over year increase, skipping countries with a single year
    increases = []
    for min_year, min_pop, max_year, max_pop in extremes.values():
        if max_year > min_year:
            increases.append((max_pop - min_pop) / (max_year - min_year))

    n = len(increases)
    if n == 0:
        return [float("nan")] * 5

    # Summary statistics, computed by hand
    increases.sort()
    mid = n // 2
    median = increases[mid] if n % 2 == 1 else (increases[mid - 1] + increases[mid]) / 2
    mean = sum(increases) / n
    if n > 1:
        # sample standard deviation, as Pandas does
        variance = sum((x - mean) ** 2 for x in increases) / (n - 1)
        std = variance ** 0.5
    else:
        std = float("nan")
    return [increases[0], median, increases[-1], mean, std]

def q11():
    # As your answer to this part, call load_input() and then
    # for_loop_pipeline() to return the 5 numbers.
    # (these should match the numbers you got in Q6.)
    # ** Please return these as Python floats, not Numpy **
    df = load_input("data/population.csv")
    return [float(x) for x in for_loop_pipeline(df)]

"""
12.
Now, let's create our pipelines for comparison.

As before, write 4 pipelines based on the datasets from Q7.
"""

def for_loop_small():
    return for_loop_pipeline(load_input_small())

def for_loop_medium():
    return for_loop_pipeline(load_input_medium())

def for_loop_large():
    return for_loop_pipeline(load_input_large())

def for_loop_latency():
    return for_loop_pipeline(load_input_single_row())

def q12():
    # Don't modify this part
    _ = for_loop_medium()
    return ["for_loop_small", "for_loop_medium", "for_loop_large", "for_loop_latency"]

"""
13.
Finally, let's compare our two pipelines,
as we did in Q9.

a. Generate a plot in output/part2-q13a.png of the throughputs
    Return the list of 6 throughputs in this order:
    baseline_small, baseline_medium, baseline_large, for_loop_small, for_loop_medium, for_loop_large

b. Generate a plot in output/part2-q13b.png of the latencies
    Return the list of 2 latencies in this order:
    baseline_latency, for_loop_latency
"""

def q13a():
    # Add all 6 pipelines for a throughput comparison
    # (sizes are the number of rows of each cleaned dataset)
    h = ThroughputHelper()
    h.add_pipeline("baseline_small", len(POPULATION_SMALL), baseline_small)
    h.add_pipeline("baseline_medium", len(POPULATION_MEDIUM), baseline_medium)
    h.add_pipeline("baseline_large", len(POPULATION_LARGE), baseline_large)
    h.add_pipeline("for_loop_small", len(POPULATION_SMALL), for_loop_small)
    h.add_pipeline("for_loop_medium", len(POPULATION_MEDIUM), for_loop_medium)
    h.add_pipeline("for_loop_large", len(POPULATION_LARGE), for_loop_large)
    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-q13a.png")
    return throughputs

def q13b():
    # Add 2 pipelines for a latency comparison
    h = LatencyHelper()
    h.add_pipeline("baseline_latency", baseline_latency)
    h.add_pipeline("for_loop_latency", for_loop_latency)
    latencies = h.compare_latency()
    h.generate_plot("output/part2-q13b.png")
    return latencies

"""
14.
Comment on the results you got!

14a. Which pipelines is faster in terms of throughput?

===== ANSWER Q14a BELOW =====

It depends on the input size, and this includes file loading time for both
pipelines. For the small dataset the for loop was faster
(about 190k vs. 70k rows/s) and for the medium dataset
it was slightly faster (about 930k vs. 790k), but for the large dataset
the vectorized Pandas pipeline had the higher throughput
(about 1.5M vs. 1.2M rows/s).

===== END OF Q14a ANSWER =====

14b. Which pipeline is faster in terms of latency?

===== ANSWER Q14b BELOW =====

The for loop pipeline was faster in terms of latency (about 1 ms vs. about
3.4 ms for the baseline) for a single row. Pandas operations like
groupby/sort/describe have a fixed overhead of several milliseconds, whereas the
for loop does almost no work for a single row.

===== END OF Q14b ANSWER =====

14c. Do you notice any other interesting observations?
What does this experiment show?

===== ANSWER Q14c BELOW =====

The result that vectorization is always faster did not hold for small
inputs: the fixed overhead of Pandas operations dominates, and the plain
Python loop wins. The advantage of vectorization only appears as the input
gets larger (the large dataset in our case); there is a crossover point
somewhere between the medium and large sizes. Also, for both pipelines
a big part of the time is reading the CSV file (as in Q9: the pandas pipeline
runs about 4x faster when the input is already in memory),
which hides the difference in computing the statistics, so the gap between
vectorized and the loop would be larger if both were run from variables.
This experiment shows that "vectorized is faster" is only true when the data is large
enough to amortize the overhead, and the best choice depends on the workload.

===== END OF Q14c ANSWER =====
"""

"""
===== Questions 15-17: Reflection Questions =====
15.

Take a look at all your pipelines above.
Which factor that we tested (file vs. variable, vectorized vs. for loop)
had the biggest impact on performance?

===== ANSWER Q15 BELOW =====

Loading from file vs. from a variable had the largest impact: up to about 4x
in throughput on the large dataset (and consistently faster at all sizes).
Vectorized vs. for loop changed throughput by less than 2.6x and in
different directions depending on the input size (for loop 2.6x faster on small,
vectorized 1.3x faster on large), so its effect is smaller and
less consistent.

===== END OF Q15 ANSWER =====

16.
Based on all of your plots, form a hypothesis as to how throughput
varies with the size of the input dataset.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q16 BELOW =====

Hypothesis: throughput increases with the size of the dataset (before it
levels off), because each pipeline has a fixed overhead per run that is
spread over more rows for larger inputs. The data supports this: the baseline went from
about 70k rows/s (small) to 790k (medium) to 1.5M (large), and the
from-variable pipeline went from about 115k to 1.8M to 6.1M rows/s.
The simple add_list pipeline, which has almost no fixed overhead, stayed about constant
(about 40-47M items/s) and then dropped for the very large list (about 20M items/s)
once the data no longer fit in cache/memory bandwidth became the limit.

===== END OF Q16 ANSWER =====

17.
Based on all of your plots, form a hypothesis as to how
throughput is related to latency.

(Any hypothesis is OK as long as it is supported by your data!
This is an open ended question.)

===== ANSWER Q17 BELOW =====

Hypothesis: throughput and latency are inversely related through the fixed
overhead of a pipeline: for a small input the time of a run is
mostly the latency, so throughput is approximately (number of items) / latency,
and pipelines with a higher latency have lower throughput
at small sizes. For example, the baseline had a latency of about 3 ms and a
small-input throughput of about 70k rows/s (261 rows / 3.7 ms), while the from
variable pipeline with a lower latency (2 ms) had a higher throughput (about
115k rows/s). As the input grows, throughput depends more on the per-item cost than on the latency,
so a pipeline with low latency (like the for loop) does not necessarily have
the highest throughput on large inputs.

===== END OF Q17 ANSWER =====
"""

"""
===== Extra Credit =====

This part is optional.

Use your pipeline to compare something else!

Here are some ideas for what to try:
- the cost of random sampling vs. the cost of getting rows from the
  DataFrame manually
- the cost of cloning a DataFrame
- the cost of sorting a DataFrame prior to doing a computation
- the cost of using different encodings (like one-hot encoding)
  and encodings for null values
- the cost of querying via Pandas methods vs querying via SQL
  For this part: you would want to use something like
  pandasql that can run SQL queries on Pandas data frames. See:
  https://stackoverflow.com/a/45866311/2038713

As your answer to this part,
as before, return
a. the list of 6 throughputs
and
b. the list of 2 latencies.

and generate plots for each of these in the following files:
    output/part2-ec-a.png
    output/part2-ec-b.png
"""

# Extra credit (optional)

# Extra credit: what is the cost of cloning the DataFrame before running
# the pipeline (compared with the fromvar pipelines from Q9)?

def clone_small():
    return population_pipeline(POPULATION_SMALL.copy())

def clone_medium():
    return population_pipeline(POPULATION_MEDIUM.copy())

def clone_large():
    return population_pipeline(POPULATION_LARGE.copy())

def clone_latency():
    return population_pipeline(POPULATION_SINGLE_ROW.copy())

def extra_credit_a():
    h = ThroughputHelper()
    h.add_pipeline("fromvar_small", len(POPULATION_SMALL), fromvar_small)
    h.add_pipeline("fromvar_medium", len(POPULATION_MEDIUM), fromvar_medium)
    h.add_pipeline("fromvar_large", len(POPULATION_LARGE), fromvar_large)
    h.add_pipeline("clone_small", len(POPULATION_SMALL), clone_small)
    h.add_pipeline("clone_medium", len(POPULATION_MEDIUM), clone_medium)
    h.add_pipeline("clone_large", len(POPULATION_LARGE), clone_large)
    throughputs = h.compare_throughput()
    h.generate_plot("output/part2-ec-a.png")
    return throughputs

def extra_credit_b():
    h = LatencyHelper()
    h.add_pipeline("fromvar_latency", fromvar_latency)
    h.add_pipeline("clone_latency", clone_latency)
    latencies = h.compare_latency()
    h.generate_plot("output/part2-ec-b.png")
    return latencies

import pytest

def test_q1():
    assert q1() == "bar"

def test_q3():
    assert q3() == 1

def test_q6_matches_for_loop():
    # the vectorized and for loop pipelines should agree (Q6 vs Q11)
    assert q6() == pytest.approx(q11())

def test_q7():
    assert q7() == [261, 5122, 55240, 1]

"""
===== Wrapping things up =====

**Don't modify this part.**

To wrap things up, we have collected
your answers and saved them to a file below.
This will be run when you run the code.
"""

ANSWER_FILE = "output/part2-answers.txt"
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

def PART_2_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    # Q1-5
    log_answer("q1", q1)
    log_answer("q2a", q2a)
    # 2b: commentary
    log_answer("q3", q3)
    log_answer("q4a", q4a)
    # 4b: commentary
    log_answer("q5a", q5a)
    log_answer("q5b", q5b)

    # Q6-10
    log_answer("q6", q6)
    log_answer("q7", q7)
    log_answer("q8", q8)
    log_answer("q9a", q9a)
    log_answer("q9b", q9b)
    # 10: commentary

    # Q11-14
    log_answer("q11", q11)
    log_answer("q12", q12)
    log_answer("q13a", q13a)
    log_answer("q13b", q13b)
    # 14: commentary

    # 15-17: reflection
    # 15: commentary
    # 16: commentary
    # 17: commentary

    # Extra credit
    log_answer("extra credit (a)", extra_credit_a)
    log_answer("extra credit (b)", extra_credit_b)

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
=== END OF PART 2 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 2", PART_2_PIPELINE)
