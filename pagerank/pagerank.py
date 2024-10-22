import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    corpus = crawl("corpus0")
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    print("---------------------RESULTS for", page, "---------------------------")
    
    print("Total pages in corpus: ", len(corpus))
    #print("Random probability per page: ", random_prob)
    print("Links in current page (", len(corpus[page]), "): ", corpus[page])

    # Initialise starting page (avoding confusion)
    start_page = page

    # Probability distribution over which page to visit next
    prob_dist = {}

    # Random choice probability per page
    random_prob = (1 - damping_factor) / len(corpus)

    # Random choice probability per page assigned to each page in corpus
    for page in corpus:
        prob_dist[page] = random_prob

    # For pages with no links, distribution is equal for all pages
    if len(corpus[start_page]) == 0:
        for page in corpus:
            prob_dist[page] += damping_factor / len(corpus) 

    # For pages with links     
    else:       
        # Loop over all links on the page
        for link in corpus[start_page]:

            # Count the number of links from the starting page
            page_link_count = len(corpus[start_page])

            # Calculate the link probability
            link_prob = damping_factor / page_link_count
            print("Link probability for page", link, ": ", link_prob)

            # Add the calculated link probability to the probability distribution
            prob_dist[link] += link_prob
    
    # Adjusting starting page for floating point imprecision
    prob_dist[start_page] += 1 - sum(prob_dist.values())

    # Print final values for probability distribution
    print("Final probability distribution (adjusted): ", prob_dist)

    # Test if probability distribution sums up to 1
    if sum(prob_dist.values()) != 1:
        print("WRONG: sum of probabilities does not equal 1, in fact it is: ", sum(prob_dist.values()))
    else:
        print("CORRECT: sum of probabilities equals 1")

    print("---------------------------------------------------------")
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    #corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}}

    # Initialise empty dictionary
    pagerank = {}

    print("testing corpus: ", corpus)

    # Initialise pagerank values to 1 over n
    for page in corpus:
        pagerank[page] = 0

    # Randomly select a page
    page = random.choice(list(corpus.keys()))

    print("Starting page: ", page)

    # Sample n pages
    for _ in range(n):
        # Launch transition model
        next_sample_prob = transition_model(corpus, page, damping_factor)
        # Add 1 to the current page rank value
        pagerank[page] += 1

        # Choose next page
        print("Next sample probability: ", next_sample_prob)
        page = random.choices(list(next_sample_prob.keys()), weights=list(next_sample_prob.values()))[0]

        print("Randomly chosen next page: ", page)
    
    # Divide pagerank values by n
    for page in pagerank:
        pagerank[page] = pagerank[page] / n

    # Adjusting last page for floating point imprecision
    pagerank[page] += 1 - sum(pagerank.values())
    
    # Test if probability distribution sums up to 1
    if sum(pagerank.values()) != 1:
        print("WRONG: sum of probabilities does not equal 1, in fact it is: ", sum(pagerank.values()))
    else:
        print("CORRECT: sum of probabilities equals 1")

    # Test final values
    print("Final pagerank values: ")
    #print(pagerank)
    for page in pagerank:
        print(page, ": ", pagerank[page])

    return pagerank



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
    pagerank = {}

    # Initialise the convergence threshold
    threshold = 0.001

    # Initialise pagerank values to 1 / (total number of pages in the corpus)
    for page in corpus:
        pagerank[page] = 1 / len(corpus)

    # Test initial values
    print("Initial probability distribution: ", pagerank)

    # Loop start here
    convergence_ongoing = True
    hard_stop = 0

    while convergence_ongoing == True:
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
            
            # Create NumLinks for each page
            NumLinks = {}

            for NumLink in links_to_p:
                if len(corpus[NumLink]) > 0:
                    NumLinks[NumLink] = len(corpus[NumLink])
                if len(corpus[NumLink]) == 0:
                    NumLinks[NumLink] = len(corpus)

            # Check NumLinks
            print("NumLinks: ", NumLinks)

            # Initialise the pagerank value before summation
            pagerank[p] = ((1 - damping_factor) / len(corpus))
            print("Probability distribution before iteration: ", pagerank)
            print("(1 - d / N) : ", (1 - damping_factor) / len(corpus))

            for NumLink in NumLinks:
                summation = damping_factor * (pagerank[NumLink] / NumLinks[NumLink])
                if summation < threshold:
                    convergence_ongoing = False
                print("Summation: ", damping_factor, "*", pagerank[NumLink], "/", NumLinks[NumLink], "=", summation)
                pagerank[p] += summation

            #print("Probability distribution after iteration", hard_stop, ": ", pagerank)

        hard_stop += 1
        if hard_stop > SAMPLES:
            convergence_ongoing = False

    # Adjusting for floating point imprecision by distributing equally across all keys
    difference = 1 - sum(pagerank.values())

    # Spread the difference equally across all keys
    adjustment = difference / len(pagerank)

    for key in pagerank:
        pagerank[key] += adjustment

    # Final output
    print("Final Output: ", pagerank)

    # Check if the sum of all pagerank values is close to 1
    pagerank_sum = 0
    for page in corpus:
        pagerank_sum += pagerank[page]

    print("Sum of all pagerank values: ", pagerank_sum)

    return pagerank


if __name__ == "__main__":
    main()
