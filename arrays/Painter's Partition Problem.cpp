bool isTrue(vector<int> &boards,int n,  int k, int mid){
    int noOfPainter =1;
    int boardSize =0;

    for(int i=0;i<n;i++){
        if(boards[i]>mid) return false;
        if(boardSize+boards[i]<=mid){
            boardSize+=boards[i];
        }
        else{
            noOfPainter++;
            if(noOfPainter>k) return false;
            boardSize = boards[i];
        }
        
    }
    return true;
}

int findLargestMinDistance(vector<int> &boards, int k)
{
    int s =0;
    int sum =0;
    int n=boards.size();


    for(int i=0;i<n; i++){
        sum += boards[i];
    }
    int e=sum;
    int ans=-1;
    while(s<=e){
        int mid = s+(e-s)/2;
        if(isTrue(boards,n,k,mid)){
            ans= mid;
            e=mid-1;
        }
        else{
            s=mid+1;
        }
    }
    return ans;
}
