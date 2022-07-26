from cs50 import get_string

# Enter text
text = get_string('Text: ')

# Initialize parameters
letters = words = sentences = 0
signs = ['.', '!', '?']

# Count letters, words and sentences
for i in range(len(text)):
    if text[i].isalpha():
        letters += 1
    if text[i].isspace():
        words += 1
    if text[i] in signs:
        sentences += 1
words = words +1

# Calculate index
L = letters * 100 / words
S = sentences * 100 / words
index = round(0.0588 * L - 0.296 * S - 15.8)

# Print grade
if index >= 16:
    print('Grade 16+')
elif index < 1:
    print('Before Grade 1')
else:
    print(f'Grade {index}')
