#include<iostream>
using namespace std;

void printArray(int arr[], int size){

  cout<<"Printing the array"<<endl;

  for(int i=0; i<size; i++){

    cout<<arr[i]<<" ";
  }
  cout<<"Printing DONE!"<<endl;

}


int main(){

  int numbers[15];

  cout<< " Value at index "<< numbers[8]<<endl;

  int second[3]= {3, 7, 11};

  cout<< " Value at 2nd index "<< second[2]<<endl;

  int third[15]={2, 7};

  int n=15;

  printArray(third, n);
  int sizethird = sizeof(third)/sizeof(int);
  cout<<"Size of third is:  "<< sizethird<<endl;

  
  int fifth[15]={1};

  n=10;

  printArray(fifth, n);


  char ch[5]= {'a', 'b', 'c', 'd', 'e'};
  cout<<ch[3]<<endl;

  cout<<"Printing the array"<<endl;

  for(int i=0; i<5; i++){

    cout<<ch[i]<<" ";
  }
  cout<<"Printing DONE!"<<endl;

  double firstDouble[5];
  float firstFloat[5];
  bool firstBool[9];



  cout<<"Everything is Fine"<<endl<<endl;

  int sizefifth = sizeof(fifth)/sizeof(int);
  cout<<"Size of Fifth is:  "<< sizefifth<<endl;
}
