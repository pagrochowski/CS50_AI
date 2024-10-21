import os
import random
import re
import sys

DAMPING = 0.85
#SAMPLES = 10000
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

   
    # Probability distribution over which page to visit next
    prob_dist = {}

    # For pages with no links, distribution is equal for all pages
    if len(corpus[page]) == 0:
        for page in corpus:
            prob_dist[page] = 1 / len(corpus)      
    else:
        # Random choice probability per page
        random_prob = (1 - damping_factor) / len(corpus)
        
        prob_dist[page] = random_prob
        # Loop over all pages in the corpus
        for link in corpus[page]:

            # Count the number of links from the current page
            page_link_count = len(corpus[page])

            # Calculate the link probability
            # Old version
            #link_prob = (1 / page_link_count) - (random_prob / page_link_count)
            link_prob = random_prob + damping_factor / page_link_count
            print("Link probability for page", link, ": ", link_prob)

            # Add the next page to the probability distribution
            prob_dist[link] = link_prob
    
    # Adjusting current page for floating point imprecision
    prob_dist[page] += 1 - sum(prob_dist.values())

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

    # Test initialisation
    #print(pagerank)
    #for page in pagerank:
        #print(page, ": ", pagerank[page])

    # Randomly select a page, but start with fixed page
    page = random.choice(list(corpus.keys()))
    #page = '3.html'

    print("Starting page: ", page)

    #transition_model(corpus, page, damping_factor)

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
    raise NotImplementedError


if __name__ == "__main__":
    main()
