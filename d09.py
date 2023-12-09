def readFile(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line[:-1])
    return lines


def all_zeroes(nums):
    for n in nums:
        if n != 0:
            return False
    return True


lines = readFile("d09input.txt")
last_total = 0
first_total = 0
for line in lines:
    nums = [int(x) for x in line.split()]
    last_nums = [nums[-1]]
    first_nums = [nums[0]]
    while not all_zeroes(nums):
        nums = [nums[i] - nums[i - 1] for i in range(1, len(nums))]
        last_nums.append(nums[-1])
        first_nums.append(nums[0])

    last_value = 0
    first_value = 0
    for i in range(1, len(last_nums) + 1):
        last_value = last_nums[len(last_nums) - i] + last_value
        first_value = first_nums[len(first_nums) - i] - first_value
    last_total += last_value
    first_total += first_value

print(last_total)
print(first_total)
