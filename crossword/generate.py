import sys
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        copy = self.domains.copy()
        for var in copy:
            for word in set(copy[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        change = False

        if self.crossword.overlaps[x, y] != None:
            overlap = self.crossword.overlaps[x, y]

            copy = deepcopy(self.domains)
            for v1 in copy[x]:
                for v2 in copy[y]:
                    if v1[overlap[0]] == v2[overlap[1]]:
                        break
                else:
                    self.domains[x].remove(v1)
                    change = True

        return change

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = []
            for var1 in self.domains:
                for var2 in self.domains:
                    if var1 == var2:
                        break
                    if self.crossword.overlaps[var1, var2] is not None:
                        arcs.append((var1, var2))
                        arcs.append((var2, var1))
        while len(arcs) > 0:
            x = arcs[0][0]
            y = arcs[0][1]
            if self.revise(x, y) is False:
                arcs.pop(0)
                continue
            else:
                for neighbor in self.crossword.neighbors(x):
                    arcs.append((x, neighbor))
                    arcs.append((neighbor, x))
                arcs.pop(0)

            if len(self.domains[x]) == 0:
                return False

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if var not in assignment:
                return False

        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        words = []
        for var in assignment:
            word = assignment[var]

            if var.length != len(word):
                return False

            if word in words:
                return False

            for neighbor in self.crossword.neighbors(var):
                if neighbor in assignment:
                    neighword = assignment[neighbor]
                    x, y = self.crossword.overlaps[var, neighbor]
                    if word[x] != neighword[y]:
                        return False
            words.append(word)

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        neighbors = self.crossword.neighbors(var)
        words = {}
        for word in self.domains[var]:
            counter = 0
            for neighbor in neighbors:
                if neighbor in assignment:
                    continue
                overlap = self.crossword.overlaps[var, neighbor]
                for neighword in self.domains[neighbor]:
                    if word[overlap[0]] != neighword[overlap[1]]:
                        counter += 1
            words[word] = counter

        # go through words len(words) times and add the smallest counter to a list each tiem
        values_sorted = []
        n = len(words)
        for i in range(n):
            w = find_shortest_count(words)
            values_sorted.append(w)
            del words[w]

        return values_sorted

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # find variable with minimum remaining values in its domain and highest degree
        vals = float('inf')
        deg = float('inf')

        for var in self.domains:
            if var in assignment:
                continue
            vals_remaining = len(self.domains[var])
            degree = len(self.crossword.neighbors(var))

            if vals_remaining < vals:
                vals = vals_remaining
                deg = degree
                returner = var
            elif vals_remaining == vals:
                if degree < deg:
                    vals = vals_remaining
                    deg = degree
                    returner = var

        return returner

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # if assignment is complete return assignment
        if self.assignment_complete(assignment) == True:
            return assignment
        # var = select unassigned variable
        var = self.select_unassigned_variable(assignment)
        domain = self.order_domain_values(var, assignment)
        for word in domain:
            assignment[var] = word

            arcs = []
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                arcs.append((var, neighbor))
                arcs.append((neighbor, var))
            self.ac3(arcs)

            # if value is consistent with assignment
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
        return None


def find_shortest_count(words):
    r = float('inf')
    for word in words:
        if words[word] < r:
            r = words[word]
            w = word
    return w


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()

# self.domain[var] is returning nothing
# self.crossword.neighbors(var) is returning nothing
