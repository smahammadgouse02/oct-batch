nums=[2,5,9,1,9,]
n=len(nums)
for i in range(n):
    for j in range(n-1):
        if nums[j]>nums[j+1]:
            nums[j],nums[j+1]=nums[j+1],nums[j]
            print(nums)  { bubble sort algorithm }