text = 'To overcome these limitations, as a future line of research the authors would like to extend the analysis of the economic impact to all the agents involved in the wine routes. We would also like to ask the wineries directly about the effects of the pandemic on their wine tourism activity, as well as their opinion on the different measures that the Spanish government has implemented to improve the situation of wine companies.'

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

print(sent_tokenize(text))