import nltk
from nltk import word_tokenize
from nltk.tree import *
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """

S -> NP VP
S -> NP V NP
S -> NP V NP NP
S -> NP V PP Adj NP NP V
S -> NP V AdjP N
S -> NP V NP
S -> NP V NP NP V PP NP
S -> NP VP VP NP
S -> N V NP NP VP PP NP

S -> N V AdjP Adj NP PP NP

NP -> Det N | P N | Conj N | N Adv | Adj N | AdjP N | N P DetP | N
VP -> V P | V Adv | Conj V | Conj V N | V
PP -> P Det | P
AdjP -> Det Adj | Adj
DetP -> Det N


"""
grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    frases = []
    frase = word_tokenize(sentence)

    for palabra in frase:
        minuscula = palabra.lower()
        if minuscula.isalpha():
            frases.append(minuscula)
    return frases

    #raise NotImplementedError

def filt(x):
    return x.label() == 'NP'


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.

    Devuelve una lista de todos los fragmentos de frases nominales en el árbol de oraciones.
    Un fragmento de sintagma nominal se define como cualquier subárbol de la oración.
    cuya etiqueta es "NP" que no contiene ningún otro
    frases nominales como subárboles.


    """

    chunco = []

    for subtree in tree.subtrees(filter= filt):
        chunco.append(subtree)
        print("subtree ", subtree)

    return chunco

    raise NotImplementedError


if __name__ == "__main__":
    main()
