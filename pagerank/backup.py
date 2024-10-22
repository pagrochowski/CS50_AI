def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html", }, "3.html": {"1.html", "2.html"}, "4.html": {}}

    # Initialise probability distribution
    prob_dist = {}

    # Initialise the convergence threshold
    threshold = 0.001

    # Initialise pagerank values to 1 / (total number of pages in the corpus)
    for page in corpus:
        prob_dist[page] = 1 / len(corpus)

    # Test initial values
    print("Initial probability distribution: ", prob_dist)

    # Loop start here
    #p = "4.html"
    for p in corpus:
        print("---------------------------Calculating for page", p, "---------------------------")

        # Gather links that point to the page p
        links_to_p = []

        for page in corpus:
            if p in corpus[page] and len(corpus[page]) > 0:
                links_to_p.append(page)

            # If page has no links, it links to all pages, including itself
            elif len(corpus[page]) == 0:
                print("Page", page, "has no links")
                links_to_p.append(page)

        # Print out all the links
        print("Links that point to the page", p, ": ")
        print(links_to_p)
        
        NumLinks = {}
        for NumLink in links_to_p:
            if len(corpus[NumLink]) > 0:
                NumLinks[NumLink] = len(corpus[NumLink])
            if len(corpus[NumLink]) == 0:
                NumLinks[NumLink] = len(corpus)

        # Check NumLinks
        print("NumLinks: ", NumLinks)

        # Initialise the pagerank value before summation
        prob_dist[p] = ((1 - damping_factor) / len(corpus))
        print("Probability distribution before iteration: ", prob_dist)
        print("(1 - d / N) : ", (1 - damping_factor) / len(corpus))

        for NumLink in NumLinks:
            summation = damping_factor * (prob_dist[NumLink] / NumLinks[NumLink])
            print("Summation: ", damping_factor, "*", prob_dist[NumLink], "/", NumLinks[NumLink], "=", summation)
            prob_dist[p] += summation

        print("Probability distribution after iteration: ", prob_dist)

    # Final output
    print("Final Output: ", prob_dist)

    # Check if the sum of all pagerank values is close to 1
    pagerank_sum = 0
    for page in corpus:
        pagerank_sum += prob_dist[page]

    print("Sum of all pagerank values: ", pagerank_sum)

    return prob_dist