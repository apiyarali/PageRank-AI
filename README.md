# PageRank AI

## Overview
This project implements the PageRank algorithm to rank web pages by importance. The algorithm is inspired by the original Google PageRank method, which evaluates web pages based on their linking structure. Two approaches were implemented:
1. **Sampling Method**: Uses a Markov Chain random surfer model to estimate PageRank by simulating a random user's navigation behavior.
2. **Iterative Method**: Uses the mathematical PageRank formula iteratively until convergence.

## Results
Running the algorithm on `corpus0` produces the following PageRank values:

```
$ python pagerank.py corpus0
PageRank Results from Sampling (n = 10000)
  1.html: 0.2223
  2.html: 0.4303
  3.html: 0.2145
  4.html: 0.1329
PageRank Results from Iteration
  1.html: 0.2202
  2.html: 0.4289
  3.html: 0.2202
  4.html: 0.1307
```

The results from both methods are similar, indicating the effectiveness of both approaches.

---

## Background
Search engines rank web pages by importance based on how frequently they are linked by other pages. The PageRank algorithm enhances this ranking by considering not only the number of links but also the importance of the linking pages.

### Random Surfer Model
The algorithm models a user who randomly follows links on a webpage or jumps to a random page with a small probability (damping factor `d`). This allows for a fairer distribution of ranks across the web graph.

<img src="https://github.com/apiyarali/PageRank-AI/blob/aded483b32d84ef23ad9ae77e81a19082e883ca5/screenshots/random_surfer.png" alt="Minesweeper AI Game" width="250">
<img src="https://github.com/apiyarali/PageRank-AI/blob/aded483b32d84ef23ad9ae77e81a19082e883ca5/screenshots/random_surfer_network_disconnected.png" alt="Minesweeper AI Game" width="250">

### Iterative Approach
The mathematical PageRank formula recursively defines a page's rank based on the ranks of pages linking to it, iterating until values stabilize.

<img src="https://github.com/apiyarali/PageRank-AI/blob/aded483b32d84ef23ad9ae77e81a19082e883ca5/screenshots/iterative.png" alt="Minesweeper AI Game" width="250">

---

## Implementation
The project consists of the following core functions:

### `transition_model(corpus, page, damping_factor)`
- Generates a probability distribution over next possible pages based on the given page.
- With probability `d`, chooses a link from the current page.
- With probability `1-d`, selects any page from the corpus at random.

### `sample_pagerank(corpus, damping_factor, n)`
- Estimates PageRank by simulating a random surfer.
- Uses the transition model to generate `n` samples and counts page visits to approximate PageRank values.

### `iterate_pagerank(corpus, damping_factor)`
- Computes PageRank values iteratively based on the mathematical formula.
- Updates each page’s rank until convergence (change < 0.001).

---

## Usage
### Running the Program
To compute PageRank for a given corpus:
```sh
python pagerank.py <corpus-directory>
```
Example:
```sh
python pagerank.py corpus0
```

### Dependencies
- Python 3.x
- Standard libraries (`random`, `sys`, `os`)

---

## Key Features
✅ Implements both sampling and iterative approaches to PageRank.  
✅ Handles cases where pages have no outbound links.  
✅ Adjustable damping factor (`d`) and sample size (`n`).  
✅ Results converge to a stable ranking.  

---

## Conclusion
This project effectively computes PageRank using two distinct approaches. The results confirm that both methods produce consistent rankings, demonstrating the robustness of the PageRank algorithm.

## Credits
Inspired by Harvard's CS80 AI course and the Uncertainty and Propbability techniques used in AI to represent and derive new knowledge.
