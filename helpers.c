#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.0);
            image[i][j].rgbtBlue = image[i][j].rgbtGreen = image[i][j].rgbtRed = average;
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
            float blue_sum = 0;
            float green_sum = 0;
            float red_sum = 0;
            int counter = 0;
            for (int m = i - 1; m <= i + 1; m++)
            {
                if (m >= 0 && m < height)
                {
                    for (int n = j - 1; n <= j + 1; n++)
                    {
                        if (n >= 0 && n < width)
                        {
                            blue_sum += tmp[m][n].rgbtBlue;
                            green_sum += tmp[m][n].rgbtGreen;
                            red_sum += tmp[m][n].rgbtRed;
                            counter++;
                        }
                    }
                }
            }
            image[i][j].rgbtBlue = round(blue_sum / counter);
            image[i][j].rgbtGreen = round(green_sum / counter);
            image[i][j].rgbtRed = round(red_sum / counter);
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
    //Create Sobel array
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    // Execute edge algorithm
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float blue_Gx = 0;
            float green_Gx = 0;
            float red_Gx = 0;
            float blue_Gy = 0;
            float green_Gy = 0;
            float red_Gy = 0;

            for (int m = -1; m <= 1; m++)
            {
                if (m + i >= 0 && m + i < height)
                {
                    for (int n = -1; n <= 1; n++)
                    {
                        if (n + j >= 0 && n + j < width)
                        {
                            blue_Gx += tmp[m + i][n + j].rgbtBlue * Gx[m + 1][n + 1];
                            green_Gx += tmp[m + i][n + j].rgbtGreen * Gx[m + 1][n + 1];
                            red_Gx += tmp[m + i][n + j].rgbtRed * Gx[m + 1][n + 1];
                            blue_Gy += tmp[m + i][n + j].rgbtBlue * Gy[m + 1][n + 1];
                            green_Gy += tmp[m + i][n + j].rgbtGreen * Gy[m + 1][n + 1];
                            red_Gy += tmp[m + i][n + j].rgbtRed * Gy[m + 1][n + 1];

                        }
                    }
                }
            }
            int blue = round(sqrt(pow(blue_Gx, 2) + pow(blue_Gy, 2)));
            int green = round(sqrt(pow(green_Gx, 2) + pow(green_Gy, 2)));
            int red = round(sqrt(pow(red_Gx, 2) + pow(red_Gy, 2)));
            image[i][j].rgbtBlue = (blue > 255) ? 255 : blue;
            image[i][j].rgbtGreen = (green > 255) ? 255 : green;
            image[i][j].rgbtRed = (red > 255) ? 255 : red;
        }
    }
    return;
}
