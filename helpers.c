#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int blue = image[i][j].rgbtBlue;
            int green = image[i][j].rgbtGreen;
            int red = image[i][j].rgbtRed;
            int average = round ((blue + green + red) / 3);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;

        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp[1][1];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0, n = floor(width / 2); j < n; j++)
        {
            tmp[0][0] = image[i][j];
            image[i][j] = image[i][width-j];
            image[i][width-j] = tmp[0][0];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbBlueSum = 0;
            int rgbGreenSum = 0;
            int rgbRedSum = 0;
            int counter = 0;
            for (int m = i - 1; m <= i + 1; m++)
            {
                if (m >= 0 && m < height)
                {
                    for (int n = j - 1; n <= j + 1; n++)
                    {
                        if (n >= 0 && n < width)
                        {
                            rgbBlueSum += image[m][n].rgbtBlue;
                            rgbGreenSum += image[m][n].rgbtGreen;
                            rgbRedSum += image[m][n].rgbtRed;
                            counter++;
                        }
                    }
                }
            }
            image[i][j].rgbtBlue = round(rgbBlueSum / counter);
            image[i][j].rgbtGreen = round(rgbGreenSum / counter);
            image[i][j].rgbtRed = round(rgbRedSum / counter);
        }
    }
    return;
    //return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double rgbBlueGX = 0;
            double rgbGreenGX = 0;
            double rgbRedGX = 0;
            double rgbBlueGY = 0;
            double rgbGreenGY = 0;
            double rgbRedGY = 0;

            for (int m = i - 1; m <= i + 1; m++)
            {
                if (m >= 0 && m < height)
                {
                    for (int n = j - 1; n <= j + 1; n++)
                    {
                        if (n >= 0 && n < width)
                        {
                            if (m == i)
                            {
                                rgbBlueGX += image[m][n].rgbtBlue * 2 * (n - j);
                                rgbGreenGX += image[m][n].rgbtGreen * 2 * (n - j);
                                rgbRedGX += image[m][n].rgbtRed * 2 * (n - j);
                            }
                            else
                            {
                                rgbBlueGX += image[m][n].rgbtBlue * (n - j);
                                rgbGreenGX += image[m][n].rgbtGreen * (n - j);
                                rgbRedGX += image[m][n].rgbtRed * (n - j);
                            }
                            if (n == j)
                            {
                                rgbBlueGY += image[m][n].rgbtBlue * 2 * (m - i);
                                rgbGreenGY += image[m][n].rgbtGreen * 2 * (m - i);
                                rgbRedGY += image[m][n].rgbtRed * 2 * (m - i);
                            }
                            else
                            {
                                rgbBlueGY += image[m][n].rgbtBlue * (m - i);
                                rgbGreenGY += image[m][n].rgbtGreen * (m - i);
                                rgbRedGY += image[m][n].rgbtRed * (m - i);
                            }
                        }
                    }
                }
            }
            image[i][j].rgbtBlue = round(sqrt(pow(rgbBlueGX, 2) + pow(rgbBlueGY, 2)));
            if (image[i][j].rgbtBlue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            image[i][j].rgbtGreen = round(sqrt(pow(rgbGreenGX, 2) + pow(rgbGreenGY, 2)));
            if (image[i][j].rgbtGreen > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            image[i][j].rgbtRed = round(sqrt(pow(rgbRedGX, 2) + pow(rgbRedGY, 2)));
            if (image[i][j].rgbtRed > 255)
            {
                image[i][j].rgbtRed = 255;
            }
        }
    }
    return;
}
