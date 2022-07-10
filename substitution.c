#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])
{

//Check command-line argument validity

    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }

//Check key validity

    //for length

    int length = strlen(argv[1]);
    if (length != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }

    //for alphabetic nature

    for (int i = 0; i < length; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            printf("Invalid key!\n");
            return 1;
        }
    }

    //for containing each letter

    string al = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    short flag = 0;
    for (int i = 0; i < 26; i++)
    {
        for (int j = 0; j < 26; j++)
        {
            flag = 0;
            if (al[i] == toupper(argv[1][j]))
            {
                flag = 1;
                break;
            }
        }
        if (flag == 0)
        {
            printf("Invalid key!\n");
            return 1;
        }
    }

//Input text to be encrypted

    string plaintext = get_string("plaintext:  ");

//Encrypt and output

    printf("ciphertext: ");
    for (int i = 0, n = strlen(plaintext); i < n; i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                printf("%c", toupper(argv[1][(int) plaintext[i] - 65]));
            }
            else
            {
                printf("%c", tolower(argv[1][(int) plaintext[i] - 97]));
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    printf("\n");
    return 0;
}