Election Result Graph Scripts
=============================

These are skunkworks python scripts that can generate seat/vote bar
graphs for first-past-the-post and mixed member proportional voting
systems. 

Since the scripts do not actually compute seat totals, you
can use them to generate graphs for a few other systems like list
proportional representation. 

They are based on Python 2.7 and matplotlib. They are tested on
Debian. 


Data Format
-----------

The scripts process CSV files that are in a poorly-documented format. See
eg/election-tallies.ods for sample files I used. Here is a summary. 

For FPTP graphs, assuming 10 parties: 

- Column A1: "Parties"
- Column B2-K2: full party names
- Column B3-K3: abbreviated party names, as should be shown on the
graphs
- Column B4-K4: party colours, represented in any format matplotlib
  can understand

(skip rows if you wish)

- Column A6: Graph title
- Columns B7-K7: 1 if this party participated in the election
- Columns B8-K8: number of seats won by this party
- Columns B9-K9: number of votes won by this party 

You can then skip more rows and repeat the pattern for rows 6-9


For MMPR graphs, the header (rows 1-4) are the same. Graph bodies are
similar except there is also a row for top-up seats: 


- Column A6: Graph title
- Columns B7-K7: 1 if this party participated in the election
- Columns B8-K8: number of riding seats won by this party
- Columns B9-K9: number of top-up seats won by this party
- Columns B10-K10: number of votes won by this party 


Usage
-----

First make CSV files (I export them from the .ods sheet)

Then run 

    python plot_bargraphs.py [-h] [--type {fptp,mmpr}] csvfile

The output goes into `/tmp`


Unfinished business
-------------------

- Switch to toggle between interactive and noninteractive mode
- Resize the graphs so they are not as squished
- Specify output folder on command line
