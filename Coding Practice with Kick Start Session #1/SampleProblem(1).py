def solve():
    number_of_candybags = int(input(" Enter number of candybags: "))
    number_of_children = int(input(" Enter number of children: "))
    total_candy = 0
    for i in range(number_of_candybags):
        candy_count = int(float(input(" Enter the candy count: ")))
        total_candy += candy_count
    return total_candy % number_of_children


number_of_cases = int(input(" Enter number of cases: "))
for i in range(number_of_cases):
    remaining_candy = solve()
    print(" Case #", i + 1, ": ", remaining_candy)
