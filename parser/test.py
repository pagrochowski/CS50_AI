from parser import preprocess, np_chunk
import nltk

''' BACKUP ------------------------------------------------------------------
NONTERMINALS = """
S -> NP VP | NP VP NP NP | NP VP Conj NP VP | NP VP NP Conj NP VP | NP VP Conj VP NP | NP VP NP NP Conj VP NP NP
NP -> N | Det N | Adj N | Det Adj N | P N | P Det N | P Det N Adv | P Det Adj N | Det Adj Adj N | Det Adj Adj Adj N
VP -> V | V P | V NP | V Adj | Adv V | V Adv 
PP -> P NP
"""
'''

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP NP | NP VP NP PP | NP VP | NP VP PP | NP VP Conj VP| NP VP Conj S | NP VP Conj VP | S Conj VP PP
NP -> N | Det N | Adj N | Det Adj N | P N | Det Adj Adj N | Det Adj Adj Adj N
VP -> V | V PP | V PP PP | V Adj | Adv V | V Adv | V NP | Adv V NP | V NP PP 
PP -> P | P NP | P NP Adv 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)

def main():

    #s = "Holmes sat in the armchair in the home"
    #    NP VP NP             PP          Adj VP        PP      
    s = "holmes sat in the armchair in the home"
    s = preprocess(s)


   # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return
    
    # Print each tree with noun phrase chunks
    for tree in trees:
        print(tree)
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def test_preprocess():
    # 1.txt
    s = preprocess("Holmes sat.")
    assert s == ["holmes", "sat"]

    # 2.txt
    s = preprocess("Holmes lit a pipe.")
    assert s == ["holmes", "lit", "a", "pipe"]

    # 3.txt
    s = preprocess("My companion smiled an enigmatical smile.")
    assert s == ["my", "companion", "smiled", "an", "enigmatical", "smile"]

    # 4.txt
    s = preprocess("I had a little moist red paint in the palm of my hand.")
    assert s == ["i", "had", "a", "little", "moist", "red", "paint", "in", "the", "palm", "of", "my", "hand"]

    s = preprocess("It looks like you're on the right track")
    assert s == ["it", "looks", "like", "you", "'re", "on", "the", "right", "track"]

if __name__ == "__main__":
    main()