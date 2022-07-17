#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // Open file
    char *infile = argv[1];
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    BYTE buffer[512];
    FILE *outptr = NULL;
    char file_name[8];
    int counter = 0;
    // Read data block to memory buffer
    while (fread(buffer, 512, 1, inptr) == 1)
    {
        // Check jpeg signature
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If end of file, stop writing and close the current output file
            if (counter != 0)
            {
                fclose(outptr);
            }
            // Name the output file
            sprintf(file_name, "%03i.jpg", counter);
            outptr = fopen(file_name, "w");
            counter++;
        }
        // Write data from memory buffer to the output file if such file exists
        if (counter != 0)
        {
            fwrite(buffer, 512, 1, outptr);
        }
    }
    // Close the input file and the output file
    fclose(inptr);
    fclose(outptr);
    return 0;
}