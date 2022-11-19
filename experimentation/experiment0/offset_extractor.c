#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#include <time.h>


void offset_collector()
{
    clock_t begin = clock();

    const int SIZE = 0x32000;

    uint64_t length;
    char *buff, *buffptr;
    FILE *stream;


    char* offset = (char*) malloc (10000000);
    char* mover = offset;

    char *filename = "3gb.vcf";
    stream = fopen(filename, "r+");

    if ( (buff = (char *) malloc (SIZE)) == NULL) {
        printf("Can't get enough memory\n");
        exit(1);
    }

    uint64_t fileoff = 0;
    FILE *downstream = fopen("offset_final.txt", "w+");
    uint64_t i;

    do {
        if ( (length = fread(buff, 1, SIZE, stream)) == -1) {
            printf("Error reading file %s\n", filename);
            exit(1);
        }

        buffptr = buff;
        uint64_t lencount = length;
        // printf("\nlen count : %d\n", lencount);

        if (strlen(offset) > 9999990) {
            int stat = fwrite(offset, 1, strlen(offset), downstream);
            memset(offset, 0, 10);
            mover = offset;
            printf("This is wrong here");
        }

        while (lencount --) {
            /** Logic to count offset */
            if (*buffptr++ == '\n') {
                i = fileoff + 1;
                snprintf(mover, 20, "%lld", i);
                mover = mover + strlen(mover);
                *mover = ',';
                mover++;
            }
            fileoff++;
        }

    } while (length);

    int stat = fwrite(offset, 1, strlen(offset), downstream);
    fclose(stream);
    fclose(downstream); 

    clock_t end = clock();   
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;

    printf("Total time taken : %f", time_spent);
}

int main()
{
    offset_collector();
    return 0;
}