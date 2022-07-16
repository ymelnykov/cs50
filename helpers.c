#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int rgbtAV = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen +image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = rgbtAV;
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
            image[i][j] = image[i][(width - 1) - j];
            image[i][(width - 1) - j] = tmp[0][0];
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    //Make a copy of original array to work with unmodified data
    RGBTRIPLE tmp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmp[i][j] = image[i][j];
        }
    }
    //Execute blur algorithm
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float rgbBlueSum = 0;
            float rgbGreenSum = 0;
            float rgbRedSum = 0;
            int counter = 0;
            for (int m = i - 1; m <= i + 1; m++)
            {
                if (m >= 0 && m < height)
                {
                    for (int n = j - 1; n <= j + 1; n++)
                    {
                        if (n >= 0 && n < width)
                        {
                            rgbBlueSum += tmp[m][n].rgbtBlue;
                            rgbGreenSum += tmp[m][n].rgbtGreen;
                            rgbRedSum += tmp[m][n].rgbtRed;
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
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    //Make a copy of original array to work with unmodified data
    RGBTRIPLE tmp[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            tmp[i][j] = image[i][j];
        }
    }
    // Execute edge algorithm
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float rgbBlueGX = 0;
            float rgbGreenGX = 0;
            float rgbRedGX = 0;
            float rgbBlueGY = 0;
            float rgbGreenGY = 0;
            float rgbRedGY = 0;

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
                                rgbBlueGX += tmp[m][n].rgbtBlue * 2 * (n - j);
                                rgbGreenGX += tmp[m][n].rgbtGreen * 2 * (n - j);
                                rgbRedGX += tmp[m][n].rgbtRed * 2 * (n - j);
                            }
                            else
                            {
                                rgbBlueGX += tmp[m][n].rgbtBlue * (n - j);
                                rgbGreenGX += tmp[m][n].rgbtGreen * (n - j);
                                rgbRedGX += tmp[m][n].rgbtRed * (n - j);
                            }
                            if (n == j)
                            {
                                rgbBlueGY += tmp[m][n].rgbtBlue * 2 * (m - i);
                                rgbGreenGY += tmp[m][n].rgbtGreen * 2 * (m - i);
                                rgbRedGY += tmp[m][n].rgbtRed * 2 * (m - i);
                            }
                            else
                            {
                                rgbBlueGY += tmp[m][n].rgbtBlue * (m - i);
                                rgbGreenGY += tmp[m][n].rgbtGreen * (m - i);
                                rgbRedGY += tmp[m][n].rgbtRed * (m - i);
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
