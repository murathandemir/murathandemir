#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// MACRO DEFINITIONS
#define MAX_NAME_LENGTH 20 // maximum length of a city name

// STRUCT DEFINITIONS
struct Destination{    // struct for the destinations of a base city
    char name[MAX_NAME_LENGTH]; 
    int distance;
    struct Destination *next;
}; typedef struct Destination dests;

struct BaseCity{ // struct for the base cities
    char name[MAX_NAME_LENGTH];
    int checked;
    dests *neighbours;
    struct BaseCity *next;
}; typedef struct BaseCity baseCities;

// FUNCTION PROTOTYPES
int *GetInfo(FILE *file); // gets the number of nodes and edges from the input file
int DFT(baseCities *baseHead, char *startCity, char *endCity, dests *tempDest); // depth first traversal
int GetNeighbourNumber(dests *someBaseNeighbours); // gets the number of neighbours of a base city
void SortNeighboursDistance(baseCities *someBase); // sorts the neighbours of a base city according to their distances
void ResetChecks(baseCities *someBase); // resets the checked values of the base cities


/* imported datas seems like that : 

Base Cities:      HEAD -> base1 -> base2 -> base3 -> base4 -> ...
                            |        |        |        |
                            v        v        v        v
neighbours                dest1    dest1    dest1    dest1 -> ...
                            |        |        |        |
                            v        v        v        v
neighbours->next          dest2    dest2    dest2    dest2 -> ...
                            |        |        |        |
                            v        v        v        v 
neighbours->next->next    dest3    dest3    dest3    dest3 -> ...
                            |        |        |        |
                            v        v        v        v
                           ...      ...      ...      ...

*/

void main(int argc, char *argv[]){
    argc == 5 ? : exit(0); // if the number of arguments is not 5 then exit
    char *inputFileName, *outputFileName; // input and output file names
    if(strcmp(argv[1], "-i") == 0){ // if the first argument is -i then the second argument is the input file name
        inputFileName = argv[2]; // input file name
    }
    else{ // if the first argument is not -i then exit
        exit(0); 
    }

    if(strcmp(argv[3], "-o") == 0){ // if the third argument is -o then the fourth argument is the output file name
        outputFileName = argv[4]; // output file name
    }
    else{
        exit(0);
    }

    FILE *inputFile = fopen(inputFileName, "r"); // open the input file
    FILE *outputFile = fopen(outputFileName, "w"); // open the output file

    int *infos = GetInfo(inputFile); // get the number of nodes and edges from the input file
    int nodeNumber = infos[0];
    int edgeNumber = infos[1]; 

    baseCities *headOfBases = malloc(sizeof(baseCities)); // head of the base cities
    dests *headOfDests = malloc(sizeof(dests)); // head of the destinations of a base city

    headOfBases->next = NULL; // initialize the head of the base cities
    
    for(int i=0; i<edgeNumber; i++){ // get the edges from the input file
        char baseCityName[MAX_NAME_LENGTH];
        char destCityName[MAX_NAME_LENGTH];
        dests *tempNeighbours = malloc(sizeof(dests)); // temporary struct for the destinations of a base city
        
        int distance, baseFound = 0;
        fscanf(inputFile, "%s %s %d", baseCityName, destCityName, &distance);
        baseCities *iterBase = headOfBases; // iterator for the base cities
        while(iterBase->next != NULL){ // check if the base city is already in the list
            if(strcmp(iterBase->next->name, baseCityName) == 0){
                baseFound = 1;
            }
            iterBase = iterBase->next;
        }
        if(!baseFound){ // if the base city is not in the list then add it to the list
            iterBase->next = malloc(sizeof(baseCities)); // add the base city to the list
            iterBase = iterBase->next; // move the iterator to the new base city
            strcpy(iterBase->name, baseCityName); // copy the name of the base city

            strcpy(tempNeighbours->name, destCityName); 
            tempNeighbours->distance = distance;
            tempNeighbours->next = NULL;
            iterBase->neighbours = tempNeighbours;

            iterBase->next = NULL;
        }
        else{ // if the base city is already in the list then add the destination to the list of the base city
            tempNeighbours = iterBase->neighbours;
            while(tempNeighbours->next != NULL){ // move the iterator to the last destination of the base city
                tempNeighbours = tempNeighbours->next;
            }
            tempNeighbours->next = malloc(sizeof(dests)); // add the destination to the list
            tempNeighbours = tempNeighbours->next;
            strcpy(tempNeighbours->name, destCityName);
            tempNeighbours->distance = distance;
            tempNeighbours->next = NULL;
        }
    }

    baseCities *iterBase = headOfBases; // iterator for the base cities
    while(iterBase->next != NULL){ // sort the neighbours of the base cities according to their distances
        SortNeighboursDistance(iterBase->next); 
        iterBase = iterBase->next;
    }

    dests *headResult = malloc(sizeof(dests)); // head of the result list
    dests *iterResult = headResult; // iterator for the result list

    while(!feof(inputFile)){ // get the paths from the input file
        int found = 0;
        ResetChecks(headOfBases); // reset the checked values of the base cities
        free(iterResult); // free the result list
        dests *iterResult = headResult; // iterator for the result list
        char city1[MAX_NAME_LENGTH], city2[MAX_NAME_LENGTH]; 
        fscanf(inputFile, "%s %s", city1, city2);
        iterBase = headOfBases;
        iterResult = headResult;
        DFT(iterBase, city1, city2, iterResult); // find the path between city1 and city2
        while(iterResult != NULL){ // check if the path is found
            if(strcmp(iterResult->name, city2) == 0){ // if the path is found then exit the loop
                found = 1;
            }
            iterResult = iterResult->next;
        }
        iterResult = headResult;
        if(!found){ // if the path is not found then print the error message
            fprintf(outputFile, "Path (%s %s): Path not found\n", city1, city2);
            fprintf(outputFile, "Distance: Path not found\n");
        }
        else{ // if the path is found then print the path and the distance
            int totalDist = 0;
            fprintf(outputFile, "Path (%s %s): %s ->", city1, city2, city1);
            while(iterResult != NULL && (strcmp(iterResult->name, city2) != 0)){ // print the path
                totalDist += iterResult->next->distance;
                fprintf(outputFile, " %s ->", iterResult->name);
                iterResult = iterResult->next;
            }

            fprintf(outputFile, " %s\nDistance: ", iterResult->name); // print the distance

            /*
            *  Actually, there is an algorithm peak which i have fixed it already. The distance between
            *  the first two cities are not added to the total distance. I have fixed in on this section.
            */  
            iterBase = headOfBases;
            int bias = 0;
            while(iterBase != NULL){
                if(strcmp(iterBase->name, city1) == 0){
                    dests *someNeighbour = iterBase->neighbours;
                    while(someNeighbour != NULL){
                        if(strcmp(someNeighbour->name, headResult->name) == 0){
                            bias = someNeighbour->distance;
                            break;
                        }
                        someNeighbour = someNeighbour->next;
                    }
                }
                iterBase = iterBase->next;
            }
            // distance bias section ends here

            fprintf(outputFile, "%d km\n", totalDist+bias);

        }
    }
    
}

int *GetInfo(FILE *file){ // get the number of the base cities and the number of the edges
    int *info = malloc(sizeof(int)*2); // info[0] = number of base cities, info[1] = number of edges
    fscanf(file, "%d %d", &info[0], &info[1]); 
    return info;
} // this function does not rewind. go ahead.

int DFT(baseCities *iterBaseHead, char *startCity, char *endCity, dests *result){ // Depth First Traversal
    baseCities *iterBase = iterBaseHead->next; // iterator for the base cities
    while(strcmp(iterBase->name, startCity) != 0){ // find the start city
        iterBase = iterBase->next;
    }
    //iterBase->checked = 1;
    int tempNeigh = GetNeighbourNumber(iterBase->neighbours); // get the number of the neighbours of the start city
    dests *iterDest = malloc(sizeof(dests)); // iterator for the neighbours of the start city
    iterDest = iterBase->neighbours; // move the iterator to the first neighbour of the start city
    /*while(iterBase->neighbours->next != NULL){
        iterDest->next = iterBase->neighbours->next;
        iterBase->neighbours = iterBase->neighbours->next;
    }*/

    if(strcmp(iterDest->name, endCity) == 0){ // if the end city is found then return 1
        strcpy(result->name, iterDest->name); // add the end city to the result list
        result->distance = iterDest->distance; // add the distance to the result list
        result->next = NULL; // set the next of the result list to NULL
        return 1;
    }
    else{ // if the end city is not found then check the neighbours of the start city
        while(iterDest != NULL){ // check the neighbours of the start city
            iterBase = iterBaseHead;
            while(strcmp(iterBase->name, iterDest->name) != 0){ // find the neighbour in the base cities
                iterBase = iterBase->next;
            }
            if(iterBase->checked == 0){ // if the neighbour is not checked then check it
                iterBase->checked = 1; // set the checked value to 1
                strcpy(result->name, iterDest->name); // add the neighbour to the result list
                result->distance = iterDest->distance;
                result->next = malloc(sizeof(dests)); // create the next node of the result list
                result = result->next;
                if(DFT(iterBaseHead, iterDest->name, endCity, result) == 1){ // check the neighbour recursively
                    return 1;
                }
            }
            iterDest = iterDest->next; // move the iterator to the next neighbour
        }
    }
}

int GetNeighbourNumber(dests *someBaseNeighbours){ // get the number of the neighbours of a base city
    dests *someBase = someBaseNeighbours; // iterator for the neighbours of a base city
    int counter = 0;
    while(someBase != NULL){ // count the neighbours
        someBase = someBase->next;
        counter++;
    }
    return counter; // return the number of the neighbours
}

void SortNeighboursDistance(baseCities *someBase){ // sort the neighbours of a base city by their distances
    int numberOfNeighbours = GetNeighbourNumber(someBase->neighbours); // get the number of the neighbours
    dests *iterNeighbour = someBase->neighbours; // iterator for the neighbours
    for(int i=0; i<numberOfNeighbours; i++){ // sort the neighbours by their distances
        for(int j=0; j<numberOfNeighbours-1; j++){ // sort the neighbours by their distances
            while(iterNeighbour->next != NULL){ // sort the neighbours by their distances
                if(iterNeighbour->distance > iterNeighbour->next->distance){ // if the distance of the neighbour is greater than the distance of the next neighbour then swap them
                    dests *temp = malloc(sizeof(dests)); // create a temporary node
                    strcpy(temp->name, iterNeighbour->name); // swap the name, distance and the next of the neighbours
                    temp->distance = iterNeighbour->distance; // swap the name, distance and the next of the neighbours
                    temp->next = iterNeighbour->next->next; // swap the name, distance and the next of the neighbours

                    strcpy(iterNeighbour->name, iterNeighbour->next->name); // swap the name, distance and the next of the neighbours
                    iterNeighbour->distance = iterNeighbour->next->distance; // swap the name, distance and the next of the neighbours
                    iterNeighbour->next = temp; // swap the name, distance and the next of the neighbours
                }
                iterNeighbour = iterNeighbour->next; // move the iterator to the next neighbour
            }
        }
    }
}

void ResetChecks(baseCities *someBase){ // reset the checked values of the base cities
    while(someBase->next != NULL){ // reset the checked values of the base cities
        someBase = someBase->next; // reset the checked values of the base cities
        someBase->checked = 0; // reset the checked values of the base cities
    }
}