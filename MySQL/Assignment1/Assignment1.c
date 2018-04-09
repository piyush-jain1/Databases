/*
Name - PIYUSH JAIN
Roll No. - 150101046
Course - CS345 : Database Laboratory
Lab Session 1
Date - 12 Jan, 2018
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>


/* structure for input record */
struct record
{
	int rollno;
	char* held_on;
	char* status;
};

/* structure for student-wise record of attendance */
struct student
{
	int rollno;
	int no_classes_present;
	double percentage;
};

/* utility function to read CSV file */
const char* getentry(char* line, int index)
{
    const char* token;
    for (token = strtok(line, ",");
            token && *token;
            token = strtok(NULL, ",\n"))
    {
        if (!--index)
            return token;
    }
    return NULL;
}


int main()
{
	/* input file */
    FILE* stream = fopen("database_12jan2017.csv", "r");

    struct record * data = malloc(1400 * sizeof(struct record));
    char line[500];
    int i = 0, k = 0;
    int roll = 780102999;

    struct student * attendance = malloc(1400 * sizeof(struct student));
    int total_classes[1400] = {0};
    attendance[i].rollno = roll;
    attendance[i].no_classes_present = 0;

    /* read CSV line-by-line, then parse each line */
    while (fgets(line, 1024, stream))
    {	
        char* temp = strdup(line);
        char* cur_roll = (char*)getentry(temp,1); 
        temp = strdup(line);
        data[k].held_on = (char*)getentry(temp,2);
        temp = strdup(line);
        char* stat = (char*)getentry(temp,3); 
        int new_roll = atoi(cur_roll);
        data[k].rollno = new_roll;
        data[k].status = stat;
        // printf("%d, %s, %s\n", data[k].rollno, data[k].held_on, data[k].status);

        /* find number of classes present for each student */
        if(new_roll == roll)
        {	
        	if(strcmp(stat, " Present") == 0)
        	{	
        		attendance[i].no_classes_present += 1;
        	}
        	total_classes[i]++;
        }
        else
        {	
        	roll--;
        	i++;
        	attendance[i].rollno = roll;
	    	attendance[i].no_classes_present = 0;
	    	if(strcmp(stat, " Present") == 0)
        	{	
        		attendance[i].no_classes_present += 1;
        	}
        	total_classes[i]++;
        }

        free(temp);
    }

    /* Writing result to CSV files */
    FILE * outputl = fopen("L75.csv", "w");
    FILE * outputg = fopen("G75.csv", "w");

    int j = 0;
    for(j = 0; j <= i; j++)
    {	
    	/* calculate percentage attendance */
    	double per = (double)attendance[j].no_classes_present/(double)total_classes[j];
    	per *= 100.0;
    	// printf("%f\n",per );

    	/* if percentage attendance greater than or equal to 75.0%, write to G75.csv, else write to L75.csv */
     	if(per >= 75.0)
    	{
    		fprintf(outputg, "%d, %d, %f\n", attendance[j].rollno, attendance[j].no_classes_present, per);
    	}
    	else
    	{
    		fprintf(outputl, "%d, %d, %f\n", attendance[j].rollno, attendance[j].no_classes_present, per);
    	}
    }

    return 0;   
}