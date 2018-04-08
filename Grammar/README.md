[![python](https://img.shields.io/badge/python-3.5-blue.svg)](https://www.python.org/downloads/)

# Portuguese Grammar
## Installation:
```
Version: Python 3.5.2 | SWI-Prolog 7.2.3 | nltk 3.2.5
$ git clone https://github.com/Truvam/IA.git
$ cd IA/Grammar/
$ sudo pip3 install -r requirements.txt
```
## Example Python:
### `Input:`
```
$ python3 grammar.py
Portuguese Grammar:
Do you want to load test_sentences.pl? [y/n]: n
Write your sentence (Example: A menina corre para a floresta):
Sentence: A menina corre para a floresta
(S[]
  (NP[G='f', NUM='sg']
    (Det[G='f', NUM='sg'] A)
    (N[G='f', NUM='sg'] menina))
  (VP[NUM='sg']
    (V[NUM='sg'] corre)
    (P[G='f', NUM='sg']
      (Prep[G='f', NUM='sg'] para)
      (NP[G='f', NUM='sg']
        (Det[G='f', NUM='sg'] a)
        (N[G='f', NUM='sg'] floresta)))))

```
### `Input:`
```
Portuguese Grammar:
Do you want to load test_sentences.pl? [y/n]: y
Sentence: A menina corre para a floresta
(S[]
  (NP[G='f', NUM='sg']
    (Det[G='f', NUM='sg'] A)
    (N[G='f', NUM='sg'] menina))
  (VP[NUM='sg']
    (V[NUM='sg'] corre)
    (P[G='f', NUM='sg']
      (Prep[G='f', NUM='sg'] para)
      (NP[G='f', NUM='sg']
        (Det[G='f', NUM='sg'] a)
        (N[G='f', NUM='sg'] floresta)))))

Sentence: A menina corre para a mae
(S[]
  (NP[G='f', NUM='sg']
    (Det[G='f', NUM='sg'] A)
    (N[G='f', NUM='sg'] menina))
  (VP[NUM='sg']
    (V[NUM='sg'] corre)
    (P[G='f', NUM='sg']
      (Prep[G='f', NUM='sg'] para)
      (NP[G='f', NUM='sg']
        (Det[G='f', NUM='sg'] a)
        (N[G='f', NUM='sg'] mae)))))

Sentence: A vida corre
(S[]
  (NP[G='f', NUM='sg']
    (Det[G='f', NUM='sg'] A)
    (N[G='f', NUM='sg'] vida))
  (VP[NUM='sg'] (V[NUM='sg'] corre)))

(...)

Sentence: A tempo corre
False.
Sentence: O tempo correram
False.
Sentence: A cacador corriam pela rosto
False.
Sentence: A tambores correu pela floresta
False.
Sentence: Os tambores bateu na porta
False.
```
## Example ProLog:
```
$ swipl
?- [grammar].
?- sentence(X, ['A',menina,corre,para,a,floresta],[]).
X = sent(noun_phrase(determiner_f('A'), noun(menina)), verbal_phrase(verb(corre), preposition(para), noun_phrase(determiner_f(a), noun(floresta)))) .

?- sentence(X, ['A',tempo,corre],[]).
false.