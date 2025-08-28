class Solution {
public:
    void rotate(vector<int>& nums, int k) {
        int n = nums.size();
        k = k % n;  // handle large k

        // step 1: reverse last k elements
        reverse(nums.begin() + n - k, nums.end());

        // step 2: reverse first n-k elements
        reverse(nums.begin(), nums.begin() + n - k);

        // step 3: reverse whole array
        reverse(nums.begin(), nums.end());
    }
};
