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
    joint = {}

    for person in people:
        # Calculate probability that a person has one copy of the gene
        if person in one_gene:
            joint[person] = PROBS["gene"][1]
        elif person in two_genes:
            joint[person] = PROBS["gene"][2]
        else:
            joint[person] = PROBS["gene"][0]
    
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