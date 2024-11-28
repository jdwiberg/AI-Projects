import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probs = {}

    if page not in corpus or corpus[page] is None:
        # If no links, return uniform probability for all pages
        for key in corpus:
            probs[key] = 1 / len(corpus)
        return probs

    # gives all the links of a page in set form
    links = corpus[page]

    # iterates and finds the probability of links
    for key in corpus:
        if key in links:
            p = (damping_factor) * (1 / len(links)) + (1 - damping_factor) * (
                1 / (len(corpus))
            )
            probs[key] = p
        # finds probability of choosing any page not in links
        else:
            p = (1 - damping_factor) * (1 / (len(corpus)))
            probs[key] = p

    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    ranks = {}
    counts = {}
    c_page = random.choice(list(corpus.keys()))

    if c_page not in counts.keys():
        counts[c_page] = 1
    else:
        counts[c_page] += 1

    for i in range(n - 1):
        next_page_dict = transition_model(corpus, c_page, damping_factor)
        pick = pick_by_prob(next_page_dict)

        if pick not in counts.keys():
            counts[pick] = 1
        else:
            counts[pick] += 1

        c_page = pick

    for key, value in counts.items():
        value = value / n
        ranks[key] = value

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # with .15 prob the page was accessed randomly out of all pages
    # .15 * 1/# of pages
    # with 0.85 prob
    ranks = {}
    old_ranks = {}
    page_rank = 1 / len(corpus)
    for key in corpus:
        ranks[f"{key}"] = page_rank

    while True:
        old_ranks = ranks.copy()
        for key in ranks:
            pr = (1 - damping_factor) / len(corpus)

            # return list of all pages that have this page in them
            sources = find_sources(corpus, key)
            if len(sources) == 0:
                for key in corpus:
                    pr += damping_factor * (ranks[page] / len(corpus))
            else:
                source_ranks = 0

                # Iterate through each source, and calculate their adder by
                # dividing their current rank by the number of links they have.
                # Then, add this to the sum (source ranks) and multiply by damping factor
                for source in sources:
                    if len(corpus[source]) != 0:
                        source_ranks += ranks[source] / len(corpus[source])
                    else:
                        source_ranks += ranks[source] / len(corpus)

                # add this second half of the equation to pr
                pr += damping_factor * source_ranks

            # update this key's value in rank
            ranks[key] = pr

        # figure out if its time to stop the loop yet
        counter = 0
        for key in ranks:
            if abs(ranks[key] - old_ranks[key]) >= 0.001:
                break
            else:
                counter += 1

            if counter == len(corpus):
                return ranks


def pick_by_prob(dict):
    n = random.random()
    adder = 0
    for key, value in dict.items():
        spot = value + adder
        if n < spot:
            return key
        else:
            adder = spot


def find_sources(corpus, page):
    sources = []
    for key in corpus:
        if page in corpus[key] or len(corpus[key]) == 0:
            sources.append(key)
    return sources


if __name__ == "__main__":
    main()

