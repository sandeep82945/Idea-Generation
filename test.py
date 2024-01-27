import re

# Your input text
text = '''The future work text from the input is as follows:
"In future studies, it would be valuable to examine other parameter settings, such as temperature, to explore their effects on the emergent behavior of LLM-generated agents. Additionally, as more advanced LLMs like GPT-4 become available, it would be interesting to investigate whether they exhibit similar limitations or are capable of more nuanced cooperative behaviors in a wider array of social dilemmas. Another potential limitation of the current study is that the LLM has been exposed to a vast literature on the iterated Prisoner’s Dilemma in its training data, and it is unclear how would it perform in more ecologically valid task environments that it has no prior exposure to. This limitation could be addressed by inventing new social dilemma games with corresponding task descriptions which are not vignettes from the existing literature.
By addressing these questions, we hope to collectively build a deeper understanding of AI alignment in the context of complex, non-zero-sum interactions across various experimental economics settings, ultimately fostering the development of AI systems that better adhere to human values and social norms."'''

# Regular expression pattern to find text within double quotes, including newlines
pattern = r'"(.*?)"'

# Find all occurrences of the pattern, using re.DOTALL to make '.' match newlines
matches = re.findall(pattern, text, re.DOTALL)

# Assuming there's only one match and you want to print it
if matches:
    print(matches[0])
else:
    print("No matches found.")