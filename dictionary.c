// Implements a dictionary's functionality
#include <stdlib.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include "dictionary.h"

unsigned int word_counter = 0;
unsigned int hash_code;

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Choose number of buckets in hash table
const unsigned int N = 90 * LENGTH;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // Calculate hash code of a word
    hash_code = hash(word);
    // Look for the word in the dictionary
    for (node *cursor = table[hash_code]; cursor != NULL; cursor = cursor->next)
    {
        // If found, return true
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    unsigned int char_code;
    // Calculate the hash code as a sum of ascii codes of all characters in the word
    while ((char_code = toupper(*word++)))
    {
        hash += char_code;
    }
    return hash;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Open the dictionary
    FILE *inptr = fopen(dictionary, "r");
    if (inptr == NULL)
    {
        printf("Could not open the dictionary.\n");
        return false;
    }
    char word[LENGTH + 1];
    // Read the dictionary word by word
    while (fscanf(inptr, "%s", word) != EOF)
    {
        // Allocate memory for the node to store the word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            return false;
        }

        // Copy the word from the buffer to the node
        strcpy(n->word, word);

        // Place the node to the hash table according to its hash code and update the word counter
        hash_code = hash(word);
        n->next = table[hash_code];
        table[hash_code] = n;
        word_counter++;
    }
    // Close the dictionary file
    fclose(inptr);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // Return words count, if any
    if (word_counter != 0)
    {
        return word_counter;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        // Set the cursor to the head of the i-th linked list
        node *cursor = table[i];
        // Free memory allocated for each node in the i-th linked list using a temporary pointer
        while (cursor)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
        if (i == N - 1 && cursor == NULL)
        {
            return true;
        }
    }
    return false;
}
