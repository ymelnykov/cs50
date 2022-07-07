#include <cs50.h>
#include <stdio.h>

//Below is the function buildind the pyramid

void pyramid(int height)
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < (height - i - 1); j++)
        {
            printf(" ");
        }
        for (int j = 0; j < (i + 1); j++)
        {
            printf("#");
        }
        printf("  ");
        for (int j = 0; j < (i + 1); j++)
        {
            printf("#");
        }
        printf("\n");
    }
}

int main(void)
{
   int height;

//The below do/while enforces the user to enter the correct height

   do
   {
        height = get_int("Height: ");
   }
   while (height > 8 || height < 1);
   pyramid(height);
}