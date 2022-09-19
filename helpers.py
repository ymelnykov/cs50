import re

from flask import redirect, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def digit_by_digit(number):
    """Name digits in a number"""
    # Make a list of number names
    numbers = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
               'eight', 'nine']
    # Initialize output list
    dbd = []
    # Check each character in the number
    for i in number:
        # if digit, append digit name
        if i.isdigit():
            dbd.append(numbers[int(i)])
        # if point, append point
        elif i == '.':
            dbd.append('point')
    # Return the output list
    return dbd


def normal_reading(number):
    """Convert number to number name"""
    # Make a list of number names
    numbers = [['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven',
               'eight', 'nine'], ['ten', 'eleven', 'twelve', 'thirteen',
                'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen',
                'nineteen'], 'twenty', 'thirty', 'forty', 'fifty', 'sixty',
               'seventy', 'eighty', 'ninety']
    # and order names
    order = ['thousand', 'million', 'billion', 'trillion',
              'quadrillion', 'quintillion', 'sextillion', 'septillion',
              'octillion', 'nonillion', 'decillion', 'duodecillion',
    'tredecillion', 'quattuordecillion', 'quindecillion', 'sedecillion',
    'septendecillion', 'octodecillion', 'novendecillion', 'vigintillion',
    'unvigintillion', 'duovigintillion', 'tresvigintillion',
    'quattuorvigintillion', 'quinvigintillion', 'sesvigintillion',
    'septemvigintillion', 'octovigintillion', 'novemvigintillion',
    'trigintillion', 'untrigintillion', 'duotrigintillion',
    'trestrigintillion', 'quattuortrigintillion', 'quintrigintillion',
    'sestrigintillion', 'septentrigintillion', 'octotrigintillion',
    'noventrigintillion', 'quadragintillion']
    # Initialize output list
    nr_output = []
    # If number contains point separator
    if '.' in number:
        # Split it in integral part (a), point (b) and fractional part (c)
        part = number.partition('.')
        a = part[0]
        # If integral part is zero, append zero
        if a == '0':
            nr_output.append('zero')
        b = 'point'
        # Process fractional part using the above function
        c = digit_by_digit(part[2])
    else:
        a = number
        b = ''
        c = ''
    # Calculate integral part length
    length_a = len(a)
    # and make it divisible by 3 by adding leading zeros, if required
    if length_a >= 3:
        if length_a % 3 != 0:
            x = a.zfill(length_a + (3 - length_a % 3))
        else:
            x = a
    else:
        x = a.zfill(3)
    # Calculate the result length
    length_x = len(x)
    # Set a pointer to the required order in the list of orders
    j = int(length_x / 3 - 1)
    # Process all digits of the integral part in triads
    for i in range(0, (length_x - 2), 3):
        j -= 1
        # If non-zero, append number of hundreds
        if x[i] != '0':
            nr_output.append(numbers[0][int(x[i])])
            nr_output.append('hundred')
        # If non-zero, append number of tens and ones, append order
        if x[i+1] != '0':
            if x[i+1] == '1':
                nr_output.append(numbers[1][int(x[i+2])])
                if j >= 0:
                    nr_output.append(order[j])
            else:
                nr_output.append(numbers[int(x[i+1])])
                if x[i+2] != '0':
                    nr_output.append(numbers[0][int(x[i+2])])
                if j >= 0:
                    nr_output.append(order[j])
        else:
            if x[i+2] != '0':
                nr_output.append(numbers[0][int(x[i+2])])
                if j >= 0:
                    nr_output.append(order[j])
    # Append point, if any
    if b:
        nr_output.append(b)
    # Append fractional part, if any
    if c:
        nr_output.extend(c)
    # Return the output list
    return nr_output


def syllables_dic():
    """Count syllables by referencing data from the Carnegie Mellon University dictionary"""
    # Open the dictionary file to read data
    fhand = open('cmudict-0_7b-mod.txt', encoding='ISO-8859-1')
    # Initialize dictionary for syllables count
    syl_count = {}
    # Read each line and separate the word from its spelling
    for line in fhand:
        line = line.split('  ')
        counter = 0
        # Count syllables by number of digital sress marks in the spelling
        for i in line[1]:
            if i.isdigit():
                counter += 1
        syl_count[(line[0]).lower()] = counter
    fhand.close()
    return syl_count


def syllables(word):
    """Count syllables if word is not in the Carnegie Mellon University dictionary"""
    syllable_count = 0
    vowels = 'aeiouy'
    if word[0] in vowels:
        syllable_count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            syllable_count += 1
    if word.endswith('e'):
        syllable_count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        syllable_count += 1
    if syllable_count == 0:
        syllable_count += 1
    return syllable_count

def timing(words, wpm):
    """Estimate time for text reading/speaking"""
    time = round(words * 60 / wpm)
    hours = time // 3600
    minutes = (time % 3600) // 60
    seconds = (time % 3600) % 60
    if hours == 0 and minutes == 0:
        time_estimate = f'{seconds} sec'
    elif hours == 0:
        time_estimate = f'{minutes} min {seconds} sec'
    else:
        time_estimate = f'{hours} hr {minutes} min'
    return time_estimate

def numeral(number):
    if number == 1:
        return '1st'
    elif number == 2:
        return '2nd'
    elif number == 3:
        return '3rd'
    else:
        return f'{number}th'

def distribute_words(words):
    """Distribute words by their length"""
    word_distr = {}
    for n in words:
        if n[1][1] in word_distr:
            word_distr[n[1][1]][0] += n[1][0]
            word_distr[n[1][1]][1] += 1
        else:
            word_distr[n[1][1]] = [n[1][0], 1]
    word_distribution = sorted((word_distr).items(), key = lambda i: i[0])
    return word_distribution


def analyse_text(text, w1, w2, sy_option, s_option, n_option):
    '''Analyse the text'''
    # Initialize parameters
    letter_count = digit_count = space_count = syllable_count = sentence_count = 0
    complex_words = long_words = zero_word = syllable_number = ignored_number = 0
    statistics = []
    readability = []
    words = {}
    results = []
    text_length = len(text)
    # Iterate over the text
    for i in range(text_length):
        # Count number of letters
        if text[i].isalpha():
            letter_count += 1
            continue
        # Count number of digits
        if text[i].isdigit():
            digit_count += 1
            continue
        # Count number of spaces
        if text[i].isspace():
            space_count += 1
            continue
    # Split text in words
    text = text.split()
    word_count = len(text)
    # Load in memory the dictionary showing the number of syllables in words if requested
    if sy_option == 'sy1' or 'sy3':
        syl_dic = syllables_dic()

    # Iterate over the list of words
    j = 0
    word_total = word_count
    while j < word_total:

        """Count number of sentences"""
        if j < word_total - 1:
            # Apply "Need capital letter" option if requested
            if s_option == 's1':
                if re.search(r'[.!?]+[)}"]*(\')*(\])*', text[j]) and re.search(r'^[({"]*(\')*(\[)*[A-Z][^.]*', text[j+1]):
                    sentence_count += 1
            # Apply "Quoted enough" option if requested
            elif s_option == 's2':
                if (re.search(r'[.!?]+[)}"]*(\')*(\])*', text[j]) and re.search(r'^[({"]*(\')*(\[)*[A-Z][^.]*', text[j+1])) or re.search(r'[.!?]+([)}"]+|(\')+|(\])+)', text[j]):
                    sentence_count += 1
            # Apply "Count them all" option if requested
            else:
                if re.search(r'[.!?]', text[j]):
                    sentence_count += 1

        """Process numbers, if any"""
        # Check if the word is a number
        x1 = re.search(r'\d+(,\d{3})*(\.\d+)?', text[j])
        # If it is a number
        if x1:
            # Apply "Ignore numbers" option if requested
            if n_option == 'n1':
                ignored_number += 1
                # Adjust number of characters, spaces, digits
                x2 = x1.group()
                text_length -= len(x2)
                space_count -= 1
                digit_count -= len(re.sub(r'[.,]', '', x2))
                j += 1
                continue
            # Apply "Digit by digit" option if requested
            elif n_option == 'n3':
                x2 = x1.group()
                num = re.sub(r',', '', x2)
                number_name = digit_by_digit(num)
                # Adjust number of characters, spaces, letters, digits
                letter_count += len(''.join(number_name))
                space_count += len(number_name) - 1
                digit_count -= len(re.sub(r'\.', '', num))
                text_length = text_length + len(''.join(number_name)) + len(number_name) - len(re.sub(r'\.', '', num))
                # Replace the number with the last word of number name
                text[j] = number_name.pop()
                # Add other words to the end of the text words list
                text.extend(number_name)
                word_total += len(number_name)
            # Apply "Normal reading" option if requested
            elif n_option == 'n4':
                x2 = x1.group()
                num = re.sub(r',', '', x2)
                number_name = normal_reading(num)
                # Adjust number of characters, spaces, letters, digits
                letter_count += len(''.join(number_name))
                space_count += len(number_name) - 1
                digit_count -= len(re.sub(r'\.', '', num))
                text_length = text_length + len(''.join(number_name)) + len(number_name) - len(re.sub(r'\.', '', num))
                # Replace the number with the last word of number name
                text[j] = number_name.pop()
                # Add other words to the end of the text words list
                text.extend(number_name)
                word_total += len(number_name)

        """Process words"""
        # Apply "Split compound words" option if requested
        if w2 == 'w2':
            # Split any compound word with a hyphen
            if '-' in text[j]:
                splitted = text[j].split('-')
                # Clear obtained new words from punctuation signs
                new_words = []
                for k in splitted:
                    new_words.append(re.sub('\W', '', k).lower())
                # Replace the compound word with the last of new words
                text[j] = new_words.pop()
                # Add other new words to the end of the text words list
                text.extend(new_words)
                word_total += len(new_words)

        # Clear every word from puctiation signs
        word = re.sub('\W', '', text[j]).lower()

        # Apply "Ignore zero-length words" option if requested
        if w1 == 'w1':
            if len(word) == 0:
                zero_word += 1
                j += 1
                continue

        # Count number of long words
        if len(word) > 6:
            long_words += 1

        """Count number of syllables"""
        # Apply "Dictionary" option if requested
        if sy_option == 'sy1':
            # Get number of syllables in each word from the dictionary
            if word in syl_dic:
                syllable_number = syl_dic[word]
            else:
                syllable_number = 1
        # Apply "Algorithm" option if requested
        elif sy_option == 'sy2':
            if len(word) > 0:
                syllable_number = syllables(word)
        # Apply "Combo" option if requested
        else:
            # Find number of syllables in each word from the dictionary
            if word in syl_dic:
                syllable_number = syl_dic[word]
            # Otherwise calculate the number of syllables
            else:
                if len(word) > 0:
                    syllable_number = syllables(word)
        syllable_count += syllable_number

        # Count number of complex words
        if syllable_number >= 3:
            complex_words += 1
        # Add word in dictionary of words
        if word in words:
            words[word][0] += 1
        else:
            words[word] = [1, len(word), syllable_number]
        j +=1
    diff_words = len(words)
    if s_option == 's1' or 's2':
        sentence_count +=1
    word_count_adj = word_total - zero_word - ignored_number
    if word_count_adj == 0:
        word_count_adj = 1

    """Calculate and interpret readability charactertistics"""
    # Calculate average number of words per sentence
    aws = word_count_adj / sentence_count
    # Calculate characters without spaces
    cwos = text_length - space_count
    # Calculate average number of syllables per word
    asw = syllable_count / word_count_adj
    # Calculate average number of characters per word
    acw = (letter_count + digit_count) / word_count_adj
    # Calculate average number of letters per word
    alw = letter_count / word_count_adj
    # Calculation and interpret Gunning Fog index
    gunning_fog = 0.4 * (aws + 100 * (complex_words/word_count_adj))
    if round(gunning_fog) >= 17:
        gunning_fog_inter = 'College graduate'
    elif round(gunning_fog) > 12:
        gunning_fog_inter = 'College student'
    else:
        gunning_fog_inter = f'{numeral(round(gunning_fog))} grade student'
    # Calculate and interpret Coleman-Liau Index
    coleman_liau = 5.88 * acw - 29.6 / aws - 15.8
    coleman_liau_inter = ''
    # Calculate and interpret Flesch-Kincaid Grade Level
    flesch_kincaid = 0.39 * aws + 11.8 * asw - 15.59
    flesch_kincaid_inter = ''
    # Calculate and interpret Flesch Reading Ease Score
    flesch = 206.835 - 1.015 * aws - 84.6 * asw
    if flesch > 90:
        summary = 'Very easy to read. Easily understood by an average 11-year-old student'
        flesch_inter = '5th grade student'
    elif flesch > 80:
        summary = 'Easy to read. Conversational English for consumers'
        flesch_inter = '6th grade student'
    elif flesch > 70:
        summary = 'Fairly easy to read'
        flesch_inter = '7th grade student'
    elif flesch > 60:
        summary = 'Plain English. Easily understood by 13- to 15-year-old students'
        flesch_inter = '8th and 9th grade student'
    elif flesch > 50:
        summary = 'Fairly difficult to read'
        flesch_inter = '10th to 12th grade student'
    elif flesch > 30:
        summary = 'Difficult to read'
        flesch_inter = 'College student'
    elif flesch > 10:
        summary = 'Very difficult to read. Best understood by university graduates'
        flesch_inter = 'College graduate'
    else:
        summary = 'Extremely difficult to read. Best understood by university graduates'
        flesch_inter = 'Professional'
    # Calculate and interpret automated readability index
    ari = 0.5 * aws + 4.71 * acw - 21.43
    if round(ari) >= 14:
        ari_inter = 'College student'
    elif round(ari) <= 1:
        ari_inter = 'Kindergarten'
    else:
        ari_inter = f'{numeral(round(ari) - 1)} grade student'
    # Calculate and interpret SMOG Grade (Simple Measure Of Gobbledygook)
    smog = 1.043 * (complex_words * (30 / sentence_count)) ** 0.5 + 3.1291
    smog_inter = ''
    # Calculate and interpret LIX (Laesbarhedsindex)
    lix = aws + ((100 * long_words) / word_count_adj)
    lix_inter = ''
    # Estimate text reading time
    read_time = timing(word_count_adj, 200)
    # Estimate text speaking time
    speak_time = timing(word_count_adj, 130)


    """List all characteristics for ease of use"""
    statistics.append(('Words', word_count))
    statistics.append(('Words adjusted', word_count_adj))
    statistics.append(('Syllables', syllable_count))
    statistics.append(('Sentences', sentence_count))
    statistics.append(('Characters', text_length))
    statistics.append(('Characters without spaces', cwos))
    statistics.append(('Letters', letter_count))
    statistics.append(('Digits', digit_count))
    statistics.append(('Letters per word', round(alw, 2)))
    statistics.append(('Syllables per word', round(asw, 2)))
    statistics.append(('Words per sentence', round(aws, 2)))
    statistics.append(('Analysis options', f'{w1}, {w2}, {sy_option}, {s_option}, {n_option}'))
    readability.append(('Reading time', (read_time, '(at 200 words per minute)')))
    readability.append(('Speaking time', (speak_time, '(at 130 words per minute)')))
    readability.append(('Different words', (diff_words, '(words excluding repetitions)')))
    readability.append(('Long words', (long_words, '(words with more than 6 characters)')))
    readability.append(('Complex words', (complex_words, '(words with 3 and more syllables)')))
    readability.append(('Gunning Fog Index', (round(gunning_fog, 2), gunning_fog_inter)))
    readability.append(('Coleman-Liau Grade', (round(coleman_liau, 2), coleman_liau_inter)))
    readability.append(('Flesch-Kincaid Grade Level', (round(flesch_kincaid, 2), flesch_kincaid_inter)))
    readability.append(('Flesch Reading Ease', (round(flesch, 2), flesch_inter)))
    readability.append(('Automated Readability Index', (round(ari, 2), ari_inter)))
    readability.append(('SMOG Grade', (round(smog, 2), smog_inter)))
    readability.append(('LIX (Laesbarhedsindex)', (round(lix, 2), lix_inter)))
    results.append(statistics)
    results.append(readability)
    results.append(list(words.items()))
    results.append(summary)

    return results





