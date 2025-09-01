//https://leetcode.com/problems/sqrtx/

class Solution {
public:
    int binarySearch(int n){
        int s =0;
        int e =n;
        long long int mid = s+(e-s)/2;
        long long int ans =-1;

        while(s<=e){
            long long int sqrt = mid*mid;
            if(sqrt==n){
                return mid;
            }
            else if(sqrt<n){
                ans =mid;
                s= mid+1;
            }
            else{
                e= mid-1;
            }
            mid = s+(e-s)/2;
        }
        return ans;
    }


    int mySqrt(int x) {
        return binarySearch(x);
        
    }
};
