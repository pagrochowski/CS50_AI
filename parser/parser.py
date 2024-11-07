import nltk
import sys


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
S -> NP VP | NP VP NP | NP VP NP PP | NP VP | NP VP PP | NP VP Conj VP| 
S -> NP VP Conj S | NP VP Conj VP | S Conj VP PP
NP -> N | Det N | Adj N | Det Adj N | P N | Det Adj Adj N | Det Adj Adj Adj N
VP -> V | V PP | V PP PP | V Adj | Adv V | V Adv | V NP | Adv V NP | V NP PP 
PP -> P | P NP | P NP Adv 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
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
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized_sentence = nltk.word_tokenize(sentence)
    list_of_words = [word.lower() for word in tokenized_sentence if any(char.isalpha() for char in word)]
    print("list of words: ", list_of_words)
    return list_of_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    noun_phrase_chunks = []

    def contains_NP(subtree):
        for child in subtree.subtrees():
            if child != subtree and child.label() == "NP":
                return True
        return False


    # Check each subtree of the main tree
    for subtree in tree.subtrees():
        # It has label NP
        if subtree.label() == "NP":
            #print("Subtree has NP label:", subtree)
            # Loop through each child
            if not contains_NP(subtree):
                #print("Adding subtree to noun_phrase_chunks: ", subtree)
                noun_phrase_chunks.append(subtree)
            else:
                #print("Subtree contains NP, skipping: ", subtree)
                continue
        
                        
    return noun_phrase_chunks


if __name__ == "__main__":
    main()
