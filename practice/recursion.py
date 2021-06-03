def sumList(nums):
    if (len(nums) == 1):
        return nums[0]
    elif (len(nums)==0):
        return "Error" 
    else:
        a = nums[1:]   #this is how to slice a list
        return nums[0]+sumList(a)

def sumListofLists(nums):
    #take first element, if number then add + recurse
    #if list, then recurse + recurse
    #if last element and number, then return value
    #if last element and list, then return recursion

    if len(nums) > 1 and type(nums[0]) is int :
        return nums[0] + sumListofLists(nums[1:])
    elif len(nums) > 1 and type(nums[0]) is list :
        return sumListofLists(nums[0]) + sumListofLists(nums[1:])
    elif  len(nums) is 1 and type(nums[0]) is int :
        return nums[0]
    elif len(nums) is 1 and type(nums[0]) is list :
        return sumListofLists(nums[0])
    else:
        return 0

# ====== Function Calls ======
print(sumList([3, 4, 5, -2, 8]))
print(sumListofLists([1, 2, [3,4,[]], [5,6]]))