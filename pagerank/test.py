from pagerank import transition_model, sample_pagerank, iterate_pagerank

def main():
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html", }, "3.html": {"1.html", "2.html"}, "4.html": {}}
    #corpus = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
    page = "4.html"
    damping_factor = 0.85
    n = 10000
    #transition_model(corpus, page, damping_factor)
    #sample_pagerank(corpus, damping_factor, n)
    iterate_pagerank(corpus, damping_factor)

def test_iterate_pagerank():
    corpus = {"1.html": {"2.html"}, "2.html": {"1.html", "3.html", }, "3.html": {"1.html", "2.html"}, "4.html": {}}
    damping_factor = 0.85
    
    """
    Final pagerank values: 
    1.html :  0.3134
    2.html :  0.4138
    3.html :  0.2237
    4.html :  0.0491
    """
    #assert iterate_pagerank(corpus, damping_factor) == {'1.html': 0.037500000000000006, '2.html': 0.8875, '3.html': 0.037500000000000006, '4.html': 0.037500000000000006}


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