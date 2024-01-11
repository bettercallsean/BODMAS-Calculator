#!/usr/bin/env python3
# bodmas_calculator.py - A rule-based calculator that follows the rules of BODMAS

# 3+((4+6)*9/(2-16+8*(3^2+7)))/3*6*4-7 - copy and paste this if you can't think of a calculation yourself
# 7^3+3*(4*5-2^2-28/7+3)+9+((3+5)/(3-1)) - another test equation
# ((3+(2*2)-7)^2)+(((2*2)+3-5)^2)


def solve(calculation):
    operator_precedence = {"^": 4, "/": 3, "*": 2, "+": 1, "-": 1}

    # bodmas_index will store the index of all the operators in the equation
    # The order of the list is the order in which the calculation will be performed
    bodmas_index = []

    # very dirty hack to check if two values are next to each other with no operators
    # in this case, this is a multiplication: bracket removals are handled in other functions
    # so in theory, calculation should be a raw list with no brackets
    insert_finished = False
    while not insert_finished:
        calculation_size = len(calculation)
        for i in range(len(calculation)):
            if i > 0:
                if isinstance(calculation[i], float) and isinstance(calculation[i - 1], float):
                    calculation.insert(i, '*')
        if calculation_size == len(calculation):
            insert_finished = True

    for i in range(len(calculation)):
        if calculation[i] in operator_precedence:
            if len(bodmas_index) == 0:  # starts off the bodmas_index list with a value (this is only executed once)
                bodmas_index.append(i)
            else:
                # Loops through the current indexes of operators and works out the order in which the operators need to be
                # arranged by comparing the operator_precedence values and seeing if a particular operator needs to be worked on
                # before or after another one (e.g all * operations will need to be performed before all - operations)
                for x in range(len(bodmas_index)):
                    if operator_precedence[calculation[i]] < operator_precedence[calculation[bodmas_index[-1]]]:
                        bodmas_index.append(i)
                        break
                    elif operator_precedence[calculation[i]] > operator_precedence[calculation[bodmas_index[x]]]:
                        bodmas_index.insert(x, i)
                        break
                    elif operator_precedence[calculation[i]] == operator_precedence[calculation[bodmas_index[x]]]:
                        if calculation[i] == "+" or calculation[i] == "-":
                            bodmas_index.append(i)
                            break
                        else:
                            bodmas_index.insert(x + 1, i)
                            break
                    else:
                        continue

    while len(bodmas_index) != 0:
        # Loops through the operator indexes from left to right and performs the required operation, storing the result
        # in calculation_result
        if calculation[bodmas_index[0]] == '^':
            calculation_result = calculation[bodmas_index[0] - 1] ** calculation[bodmas_index[0] + 1]
        elif calculation[bodmas_index[0]] == '/':
            calculation_result = calculation[bodmas_index[0] - 1] / calculation[bodmas_index[0] + 1]
        elif calculation[bodmas_index[0]] == '*':
            calculation_result = calculation[bodmas_index[0] - 1] * calculation[bodmas_index[0] + 1]
        elif calculation[bodmas_index[0]] == '+':
            calculation_result = calculation[bodmas_index[0] - 1] + calculation[bodmas_index[0] + 1]
        else:
            calculation_result = calculation[bodmas_index[0] - 1] - calculation[bodmas_index[0] + 1]

        # calculation_result stores the result which is then inserted into the equation in place of the
        # two values and operator that was used to calculate it.
        calculation[bodmas_index[0] - 1] = calculation_result
        calculation.pop(bodmas_index[0] + 1)
        calculation.pop(bodmas_index[0])

        # Any operator indexes that are higher than the index stored at bodmas_index[0] will need to have their index position shifted by -2
        # to accommodate for the shortening calculation. It's been about 2 years since I wrote this code and I never commented on its behaviour,
        # so here I am 2 years later trying to remember why I chose to do the loop this way.
        print(bodmas_index)
        for i in range(len(bodmas_index)):
            if bodmas_index[i] > bodmas_index[0]:
                bodmas_index.insert(i, bodmas_index[i] - 2)
                bodmas_index.pop(i + 1)

        bodmas_index.pop(0)

    return calculation[0]


def bracket_pair_finder(calculation):
    # Pairs brackets together, so that the program knows which calculations to work out first
    start_bracket_index_array = []
    end_bracket_index_array = []
    bracket_pairs = {}

    for i in range(len(calculation)):
        if calculation[i] == '(':
            start_bracket_index_array.append(i)
        elif calculation[i] == ')':
            end_bracket_index_array.append(i)

    # Finds the innermost brackets so that they can be solved first
    # Only returns one pair of brackets at a time.
    # If all of them were returned, they could potentially be solved recursively, but I haven't tried it
    for i in range(len(start_bracket_index_array) - 1, -1, -1):
        for x in range(len(end_bracket_index_array)):
            if end_bracket_index_array[x] < start_bracket_index_array[i] or end_bracket_index_array[x] in bracket_pairs.values():
                continue
            else:
                bracket_pairs[start_bracket_index_array[i]] = end_bracket_index_array[x]
                break
        break
    if len(bracket_pairs) != 0:
        return bracket_pairs


def calculator(calculation):
    brackets = bracket_pair_finder(calculation)
    answer = []

    if brackets is None:
        return float(solve(calculation))
    else:
        start_bracket_index = list(brackets.keys())[0]
        end_bracket_index = brackets[start_bracket_index]
        answer.append(solve(calculation[start_bracket_index + 1:end_bracket_index]))
        calculation = calculation[:start_bracket_index] + answer + calculation[end_bracket_index + 1:]
        print(calculation)
        return calculator(calculation)


def calc_input():
    # Splits the calculation into an array of integers and BODMAS operators

    calculation_array = []
    calculation = input('Enter your calculation: ')
    number = ""

    for i in range(len(calculation)):

        # If the current value is an int
        if calculation[i].isnumeric() or calculation[i] == ".":
            # Because the equation is stored as a string, the numbers can be
            # appended to (e.g. the string '34' can have '6' appended to it, so it becomes '346')
            number = number + calculation[i]

            # If the current iteration value is the last in the calculation, it can simply be appended,
            # as there will be nothing left to append to the array after
            if i == len(calculation) - 1:
                calculation_array.append(float(number))
        else:
            # If the value being stored is not an int, it will be a BODMAS operator

            # If there is no number currently being held in number, then the operator can be appended to the array
            if number == "":
                calculation_array.append(calculation[i])

            # Else, if there is a number currently being held in number, append it to the array and then append the operator after it
            # Then reset the number variable to be empty, ready for the next lot of numbers to be stored in it.
            else:
                calculation_array.append(float(number))
                calculation_array.append(calculation[i])
                number = ""

    return calculator(calculation_array)


if __name__ == "__main__":
    answer = calc_input()
    print(answer)
