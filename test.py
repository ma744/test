from random import randint
from math import gcd
from functools import reduce


class Equation:
    """
    A chemistry equation
    """
    def __init__(self, equation):
        """
        Initializes the chemistry equation

        @type of equation: str
        """
        self.left = list()
        self.right = list()
        self.balanced = True

        integers = '0123456789'
        split = equation.split(' = ')

        """
        (H)2 + (O)2 = (H)2(O)1
        """
        left = split[0]
        right = split[1]
        left_components = left.split(' + ')
        right_components = right.split(' + ')

        total_left = dict()
        total_right = dict()

        # Parsing the entered equation (left side)
        # and counting the elements on the left side of the equation
        for component in left_components:
            left_counts = dict()
            for i in range(0, len(component)):
                if component[i] == ')':
                    if component[i - 2] == '(':
                        element = component[i - 1]
                    elif component[i -3] == '(':
                        element = component[i - 2: i]
                    try:
                        if component[i + 3] in integers:
                            number = int(component[i + 1: i + 4])
                        elif component[i + 2] in integers:
                            number = int(component[i + 1: i + 3])
                        else:
                            number = int(component[i + 1])
                    except IndexError:
                        try:
                            if component[i + 2] in integers:
                                number = int(component[i + 1: i + 3])
                            else:
                                number = int(component[i + 1])
                        except IndexError:
                            # Fehler
                            number = int(component[i + 1])
                            """
                            if component[i + 1] in integers:
                                number = int(component[i + 1])
                            """
                    if element in left_counts:
                        left_counts[element] += number
                    else:
                        left_counts[element] = number
                    if element in total_left:
                        total_left[element] += number
                    else:
                        total_left[element] = number
            self.left.append(left_counts)

        # Parsing the entered equation (right side)
        # and counting the elements on the right side of the equation
        for component in right_components:
            right_counts = dict()
            for i in range(0, len(component)):
                if component[i] == ')':
                    if component[i - 2] == '(':
                        element = component[i - 1]
                    elif component[i -3] == '(':
                        element = component[i - 2: i]
                    try:
                        if component[i + 3] in integers:
                            number = int(component[i + 1: i + 4])
                        elif component[i + 2] in integers:
                            number = int(component[i + 1: i + 3])
                        else:
                            number = int(component[i + 1])
                    except IndexError:
                        try:
                            if component[i + 2] in integers:
                                number = int(component[i + 1: i + 3])
                            else:
                                number = int(component[i + 1])
                        except IndexError:
                            # Fehler
                            number = int(component[i + 1])
                            """
                            if component[i + 1] in integers:
                                number = int(component[i + 1])
                            """         
                    if element in right_counts:
                        right_counts[element] += number
                    else:
                        right_counts[element] = number
                    if element in total_right:
                        total_right[element] += number
                    else:
                        total_right[element] = number
            self.left.append(right_counts)

        # Check if the equation is balanced
        # if not continue
        for key in total_right:
            if total_left[key] != total_right[key]:
                self.balanced = False
            else:
                continue

    def balance(self):
        """
        Balances the chemical equation
        """
        if self.balanced:
            string = str()
            for dictionary in self.left:
                compound = str()
                for key in dictionary:
                    compound += str(dictionary[key])
                string += compound
                string += ' + '
            string = string[:len(string) - 3] + ' = '
            for dictionary in self.left:
                compound = str()
                for key in dictionary:
                    compound += str(dictionary[key])
                string += compound
                string += ' + '
                string = string[:len(string) - 2]

                return string
            else:
                # Keeps iterating till equation is equal
                while not self.balanced:
                    tmp_left = list()
                    tmp_right = list()
                    total_left = dict()
                    total_right = dict()

                    for item in self.left:
                        new_dict = dict()
                        for key in item:
                            new_dict[key] = item [key]
                        tmp_left.append(new_dict)

                    for item in self.right:
                        new_dict = dict()
                        for key in item:
                            new_dict[key] = item [key]
                        tmp_right.append(new_dict)

                    # Generate a random set of coefficients for each component
                    left_coefficients = [randint(0, 10) for _ in range(len(tmp_left))]
                    right_coefficients = [randint(0, 10) for _ in range(len(tmp_right))]

                    #
                    for i in range(0, len(left_coefficients)):
                        for key in tmp_left[i]:
                            tmp_left[i][key] *= left_coefficients[i]
                            if key not in total_left:
                                total_left[key] = tmp_left[i][key]
                            else:
                                total_left[key] += tmp_left[i][key]

                    # Same for the right side
                    for i in range(0, len(right_coefficients)):
                        for key in tmp_right[i]:
                            tmp_right[i][key] *= right_coefficients[i]
                            if key not in total_right:
                                total_right[key] = tmp_right[i][key]
                            else:
                                total_right[key] += tmp_right[i][key]

                    # Testing
                    self.balanced = True
                    for key in total_left:
                        if total_left[key] != total_right[key]:
                            self.balanced = False
                        else:
                            continue
                    

                big_tup = tuple(left_coefficients + right_coefficients)
                left_coefficients = list(map(lambda x: int(x/reduce(gcd, big_tup)), left_coefficients))
                right_coefficients = list(map(lambda x: int(x/reduce(gcd, big_tup)), right_coefficients))

                string = str()
                for i in range(0, len(self.left)):
                    if left_coefficients[i] != 1:
                        compound = str(left_coefficients[i])
                    else:
                        compound = str()
                    for key in self.left[i]:
                        compound += key
                        if self.left[i][key] != 1:
                            compound += str(self.left[i][key])
                        else:
                            continue
                    string += compound
                    string += ' + '
                string += string[:len(string) - 3] + ' = '

                # Same for the right side
                for i in range(0, len(self.right)):
                    if right_coefficients[i] != 1:
                        compound = str(right_coefficients[i])
                    else:
                        compound = str()
                    for key in self.right[i]:
                        compound += key
                        if self.right[i][key] != 1:
                            compound += str(self.right[i][key])
                        else:
                            continue
                    string += compound
                    string += ' + '
                string += string[:len(string) - 2]

                return string
                
                    










                                
                                
