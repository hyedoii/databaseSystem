//
//  main.c
//  database
//
//  Created by 박혜정 on 15/09/2019.
//  Copyright © 2019 박혜정. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define fNum 60000

typedef struct Data {
    char name[100];
    char phone[20];
}data;

data datagroup[fNum];
int total = 0;

void loadData ( char* filename ){
    char something[200];
    int cnt = 0;
    
    FILE * fp = fopen (filename, "r");
    
    if ( fp != NULL ){
        fscanf(fp,"%s", something);
        while (EOF!=fscanf(fp, "%s", something)){
            strcpy( datagroup[cnt].name, strtok(something, ","));
            strcpy( datagroup[cnt].phone, strtok(NULL, " "));

            ++cnt;
        }
        fclose(fp);
    }
    total = cnt-1;
}

void insert (char* inputName){
    char newnum[20] ;
    total++;
    
    strcpy(datagroup[total].name, inputName);
    printf("datagroup[%d].name : %s , inputName : %s\n", total, datagroup[total].name, inputName);
    printf("저장할 전화번호를 입력해주세요.\n");
    scanf("%s", newnum);
    while(1){
        if ((strlen(newnum) != 11) || (strncmp(newnum, "010", 3)!=0)){
            printf("010으로 시작하는 11자리 수를 입력해주세요.\n");
            scanf("%s", newnum);
        }
        else {
            strcpy(datagroup[total].phone, newnum);
            printf("datagroup[%d].phone : %s , inputName : %s\n", total, datagroup[total].phone, newnum);
            break;
        }
    }
    /*
    for( int i = 0 ; i <= total; i++){
        printf("%d\n%s,%s\n", i , datagroup[i].name , datagroup[i].phone);
    }*/
}

int findData(char* inputName) {
    int found[60000];
    int fcnt = 0;
    int select = 0;
    found[0] = -1;
    
    for ( int i = 0 ; i <= total ; i++ ) {
        //같으면
        if( strstr( datagroup[i].name, inputName) != NULL ) {
            found[fcnt] = i;
            fcnt++;
        }
    }
    if (fcnt == 1) {
        printf("연락처가 존재합니다.\n");
    }
    if( fcnt != 0 && fcnt != 1) {
        printf("연락처가 다수 존재합니다. 연락처를 선택해주세요.\n");
        for (int i = 0 ; i < fcnt ; i++) {
            printf("%d : %s,%s\n", i, datagroup[found[i]].name, datagroup[found[i]].phone);
        }
        scanf("%d", &select);
    }
    else {
        select = 0;
    }
    return found[select];
}

void editNum ( int index, char* newnum){
    char newname[100];
    char newInputname[100];
    int option = 0;
    while(index == -1) {
        printf("존재하지 않는 연락처입니다. 검색할 이름을 다시 입력해주세요.\n");
        scanf("%s", newname);
        index = findData(newname);
    }
    printf("선택된 연락처 : %s, %s\n", datagroup[index].name, datagroup[index].phone );
    printf("수정할 부분을 선택해주세요. 0 : 이름 , 1 : 전화번호\n");
    scanf("%d", &option);
    switch (option) {
        case 0:
            printf("<이름 변경>\n수정할 이름을 입력해주세요.\n");
            scanf("%s", newInputname);
            strcpy(datagroup[index].name , newInputname);
            printf("변경된 연락처 : %s, %s\n",datagroup[index].name, datagroup[index].phone);
            break;
        
        case 1:
            printf("<전화번호 변경>\n수정할 연락처를 입력해주세요.\n");
            scanf("%s", newnum);
            while(1){
                if ((strlen(newnum) != 11) || (strncmp(newnum, "010", 3)!=0)){
                    printf("010으로 시작하는 11자리 수를 입력해주세요.\n");
                    scanf("%s", newnum);
                }
                else {
                    strcpy(datagroup[index].phone, newnum);
                    printf("변경된 연락처 : %s,%s\n", datagroup[index].name, datagroup[index].phone);
                    break;
                }
            }
            break;
            
        default:
            break;
    }
}

void delete( char* inputName ) {
    int index = findData(inputName);
    for (int i = index ; i < total ; i++){
        datagroup[i] = datagroup[i+1];
    }
    total--;
}

void backUpData() {
    remove("2017029716_박혜정.csv");
    FILE * fw = fopen( "2017029716_박혜정.csv", "w" );
    
    fprintf(fw, "name,phone\n");
    for ( int i = 0 ; i <= total ; i++ ){
        fprintf(fw, "%s,%s\n", datagroup[i].name, datagroup[i].phone);
    }
    fclose(fw);
}

int main(int argc, const char * argv[]) {
    char inputName[100];
    char newnum[20];
    int index = -1;
    int option = -1;
    int yes = -1;
    
    yes = access("2017029716_박혜정.csv",0);
    
    if(yes == 0 ){
        loadData("2017029716_박혜정.csv");
    }
    else{
        loadData("contact.csv");
    }
    /*
    for ( int i = 0 ; i <= total ; ++i ){
        printf("***%d : %s,%s\n",i, datagroup[i].name, datagroup[i].phone);
    }*/
    while(1){
        printf("1.검색 2.수정 3.삭제 4.삽입 5.출력 6.종료\n");
        scanf("%d", &option);
    
        switch (option) {
            case 1:
                index = -1;
                printf("<검색>\n검색할 이름을 입력하세요.\n");
                scanf("%s", inputName);
                index = findData(inputName);
            
                if( index == -1 ){
                    printf("연락처가 존재하지 않습니다. 연락처를 추가합니다.\n");
                    insert(inputName);
                }
                /*
                else {
                 
                }*/
                backUpData();
                break;
        
            case 2:
                index = -1;
                printf("<수정>\n연락처를 수정합니다. 수정할 이름을 입력해주세요.\n");
                scanf("%s", inputName);
                index = findData(inputName);
                editNum(index, newnum);
                backUpData();
                break;
            
            case 3:
                index = -1;
                printf("<삭제>\n연락처를 삭제합니다. 삭제할 이름을 입력해주세요.\n");
                scanf("%s", inputName);
                delete(inputName);
                backUpData();
                break;
        
            case 4:
                printf("<삽입>\n연락처를 삽입합니다. 삽입할 연락처를 입력해주세요.\n이름 : ");
                scanf("%s", inputName);
                insert(inputName);
                backUpData();
                break;
        
            case 5:
                printf("연락처를 출력합니다.\n");
                for ( int i = 0 ; i <= total ; i++ ){
                    printf("%s,%s\n", datagroup[i].name, datagroup[i].phone);
                }
                printf("total : %d\n", total);
                break;
        
            case 6:
                return 0;
            
            default:
                break;
        }
    }
    
    return 0;
}
