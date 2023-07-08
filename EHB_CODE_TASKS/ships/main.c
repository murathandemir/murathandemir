#include <stdio.h>

#define NUMBER_OF_SHIPS 3

enum Types{passenger, cargo};

/* There is a structure which contains ship id, ship type and 
* number of passengers in ship or ship weight with depends on ship type.
* used union for those 2 variables because it saves 4bytes of memory
* for each ship member. If we think there are 1000 ships, it makes
* 4000byte and that is nearly 4MB. in embedded systems, this memory
* saving is an lifesaver.
*/
struct shipAttributes{
    int shipId;
    int shipTypes;
    union{
        struct{
            int numberOfPassengers;
        }passengerShip;
        struct{
            int weight;
        }cargoShip;
    }shipType;
}ship[NUMBER_OF_SHIPS];

void showShip(struct shipAttributes *infos);

int main(){
    struct shipAttributes *shipPtr;
    shipPtr = &ship;
    for(int i=0; i<NUMBER_OF_SHIPS; i++){
        printf("Enter the %d. ship's attributes :\n", i+1);
        printf("Ship ID > "); scanf("%d", &shipPtr[i].shipId);
        int chosenType;
        printf("Ship Type (0:passenger/1:cargo) > "); scanf("%d", &chosenType);
        if(chosenType == cargo){
            ship[i].shipTypes = cargo;
            printf("Weight > "); scanf("%d", &shipPtr->shipType.cargoShip.weight);
        }
        else if(chosenType == passenger){
            ship[i].shipTypes = passenger;
            printf("Number of passengers > "); scanf("%d", &shipPtr[i].shipType.passengerShip.numberOfPassengers);
        }
        else{
            printf("\nUnknown Type of Ship. Try Again.\n");
            i--;
        }
        printf("\n");
    }

    showShip(shipPtr);
    fileProcesses(shipPtr);
    puts("Press any key to stop program...");
    char a;
    getc(a);
}

void showShip(struct shipAttributes *infos){
    for(int i=0; i<NUMBER_OF_SHIPS; i++){
        printf("\n##### %d. SHIP\'S ATTRIBUTES #####\n\n",i+1);
        printf("Ship ID :\t\t%d\n", infos[i].shipId);
        if(infos[i].shipTypes == passenger){
            printf("Ship Type :\t\tPassenger Ship\n");
            printf("Passengers :\t\t%d\n", infos[i].shipType.passengerShip.numberOfPassengers);
        }
        else if(infos[i].shipTypes == cargo){
            printf("Ship Type :\t\tCargo Ship\n");
            printf("Ship weight :\t\t%d\n", infos[i].shipType.cargoShip.weight);
        }
        else{
            printf("Ship Type :\t\tUnknown!");
        }
        printf("After");
    }
}

void fileProcesses(struct shipAttributes *infos){
    FILE *passengerShip, *cargoShip, *unknownType;
    passengerShip = fopen("passenger_ship.txt", "a");
    cargoShip = fopen("cargo_ship.txt", "a");
    unknownType = fopen("unknown_type.txt", "a");

    for(int i=0; i<NUMBER_OF_SHIPS; i++){
        if(infos[i].shipTypes == passenger){
            fprintf(passengerShip, "%d\n", infos[i].shipId);
        }
        else if(infos[i].shipTypes == cargo){
            fprintf(cargoShip, "%d\n", infos[i].shipId);
        }
        else{
            // Firstly i decided to creating a file for ships which are not have a known type
            // if user wrote anything except 0/1, program keeps that but at the end of processes
            // program was giving an extra output file for unknown types.
            // After that i decided to remove this feature and i gave a limit for choosing.
            // this fprintf is here again, i dont want to delete this ^^
            fprintf(unknownType, "%d\n", infos[i].shipId);
        }
    }

    fclose(unknownType);
    fclose(cargoShip);
    fclose(passengerShip);
}