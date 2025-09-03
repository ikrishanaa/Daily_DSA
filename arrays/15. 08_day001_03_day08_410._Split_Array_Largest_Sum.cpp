class Solution {
public:
    bool isPossible(vector<int>& nums, int n, int k, int mid){
        int part =1;
        int countSum =0;
        for(int i=0; i<n; i++){
            if (nums[i]>mid) return false;
            if(countSum + nums[i]<=mid){
                countSum += nums[i];
            }
            else{
                part++;
                if(k<part) return false;
                countSum=nums[i];
            }
        }
        return true;
    }


    int splitArray(vector<int>& nums, int k) {
        
        int s=0;
        int sum=0;
        int n=nums.size();
        for(int i=0; i<n; i++){
            sum += nums[i];
        }
        int e= sum;
        
        int ans=-1;
        while(s<=e){
            int mid =s+(e-s)/2;
            if(isPossible(nums, n, k, mid)){
                ans=mid;
                e=mid-1;
            }
            else{
                s=mid+1;
            }
            
        }
        return ans;
        
    }
};
