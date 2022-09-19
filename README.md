# Text Analyser
#### Video Demo:  <https://youtu.be/o6IdKmwympQ>

## Description

**Text Analyser** is a language tool in the form of a website that allows a user to analyse texts of different nature using various analysis options to generate text statistic and determine text readability characteristics.
This project has been developed by Yuriy Melnykov as a final project of [CS50’s Introduction to Computer Science]( https://learning.edx.org/course/course-v1:HarvardX+CS50+X/home) course by Harvard University.

### Technologies
The project has been built using 7 programming languages and frameworks: Python, Flask, Jinja, SQL, HTML, CSS, Bootstrap.

### Contents
The project contains 2 Python files, 5 HTML files, 1 CSS file, 1 SQL database consisting of 5 tables and also auxiliary graphic and text files:

**app.py**
is a Flask application file that contains all website logic and controls website operation.

**helpers.py**
contains functions with all counting, processing and calculating algorithms.

**index.html**
is the main webpage file a user interacts with. It is where all major inputs and outputs take place.

**layout.html**
is the template that contains webpage header and footer.

**login.html**
is a webpage file for a registered user to log in.

**register.html**
is a webpage file for a user to register.

**texts.html**
is a webpage file for a registered user where he/she can access all his/her saved text analysis results.

**styles.css**
contains some style features.

**text_analysis.db**
is a SQL database where records of all registered users and text analysis results saved by them are stored.

### Background
Having more than 20 years’ experience in the field of translations I used to work with lots of various texts. That is why I found it very interesting to solve the Readability problem during CS50x course and decided to develop on it in my final project and create a website to analyse.

To start with, I began searching for various information on the topic and found out that in addition to Coleman-Liau Index mentioned in CS50x course there are many other readability formulas developed and widely used. Generally, most of them can be split in two groups: those that rely on the number of characters per word (e.g., Coleman-Liau Grade and Automated Readability Index) and those that suppose that the number of syllables per word is the key to defining the readability (e.g., Gunning Fog Index, Flesch-Kincaid Grade Level, SMOG Grade).

Then, I took a look at some similar text analysers available on the internet, both the free projects and the commercial ones ([textinspector.com]( https://textinspector.com/workflow), [english.com]( https://www.english.com/gse/teacher-toolkit/user/textanalyzer), [lexicool.com]( https://www.lexicool.com/text_analyzer.asp), [online-utility.org]( https://www.online-utility.org/text/analyzer.jsp), [seotoolscentre.com]( https://seotoolscentre.com/online-sentence-counter), [ usingenglish.com]( https://www.usingenglish.com/members/text-analysis/)), some of which claim to be trusted by world-known universities, colleges and organisations. Since even commercial projects offered some limited free use, I tested all of them using different texts from the CS50x’s Speller problem package. I was so much surprised when I found out that some results generated by them matched, other did not, but there were no two text analysers generating all the same equal results.

My initial counting algorithms did not stand out and followed the general trend. Nevertheless, a perfectionist living inside of me required the answers and I started digging in.

To make a long story short, I have finally managed to find the reasons for the difference in calculations and developed the text analyser allowing the user to perform the text analysis according to his/her preferences, using 12 available text analysis options.

### Project Features
**Count and calculate 23 text statistic and readability characteristics:** number of words, syllables, sentences, characters, spaces, letters, digits, letters per word, syllables per word, words per sentence, readability summary, estimated reading time and speaking time, number of different words, long words and complex words, Gunning Fog Index, Coleman Liau Grade, Flesch Kincaid Grade Level, Flesch Reading Ease, Automated Readability Index, SMOG Grade and LIX (Laesbarhedsindex).

**See text words distribution by length and output all or a specified number of text words sorted** by one of 4 criteria (alphabet, occurrence, length, number of syllables) in ascending or descending order.

**Fine tune the text analysis using a total of 12 counting, processing and calculating options** (2 for words, 3 for syllables, 3 for sentences and 4 for numbers).

**Register to analyse longer texts and save text analysis results for future reference**.

### Project Flavour
Texts of different nature may vary a lot in terms of means of language used. Imaginative literature may be rich in quoted speech and various combinations of punctuation signs. Scientific texts may have many complex words and numbers. Legal papers are known for their hard-to-read long and intricate wording. Therefore, each text requires a special approach.

What makes this project stand out? Unlike other text analysers I used, this one allows a user to take advantage of 12 available text analysis options and fine tune the analysis considering the nature of the text to be analysed. These options are worth of more detailed description.

#### Text Analysis Options
*For words:*

**Ignore “zero-length words”**.
Allows to avoid including zero-length words in readability calculations. The zero-length word means a non-readable character or a group of characters, other than letters or digits (e.g., dash “–“, ellipse “…”), separated by a space on both sides. During processing these characters are removed leaving a word of zero length. This option is highly recommended.

**Split compound words**.
Allows splitting compound words that contain a hyphen (e.g., “flower-pot” will be processed as “flower” and “pot”). It avoids including such compound words in readability calculations as some readability calculation algorithms (e.g., Gunning-Fog Index) require.

*For syllables:*

**Dictionary**.
Syllables are counted by referencing data from the [Carnegie Mellon dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict), which includes over 134,000 words with accurate syllable counts. If a word is not in the dictionary, the number of syllables is assumed to be one.

**Algorithm**.
Syllables are counted using an [algorithm](https://medium.com/@mholtzscher/programmatically-counting-syllables-ca760435fab4) proposed by Michael Holtzscher.

**Combo**.
This option combines the above two. First, the dictionary is requested. If a word is not found in the dictionary, the number of syllables is calculated using the algorithm.

*For sentences:*

**Need capital letter**.
In addition to other requirements, a sentence is counted only if a word following a punctuation sign (“.”, “?”, “!”) starts with a capital letter (e.g., 'I wonder how many miles I've fallen by this time?' she said aloud.’ will be counted as one sentence).

**Quotes enough**.
In contrast to the above option, this one assumes that any kind of quotes or brackets following a punctuations sign (“.”, “?”, “!”) is enough to count a sentence (e.g., 'I wonder how many miles I've fallen by this time?' she said aloud.’ will be counted as two sentences).

**Count them all**.
Any occurrence of a punctuation sign (“.”, “?”, “!”) or a group of such signs is counted as a sentence.

*For numbers:*

**Ignore numbers**.
Allows to avoid including numbers in readability calculations.

**One number - one word**.
Allows processing each number as one word that contains one syllable (e.g., “1,345,617.304” will be processed as “1,345,617.304” giving one long word with one syllable).

**Digit-by-digit**.
Allows processing each number as a sequence of digits (e.g., “1,345,617.304” will be processed as “one three four five six one seven point three zero four”, i.e. a total of 11 words).

**Normal reading**.
Allows processing each number as a human would read it (e.g., “1,345,617.304” will be processed as “one million three hundred forty five thousand six hundred seventeen point three zero four”, i.e. a total of 14 words).



