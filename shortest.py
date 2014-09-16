def shortest_formula(n):
    characters = ("0","1","2","3","4","5","6","7","8","9","+","*","**",")","(")
    i = 1
    formulas = [""]
    while True:
        formulas = add_perms(formulas, characters)
        for f in formulas:
            try:
                if eval(f) == n:
                    return f, i
            except:
                pass
        i+=1

def permutations(length, characters):
    if length <= 0:
        return [""]
    old_result = permutations(length-1, characters)
    new_result = []
    for i in range(len(characters)):
        for string in old_result:
            new_result += [string + characters[i]]
    return new_result

def add_perms(permutations, characters):
    new_permutations = []
    for c in characters:
        for p in permutations:
            new_permutations += [p + c]
    return new_permutations

# a1 = shortest_formula(125**3)
# print("number {0} | shortest formula {1} | length {2}".format(125**3, a1[0], a1[1]))
# a1 = shortest_formula(2**30)
# print("number {0} | shortest formula {1} | length {2}".format(2**30, a1[0], a1[1]))
# a1 = shortest_formula(2**15+1)
# print("number {0} | shortest formula {1} | length {2}".format(2**15+1, a1[0], a1[1]))
# a1 = shortest_formula((50*2)**10)
# print("number {0} | shortest formula {1} | length {2}".format((50*2)**10, a1[0], a1[1]))
# a1 = shortest_formula((2**8)*(2**8-1))
# print("number {0} | shortest formula {1} | length {2}".format((2**8)*(2**8-1), a1[0], a1[1]))



