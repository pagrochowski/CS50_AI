from pagerank import *

def main():
    #corpus = crawl("corpus0")
    #print(corpus)
    #keys = list(corpus.keys())
    #page1 = keys[0]
    #print(page1)
    corpus = {"1.html": {"2.html", "3.html"}}
    page = "1.html"
    damping_factor = 0.85
    transition_model(corpus, page, damping_factor)

def test_transition_model():
    # Case 1: one page links to two pages
    corpus = {"1.html": {"2.html", "3.html"}}
    page = "1.html"
    damping_factor = 0.85
    assert transition_model(corpus, page, damping_factor) == {'1.html': 0.15, '3.html': 0.425, '2.html': 0.425}

if __name__ == "__main__":
    main()