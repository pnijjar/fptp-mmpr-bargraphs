#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt

import csv
import collections
import argparse


FILENAME="./csv/election-tallies05.csv"
BAR_WIDTH=0.4

PartyInfo = collections.namedtuple(
    'PartyInfo', 
    ['fullname', 'colour'],
    )

ResultInfo = collections.namedtuple(
    'ResultInfo',
    ['partyabbr', 'seats', 'votes', 'topup_seats'],
    )



# Data structures are hard!
# I think I want named tuples for party_info
# and then dictionaries of named tuples (?) for 
# party_result in an election. 

party_lookup = {}
party_listing = ['Empty', ]

graph_type = "fptp"


# La la la define a format by an implementation la la la


# ====== FUNCTIONS =========

# -----------------
def format_onepercent(label):
    """ return a label nicely formatted to one 
    decimal place """

    #return "%.1f" % (label)
    return "%.1f%%" % (label)

# -----------------
def format_oneseatlabel(label):
    """ Format a single label for seats"""
    retval = ""
    if label > 10: 
        retval = "%s\nSeats" % (label)

    elif label == 0:
        retval = ""

    else:
        # small bars are bad news
        retval = "%s" % (label)

    return retval


# -----------------
def labelbars(rects, labels, pos="top", bottom=None): 
    """ Make bar labels.

    Stolen from barchart_demo.py
    Assume labels are already formatted nicely. 
    Assume there are the same number of items in each
    "pos" can be top or middle

    """

    for i in range(0,len(labels)):
        height = rects[i].get_height()

        if bottom != None:
            base = bottom[i].get_height()
        else:
            base = 0


        # By default label above
        ypos = 2 + height + base

        if pos == "middle":
            ypos = height / 2 + base;


        plt.text(rects[i].get_x() + rects[i].get_width() / 2,
            ypos,
            labels[i],
            fontdict={
                "size" :"small",
                "stretch": "condensed"
                },
            ha="center",
            )

# -----------------

def sanitize_title(title): 
    """ Make a title for a graph that is not insane.
    """

    retval = title.strip()
    retval = retval.replace(' ','_')
    return retval

# -----------------
def plot_election_graph(graphtitle, 
    election_result,
    party_lookup_list,
    election_type):
    """ Assume the party lookup is a global variable
        or something.
        
        Plot the graph based on a list of tuples.

        Make the election_type either "fptp" or "mmpr". 
        The default is "fptp", of course.

    """

    height_seats = []
    height_votes = []
    height_topup = []

    xpos = np.arange(len(election_result))


    # This should be a parameter, but I am going to sort
    # by votes.
    election_result.sort(key=lambda q: q.votes, 
        reverse=True)

    parties = map(lambda q: q.partyabbr, election_result)
    colours = map(
        lambda q: party_lookup[q.partyabbr].colour, 
        election_result)

    seats = map(lambda q: q.seats, election_result)
    votes = map(lambda q: q.votes, election_result)
    topup = []
    
    if election_type == "mmpr":
        topup = map(lambda q: q.topup_seats, election_result)


    for i in range(0,len(election_result)): 
        height_votes.append((votes[i] * 100.0 / sum(votes))  ) 

    
    allseats = 0 

    if election_type == "mmpr":

        allseats = sum(seats) + sum(topup)

        for i in range(0,len(election_result)): 
            height_topup.append((topup[i] * 100.0 / allseats)) 
    else:
        allseats = sum(seats)

    for i in range(0,len(election_result)):
        height_seats.append((seats[i] * 100.00 / allseats)) 
    
    

    #print "%s" % (height_seats)

    votebar = plt.bar(xpos,  height_votes, width=BAR_WIDTH, 
        edgecolor = colours, color = colours, alpha=1.0, linewidth=2 )
    seatbar = plt.bar(xpos + BAR_WIDTH, height_seats, width=BAR_WIDTH, 
        color = colours, edgecolor = colours , alpha=0.5, linewidth = 2)

    if election_type == "mmpr":
        topupbar = plt.bar(xpos + BAR_WIDTH, height_topup, width=BAR_WIDTH,
            edgecolor = colours, color = "white", alpha=1.0,
            linewidth=2, hatch="/", bottom = height_seats)


    labelbars(votebar, map(format_onepercent, height_votes), "top")

    seat_labels = map(format_oneseatlabel, seats)
    labelbars(seatbar, seat_labels, "middle")

    if election_type == "mmpr":
        sum_seats = map(lambda a,b:a+b, height_seats, height_topup)
        labelbars(topupbar, map(format_onepercent, sum_seats), "top",
            bottom=seatbar)

        topup_labels = map(format_oneseatlabel, topup)
        labelbars(topupbar, topup_labels, "middle", bottom=seatbar)

    else:
        labelbars(seatbar, map(format_onepercent, height_seats), "top")

    

   
    plt.xlabel("Parties")
    plt.ylabel("% votes/seats")
    plt.title(graphtitle)
    plt.xticks(xpos + BAR_WIDTH, parties)
    plt.ylim(0,100)
    plt.xlim(0,len(election_result))
    
    if election_type == "mmpr":
        plt.legend(('Votes','Seats', 'Topup'))
    else:
        plt.legend(('Votes','Seats'))
    
    # Plot the majority threshold (light grey is too subtle)
    plt.axhline(y=50, color="red", linestyle="--")


    outfile = "/tmp/%s.png" % (sanitize_title(graphtitle))
    print "Filename is %s" % outfile
    plt.savefig(outfile, dpi=100, format="png", 
        bbox_inches="tight", pad_inches=0.01)
    #plt.show()
    plt.clf()
    


# ------- MAIN PROGRAM ------------

parser = argparse.ArgumentParser(
    description="Plot election graphs in FPTP or MMPR"
    )
parser.add_argument('csvfile', help="File name to process")
parser.add_argument('--type', 
    default="fptp", choices=["fptp", "mmpr"], 
    help="What type of electoral system info to graph")
  

args=parser.parse_args()

FILENAME=args.csvfile
csv_reader = csv.reader(open(FILENAME,'rb'))

if args.type:
    graph_type = args.type


try:

    # First line: "Parties"
    # Next lines: party names, party abbreviations, 
    #   party colours. First column should be blank.

    line = csv_reader.next()
    if line[0] != "Parties":
        print "Uh oh. First line should be parties!"

    party_names = csv_reader.next()
    party_abbr = csv_reader.next()
    party_colours = csv_reader.next()

    for i in range(1, len(party_names)):
        party_listing.append(party_abbr[i])
        
        party_lookup[party_abbr[i]] = \
            PartyInfo(
                fullname=party_names[i],
                colour=party_colours[i],
                )

    # print "Party info: %s" % (party_lookup)

    while True: 

        # Skip empty lines for a while.

        is_emptyline = True
        line = []
        while is_emptyline:
            line = csv_reader.next()
            for elem in line:
                if elem != "":
                    is_emptyline = False

            if is_emptyline:
                print "Found empty line"

        title = line[0]
        if title == "":
            print "Uh oh. Empty title in %s" % (line)

        active_parties = csv_reader.next()
        seats_won = csv_reader.next()

        if graph_type == "mmpr":
            topup_seats_won = csv_reader.next()


        votes_won = csv_reader.next() 

        election_result = []

        for i in range(1, len(active_parties)):
            # Only include active parties. The entry 
            # had better be 1, or else. 
            if active_parties[i] == "1":

                topup_seat_tally = 0

                if graph_type == "mmpr":
                    topup_seat_tally=int(topup_seats_won[i])


                election_result.append(
                    ResultInfo(
                        partyabbr=party_listing[i],
                        seats=int(seats_won[i]),
                        votes=int(votes_won[i]),
                        topup_seats=topup_seat_tally,
                        )
                    )

        #print ""
        #print "Election: %s" % (title)
        #print "Result info: %s" % (election_result)


        """
        plot_fptp_graph(
            title, 
            election_result,
            party_lookup,
            )
        """
        
        plot_election_graph(
            title,
            election_result,
            party_lookup,
            graph_type,
            )

except StopIteration:
    print "All done now!"


