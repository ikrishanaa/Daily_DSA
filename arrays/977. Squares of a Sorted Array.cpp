class Solution {
public:
    vector<int> sortedSquares(const vector<int>& nums) {
        int n = nums.size();
        vector<int> result(n);
        
        int l = 0, r = n - 1, k = n - 1;
        
        while (l <= r) {
            int leftVal = nums[l] * nums[l];
            int rightVal = nums[r] * nums[r];
            
            if (leftVal > rightVal) {
                result[k--] = leftVal;
                l++;
            } else {
                result[k--] = rightVal;
                r--;
            }
        }
        return result;
    }
};
