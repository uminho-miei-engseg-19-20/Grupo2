#include <stdio.h>
#include <string.h>
#include <stdlib.h>


int main(int argc, char **argv) {

    int argv_size = strlen(argv[1]);
    
    int laranjas_size = strlen("laranjas");
    
    
    char *dummy = (char *) malloc (sizeof(char) * argv_size);
    char *readonly = (char *) malloc (sizeof(char) * laranjas_size);
    
    
    if ((strlen("laranjas")) > laranjas_size) {
        printf("Not enough space!");
        return -1;
    }
    
    else {
        strcpy(readonly,"laranjas");  
    }
    
    if ((strlen(argv[1])) > argv_size) {
        printf("Not enough space for argv[1]!");
        return -1;
    }
    strcpy(dummy, argv[1]);
    printf("%s\n", readonly); 
    
}
