from pagerank import transition_model, sample_pagerank

def main():
    #corpus = crawl("corpus0")
    #print(corpus)
    #keys = list(corpus.keys())
    #page1 = keys[0]
    #print(page1)
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html", }, "3.html": {"1.html", "2.html", "4.html"}, "4.html": {}}
    #corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "4.html"
    damping_factor = 0.85
    n = 1
    transition_model(corpus, page, damping_factor)
    #sample_pagerank(corpus, damping_factor, n)




def test_transition_model():
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html", }, "3.html": {"1.html", "2.html", "4.html"}, "4.html": {}}
    damping_factor = 0.85

    # Case 1: one page links to one page
    page = "1.html"
    assert transition_model(corpus, page, damping_factor) == {'1.html': 0.037500000000000006, '2.html': 0.8875, '3.html': 0.037500000000000006, '4.html': 0.037500000000000006}

    # Case 2: second page links to two pages
    page = "2.html"
    assert transition_model(corpus, page, damping_factor) == {'1.html': 0.4625, '2.html': 0.037500000000000006, '3.html': 0.4625, '4.html': 0.037500000000000006}

    # Case 3: third page links to three pages
    page = "3.html"
    assert transition_model(corpus, page, damping_factor) == {'1.html': 0.3208333333333333, '2.html': 0.3208333333333333, '3.html': 0.03750000000000012, '4.html': 0.3208333333333333}

    # Case 4: fourth page links to no pages
    page = "4.html"
    assert transition_model(corpus, page, damping_factor) == {'1.html': 0.25, '2.html': 0.25, '3.html': 0.25, '4.html': 0.25}


if __name__ == "__main__":
    main()