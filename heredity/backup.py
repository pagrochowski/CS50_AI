# One gene
# Case 1: received from mother and not father OR 
# Case 2: received from father and not mother
elif person in one_gene:
    # Both parents have two genes 0.0198
    if people[person]["mother"] in two_genes and people[person]["father"] in two_genes:
        joint[person] = 0.99 * 0.01 + 0.01 * 0.99
        print(person, " was here 13")
    # One parent has one gene, the other has two genes 0.5
    elif ((people[person]["mother"] in one_gene and people[person]["father"] in two_genes) or 
          (people[person]["mother"] in two_genes and people[person]["father"] in one_gene)):
        joint[person] = 0.5 * 0.01 + 0.5 * 0.99
        print(person, " was here 14")
    # Both parents have one gene 0.5
    elif people[person]["mother"] in one_gene and people[person]["father"] in one_gene:
        joint[person] = 0.5 * 0.5 + 0.5 * 0.5
        print(person, " was here 15")
    # One parent has no genes, the other has two genes 0.9802
    elif ((people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes) and \
          people[person]["father"] in two_genes) or \
         (people[person]["mother"] in two_genes and \
          people[person]["father"] not in one_gene and people[person]["father"] not in two_genes):
        joint[person] = 0.99 * 0.99 + 0.01 * 0.01
        print(person, " was here 16")
    # One parent has no genes, the other has one gene 0.5
    elif ((people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes) and \
          people[person]["father"] in one_gene) or \
         (people[person]["mother"] in one_gene and \
          people[person]["father"] not in one_gene and people[person]["father"] not in two_genes):
        joint[person] = 0.01 * 0.5 + 0.99 * 0.5
        print(person, " was here 17")
    # Both parents have no genes 0.0198
    elif people[person]["mother"] not in one_gene and people[person]["mother"] not in two_genes and \
         people[person]["father"] not in one_gene and people[person]["father"] not in two_genes:
        joint[person] = 0.01 * 0.01
        print(person, " was here 18")
