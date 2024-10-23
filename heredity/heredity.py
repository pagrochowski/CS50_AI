import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    #if len(sys.argv) != 2:
        #sys.exit("Usage: python heredity.py data.csv")
    #people = load_data(sys.argv[1])
    people = load_data("data/family0.csv")

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    #print("Probabilities loaded from CSV:")
    #print(probabilities)
    

    
    # Loop over all sets of people who might have the trait
    names = set(people)
    print("Set of people: ", names)
    print("Powerset: ", powerset(names))

    name = {'James'}

    for have_trait in name:

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
            people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in name:
            for two_genes in name:

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                print("Joint probability result: ")
                print(p)
                #update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    #normalize(probabilities)

    """
    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")
    """

def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.

    Note FROM SELF: 
    Consider example:
    Finally, we consider Harry. What’s the probability that Harry has 1 copy of the gene? There are two ways this can happen. Either he gets the gene from his mother and not his father, or he gets the gene from his father and not his mother. His mother Lily has 0 copies of the gene, so Harry will get the gene from his mother with probability 0.01 (this is PROBS["mutation"]), since the only way to get the gene from his mother is if it mutated; conversely, Harry will not get the gene from his mother with probability 0.99. His father James has 2 copies of the gene, so Harry will get the gene from his father with probability 0.99 (this is 1 - PROBS["mutation"]), but will get the gene from his mother with probability 0.01 (the chance of a mutation). Both of these cases can be added together to get 0.99 * 0.99 + 0.01 * 0.01 = 0.9802, the probability that Harry has 1 copy of the gene.
    
    """

    print("ONE_gene:", one_gene, "TWO_genes: ", two_genes, "have_trait: ", have_trait)

    # Initiate joint probability variable
    joint = {}

    print("People: ")
    print(people)

    for person in people:
        # No parents
        if people[person]["mother"] is None and people[person]["father"] is None:
            # Two genes
            if person in two_genes:
                joint[person] = PROBS["gene"][2]
                # Has trait
                if person in have_trait:
                    joint[person] *= PROBS["trait"][2][True]
                # Does not have trait
                else:
                    joint[person] *= PROBS["trait"][2][False]

            # One gene
            elif person in one_gene:
                joint[person] = PROBS["gene"][1]
                # Has trait
                if person in have_trait:
                    joint[person] *= PROBS["trait"][1][True]
                # Does not have trait
                else:
                    joint[person] *= PROBS["trait"][1][False]
            
            # No gene
            elif person not in (one_gene, two_genes):
                joint[person] = PROBS["gene"][0]
                # Has trait
                if person in have_trait:
                    joint[person] *= PROBS["trait"][0][True]
                # Does not have trait
                else:
                    joint[person] *= PROBS["trait"][0][False]
        
        # Parents
        elif people[person]["mother"] is not None and people[person]["father"] is not None:

            # Two genes
            if person in two_genes:
                # Both parents have two genes
                if people[person]["mother"] in two_genes and people[person]["father"] in two_genes:
                    joint[person] = (1 - 0.01) * (1 - 0.01)
                # One parent has one gene, the other has two genes
                elif ((people[person]["mother"] in one_gene and people[person]["father"] in two_genes) or 
                    (people[person]["mother"] in two_genes and people[person]["father"] in one_gene)):
                    joint[person] = (0.5 - 0.01) * (1 - 0.01)
                # Both parents have one gene
                elif people[person]["mother"] in one_gene and people[person]["father"] in one_gene:
                    joint[person] = (0.5 - 0.01) * (0.5 - 0.01)
                # One parent has no genes, the other has two genes
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in two_genes) or
                    (people[person]["mother"] in two_genes and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = 0.01 * (1 - 0.01)
                # One parent has no genes, the other has one gene
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in one_gene) or
                    (people[person]["mother"] in one_gene and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = 0.01 * (0.5 - 0.01)
                # Both parents have no genes
                elif people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] not in (one_gene, two_genes):
                    joint[person] = 0.01 * 0.01

            # One gene
            elif person in one_gene:
                # Both parents have two genes
                if people[person]["mother"] in two_genes and people[person]["father"] in two_genes:
                    joint[person] = (1 - 0.01) * (1 - 0.01)
                # One parent has one gene, the other has two genes
                elif ((people[person]["mother"] in one_gene and people[person]["father"] in two_genes) or 
                    (people[person]["mother"] in two_genes and people[person]["father"] in one_gene)):
                    joint[person] = ((0.5 - 0.01) * (0.5 + 0.01)) + (1 - 0.01)
                # Both parents have one gene
                elif people[person]["mother"] in one_gene and people[person]["father"] in one_gene:
                    joint[person] = ((0.5 - 0.01) * (0.5 + 0.01)) + ((0.5 + 0.01) * (0.5 - 0.01))
                # One parent has no genes, the other has two genes
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in two_genes) or
                    (people[person]["mother"] in two_genes and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = 0.01 + (1 - 0.01)
                # One parent has no genes, the other has one gene
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in one_gene) or
                    (people[person]["mother"] in one_gene and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = 0.01 + ((0.5 - 0.01) * (0.5 + 0.01))
                # Both parents have no genes
                elif people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] not in (one_gene, two_genes):
                    joint[person] = 0.01 + 0.01
                    
            # No gene
            if person not in (one_gene, two_genes):
                # Both parents have two genes
                if people[person]["mother"] in two_genes and people[person]["father"] in two_genes:
                    joint[person] = 0.01 * 0.01
                # One parent has one gene, the other has two genes
                elif ((people[person]["mother"] in one_gene and people[person]["father"] in two_genes) or 
                    (people[person]["mother"] in two_genes and people[person]["father"] in one_gene)):
                    joint[person] = (0.5 + 0.01) * 0.01
                # Both parents have one gene
                elif people[person]["mother"] in one_gene and people[person]["father"] in one_gene:
                    joint[person] = (0.5 + 0.01) * (0.5 + 0.01)
                # One parent has no genes, the other has two genes
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in two_genes) or
                    (people[person]["mother"] in two_genes and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = (1 - 0.01) * 0.01
                # One parent has no genes, the other has one gene
                elif ((people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] in one_gene) or
                    (people[person]["mother"] in one_gene and people[person]["father"] not in (one_gene, two_genes))):
                    joint[person] = (1 - 0.01) * (0.5 + 0.01)
                # Both parents have no genes
                elif people[person]["mother"] not in (one_gene, two_genes) and people[person]["father"] not in (one_gene, two_genes):
                    joint[person] = (1 - 0.01) * (1 - 0.01)

    
    print("Joint probability result: ")    
    print(joint)
    
    
    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    return probabilities


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    return probabilities


if __name__ == "__main__":
    main()
