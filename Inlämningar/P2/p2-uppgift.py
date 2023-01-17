# TDP015 Programming Assignment 2
# Recursion
# Skeleton Code

# Do not use any imports!

# In this assignment you are asked to implement functions on *nested
# pairs*. The set of nested pairs is defined recursively:
#
# 1. The empty tuple () forms a nested pair.
#
# 2. If a and b are nested pairs, then the tuple (a, b) forms a nested
#    pair.
#
# Here are some examples of nested pairs sorted by their *degree*. The
# degree of a nested pair is the number of empty tuples contained in it.
#
# degree 1 (1 pair):
#
# ()
#
# degree 2 (1 pair):
#
# ((), ())
#
# degree 3 (2 pairs):
#
# ((), ((), ()))
# (((), ()), ())
#
# degree 4 (5 pairs):
#
# ((), ((), ((), ())))
# ((), (((), ()), ()))
# (((), ()), ((), ()))
# (((), ((), ())), ())
# ((((), ()), ()), ())
#
# The following sequence gives the number of nested pairs with degrees
# 1, 2, 3, ...:
#
# 1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900,
# 2674440, 9694845, 35357670, 129644790, 477638700, 1767263190, ...

# ## Problem 1
#
# Implement a function nested_pairs() that yields all nested pairs
# with a specified degree. Each nested pair should be yielded exactly
# once. For example, nested_pairs(4) should yield the 5 nested pairs
# listed above. Use recursion. Test your function by counting the
# number of nested pairs yielded by it and comparing against the
# sequence of numbers given above.


def nested_pairs(n):
    """Yield all nested pairs with degree *n*."""
    # TODO: Replace the following line with your own code.
    if n <= 1:
        yield()

    for i in range (1, n):
        for k in nested_pairs(i):
            for p in nested_pairs(n - i):
                yield(k, p)

## TEST for nested_pairs()

""" for i in nested_pairs(4):
    print(i)
for k in nested_pairs(5):
    print(k) """


# ## Problem 2
#
# Implement a function count_nested_pairs() that counts the number of
# nested pairs with a specified degree. A naive implementation of this
# function would call the nested_pairs() function from Problem 1. This
# is not what you are supposed to do! Instead, try to come up with a
# solution that counts the number of nested pairs without generating
# them. There is a way to solve this problem using a formula; but your
# solution should use recursion. Test your implementation by comparing
# your numbers to the numbers that you got above. What is the maximal
# degree for which you can compute the number of nested pairs in under
# one minute?


def count_nested_pairs(n):
    """Count the number of nested pairs with degree *n*."""
    # TODO: Replace the following line with your own code.

    if n <= 1:
        return 1

    counter = 0
    for p in range(1, n):
        counter += count_nested_pairs(p) * count_nested_pairs(n - p)

    return counter

## TEST for count_nested_pairs()

""" print("The number of tested pairs with degree 'n': \n")
for p in range(50):
    print("p: {} has {} number of pair/s.".format(p, count_nested_pairs(p)))   """ 

# ## Problem 3
#
# Because it uses recursion, the function that you implemented in
# Problem 2 will call itself many times, and many times with the same
# argument. One way to speed things up is to cache the results of
# these calls. This strategy is called *memoization*.
#
# The idea is the following: All recursive calls of the function get
# access to a common cache in the form of a dictionary. Before a
# recursive call computes the number of nested pairs of a given degree
# *n*, it first checks whether that number is already stored in the
# cache. If yes, then the recursive call simply returns that
# value. Only if the value has not already been cached, the recursive
# call starts a computation on its own; but then it stores the result
# of that computation in the common cache, under the key *n*, so that
# subsequent calls will not have to recompute it.
#
# Write a function count_nested_pairs_memoized() that implements this
# idea. Test your implementation as above. How long does it take you to
# compute the number of nested pairs for the maximal degree that you
# could do in under one minute in Problem 2?

memoized_dic = {}
def count_nested_pairs_memoized(n):
    # TODO: Replace the following line with your own code.

    if n <= 1:
        return 1

    counter = 0
    if n not in memoized_dic:
        for p in range(1, n):
            counter += count_nested_pairs_memoized(p) * count_nested_pairs_memoized(n - p)
        memoized_dic[n] = counter
    return memoized_dic[n]

    ## TEST for count_nested_pairs_memoized()

""" print("Nested pairs memoized: \n")
for k in range(5):
    print("k: {} has {} number of pairs memoized.".format(k, count_nested_pairs_memoized(k)))
     """

"""  DET TAR BETYDLIGT MER TID FÖR ATT BERÄKNA I UPPGIFT 2 I JÄMFÖRELSE MED UPPGIFT 3.
 ANLEDNING TILL DET ÄR FÖRMODLIGEN FÖR ATT ALLA BERÄKNINGAR SPARAS I EN DICTIONARY 
 VILKET LIGGER NÅGONSTANS I MINNET. DETTA GÖR ATT DATORN BERÄKNAR INTE DE SPARADE 
 UTRÄKNINGAR. """ 
 