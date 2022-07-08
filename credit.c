#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    long num = get_long("Number: ");

//Calculating the checksum as per Luhn’s Algorithm

    int sum = 0;
    int digit = 0;
    int digit_2 = 0;
    int digits_no = 0;
    for (int i = 1; i <= 16; i++)
    {
        if (num % (long) pow(10, i-1) == num)
        {
            break;
        }
        digit = floor(num % (long) pow(10, i) / pow(10, i-1));
        digit_2 = floor(num % (long) pow(10, i-1) / pow(10, i-2));
        digits_no = i;
        if (i % 2 == 0)
        {
            sum = (digit * 2 > 9) ? sum + ((digit * 2) % 10 + floor (digit * 2 / 10)) : sum + digit * 2;
        }
        else
        {
            sum += digit;
        }
    }
    int digits = digit * 10 + digit_2;

//Checking the card number

    if (sum % 10 == 0)
    {
        if ((digits == 34 || digits == 37) && digits_no == 15)
        {
            printf("AMEX\n");
        }
        else if (digit == 4 && (digits_no == 13 || digits_no == 16))
        {
            printf("VISA\n");
        }
        else if ((digits == 51 || digits == 52 || digits == 53 || digits == 54 || digits == 55) && digits_no == 16)
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}