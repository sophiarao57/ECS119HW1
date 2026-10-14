"""
Part 1: Data Processing in Pandas

=== Instructions ===

There are 22 questions in this part.
For each part you will implement a function (q1, q2, etc.)
Each function will take as input a data frame
or a list of data frames and return the answer
to the given question.

To run your code, you can run `python3 part1.py`.
This will run all the questions that you have implemented so far.
It will also save the answers to part1-answers.txt.

=== Dataset ===

In this part, we will use a dataset of world university rankings
called the "QS University Rankings".

The ranking data was taken 2019--2021 from the following website:
https://www.topuniversities.com/university-rankings/world-university-rankings/2021

=== Grading notes ===

- Once you have completed this part, make sure that
  your code runs, that part1-answers.txt is being re-generated
  every time the code is run, and that the answers look
  correct to you.

- Be careful about output types. For example if the question asks
  for a list of DataFrames, don't return a numpy array or a single
  DataFrame. When in doubt, ask on Piazza!

- Make sure that you remove any NotImplementedError exceptions;
  you won't get credit for any part that raises this exception
  (but you will still get credit for future parts that do not raise it
  if they don't depend on the previous parts).

- Make sure that you fill in answers for the parts
  marked "ANSWER ___ BELOW" and that you don't modify
  the lines above and below the answer space.

- Q6 has a few unit tests to help you check your work.
  Make sure that you removed the `@pytest.mark.skip` decorators
  and that all tests pass (show up in green, no red text!)
  when you run `pytest part3.py`.

- For plots: There are no specific requirements on which
  plotting methods you use; if not specified, use whichever
  plot you think might be most appropriate for the data
  at hand.
  Please ensure your plots are labeled and human-readable.
  For example, call .legend() on the plot before saving it!

===== Questions 1-6: Getting Started =====

To begin, let's load the Pandas library.
"""

import pandas as pd

"""
1. Load the dataset into Pandas

Our first step is to load the data into a Pandas DataFrame.
We will also change the column names
to lowercase and reorder to get only the columns we are interested in.

Implement the rest of the function load_input()
by filling in the parts marked TODO below.

Return as your answer to q1 the number of dataframes loaded.
(This part is implemented for you.)
"""

NEW_COLUMNS = ['rank', 'university', 'region', 'academic reputation', 'employer reputation', 'faculty student', 'citations per faculty', 'overall score']

def load_input():
    """
    Input: None
    Return: a list of 3 dataframes, one for each year.
    """

    # Load the input files and return them as a list of 3 dataframes.
    df_2019 = pd.read_csv('data/2019.csv', encoding='latin-1')
    df_2020 = pd.read_csv('data/2020.csv', encoding='latin-1')
    df_2021 = pd.read_csv('data/2021.csv', encoding='latin-1')

    # Standardizing the column names
    df_2019.columns = df_2019.columns.str.lower()
    df_2020.columns = df_2020.columns.str.lower()
    df_2021.columns = df_2021.columns.str.lower()

    # Restructuring the column indexes
    # Keep only the columns we are interested in, in the new order.
    df_2019 = df_2019[NEW_COLUMNS].copy()
    df_2020 = df_2020[NEW_COLUMNS].copy()
    df_2021 = df_2021[NEW_COLUMNS].copy()

    return [df_2019, df_2020, df_2021]

def q1(dfs):
    # As the "answer" to this part, let's just return the number of dataframes.
    # Check that your answer shows up in part1-answers.txt.
    return len(dfs)

"""
2. Input validation

Let's do some basic sanity checks on the data for Q1.

Check that all three data frames have the same shape,
and the correct number of rows and columns in the correct order.

As your answer to q2, return True if all validation checks pass,
and False otherwise.
"""

def q2(dfs):
    """
    Input: Assume the input is provided by load_input()

    Return: True if all validation checks pass, False otherwise.

    Make sure you return a Boolean!
    From this part onward, we will not provide the return
    statement for you.
    You can check that the "answers" to each part look
    correct by inspecting the file part1-answers.txt.
    """
    # Same shape across all three years
    if len({df.shape for df in dfs}) != 1:
        return False
    # 100 universities (rows) and 8 columns
    if dfs[0].shape != (100, len(NEW_COLUMNS)):
        return False
    # Columns are listed in the correct order
    return all(list(df.columns) == NEW_COLUMNS for df in dfs)

"""
===== Interlude: Checking your output so far =====

Run your code with `python3 part1.py` and open up the file
output/part1-answers.txt to see if the output looks correct so far!

You should check your answers in this file after each part.

You are welcome to also print out stuff to the console
in each question if you find it helpful.
"""

ANSWER_FILE = "output/part1-answers.txt"

def interlude():
    print("Answers so far:")
    with open(f"{ANSWER_FILE}") as fh:
        print(fh.read())

"""
===== End of interlude =====

3a. Input validation, continued

Now write a validate another property: that the set of university names
in each year is the same.
As in part 2, return a Boolean value.
(True if they are the same, and False otherwise)

Once you implement and run your code,
remember to check the output in part1-answers.txt.
(True if the checks pass, and False otherwise)
"""

def q3(dfs):
    name_sets = [set(df["university"]) for df in dfs]
    return all(names == name_sets[0] for names in name_sets)

"""
3b (commentary).
Did the checks pass or fail?
Comment below and explain why.

=== ANSWER Q3b BELOW ===

The check fails (q3 returns False). 2019 and 2020 do not contain the same
universities: three universities in the 2019 top 100 (Eindhoven University of
Technology, Purdue University, The Ohio State University) are not in 2020,
while three others (KTH Royal Institute of Technology, Sungkyunkwan
University, The Hong Kong Polytechnic University) entered the top 100 in 2020.
This is expected: the dataset is the top 100 of each year's ranking, so
universities near the cutoff move in and out as scores change. 2020 and 2021
contain the same set of names (they are almost identical files; see Q12a).

=== END OF Q3b ANSWER ===
"""

"""
4. Random sampling

Now that we have the input data validated, let's get a feel for
the dataset we are working with by taking a random sample of 5 rows
at a time.

Implement q4() below to sample 5 points from each year's data.

As your answer to this part, return the *university name*
of the 5 samples *for 2021 only* as a list.
(That is: ["University 1", "University 2", "University 3", "University 4", "University 5"])

Code design: You can use a for for loop to iterate over the dataframes.
If df is a DataFrame, df.sample(5) returns a random sample of 5 rows.

Hint:
    to get the university name:
    try .iloc on the sample, then ["university"].
"""

def q4(dfs):
    samples = []
    for year, df in zip([2019, 2020, 2021], dfs):
        sample = df.sample(5)
        print(f"Random sample of 5 rows from {year}:")
        print(sample)
        samples.append(sample)

    # Answer as a list of 5 university names (2021 only)
    return list(samples[-1]["university"])

"""
Once you have implemented this part,
you can run a few times to see different samples.

4b (commentary).
Based on the data, write down at least 2 strengths
and 3 weaknesses of this dataset.
This is subjective - you may interpret this however you like!
If you were to use this dataset for a project, what would *you* consider to be
some advantages and drawbacks?

=== ANSWER Q4b BELOW ===

Strengths:
1. Clean and small: 100 rows per year, no missing values, and consistent
   column names/types, so it is easy to load, join across years and plot.
2. Covers several indicators (academic/employer reputation, faculty-student
   ratio, citations) plus region, so we can compare universities and
   countries on more than a single number, and look at change over time.

Weaknesses:
1. Only the top 100 universities are included, so there is selection bias:
   we cannot say anything about universities outside the top 100 or about
   what separates ranks 100 and 101.
2. The 2021 file is nearly identical to 2020 (flawed data), and only three
   years are available, so trend analysis is weak. The university names also
   differ between years (e.g. "UCL", "Sungkyunkwan University(SKKU)"),
   which makes matching fragile.
3. Reputation scores come from subjective surveys, scores are normalized
   (capped at 100), and the ranking methodology/weights are not documented
   in the data. Some columns (international faculty/students) were dropped
   and there are many rank ties, so the scores are hard to interpret causally.

=== END OF Q4b ANSWER ===
"""

"""
5. Data cleaning

Let's see where we stand in terms of null values.
We can do this in two different ways.

a. Use .info() to see the number of non-null values in each column
displayed in the console.

b. Write a version using .count() to calculate the number of
non-null values in each column.

In both 5a and 5b: return as your answer
*for the 2021 data only*
as a list of the number of non-null values in each column.

Example: if there are 5 non-null values in the first column, 3 in the second, 4 in the third, and so on, you would return
    [5, 3, 4, ...]
"""

def q5a(dfs):
    # Prints the non-null count of each column for 2021
    dfs[2].info()
    # .info() does not return anything, so the counts below were copied
    # from its output: all 8 columns have 100 non-null entries.
    return [100, 100, 100, 100, 100, 100, 100, 100]

def q5b(dfs):
    return [int(n) for n in dfs[2].count()]

"""
5c.
One other thing:
Also fill this in with how many non-null values are expected (for the 2021 data).
This should be a list for each column as before.
We will use this in the unit tests below.
"""

def q5c():
    # 100 universities and no missing values, for each of the 8 columns
    num_non_null = [100] * len(NEW_COLUMNS)
    return num_non_null

"""
===== Interlude again: Unit tests =====

Unit tests

Now that we have completed a few parts,
let's talk about unit tests.
We won't be using them for the entire assignment
(in fact we won't be using them after this),
but they can be a good way to ensure your work is correct
without having to manually inspect the output.

We need to import pytest first.
"""

import pytest

"""
The following are a few unit tests for Q1-5.

To run the unit tests,
first, remove (or comment out) the `@pytest.mark.skip` decorator
from each unit test (function beginning with `test_`).
Then, run `pytest part1.py` in the terminal.
"""

def test_q1():
    dfs = load_input()
    assert len(dfs) == 3
    assert all([isinstance(df, pd.DataFrame) for df in dfs])

def test_q2():
    dfs = load_input()
    assert q2(dfs)

@pytest.mark.xfail
def test_q3():
    dfs = load_input()
    assert q3(dfs)

def test_q4():
    dfs = load_input()
    samples = q4(dfs)
    assert len(samples) == 5

def test_q5():
    dfs = load_input()
    num_non_null = q5c()
    assert len(num_non_null) > 0
    assert q5a(dfs) == num_non_null
    assert q5b(dfs) == num_non_null

"""
6a. Are there any tests which fail?

=== ANSWER Q6a BELOW ===

test_q3 fails: q3(dfs) returns False, so `assert q3(dfs)` raises an AssertionError.
All other tests (test_q1, test_q2, test_q4, test_q5) pass.

=== END OF Q6a ANSWER ===

6b. For each test that fails, is it because your code
is wrong or because the test is wrong?

=== ANSWER Q6b BELOW ===

The test is wrong, not the code. The data genuinely differs between years
(3 universities left and 3 joined the top 100 between 2019 and 2020), so
the correct answer of q3 is False. The assertion that the sets are equal does
not hold for this dataset, so test_q3 is marked @pytest.mark.xfail.

=== END OF Q6b ANSWER ===

IMPORTANT: for any failing tests, if you think you have
not made any mistakes, mark it with
@pytest.mark.xfail
above the test to indicate that the test is expected to fail.
Run pytest part1.py again to see the new output.

6c. Return the number of tests that failed, even after your
code was fixed as the answer to this part.
(As an integer)
Please include expected failures (@pytest.mark.xfail).
(If you have no failing or xfail tests, return 0.)
"""

def q6c():
    # Only test_q3 fails (marked xfail above)
    return 1

"""
===== End of interlude =====

===== Questions 7-10: Data Processing =====

7. Adding columns

Notice that there is no 'year' column in any of the dataframe. As your first task, append an appropriate 'year' column in each dataframe.

Append a column 'year' in each dataframe. It must correspond to the year for which the data is represented.

As your answer to this part, return the number of columns in each dataframe after the addition.
"""

def q7(dfs):
    for year, df in zip([2019, 2020, 2021], dfs):
        df["year"] = year
    return [df.shape[1] for df in dfs]

"""
8a.
Next, find the count of universities in each region that made it to the Top 100 each year. Print all of them.

As your answer, return the count for "USA" in 2021.
"""

def q8a(dfs):
    counts = {}
    for year, df in zip([2019, 2020, 2021], dfs):
        top_100 = df[df["rank"] <= 100]
        counts[year] = top_100.groupby("region").size().sort_values(ascending=False)
        print(f"Universities per region in the top 100 in {year}:")
        print(counts[year])
    return int(counts[2021]["USA"])

"""
8b.
Do you notice some trend? Comment on what you observe and why might that be consistent throughout the years.

=== ANSWER Q8b BELOW ===

The USA has the most universities in the top 100 in every year (30, 29, 29),
followed by the UK (18-19), China (11), and Australia (6-7). The
counts of every region barely change from year to year.
This is consistent because the rankings change slowly: reputation surveys,
citation counts and research funding/infrastructure of established universities
take decades to build up, and the dominant countries (US, UK) have a large
head start in funding, English-language publishing (which drives citations
and reputation) and old, well-endowed universities.

=== END OF Q8b ANSWER ===
"""

"""
9.
From the data of 2021, find the average score of all attributes for all universities.

As your answer, return the list of averages (for all attributes)
in the order they appear in the dataframe:
academic reputation, employer reputation, faculty student, citations per faculty, overall score.

The list should contain 5 elements.
"""

def q9(dfs):
    attributes = ["academic reputation", "employer reputation",
                  "faculty student", "citations per faculty", "overall score"]
    return [float(x) for x in dfs[2][attributes].mean()]

"""
10.
From the same data of 2021, now find the average of *each* region for **all** attributes **excluding** 'rank' and 'year'.

In the function q10_helper, store the results in a variable named **avg_2021**
and return it.

Then in q10, print the first 5 rows of the avg_2021 dataframe.
"""

def q10_helper(dfs):
    df_2021 = dfs[2]
    avg_2021 = (df_2021
                .drop(columns=["rank", "year", "university"])
                .groupby("region")
                .mean())
    return avg_2021

def q10(avg_2021):
    """
    Input: the avg_2021 dataframe
    Print: the first 5 rows of the dataframe

    As your answer, simply return the number of rows printed.
    (That is, return the integer 5)
    """
    print(avg_2021.head(5))
    return 5

"""
===== Questions 11-14: Exploring the avg_2021 dataframe =====

11.
Sort the avg_2021 dataframe from the previous question based on overall score in a descending fashion (top to bottom).

As your answer to this part, return the first row of the sorted dataframe.
"""

def q11(avg_2021):
    sorted_avg = avg_2021.sort_values("overall score", ascending=False)
    print(sorted_avg)
    return sorted_avg.iloc[0]

"""
12a.
What do you observe from the table above? Which country tops the ranking?

What is one country that went down in the rankings
between 2019 and 2021?

You will need to load the data from 2019 to get the answer to this part.
You may choose to do this
by writing another function like q10_helper and running q11,
or you may just do it separately
(e.g., in a Python shell) and return the name of the country/region
that you found went down in the rankings.

Errata: please note that the 2021 dataset we provided is flawed
(it is almost identical to the 2020 data).
This is why the question now asks for the difference between 2019 and 2021.

For the answer to this part return the name of the country/region that tops the ranking
and the name of one country/region that went down in the rankings.
"""

def q12a(avg_2021):
    # Region at the top of the 2021 ranking
    top_region = avg_2021["overall score"].idxmax()

    # Compare average overall score by region in 2019 vs. 2021
    dfs = load_input()
    avg_2019 = dfs[0].groupby("region")["overall score"].mean()
    change = avg_2021["overall score"] - avg_2019
    print("Change in average overall score, 2019 to 2021:")
    print(change.dropna().sort_values())
    # Region with the largest drop in average score
    down_region = change.dropna().idxmin()
    return (top_region, down_region)

"""
12b.
Comment on why the country above is at the top of the list.
(Note: This is an open-ended question.)

=== ANSWER Q12b BELOW ===

Singapore tops the regional ranking with an average overall score of 91.8,
but note that it only has two universities in the data (NUS and NTU),
both of which score very high, so the average is based on a very small
sample. Singapore does well because it invests heavily in a few research
universities, has a very high faculty/student ratio (100), high citations
per faculty (95.9) and a strong international outlook, and the country has
no weaker universities in the top 100 to pull the average down. Large
countries like the USA or UK have many universities in the list,
including lower-ranked ones, which lowers their average. Between 2019 and 2021 the
average score of South Korea went down the most (-2.35).

=== END OF Q12b ANSWER ===
"""

"""
13a.
Represent all the attributes in the avg_2021 dataframe using a box and whisker plot.

Store your plot in output/part1-13a.png.

As the answer to this part, return the name of the plot you saved.

**Hint:** You can do this using subplots (and also otherwise)
"""

import matplotlib
matplotlib.use("Agg")  # we only save figures; no display needed
import matplotlib.pyplot as plt

def q13a(avg_2021):
    # One subplot per attribute so each box has its own scale
    fig, axes = plt.subplots(1, len(avg_2021.columns), figsize=(14, 5))
    for ax, column in zip(axes, avg_2021.columns):
        ax.boxplot(avg_2021[column].dropna())
        ax.set_title(column)
        ax.set_xticks([])
        ax.set_ylabel("average score (0-100)")
    fig.suptitle("Distribution of regional average scores by attribute (2021)")
    fig.tight_layout()
    fig.savefig("output/part1-13a.png")
    plt.close(fig)
    return "output/part1-13a.png"

"""
b. Do you observe any anomalies in the box and whisker
plot?

=== ANSWER Q13b BELOW ===

Yes. The attributes are on very different scales and spreads: citations per
faculty and overall score are tightly clustered (overall 61-92, citations
59-96), while academic reputation ranges from 2.4 (Argentina) to 85 and has a very
wide box. Overall score has a high outlier: Singapore (91.8), far above the
other regions (the next one is Canada at 81). The very low academic
reputation values (Argentina 2.4, Russia 7.2) are also outliers
compared to the median. These are averages of very few universities for
some regions (many regions have only 1 or 2 universities), so these outliers
are driven by small sample sizes rather than by whole countries.

=== END OF Q13b ANSWER ===
"""

"""
14a.
Pick two attributes in the avg_2021 dataframe
and represent them using a scatter plot.

Store your plot in output/part1-14a.png.

As the answer to this part, return the name of the plot you saved.
"""

def q14a(avg_2021):
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(avg_2021["academic reputation"], avg_2021["overall score"],
               label="region")
    for region, row in avg_2021.iterrows():
        ax.annotate(region, (row["academic reputation"], row["overall score"]),
                    fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.set_xlabel("average academic reputation")
    ax.set_ylabel("average overall score")
    ax.set_title("Academic reputation vs. overall score by region (2021)")
    ax.legend()
    fig.tight_layout()
    fig.savefig("output/part1-14a.png")
    plt.close(fig)
    return "output/part1-14a.png"

"""
Do you observe any general trend?

=== ANSWER Q14b BELOW ===

There is a positive trend: regions with a higher average academic reputation tend
to have a higher overall score, although it is quite noisy (some regions such
as Belgium and the Netherlands have high reputation but only an average
overall score, and Canada has low reputation but a high overall score).
This agrees with the correlation matrix, where academic reputation and
overall score have a modest positive correlation (about 0.39).

=== END OF Q14b ANSWER ===

===== Questions 15-20: Exploring the data further =====

We're more than halfway through!

Let's come to the Top 10 Universities and observe how they performed over the years.

15. Create a smaller dataframe which has the top ten universities from each year, and only their overall scores across the three years.

Hint:

*   There will be four columns in the dataframe you make
*   The top ten universities are same across the three years. Only their rankings differ.
*   Use the merge function. You can read more about how to use it in the documentation: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.merge.html
*   Shape of the resultant dataframe should be (10, 4)

As your answer, return the shape of the new dataframe.
"""

def q15_helper(dfs):
    # Top ten universities of each year with only their overall scores
    tops = [df[df["rank"] <= 10][["university", "overall score"]] for df in dfs]
    # Merging on the university name auto-assigns suffixes to the score columns
    top_10 = tops[0].merge(tops[1], on="university").merge(tops[2], on="university")
    return top_10

def q15(top_10):
    return top_10.shape

"""
16.
You should have noticed that when you merged,
Pandas auto-assigned the column names. Let's change them.

For the columns representing scores, rename them such that they describe the data that the column holds.

You should be able to modify the column names directly in the dataframe.
As your answer, return the new column names as a list.
"""

def q16(top_10):
    top_10.columns = ["university", "overall score 2019",
                      "overall score 2020", "overall score 2021"]
    return list(top_10.columns)

"""
17a.
Draw a suitable plot to show how the overall scores of the Top 10 universities varied over the three years. Clearly label your graph and attach a legend. Explain why you chose the particular plot.

Save your plot in output/part1-17a.png.

As the answer to this part, return the name of the plot you saved.

Note:
*   All universities must be in the same plot.
*   Your graph should be clear and legend should be placed suitably
"""

def q17a(top_10):
    # A line chart (one line per university) makes it easy to see
    # how each university's score changes from year to year.
    years = [2019, 2020, 2021]
    fig, ax = plt.subplots(figsize=(10, 6))
    for _, row in top_10.iterrows():
        ax.plot(years, row.iloc[1:].astype(float), marker="o", label=row["university"])
    ax.set_xticks(years)
    ax.set_xlabel("year")
    ax.set_ylabel("overall score")
    ax.set_title("Overall score of the top 10 universities, 2019-2021")
    ax.legend(loc="center left", bbox_to_anchor=(1, 0.5), fontsize=8)
    fig.tight_layout()
    fig.savefig("output/part1-17a.png")
    plt.close(fig)
    return "output/part1-17a.png"

"""
17b.
What do you observe from the plot above? Which university has remained consistent in their scores? Which have increased/decreased over the years?

=== ANSWER Q17b BELOW ===

MIT stays at 100 in all three years, and is the most consistent. Stanford (98.6 ->
98.4), Harvard (98.5 -> 97.4), Caltech (97.2 -> 96.9), Cambridge (95.6 -> 95.0) and the
University of Chicago (93.2 -> 92.0) went down slightly. Oxford (96.8 -> 97.2), ETH Zurich
(95.3 -> 95.9), Imperial (93.3 -> 94.1) and UCL (92.9 -> 94.8) went up.
Note that 2020 and 2021 are identical (the flawed data) so all changes
happen between 2019 and 2020 and the lines are flat afterwards.
A line plot is appropriate since it shows change over time for each university,
with a small number of series so that the legend stays readable.

=== END OF Q17b ANSWER ===
"""

"""
===== Questions 18-19: Correlation matrices =====

We're almost done!

Let's look at another useful tool to get an idea about how different variables are corelated to each other. We call it a **correlation matrix**

A correlation matrix provides a correlation coefficient (a number between -1 and 1) that tells how strongly two variables are correlated. Values closer to -1 mean strong negative correlation whereas values closer to 1 mean strong positve correlation. Values closer to 0 show variables having no or little correlation.

You can learn more about correlation matrices from here: https://www.statology.org/how-to-read-a-correlation-matrix/

18.
Plot a correlation matrix to see how each variable is correlated to another. You can use the data from 2021.

Print your correlation matrix and save it in output/part1-18.png.

As the answer to this part, return the name of the plot you saved.

**Helpful link:** https://datatofish.com/correlation-matrix-pandas/
"""

def q18(dfs):
    # Correlation matrix of the numeric columns of the 2021 data
    # (year is constant, so it has no correlation with anything)
    numeric = dfs[2].select_dtypes("number").drop(columns=["year"])
    corr = numeric.corr()
    print(corr)

    fig, ax = plt.subplots(figsize=(8, 7))
    image = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(corr.columns)))
    ax.set_yticklabels(corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    fig.colorbar(image, ax=ax, label="correlation coefficient")
    ax.set_title("Correlation matrix of 2021 attributes")
    fig.tight_layout()
    fig.savefig("output/part1-18.png")
    plt.close(fig)
    return "output/part1-18.png"

"""
19. Comment on at least one entry in the matrix you obtained in the previous
part that you found surprising or interesting.

=== ANSWER Q19 BELOW ===

The correlation between employer reputation and faculty/student ratio is 0.69,
which is by far the strongest between two different indicators, and
was surprising: I expected the employer survey to be unrelated to
staffing ratios. A possible explanation is that wealthy, well-known
universities do well on both. Also interesting: citations per faculty
(0.77) correlates with overall score much more than academic reputation
(0.39), and academic reputation is almost uncorrelated with citations (0.10),
which suggests that the reputation survey and the research output measure
different things. Rank has a -0.99 correlation with overall score, as expected.

=== END OF Q19 ANSWER ===
"""

"""
===== Questions 20-23: Data manipulation and falsification =====

This is the last section.

20. Exploring data manipulation and falsification

For fun, this part will ask you to come up with a way to alter the
rankings such that your university of choice comes out in 1st place.

The data does not contain UC Davis, so let's pick a different university.
UC Berkeley is a public university nearby and in the same university system,
so let's pick that one.

We will write two functions.
a.
First, write a function that calculates a new column
(that is you should define and insert a new column to the dataframe whose value
depends on the other columns)
and calculates
it in such a way that Berkeley will come out on top in the 2021 rankings.

Note: you can "cheat"; it's OK if your scoring function is picked in some way
that obviously makes Berkeley come on top.
As an extra challenge to make it more interesting, you can try to come up with
a scoring function that is subtle!

b.
Use your new column to sort the data by the new values and return the top 10 university names as a list.

"""

def add_research_score(df):
    """
    Add a "research score" column to a copy of df.

    It rewards academic reputation, faculty/student ratio and citations,
    and discounts employer reputation (framed as a commercial-bias metric).
    The weights happen to favor Berkeley, whose employer reputation is low.
    """
    df = df.copy()
    df["research score"] = (0.75 * df["academic reputation"]
                            - 1.0 * df["employer reputation"]
                            + 0.75 * df["faculty student"]
                            + 1.0 * df["citations per faculty"])
    return df

BERKELEY = "University of California, Berkeley (UCB)"

def q20a(dfs):
    df = add_research_score(dfs[2])
    # Return the score for Berkeley in the new column.
    return float(df.loc[df["university"] == BERKELEY, "research score"].iloc[0])

def q20b(dfs):
    df = add_research_score(dfs[2])
    top = df.sort_values("research score", ascending=False).head(10)
    return list(top["university"])

"""
21. Exploring data manipulation and falsification, continued

This time, let's manipulate the data by changing the source files
instead.
Create a copy of data/2021.csv and name it
data/2021_falsified.csv.
Modify the data in such a way that UC Berkeley comes out on top.

For this part, you will also need to load in the new data
as part of the function.
The function does not take an input; you should get it from the file.

Return the top 10 university names as a list from the falsified data.
"""

def q21():
    # data/2021_falsified.csv is a copy of data/2021.csv in which Berkeley's
    # scores were raised to 100 and its rank changed to 1
    # (every university that was ranked above it moved down one place).
    df = pd.read_csv("data/2021_falsified.csv", encoding="latin-1")
    df.columns = df.columns.str.lower()
    df = df[NEW_COLUMNS].sort_values("rank", kind="stable")
    return list(df["university"].head(10))

"""
22. Exploring data manipulation and falsification, continued

Which of the methods above do you think would be the most effective
if you were a "bad actor" trying to manipulate the rankings?

Which do you think would be the most difficult to detect?

=== ANSWER Q22 BELOW ===

Most effective: changing the source data (Q21). The falsified file feeds every
downstream analysis (averages, plots, correlations), so the manipulated
result is reproduced consistently everywhere and nobody has to trust a
special formula. The scoring function in Q20 is also easy to do, but the
weights are visible and the resulting top 10 is very different from the
published ranking (e.g. Tsinghua and KU Leuven land in the top 5), which
invites questions about the formula.

Most difficult to detect: a small, subtle change to the source data (a few
points on one indicator for one university), because it is hard to tell
apart from the noise in survey-based scores unless someone has the
original data, or checks that the overall score is consistent with its
components. A blunt change like the one in Q21 (a 100 in every indicator, rank 1)
is easy to catch with simple sanity checks.

=== END OF Q22 ANSWER ===
"""

"""
===== Wrapping things up =====

To wrap things up, we have collected
everything together in a pipeline for you
below.

**Don't modify this part.**
It will put everything together,
run your pipeline and save all of your answers.

This is run in the main function
and will be used in the first part of Part 2.
"""

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

def PART_1_PIPELINE():
    open(ANSWER_FILE, 'w').close()

    try:
        dfs = load_input()
    except NotImplementedError:
        print("Welcome to Part 1! Implement load_input() to get started.")
        dfs = []

    # Questions 1-6
    log_answer("q1", q1, dfs)
    log_answer("q2", q2, dfs)
    log_answer("q3a", q3, dfs)
    # 3b: commentary
    log_answer("q4", q4, dfs)
    # 4b: commentary
    log_answer("q5a", q5a, dfs)
    log_answer("q5b", q5b, dfs)
    log_answer("q5c", q5c)
    # 6a: commentary
    # 6b: commentary
    log_answer("q6c", q6c)

    # Questions 7-10
    log_answer("q7", q7, dfs)
    log_answer("q8a", q8a, dfs)
    # 8b: commentary
    log_answer("q9", q9, dfs)
    # 10: avg_2021
    avg_2021 = q10_helper(dfs)
    log_answer("q10", q10, avg_2021)

    # Questions 11-15
    log_answer("q11", q11, avg_2021)
    log_answer("q12", q12a, avg_2021)
    # 12b: commentary
    log_answer("q13", q13a, avg_2021)
    # 13b: commentary
    log_answer("q14a", q14a, avg_2021)
    # 14b: commentary

    # Questions 15-17
    top_10 = q15_helper(dfs)
    log_answer("q15", q15, top_10)
    log_answer("q16", q16, top_10)
    log_answer("q17", q17a, top_10)
    # 17b: commentary

    # Questions 18-20
    log_answer("q18", q18, dfs)
    # 19: commentary

    # Questions 20-22
    log_answer("q20a", q20a, dfs)
    log_answer("q20b", q20b, dfs)
    log_answer("q21", q21)
    # 22: commentary

    # Answer: return the number of questions that are not implemented
    if UNFINISHED > 0:
        print("Warning: there are unfinished questions.")

    return UNFINISHED

"""
That's it for Part 1!

=== END OF PART 1 ===

Main function
"""

if __name__ == '__main__':
    log_answer("PART 1", PART_1_PIPELINE)
