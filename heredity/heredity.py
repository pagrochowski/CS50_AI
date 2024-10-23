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
    """

    print("ONE_gene:", one_gene, "TWO_genes: ", two_genes, "have_trait: ", have_trait)

    # Initiate joint probability variable
    joint = 1

    # Calculate probability that a person has one copy of the gene
    prob_one_gene = 1
    for person in one_gene:
        prob_one_gene = prob_one_gene * PROBS["gene"][1]
        print("Probability that", person, "has ONE gene: ", PROBS["gene"][1])
    print("Joint probability for one gene: ", prob_one_gene)

    # Calculate probability that a person has two copies of the gene
    prob_two_genes = 1
    for person in two_genes:
        prob_two_genes = prob_two_genes * PROBS["gene"][2]
        print("Probability that", person, "has TWO genes: ", PROBS["gene"][2])
    print("Joint probability for two genes: ", prob_two_genes)

    # Calculate probability that a person does not have the gene
    prob_no_gene = 1
    for person in people:
        if person not in one_gene and person not in two_genes:
            prob_no_gene = prob_no_gene * PROBS["gene"][0]
            print("Probability that", person, "DOES NOT have the gene: ", PROBS["gene"][0])
    print("Joint probability for no gene: ", prob_no_gene)

    # Caclulate probability that a person has the trait, given that they have the gene
    prob_has_trait_one_gene = 1
    for person in people:
        if person in have_trait and person in one_gene:
            prob_has_trait_one_gene = prob_has_trait_one_gene * PROBS["trait"][1][True]
            print("Probability that", person, "(ONE gene) has the TRAIT: ", PROBS["trait"][1][True])
    print("Joint probability that a person has the trait, given that they have the gene: ", prob_has_trait_one_gene)

    # Caclulate probability that a person has the trait, given that they have two genes
    prob_has_trait_two_genes = 1
    for person in people:
        if person in have_trait and person in two_genes:
            prob_has_trait_two_genes = prob_has_trait_two_genes * PROBS["trait"][2][True]
            print("Probability that", person, "(TWO genes) has the TRAIT: ", PROBS["trait"][2][True])
    print("Joint probability that a person has the trait, given that they have two genes: ", prob_has_trait_two_genes)

    # Caclulate probability that a person has the trait, given that they have none of the genes
    prob_has_trait_none_of_the_genes = 1
    for person in people:
        if person in have_trait and person not in one_gene and person not in two_genes:
            prob_has_trait_none_of_the_genes = prob_has_trait_none_of_the_genes * PROBS["trait"][0][True]
            print("Probability that", person, "(NONE of the genes) has the TRAIT: ", PROBS["trait"][0][True])
    print("Joint probability that a person has the trait, given that they have none of the genes: ", prob_has_trait_none_of_the_genes)

    # Caclulate probability that a person does not have the trait, given that they have the gene
    prob_no_trait_one_gene = 1
    for person in people:
        if person not in have_trait and person in one_gene:
            prob_no_trait_one_gene = prob_no_trait_one_gene * PROBS["trait"][1][False]
            print("Probability that", person, "(ONE gene) does NOT have the trait: ", PROBS["trait"][1][False])

    # Caclulate probability that a person does not have the trait, given that they have two genes
    prob_no_trait_two_genes = 1
    for person in people:
        if person not in have_trait and person in two_genes:
            prob_no_trait_two_genes = prob_no_trait_two_genes * PROBS["trait"][2][False]
            print("Probability that", person, "(TWO genes) does NOT have the trait: ", PROBS["trait"][2][False])

    # Caclulate probability that a person does not have the trait, given that they have none of the genes
    prob_no_trait_none_of_the_genes = 1
    for person in people:
        if person not in have_trait and person not in one_gene and person not in two_genes:
            prob_no_trait_none_of_the_genes = prob_no_trait_none_of_the_genes * PROBS["trait"][0][False]
            print("Probability that", person, "(NONE of the genes) does NOT have the trait: ", PROBS["trait"][0][False])

    lily = prob_no_gene * prob_no_trait_none_of_the_genes
    print("Lily: ", lily)

    james = prob_two_genes * prob_has_trait_two_genes
    print("James: ", james)

    harry = prob_one_gene * prob_has_trait_one_gene
    print("Harry: ", harry)

    joint = lily * james * harry

    #joint = joint * prob_has_trait_one_gene * prob_has_trait_two_genes * prob_has_trait_none_of_the_genes * prob_no_trait_one_gene * prob_no_trait_two_genes * prob_no_trait_none_of_the_genes

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
