# 3+((4+6)*9/(2-16+8*(3^2+7)))/3*6*4-7 - copy and paste this if you can't think of a calculation yourself
# 7^3+3*(4*5-2^2-28/7+3)+9+((3+5)/(3-1)) - another test equation


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


def bracketSolver(calculation):
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
            if endBracketIndex[x] < startBracketIndex[i]:
                continue
            elif endBracketIndex[x] in bracketPairs.values():
                continue
            else:
                bracketPairs[startBracketIndex[i]] = endBracketIndex[x]
                break
        break
    if len(bracketPairs) != 0:
        return bracketPairs


def calculator(calculation):
    brackets = bracketSolver(calculation)
    ans = []

    if brackets is None:
        return solve(calculation)
    else:
        s = list(brackets.keys())[0]
        e = brackets[s]
        ans.append(solve(calculation[s + 1:e]))
        calculation = calculation[:s] + ans + calculation[e + 1:]
        print(calculation)
        return calculator(calculation)


def calcInput():
    calcArray = []
    calculation = input('Enter your calculation: ')
    num = ""

    for i in range(len(calculation)):
        if calculation[i].isnumeric():
            num = num + calculation[i]
            if i == len(calculation)-1:
                calcArray.append(int(num))
        else:
            if num == "":
                calcArray.append(calculation[i])
            else:
                calcArray.append(int(num))
                calcArray.append(calculation[i])
                num = ""

    return calculator(calcArray)


ans = calcInput()
print(ans)
