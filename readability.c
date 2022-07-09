#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    string text = get_string("Text: ");

    // Calculate Coleman-Liau index

    float L = count_letters(text) * 100 / (float) count_words(text);
    float S = count_sentences(text) * 100 / (float) count_words(text);
    int index = round(0.0588 * L - 0.296 * S - 15.8);

    // Show the Grade

    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

//Count letters

int count_letters(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int a_value = (int) text[i];
        counter = ((a_value >= 65 && a_value <= 90) || (a_value >= 97 && a_value <= 122)) ? counter + 1 : counter;
    }
    return counter;
}

//Count words

int count_words(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int a_value = (int) text[i];
        counter = (a_value == 32) ? counter + 1 : counter;
    }
    return counter + 1;
}

//Count sentences

int count_sentences(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        int a_value = (int) text[i];
        counter = (a_value == 33 || a_value == 46 || a_value == 63) ? counter + 1 : counter;
    }
    return counter;
}