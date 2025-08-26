void sortZeroesAndOne(int input[], int size)
{
    int left =0;
    int right = size-1;

    while(left<right){

        while(input[left]==0 && left< right){
            left++;
        }
        while(input[right]==1 && left<right){
            right--;
        }
        if(left<right){
            swap(input[left], input[right]);
            left++;
            right--;
        }
    }
}
