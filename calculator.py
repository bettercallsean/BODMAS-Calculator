# 3+((4+6)*9/(2-16+8*(3^2+7)))/3*6*4-7 - copy and paste this if you can't think of a calculation yourself


def solve(calculation):
    precedence = {"^": 5, "/": 4, "*": 3, "+": 2, "-": 2}
    bodmasIndex = []
    highestOperatorIndex = 0
    calc = ""

    for i in range(len(calculation)):
        calc += str(calculation[i])
        if calculation[i] in precedence:
            if len(bodmasIndex) == 0:  # starts off the bodmasIndex list with a value (this is only executed once)
                bodmasIndex.append(i)
            else:
                highestOperatorIndex = i
                for x in range(len(bodmasIndex)):  # for each of the values stored in bodmasIndex
                    if precedence[calculation[i]] > precedence[calculation[bodmasIndex[x]]]:
                        bodmasIndex.insert(x, i)  # insert the index value
                        break
                    elif precedence[calculation[i]] == precedence[calculation[bodmasIndex[x]]]:
                        bodmasIndex.insert(x + 1, i)
                        break
                    else:
                        bodmasIndex.append(i)
                        break

    for i in range(len(bodmasIndex)):

        if calculation[bodmasIndex[0]] == '^':
            currentCalculation = float(calculation[bodmasIndex[0] - 1]) ** float(calculation[bodmasIndex[0] + 1])
        elif calculation[bodmasIndex[0]] == '/':
            currentCalculation = float(calculation[bodmasIndex[0] - 1]) / float(calculation[bodmasIndex[0] + 1])
        elif calculation[bodmasIndex[0]] == '*':
            currentCalculation = float(calculation[bodmasIndex[0] - 1]) * float(calculation[bodmasIndex[0] + 1])
        elif calculation[bodmasIndex[0]] == '+':
            currentCalculation = float(calculation[bodmasIndex[0] - 1]) + float(calculation[bodmasIndex[0] + 1])
        else:
            currentCalculation = float(calculation[bodmasIndex[0] - 1]) - float(calculation[bodmasIndex[0] + 1])

        calculation[bodmasIndex[0] - 1] = currentCalculation
        calculation.pop(bodmasIndex[0] + 1)
        calculation.pop(bodmasIndex[0])

        if len(calculation) != 1:
            bodmasIndex.remove(highestOperatorIndex)
        highestOperatorIndex -= 2

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
    done = []

    for i in range(len(calculation)):
        try:
            if i in done:
                continue
            elif isinstance(int(calculation[i]), int):
                num = calculation[i]
                for x in range(i+1, len(calculation[i + 1:])):
                    try:
                        if isinstance(int(calculation[x]), int):
                            num = num + calculation[x]
                            done.append(x)
                    except ValueError:
                        break
                calcArray.append(int(num))
        except ValueError:
            calcArray.append(calculation[i])

    return calculator(calcArray)


ans = calcInput()
print(ans)
