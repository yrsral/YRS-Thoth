#Modified from http://norvig.com/spell-correct.html
import json
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


#This piece of code calculates the probability of the author meaning to write a particular real word given that they have written an incorrectly spelled word

#Need to calculate and maximise p(c|w) #Probability that they meant to write word c when they have written incorrect word w

#Bayes' theorem:
  #p(a and b) = p(a|b) * p(b) = p(a) * p(b|a)
  #Therefore p(a|b) = p(a)/p(b) * p(b|a)

#So p(c|w) = p(w|c)*p(c)/p(w)
#p(w) is always the same so does not make  difference to the maximisation
#So we need to maximise p(w|c)*p(c)
#p(w|c) is the probability that w could be formed by editting c (the "edit distance")
#p(c) is the probability that c stands as a correct word on its own


def init():
  global spellcheck_NWORDS   #Makes the dict accessible by other functions
  model_file = open("spell_check_model.json").read()   #Gets data from a model file
  spellcheck_NWORDS = json.loads(model_file)           


#Returns the set of all words of an edit distance of 1 away from "word"
def edits1(word):
  splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
  deletes    = [a + b[1:] for a, b in splits if b]                       #Words that can be generated by deleting letters
  transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]  #Words that can be generated by transposing letters
  replaces   = [a + c + b[1:] for a, b in splits for c in ALPHABET if b] #Words that can be generated by replacing letters
  inserts    = [a + c + b     for a, b in splits for c in ALPHABET]      #Words that can be generated by inserting letters
  return set(deletes + transposes + replaces + inserts)


#Returns a set of all words that are two edits away from "word"
def known_edits2(word):
  return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in spellcheck_NWORDS)


#Reduces the set of words to ones which have been seen before
def known(words):
  return set(w for w in words if w in spellcheck_NWORDS)


def correct(word):
  candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word] #Checks for potential candidates in this order
  return max(candidates, key=spellcheck_NWORDS.get) #Gets the best candidate