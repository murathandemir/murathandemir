/*****************************************************
**      @author: MURATHAN DEMIR                     **
**      @title: EHB208E 1ST HOMEWORK                **
**      STUDENT ID : 040210220                      **
**      E-MAIL : DEMIRMU21 AT ITU.EDU.TR            **
**      ELECTRONICS AND COMMUNICATION ENGINEERING   **
**      YEAR : 2023                                 **
******************************************************/


// including necessary libraries for further code.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define READ_BUFFER 30 // it is a necessary buffer to reading data from file.
// it defines length of just a single line.
// if there are some lines which longer than 20 charachter,
// only its first 20 character will be received.


struct ContentList{ // it is a linkedlist structure for input data, which has attributes row,column numbers and data.
    int rowNumber;
    int columnNumber;
    int content;
    struct ContentList *next;
}; typedef struct ContentList contentNodes;

struct DuplicateList{ // it is a linkedlist structure for counting frequency of each element.
    int content;
    int pairs;
    struct DuplicateList *next;
}; typedef struct DuplicateList duplicateNodes;

// prototypes of my functions.
int ParameterChecker(char* arr[]);
void HelpText();

int main(int argc, char *argv[]){
    /*
        argv[0] = program name
        argv[1] = option (--print, --nzeros, --duplicates, --help)
        argv[2] = input parameter (-i)
        argv[3] = input file
        argv[4] = output parameter (-o)
        argv[5] = output file
    */
    int parameterStatus = ParameterChecker(argv);/*
        if returned 1 : option == --print
        if returned 2 : option == --nzeros
        if returned 3 : option == --duplicates 
        if returned 4 : option == --help */
    if(parameterStatus > 0 && parameterStatus < 4){ // file operations will be done here. there is no need to file operations on the other conditions.
        FILE *inputFile = fopen(argv[3], "r"); // open the input file with read permission
        FILE *outputFile = fopen(argv[5], "w+"); // open the output file with write permission

        if (inputFile == NULL) { // check is input file opened correctly
            perror("Failed: ");
            return 1;
        }
        else if (outputFile == NULL) { // check is output file opened correctly
            printf("Failed to open output file.\n");
            return 1;
        }
        else{ // files opened correctly.
            char readLine[READ_BUFFER]; // buffer for reading line.
            contentNodes *rootNode = malloc(sizeof(contentNodes)); // creating a root node for read data.
            contentNodes *iterNode; // iterator on read data
            iterNode = rootNode;

             // default definitions of attributes
            int currRowNumber = 1;
            int currColumnNumber = 1;
            int temp = 0; // temp data to converting read string to integer.
            while (fgets(readLine, READ_BUFFER, inputFile)) { // get new line from input file
                char *token = strtok(readLine, ","); // tokenize the line with commas.

                while (token != NULL) { // get new column
                    temp = atoi(token); // convert read data to int and save it on temp var.
                    token = strtok(NULL, ","); // get the new token.

                    // adding read token to my ContentList structure.
                    iterNode->next = malloc(sizeof(contentNodes));
                    iterNode->rowNumber = currRowNumber;
                    iterNode->columnNumber = currColumnNumber;
                    iterNode->content = temp;

                    iterNode = iterNode->next;
                    currColumnNumber++;
                }
                currRowNumber++;
                currColumnNumber = 1;
            }
            if (parameterStatus == 1){ // print option selected
                contentNodes *travelerNode = rootNode; // new iterator on ContentList root.
                int currRowNumber = travelerNode->rowNumber; // setting up current row number (on each row it changes.)
                while(travelerNode->next != NULL){ // while there is more nodes after current node, 
                    if(currRowNumber == travelerNode->rowNumber){ // if row has not changed, 
                        if(travelerNode->next->rowNumber != currRowNumber){ // if there is no more column on current row,
                            fprintf(outputFile, "%d", travelerNode->content); // write the content without the comma to the output file.
                        }
                        else{ // if there is more column on current row,
                        fprintf(outputFile, "%d,", travelerNode->content); // write the content with the comma to the output file.
                        }
                    }
                    else{ // if row has changed
                        currRowNumber = travelerNode->rowNumber; // change the current row
                        fprintf(outputFile, "\n%d,", travelerNode->content); // make a new line, after write the content
                    }
                    travelerNode = travelerNode->next; // go through on nodes.
                }
                printf("--print operation is done succesfully.\n"); // there is no crush while operating.
            }
            else if (parameterStatus == 2){ // nzeros option selected
                contentNodes *travelerNode = rootNode; // reset the traveler node
                int nzeros = 0; // default number of zeros.
                while (travelerNode->next != NULL){  // while there is more nodes after current node, 
                    if(travelerNode->content == 0){ // if the content is zero,
                        nzeros++; // add 1 to nzeros var.
                    }
                    travelerNode = travelerNode->next; // go through
                }
                fprintf(outputFile, "%d", nzeros); // write the number of zeros to output.
                printf("--nzeros operation is done succesfully.\n"); // there is no crush while operating.
            }
            else if (parameterStatus == 3){ // duplicates option selected
                contentNodes *travelerNode = rootNode; // reset the traveler node.
                duplicateNodes *rootDuplicateNode = malloc(sizeof(duplicateNodes)); // creating root node of DuplicateList structure
                duplicateNodes *duplicateTraveler = rootDuplicateNode; // creating iterator on DuplicateList structure.
                while(travelerNode->next != NULL){ // while there is more nodes after current node, 
                    int currCont = travelerNode->content; // determine which content is searching for
                    int isFound = 0; // flag for if current content is found
                    duplicateTraveler = rootDuplicateNode; // reset the DuplicateTravele
                    while(duplicateTraveler->next != NULL){  // while there is more nodes after current node, 
                        if(duplicateTraveler->content == currCont){ // if searching data is found,
                            isFound = 1; // raise the flag
                            duplicateTraveler->pairs++; // increase the number of found data's node.
                            break; // exit the while block.
                        }
                        duplicateTraveler = duplicateTraveler->next; // go through
                    }
                    if(isFound == 0){ // if flag is not raised,
                        duplicateTraveler->next = malloc(sizeof(duplicateNodes)); // create new node at the enf of the duplicateTraveler
                        duplicateTraveler->content = currCont; // which content equals to couldn't found content,
                        duplicateTraveler = duplicateTraveler->next; // and go through
                    }
                    travelerNode = travelerNode->next; // go through
                }
                
                // in the following 3 lines and while block, basicly created a new linkedlist from my second structure
                // and creating with nodes from first linkedlist of the structure which has "pairs" attribute is 1,
                // if pairs attribute equals to 1, that means relating content is appeared just 2 times. that means it is duplicated.
                duplicateTraveler = rootDuplicateNode; // reset the duplicate traveler list
                duplicateNodes *onlyDuplicates = malloc(sizeof(duplicateNodes)); // create new LinkedList from DuplicateList structure
                duplicateNodes *onlyDuplicatesTraveler = onlyDuplicates; // creating an iter on onlyDuplicates list.
                while(duplicateTraveler->next != NULL){  // while there is more nodes after current node, 
                    if(duplicateTraveler->pairs == 1){ // if "pairs" attribute equals to 1
                        onlyDuplicatesTraveler->next = malloc(sizeof(duplicateNodes)); // create new node on onlyDuplicatesTraveler (only duplicated numbers iter) at the end 
                        onlyDuplicatesTraveler->content = duplicateTraveler->content; // set the content
                        onlyDuplicatesTraveler->pairs = duplicateTraveler->pairs; // set the pairs to 1, which is different to default int value (0) (I will use that on my further code)
                        onlyDuplicatesTraveler = onlyDuplicatesTraveler->next; // go through
                    }
                    duplicateTraveler = duplicateTraveler->next; // go through
                }

                onlyDuplicatesTraveler = onlyDuplicates; // reset the onlyDuplicatesTraveler list.
                while(onlyDuplicatesTraveler->next != NULL){  // while there is more nodes after current node, 
                    if(onlyDuplicatesTraveler->next->pairs != 1){ // while next node is not set up, (that means next node is just a node with default values.)
                        fprintf(outputFile, "%d", onlyDuplicatesTraveler->content); // print the content to output file without comma
                    }
                    else{ // if the next node is set up, 
                        fprintf(outputFile, "%d,", onlyDuplicatesTraveler->content); // write the content to output file with comma.
                    }
                    onlyDuplicatesTraveler = onlyDuplicatesTraveler->next; // go through
                }
                printf("--duplicates operation is done succesfully.\n"); // there is no crush while operating.
            }
            else{ // invalid option selected
                // actually, code can not enter this block, because I have already detected invalid options on parameterChecker function
                // but I just don't want to disrupt if-else hierarchy 
            }
        }
    }
    else if (parameterStatus == 4){ // help option selected
        HelpText(); // get the help text. i write it as a function because it is too long.
        return 0; // exit the code
        }
    else{ // if parameterStatus is not 1, 2, 3 or 4, that means there is an mistake on running code.
        printf("Aborted.\n");
        return 1; // exit the code with return code 1.
    }
}

int ParameterChecker(char *arr[]){ // a function to check the parameters
    // actually, there is nothing to explain, just a bunch of if-else blocks.
    // basically, I am checking the parameters and returning a number to main function.
    // that number will be used to determine which option is selected.
    // return 0 means invalid operation.
    if(arr[1] == NULL){ 
        printf("Lack of parameters: no option\n");
        return 0;
    }
    else if(strcmp(arr[1], "--print") == 0 ||
       strcmp(arr[1], "--nzeros") == 0 ||
       strcmp(arr[1], "--duplicates") == 0){
        if(arr[2] == NULL){
            printf("Lack of parameters: no input parameter\n");
            return 0;
        }
        else if(strcmp(arr[2], "-i") == 0){
            if(arr[3] == NULL){
                printf("Lack of parameters: no input file\n");
                return 0;
            }
            else{
                if(arr[4] == NULL){
                    printf("Lack of parameters: no output parameter\n");
                    return 0;
                }
                else if(strcmp(arr[4], "-o") == 0){
                    if(arr[5] == NULL){
                        printf("Lack of parameters: no output file\n");
                        return 0;
                    }
                    else{
                        if(strcmp(arr[1], "--print") == 0){
                            return 1;
                        }
                        else if(strcmp(arr[1], "--nzeros") == 0){
                            return 2;
                        }
                        else if(strcmp(arr[1], "--duplicates") == 0){
                            return 3;
                        }
                        else{
                            return 0;
                        }
                    }
                }
                else{
                    printf("Invalid parameter: %s\n", arr[4]);
                    return 0;
                }
            }
        }
        else{
            printf("Invalid parameter: %s\n", arr[2]);
            return 0;
        }
    }
    else if(strcmp(arr[1], "--help") == 0){
        return 4;
    }
    else{
        printf("Invalid option: %s.\n", arr[1]);
        return 0;
    }
}

void HelpText(){
    printf("USAGE : ./main [OPTION] -i [INPUT FILE] -o [OUTPUT FILE]\n");
    printf("Valid options are:\n");
    printf("> --print\t:prints the content of the input file to the output file.\n");
    printf("> --nzeros\t:prints the number of zeros in the input file to the output file.\n");
    printf("> --duplicates\t:prints the duplicated numbers in the input file to the output file.\n");
    printf("> --help\t:prints this help text.\n");
    printf("\n");

    printf("[INPUT FILE]\t:the name of the input file.\n");
    printf("\n");

    printf("[OUTPUT FILE]\t:the name of the output file.\n");
}
