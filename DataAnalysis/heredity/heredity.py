import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):
        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


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
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False
                    if row["trait"] == "0"
                    else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
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

    probs_list = []

    for person in people:
        if person in one_gene:
            # calculate prob of one gene
            # p = this prob
            if people[person]["mother"] == None:
                gene_p = PROBS["gene"][1]
            else:
                # calculate the prob their parents passed on exactly one copy
                gene_p = find_parent_pass(people, person, one_gene, two_genes)

        elif person in two_genes:
            # calculate prob of two genes
            # p = this prob
            if people[person]["mother"] == None:
                gene_p = PROBS["gene"][2]
            else:
                # calculate prob of being passed two copies
                gene_p = find_parent_pass(people, person, one_gene, two_genes)
        else:
            # calculate prob they have no genes
            # p = this prob
            if people[person]["mother"] == None:
                gene_p = PROBS["gene"][0]
            else:
                gene_p = find_parent_pass(people, person, one_gene, two_genes)

        probs_list.append(gene_p)

        if person in have_trait:
            # calculate prob they have the trait
            if person in one_gene:
                trait_p = 0.56
            elif person in two_genes:
                # p based on two genes
                trait_p = 0.65
            else:
                # p based on no genes
                trait_p = 0.01
        else:
            if person in one_gene:
                trait_p = 0.44
            elif person in two_genes:
                trait_p = 0.35
            else:
                trait_p = 0.99

        probs_list.append(trait_p)

    joint = 1
    for prob in probs_list:
        joint *= prob

    return joint


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in two_genes:
            probabilities[person]["gene"][2] = p
        elif person in one_gene:
            probabilities[person]["gene"][1] = p
        else:
            probabilities[person]["gene"][0] = p

        if person in have_trait:
            probabilities[person]["trait"][True] = p
        else:
            probabilities[person]["trait"][False] = p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """

    for person in probabilities:
        # calculate the sum of the probabilites of counts of genes for each person
        total = sum(
            probabilities[person]["gene"][count]
            for count in probabilities[person]["gene"]
        )

        # loop over all the counts of genes and adjust them by making them a percentage of the total
        for count in probabilities[person]["gene"]:
            probabilities[person]["gene"][count] = (
                probabilities[person]["gene"][count] / total
            )

        # make each prob of each value, True and False, itself over the total of the two
        total = (
            probabilities[person]["trait"][True] + probabilities[person]["trait"][False]
        )
        probabilities[person]["trait"][True] = (
            probabilities[person]["trait"][True] / total
        )
        probabilities[person]["trait"][False] = (
            probabilities[person]["trait"][False] / total
        )


def find_parent_pass(people, person, one_gene, two_genes):
    if people[person]["mother"] in two_genes:
        p_mother = 0.99
    elif people[person]["mother"] in one_gene:
        p_mother = 0.5
    else:
        p_mother = 0.01

    if people[person]["father"] in two_genes:
        p_father = 0.99
    elif people[person]["father"] in one_gene:
        p_father = 0.5
    else:
        p_father = 0.01

    if person in two_genes:
        p = p_mother * p_father
    elif person in one_gene:
        p = (p_father * (1 - p_mother)) + (p_mother * (1 - p_father))
    else:
        p = (1 - p_mother) * (1 - p_father)

    return p


if __name__ == "__main__":
    main()

# parent_passing = (PROBS["gene"][2] * 0.99) + (PROBS["gene"][1] * 0.5 * 0.99) + (PROBS["gene"][1] * 0.5 * 0.01) + (PROBS["gene"][0] * 0.01)
# # parent_not_passing = (PROBS["gene"][1] * 0.5 * 0.99) + (PROBS["gene"][0] * 0.99) + (PROBS["gene"][1] * 0.5 * 0.01) + (PROBS["gene"][2] * 0.01)
# parent_not_passing = 1 - parent_passing

# p_pass_2 = (parent_passing * parent_passing)
# p_pass_1 = (2 * (parent_passing * parent_not_passing))
# p_pass_0 = parent_not_passing * parent_not_passing

# havetrait = (p_pass_2 * 0.65) + (p_pass_1 * 0.56) + (p_pass_0 * 0.01)
# no_trait = 1 - havetrait
# not_trait = (p_pass_2 * 0.35) + (p_pass_1 * 0.44) + (p_pass_0 * 0.99)

# print(havetrait)
# print(no_trait)
# print(not_trait)
