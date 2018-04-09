/*
Name - PIYUSH JAIN
Roll No. - 150101046
Course - CS345 : Database Laboratory
Lab Session 2
Date - 19 Jan, 2018
*/

/*
ASSUMPTION : 
1. Directory structure is : 
    -150101046.c (Note the location of C-file)
    -database-19-jan-2018/
        -database-19-jan-2018
            -course-credits.csv
            -exam-time-table.csv
            -course-wise-students-list
                -*dept*
                    -*course_code*.csv

2. Assuming each course has at max two distinct exam timings (mid-sem and end-sem) , although the exam-time-table.csv 
contains more than two entries fro some courses, but they are repeated.

3. Printing output (both parts) in the console as well as files.
    output1.csv : List of students who have exam time-table clash
    output2.csv : List of students whose total number of credits registered is greater than 40 
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>

/* structure to store data of each student */
struct student
{   
    char* name;             
    char* roll_number;
    char* course[50];
    char* start_time1[50];
    char* end_time1[50];
    char* start_time2[50];
    char* end_time2[50];
    char* date1[50];
    char* date2[50];
    int credit;
    int no_of_courses;
};
struct student data[5000];
int s_index = 0;        /* total number of students    */

/* structure to store details about each course */
struct course
{
    char* name;
    char* date1;
    char* date2;
    int credit;
    char* start_time1;
    char* end_time1;
    char* start_time2;
    char* end_time2;
};
struct course  cdata[5000];
int total = 0;      /* total number of courses    */


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

/* Directory read : function to get list of files in each directories */ 
char** list_files(char* dept)
{   
    char** all_files;
    all_files =  (char**) malloc (100*sizeof(char *));  //allocating array of 50 string 
    DIR *dir;
    struct dirent *ent;
    char dir_name[500];
    strcpy(dir_name,"./database-19-jan-2018/database-19-jan-2018/course-wise-students-list/");
    strcat(dir_name,dept);
    strcat(dir_name,"/");
    int i = 0;
    if ((dir = opendir (dir_name)) != NULL) 
    {
        /* print all the files and directories within directory */
        while ((ent = readdir (dir)) != NULL) 
        {
            if (strcmp(ent->d_name, ".") == 0 || strcmp(ent->d_name, "..") == 0)
                continue;
            all_files[i] = (char*) malloc (100*sizeof(char));
            char* temp = (char* )ent->d_name;
            char *ptr;
            ptr = strchr(temp, '.');
            if (ptr != NULL)    *ptr = '\0';
            strcpy(all_files[i],temp);
            i++;
        }
        all_files[i] = (char*) malloc (100*sizeof(char));
        char* temp = "NULL";
        strcpy(all_files[i],temp);
        closedir (dir);
        return all_files;
    } 
}

/* function to interpret all information about each student */
void process(char* dept_code, char** file_list)
{   
    int i = 0;

    while(strcmp(file_list[i],"NULL") != 0)
    {   
        char base_addr[500];
        strcpy(base_addr,"./database-19-jan-2018/database-19-jan-2018/course-wise-students-list/");
        strcat(base_addr, dept_code);
        strcat(base_addr,"/");
        strcat(base_addr,file_list[i]);
        strcat(base_addr,".csv");
        FILE* stream = fopen(base_addr,"r");
        char line[500];
        while (fgets(line, 1024, stream))
        {
            char* temp = strdup(line);
            char* r = (char*)getentry(temp,2);
            temp = strdup(line);
            char* name = (char*)getentry(temp,3);
            int j = 0;
            int flag = 0;
            for(j = 0; j < s_index; j++)
            {   
                /* if this roll number already available, just add new course */
                if(strcmp(data[j].roll_number,r) == 0)
                {   
                    data[j].course[data[j].no_of_courses] = file_list[i]; 
                    int p;
                    for(p = 0; p < total; p++)
                    {
                        if(strcmp(cdata[p].name,file_list[i]) == 0)
                        {
                            data[j].date1[data[j].no_of_courses] = cdata[p].date1;
                            data[j].date2[data[j].no_of_courses] = cdata[p].date2;
                            data[j].start_time1[data[j].no_of_courses] = cdata[p].start_time1;
                            data[j].end_time1[data[j].no_of_courses] = cdata[p].end_time1;
                            data[j].start_time2[data[j].no_of_courses] = cdata[p].start_time2;
                            data[j].end_time2[data[j].no_of_courses] = cdata[p].end_time2;
                            data[j].credit += cdata[p].credit;
                            data[j].no_of_courses += 1;
                            flag = 1;
                            break;
                        }
                    }
                    break;
                }
            }

            /* if new roll number found, add new student and corresponding course */
            if(flag == 0)
            {   
                data[s_index].name = name;
                data[s_index].roll_number = r;
                data[s_index].course[data[j].no_of_courses] = file_list[i];
                data[s_index].credit = 0;
                data[s_index].no_of_courses = 0;
                int p;
                for(p = 0; p < total; p++)
                {   
                    if(strcmp(cdata[p].name,file_list[i]) == 0)
                    {   
                        data[s_index].date1[data[j].no_of_courses] = cdata[p].date1;
                        data[s_index].date2[data[j].no_of_courses] = cdata[p].date2;
                        data[s_index].start_time1[data[j].no_of_courses] = cdata[p].start_time1;
                        data[s_index].end_time1[data[j].no_of_courses] = cdata[p].end_time1;
                        data[s_index].start_time2[data[j].no_of_courses] = cdata[p].start_time2;
                        data[s_index].end_time2[data[j].no_of_courses] = cdata[p].end_time2;
                        data[s_index].credit += cdata[p].credit;
                        data[s_index].no_of_courses += 1;
                        break;
                    }
                }
                s_index++; 
            }

        }
        i++;
    }
}
int main()
{
    /* input files */
    FILE* course_credit = fopen("./database-19-jan-2018/database-19-jan-2018/course-credits.csv", "r");
    FILE* exam_time_table = fopen("./database-19-jan-2018/database-19-jan-2018/exam-time-table.csv", "r");
    int k = 0;
    char line[500];

    /* store all information about each course */
    while (fgets(line, 1024, course_credit))
    {
        char* temp = strdup(line);
        char* tm = (char* )getentry(temp,1);
        char *ptr;
        ptr = strchr(tm, '.');
        if (ptr != NULL) {
            *ptr = '\0';
        }
        cdata[k].name = tm;
        temp = strdup(line);
        cdata[k].credit = atoi((char* )getentry(temp,2));
        cdata[k].date1 = "NULL";
        cdata[k].date2 = "NULL";
        cdata[k].start_time1 = "NULL";
        cdata[k].end_time1 = "NULL";
        cdata[k].start_time2 = "NULL";
        cdata[k].end_time2 = "NULL";
        k++;
    }
    total = k;
    while (fgets(line, 1024, exam_time_table))
    {
        char* temp = strdup(line);
        char* course_name = (char* )getentry(temp,1);
        temp = strdup(line);
        char* date = (char* )getentry(temp,2);
        temp = strdup(line);
        char* stime = (char* )getentry(temp,3);
        temp = strdup(line);
        char* etime = (char* )getentry(temp,4);
        int j = 0;
        for(j = 0; j < total; j++)
        {
            if(strcmp(cdata[j].name,course_name) == 0)
            {
                if(strcmp(cdata[j].date1,"NULL") == 0)
                {
                    cdata[j].date1 = date;
                    cdata[j].start_time1 = stime;
                    cdata[j].end_time1 = etime;
                } 
                else
                {   
                    /* ignore repeated dates */ 
                    if(strcmp(date,cdata[j].date1) != 0)
                    {
                        cdata[j].date2 = date;
                        cdata[j].start_time2 = stime;
                        cdata[j].end_time2 = etime;
                    }    
                }
                break;
            }
        }
    }

    /* Get all files of each directory */
    char** bt_files = list_files("bt"); 
    char** ce_files = list_files("ce");
    char** ch_files = list_files("ch");
    char** cl_files = list_files("cl");
    char** cse_files = list_files("cse");
    char** dd_files = list_files("dd");
    char** eee_files = list_files("eee");
    char** hs_files = list_files("hs");
    char** ma_files = list_files("ma");
    char** me_files = list_files("me");
    char** ph_files = list_files("ph");


    /* Get all information about each student */
    process("bt", bt_files);
    process("ce", ce_files);
    process("ch", ch_files);
    process("cl", cl_files);
    process("cse", cse_files);
    process("dd", dd_files);
    process("eee", eee_files);
    process("hs", hs_files);
    process("ma", ma_files);
    process("me", me_files);
    process("ph", ph_files);

    /* Printing results */
    FILE* output1 = fopen("output1.csv","w");
    FILE* output2 = fopen("output2.csv","w");

    int j;
    printf("\nList of students who have exam time-table clash : \n\n");
    for(j = 0; j < s_index; j++)
    {   
        int p = 0, q = 0;
        for(p = 0; p < data[j].no_of_courses; p++)
        {   
            for(q = p+1; q < data[j].no_of_courses; q++)
            {   

                if((data[j].date1[p] != "NULL" && data[j].date1[q] != "NULL" && strcmp(data[j].date1[p],data[j].date1[q]) == 0 && strcmp(data[j].start_time1[p],data[j].start_time1[q]) == 0)
                    || (data[j].date1[p] != "NULL" && data[j].date2[q] != "NULL" && strcmp(data[j].date1[p],data[j].date2[q]) == 0 && strcmp(data[j].start_time1[p],data[j].start_time2[q]) == 0)
                    || (data[j].date2[p] != "NULL" && data[j].date1[q] != "NULL" && strcmp(data[j].date2[p],data[j].date1[q]) == 0 && strcmp(data[j].start_time2[p],data[j].start_time1[q]) == 0)
                    || (data[j].date2[p] != "NULL" && data[j].date2[q] != "NULL" && strcmp(data[j].date2[p],data[j].date2[q]) == 0 && strcmp(data[j].start_time2[p],data[j].start_time2[q]) == 0))
                {
                    fprintf(output1, "%s, %s, %s, %s\n", data[j].roll_number, data[j].name, data[j].course[p], data[j].course[q]);
                    printf("%s, %s, %s, %s\n", data[j].roll_number, data[j].name, data[j].course[p], data[j].course[q]);
                }
            }
        }   
    }

    printf("\n\n-------------------------------------------------------------------------\n\n");
    printf("List of students whose total number of credits registered is greater than 40 : \n\n");
    for(j = 0; j < s_index; j++)
    {
       if(data[j].credit > 40)
        {
            fprintf(output2, "%s, %s, %d\n", data[j].roll_number, data[j].name, data[j].credit);
            printf("%s, %s, %d\n", data[j].roll_number, data[j].name, data[j].credit);
        }
    }
    
    // printf("Total no. of students : %d\n",s_index );
    // printf("Total no. of courses : %d\n", total);

    return 0;
}