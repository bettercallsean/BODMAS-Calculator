#!/usr/bin/env python3
# bodmas_calculator.py - A rule-based calculator that follows the rules of BODMAS/PEDMAS 

# 3+((4+6)*9/(2-16+8*(3^2+7)))/3*6*4-7 - copy and paste this if you can't think of a calculation yourself
# 7^3+3*(4*5-2^2-28/7+3)+9+((3+5)/(3-1)) - another test equation
# ((3+(2*2)-7)^2)+(((2*2)+3-5)^2)


def solve(calculation):
    precedence = {"^": 4, "/": 3, "*": 2, "+": 1, "-": 1}
    bodmasIndex = []
    calc = ""

    for i in range(len(calculation)):
        calc += str(calculation[i])
        if calculation[i] in precedence:
            if len(bodmasIndex) == 0:  # starts off the bodmasIndex list with a value (this is only executed once)
                bodmasIndex.append(i)
            else:
                for x in range(len(bodmasIndex)):  # for each of the values stored in bodmasIndex
                    if precedence[calculation[i]] < precedence[calculation[bodmasIndex[-1]]]:
                        bodmasIndex.append(i)
                        break
                    elif precedence[calculation[i]] > precedence[calculation[bodmasIndex[x]]]:
                        bodmasIndex.insert(x, i)  # insert the index value
                        break
                    elif precedence[calculation[i]] == precedence[calculation[bodmasIndex[x]]]:
                        if calculation[i] == "+" or calculation[i] == "-":
                            bodmasIndex.append(i)
                            break
                        else:
                            bodmasIndex.insert(x + 1, i)
                            break
                    else:
                        continue

    while len(bodmasIndex) != 0:
        # Performs calculations on the numbers on either side of the operator 
        if calculation[bodmasIndex[0]] == '^':
            currentCalculation = calculation[bodmasIndex[0] - 1] ** calculation[bodmasIndex[0] + 1]
        elif calculation[bodmasIndex[0]] == '/':
            currentCalculation = calculation[bodmasIndex[0] - 1] / calculation[bodmasIndex[0] + 1]
        elif calculation[bodmasIndex[0]] == '*':
            currentCalculation = calculation[bodmasIndex[0] - 1] * calculation[bodmasIndex[0] + 1]
        elif calculation[bodmasIndex[0]] == '+':
            currentCalculation = calculation[bodmasIndex[0] - 1] + calculation[bodmasIndex[0] + 1]
        else:
            currentCalculation = calculation[bodmasIndex[0] - 1] - calculation[bodmasIndex[0] + 1]

        calculation[bodmasIndex[0]-1] = currentCalculation
        calculation.pop(bodmasIndex[0]+1)
        calculation.pop(bodmasIndex[0])

        for i in range(len(bodmasIndex)):
            if bodmasIndex[i] > bodmasIndex[0]:
                bodmasIndex.insert(i, bodmasIndex[i] - 2)
                bodmasIndex.pop(i + 1)

        bodmasIndex.pop(0)

    return calculation[0]


def bracket_solver(calculation):
    # Pairs brackets together, so that the program knows which calculations to work out first
    startBracketIndex = []
    endBracketIndex = []
    bracketPairs = {}

    for i in range(len(calculation)):
        if calculation[i] == '(':
            startBracketIndex.append(i)
        elif calculation[i] == ')':
            endBracketIndex.append(i)

    for i in range(len(startBracketIndex) - 1, -1, -1):
        for x in range(len(endBracketIndex)):
            if endBracketIndex[x] < startBracketIndex[i] or endBracketIndex[x] in bracketPairs.values():
                continue
            else:
                bracketPairs[startBracketIndex[i]] = endBracketIndex[x]
                break
        break
    if len(bracketPairs) != 0:
        return bracketPairs


def calculator(calculation):
    brackets = bracket_solver(calculation)
    ans = []

    if brackets is None:
        return int(solve(calculation))
    else:
        s = list(brackets.keys())[0]
        e = brackets[s]
        ans.append(solve(calculation[s + 1:e]))
        calculation = calculation[:s] + ans + calculation[e + 1:]
        print(calculation)
        return calculator(calculation)


def calc_input():
    # Splits the calculation into an array of integers and BODMAS operators

    calcArray = []
    calculation = input('Enter your calculation: ')
    num = ""

    for i in range(len(calculation)):

        # If the current value is an int
        if calculation[i].isnumeric():
            # Because the equation is stored as a string, the numbers can be
            # appended to (e.g. the string '34' can have '6' appended to it, so it becomes '346')
            num = num + calculation[i]

            # If the current iteration value is the last in the calculation, it can simply be appended,
            # as there will be nothing left to append to the array after
            if i == len(calculation)-1:
                calcArray.append(int(num))
        else:
            #If the value being stored is not an int, it will be a BODMAS operator

            # If there is no number currently being held in num, then the operator can be appended to the array 
            if num == "":
                calcArray.append(calculation[i])
            
            # Else, if there is a number currently being held in num, append it to the array and then append the operator after it
            # Then reset the num variable to be empty, ready for the next lot of numbers to be stored in it.
            else:
                calcArray.append(int(num))
                calcArray.append(calculation[i])
                num = ""

    return calculator(calcArray)


ans = calc_input()
print(ans)
