#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (!strcasecmp(candidates[i].name, name))
        {
            candidates[i].votes++;
            return true;
        }
    }
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    //Sort candidates by votes using bubble sort

    int j = 0;
    while (j < candidate_count)
    {
        for (int i = 0; i <= candidate_count - 2; i++)
        {
            if (candidates[i].votes > candidates[i + 1].votes)
            {
                candidate temp = candidates[i];
                candidates[i] = candidates[i + 1];
                candidates[i + 1] = temp;
            }
        }
        if (j == 0)
        {
            printf("%s\n", candidates[candidate_count - 1].name);
            j++;
        }
        else if (j > 0 && candidates[candidate_count - j].votes == candidates[candidate_count - j - 1].votes)
        {
            printf("%s\n", candidates[candidate_count - j - 1].name);
            j++;
        }
        else
        {
            break;
        }
    }
    return;
}