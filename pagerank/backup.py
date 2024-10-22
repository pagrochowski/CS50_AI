# Gather links that point to the given page
    p = "1.html"
    links_to_p = []

    for page in corpus:
        if p in corpus[page]:
            links_to_p.append(page)

    # Print out all the links
    print("Links that point to the given page: ")
    print(links_to_p)

    for i in links_to_p:
        print("NumLinks on page ", i, ": ", len(corpus[i]))


    # Initialise the pagerank value before summation
    prob_dist[p] = ((1 - damping_factor) / len(corpus))
    print("Probability distribution before iteration: ", prob_dist)

    convergence = True
    # Iterate until the probability distribution converges
    while convergence:
        for i in links_to_p:
            summation = damping_factor * (prob_dist[i] / len(corpus[i]))
            prob_dist[p] += summation
            print("Probability distribution after iteration: ", prob_dist)
            if summation < threshold:
                convergence = False
    
    print("Final probability distribution: ", prob_dist)