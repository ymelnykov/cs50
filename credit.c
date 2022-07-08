#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long num;
    do
    {
        num = get_long("Number: ");
    }
    while (num % (long) pow(10, 12) == num || num % (long) pow(10, 16) != num);

//Calculating the checksum as per Luhn’s Algorithm

    int sum = 0;
    int digit = 0;
    for (int i = 1; i <= 16; i++)
    {
        if (num % (long) pow(10, i-1) == num)
        {
            break;
        }
        digit = floor(num % (long) pow(10, i) / pow(10, (i-1)));
        if (i % 2 == 0)
        {
            sum = (digit * 2 > 9) ? sum + ((digit * 2) % 10 + floor (digit * 2 / 10)) : sum + digit * 2;
        }
        else
        {
            sum += digit;
        }
    }

//Checking the card number

    if (sum % 10 == 0)
    {
        switch(digit)
        {
            case 3:
                printf("AMEX\n");
                break;
            case 4:
                printf("VISA\n");
                break;
            case 5:
                printf("MASTERCARD\n");
                break;
            default:
                printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}