import os
import random
import re
import sys


# REFERENCE: (just for my learning and future reference):
# choice: https://www.w3schools.com/python/ref_random_choice.asp
# choices: https://www.w3schools.com/python/ref_random_choices.asp
# for loop withou iterator variable:
# https://stackoverflow.com/questions/818828/is-it-possible-to-implement-a-python-for-range-loop-without-an-iterator-variable


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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Initialize probabilty distribution
    prob_dist = {}

    # Every page gets probability of 1-d / len(corpus.keys)
    prob_page = (1 - damping_factor) / len(corpus)
    for p in corpus:
        prob_dist[p] = prob_page

    # If page has links
    if corpus[page]:
        # Extra probability for every page
        # Probabilty of linked: damping factor / num of pages
        prob_link = damping_factor / len(corpus[page])
        for p in corpus[page]:
            prob_dist[p] += prob_link

    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank
    ranks = {}

    # First page at random
    current_page = random.choice(list(corpus.keys()))

    # Iteratnig
    for _ in range(n - 1):
        ranks[current_page] = ranks.get(current_page, 0) + (1 / n)
        # Get the page based on the transition model
        prob_dist = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(
            list(prob_dist.keys()), list(prob_dist.values())
        )[0]

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Base probabiltiy (1 / len(corpus)) set at beginning page
    # for page in corpus: ranks[page] = 1/len(corpus)
    ranks = {p: (1 / len(corpus)) for p in corpus}
    close = False

    while not close:
        close = True
        new_ranks = {page: 0 for page in corpus}

        for first_page in corpus:
            # Assign new rank first page constant probability
            new_ranks[first_page] += ((1 - damping_factor) / len(corpus))

            if corpus[first_page]:
                new_prob = damping_factor / len(corpus[first_page])
                for link_page in corpus[first_page]:
                    new_ranks[link_page] += new_prob * ranks[first_page]
                    if new_ranks[link_page] - ranks[link_page] > 0.001:
                        close = False
            else:
                new_prob = damping_factor / len(corpus)
                for link_page in corpus:
                    new_ranks[link_page] += new_prob * ranks[first_page]
                if new_ranks[link_page] - ranks[link_page] > 0.001:
                    close = False

        ranks = new_ranks.copy()

    return ranks


if __name__ == "__main__":
    main()
