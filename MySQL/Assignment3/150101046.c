#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>

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
void populate_table_ett()
{
    FILE* input = fopen("./database-19-jan-2018/database-19-jan-2018/exam-time-table.csv","r");
    FILE* output = fopen("150101046_ett.sql","w");
    char line[500];
    while (fgets(line, 1024, input))
    {   
        char* temp = strdup(line);
        char* course_id = (char* )getentry(temp,1);
        temp = strdup(line);
        char* date = (char* )getentry(temp,2);
        temp = strdup(line);
        char* stime = (char* )getentry(temp,3);
        temp = strdup(line);
        char* etime = (char* )getentry(temp,4);
        fprintf(output, "INSERT INTO ett (course_id, exam_date, start_time, end_time) VALUES ('%s', '%s', '%s', '%s');\n", course_id, date, stime, etime);
        fprintf(output, "INSERT INTO ett_temp (course_id, exam_date, start_time, end_time) VALUES ('%s', '%s', '%s', '%s');\n", course_id, date, stime, etime);
        fprintf(output, "INSERT INTO ett_clone (course_id, exam_date, start_time, end_time) VALUES ('%s', '%s', '%s', '%s');\n", course_id, date, stime, etime);
    }
    return;
}

void populate_table_cc()
{
    FILE* input = fopen("./database-19-jan-2018/database-19-jan-2018/course-credits.csv","r");
    FILE* output = fopen("150101046_cc.sql","w");
    char line[500];
    while (fgets(line, 1024, input))
    {   
        char* temp = strdup(line);
        char* course_id = (char* )getentry(temp,1);
        temp = strdup(line);
        int credits = atoi((char* )getentry(temp,2));
        fprintf(output, "INSERT INTO cc (course_id, number_of_credits) VALUES ('%s', %d);\n", course_id, credits);
        fprintf(output, "INSERT INTO cc_temp (course_id, number_of_credits) VALUES ('%s', %d);\n", course_id, credits);
        fprintf(output, "INSERT INTO cc_clone (course_id, number_of_credits) VALUES ('%s', %d);\n", course_id, credits);
    }
    return;
}

void populate_table_cwsl()
{
    /* Get all files of each directory */
    char* dept_code[] = {"bt", "ce" , "ch", "cl", "cse", "dd", "eee", "hs", "ma", "me", "ph"};
    int k = 0;
    char** file_list;
    FILE* output = fopen("150101046_cwsl.sql","w");
    for(k = 0; k < 11; k++)
    {
        file_list = list_files(dept_code[k]); 
        int i = 0;
        while(strcmp(file_list[i],"NULL") != 0)
        {   
            char base_addr[500];
            strcpy(base_addr,"./database-19-jan-2018/database-19-jan-2018/course-wise-students-list/");
            strcat(base_addr, dept_code[k]);
            strcat(base_addr,"/");
            strcat(base_addr,file_list[i]);
            strcat(base_addr,".csv");
            // printf("%s\n",file_list[i]);
            FILE* input = fopen(base_addr,"r");            
            char line[500];
            while (fgets(line, 1024, input))
            {
                char* temp = strdup(line);
                int ser = atoi((char*)getentry(temp,1));
                temp = strdup(line);
                char* roll = (char*)getentry(temp,2);
                temp = strdup(line);
                char* name = "null";
                // if((char*)getentry(temp,3)) 
                name = (char*)getentry(temp,3);
                temp = strdup(line);
                char* email = "null";
                // if((char*)getentry(temp,4) != null) 
                email = (char*)getentry(temp,4);
                fprintf(output, "INSERT INTO cwsl (cid, serial_number, roll_number, name, email) VALUES ('%s', %d, '%s', '%s', '%s');\n", file_list[i], ser, roll, name, email);
                fprintf(output, "INSERT INTO cwsl_temp (cid, serial_number, roll_number, name, email) VALUES ('%s', %d, '%s', '%s', '%s');\n", file_list[i], ser, roll, name, email);
                fprintf(output, "INSERT INTO cwsl_clone (cid, serial_number, roll_number, name, email) VALUES ('%s', %d, '%s', '%s', '%s');\n", file_list[i], ser, roll, name, email);
            }
            i++;
        }
    }


    

}

int main()
{	
	populate_table_ett();
    populate_table_cc();
    populate_table_cwsl();
    
}