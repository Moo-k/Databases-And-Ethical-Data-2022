import statistics
import pandas as pd

data_file = "movies.nt"
language_tag = "@en-US"
line_ending = " ."
query_person_name = "\"Guy Ritchie\""

predicate_has_type = "<http://adelaide.edu.au/dbed/hasType>"
predicate_has_name = "<http://adelaide.edu.au/dbed/hasName>"
predicate_has_actor = "<http://adelaide.edu.au/dbed/hasActor>"
uri_person = "<http://adelaide.edu.au/dbed/Person>"
predicate_prefix = "<http://adelaide.edu.au/dbed/has"


def _is_uri(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("<") and some_text.endswith(">")

def _is_blank_node(some_text):
    # simple text without regular expressions
    if some_text.find(' ') >= 0:
        return False
    return some_text.startswith("_:")

def _is_literal(some_text):
    return some_text.startswith("\"") and some_text.endswith("\"")

def _parse_line(line):
    # this could be done using regex

    # for each line, remove newline character(s)
    line = line.strip()
    #print(line)

    # throw an error if line doesn't end as required by file format
    assert line.endswith(line_ending), line
    # remove the ending part
    line = line[:-len(line_ending)]

    # find subject
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into subject and the rest
    s = line[:i]
    line = line[(i + 1):]
    # throw an error if subject is neither a URI nor a blank node
    assert _is_uri(s) or _is_blank_node(s), s

    # find predicate
    i = line.find(" ")
    # throw an error, if no whitespace
    assert i >= 0, line
    # split string into predicate and the rest
    p = line[:i]
    line = line[(i + 1):]
    # throw an error if predicate is not a URI
    assert _is_uri(p), str(p)

    # object is everything else
    o = line

    # remove language tag if needed
    if o.endswith(language_tag):
        o = o[:-len(language_tag)]

    # object must be a URI, blank node, or string literal
    # throw an error if it's not
    assert _is_uri(o) or _is_blank_node(o) or _is_literal(o), o

    #print([s, p, o])
    return s, p, o

def _compute_stats():
    # ... you can add variables here ...

    # open file and read it line by line
    ll = set() # set for distinct lines
    pp = set() # set for people
    actorsset = set() # set of actors
    actors = [] # list of actors
    guy = 0 # jobs guy ritchie has starred in (assuming guy ritchie only has 1 id)

    # assume utf8 encoding, ignore non-parseable characters
    with open(data_file, encoding="utf8", errors="ignore") as f:
        for line in f:
            # get subject, predicate and object
            ll.add(line) # add lines to set (distinct)
            s, p, o = _parse_line(line)
            if s.startswith("_:p_"): # if subject is a person, add to the people set
                pp.add(s)
            if o == "_:p_956": # if object is guy ritchie, increment guy ritchie's jobs
                guy+=1
            if p == "<http://adelaide.edu.au/dbed/hasActor>": # if the predicate is (the movie) having an actor, add to actor set and actor list (set is unique)
                actorsset.add(o)
                actors.append(o)

    ###########################################################
    # ... your code here ...
    # you can add functions and variables as needed;
    # however, do NOT remove or modify existing code;
    # _compute_stats() must return four values as described;
    # you can add print statements if you like, but only the
    # last four printed lines will be assessed;
    ###########################################################
    mostjobs = statistics.mode(actors) # actor with most jobs
    num = 0

    for i in actors:
        if i == mostjobs:
            num+=1
    d = {}
    for i in actorsset: # set default dict value for all actors to 0
        d[i]=0

    for i in actors: # for each appearance of actor, increment their dict value by 1
        d[i]+=1

    count = 0
    for i in d: # if the actor appears (max) times, increment the number of actors who've appeared (max) times
        if d[i] == num:
            count+=1

    n_triples = len(ll)
    n_people = len(pp)
    n_top_actors = count
    n_guy_jobs = guy
    ###########################################################
    # n_triples -- number of distinct triples
    # n_people -- number of distinct people mentioned in ANY role
    #             (e.g., actor, director, producer, etc.)
    # n_top_actors -- number of people appeared as ACTORS in
    #                 M movies, where M is the maximum number
    #                 of movies any person appeared in as an actor
    # n_guy_jobs -- number of distinct jobs that "Guy Ritchie" had
    #               across different movies (e.g., he could be a
    #               director in one movie, producer in another, etc.)
    ###########################################################

    return n_triples, n_people, n_top_actors, n_guy_jobs


if __name__ == "__main__":
    n_triples, n_people, n_top_actors, n_guy_jobs = _compute_stats()
    print()
    print(f"{n_triples:,} (n_triples)")
    print(f"{n_people:,} (n_people)")
    print(f"{n_top_actors} (n_top_actors)")
    print(f"{n_guy_jobs} (n_guy_jobs)")
