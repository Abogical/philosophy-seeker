# Philosophy wiki seeker

A python script that demonstrates the ["Getting to Philosophy" law](https://en.wikipedia.org/wiki/Wikipedia:Getting_to_Philosophy).

Given a wikipedia URL, the script repeatedly visits the first regular\* link on the wiki article and repeats the process until it hits the [philosophy article](https://en.wikipedia.org/wiki/Philosophy).

The law is true for most articles, but the script may hit a link loop. The script also terminates when such a loop is detected.

\*: A regular link is a link that is in the main article and is not either of:

-   Between parenthesis
-   Dead link
-   Citation

## Usage

```
python3 main.py <Wikipedia URL>
```

## Example

```
$ python3 main.py https://en.wikipedia.org/wiki/Special:Random
Visiting topic Village
Visiting topic Human_settlement
Visiting topic Geography
Visiting topic Science
Visiting topic Knowledge
Visiting topic Perception
Visiting topic Sense
Visiting topic Stimulus_(physiology)
Visiting topic Physiology
Visiting topic Function_(biology)
Visiting topic Biology
Visiting topic Natural_science
Visiting topic Branches_of_science
Visiting topic Empirical
Visiting topic Information
Visiting topic Uncertainty
Visiting topic Epistemic
Found philosophy wiki! Link Path:
Peremyotnoye -> Village -> Human_settlement -> Geography -> Science -> Knowledge -> Perception -> Sense -> Stimulus_(physiology) -> Physiology -> Function_(biology) -> Biology -> Natural_science -> Branches_of_science -> Empirical -> Information -> Uncertainty -> Epistemic -> Philosophy
```

&copy; Abdelrahman Abdelrahman 2020
