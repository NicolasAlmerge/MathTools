#!/usr/bin/env python3

import re
from .fraction import Fraction


__all__ = (
    "Matrix",
    "AugmentedMatrix",
    "gauss_elim",
)

pattern = re.compile(r"\s*(-?\d+)\s*/\s*(-?\d+)\s*")


class Matrix:
    """Represents a matrix of size n_lines*n_columns. Values can be changed anytime, however the size is fixed."""

    def __init__(self, n_lines, n_columns, /):
        if not isinstance(n_lines, int) or not isinstance(n_columns, int):
            raise TypeError("arguments must be integers.")
        if n_lines <= 0 or n_columns <= 0:
            raise ValueError("arguments must be strictly positive.")
        self.n_lines = n_lines
        self.n_columns = n_columns
        self.lines = [[0 for i in range(self.n_columns)] for j in range(self.n_lines)]
        self.is_square = (self.n_lines == self.n_columns)
        self.is_row = (self.n_lines == 1)
        self.is_column = (self.n_columns == 1)

    @classmethod
    def from_coor(cls, *l: list):
        """Constructs the matrix from the list of coordinates."""
        if not isinstance(l, (list, tuple)):
            raise TypeError("coordinates must be list or tuple.")
        n_rows = len(l)
        if not n_rows:
            raise ValueError("list cannot be empty.")
        if not isinstance(l[0], (list, tuple)):
            raise TypeError("coordinates must be lists/tuples of lists/tuples.")
        n_columns = len(l[0])
        lines = []
        for x in l:
            if not isinstance(x, (list, tuple)):
                raise TypeError("coordinates must be lists/tuples of lists/tuples.")
            if len(x) != n_columns:
                raise ValueError("coordinates must have the same number of columns.")
            lines.append(x)
        m = cls(n_rows, n_columns)
        m.lines = lines
        return m

    def __str__(self):
        return "(" + ")\n(".join("  ".join(str(number) for number in line) for line in self.lines) + ")"

    def __repr__(self):
        return self.__str__()

    def display(self, *, add_newline=True):
        """Prints the matrix. If `add_newline` is set to `True`, it will add a newline character at the end."""
        if not isinstance(add_newline, bool):
            raise TypeError("add_newline argument must be boolean.")
        print(self.__str__() + "\n") if add_newline else print(self.__str__())

    @property
    def columns(self):
        return [list(x) for x in zip(*self.lines)]

    @property
    def is_null(self):
        return self == Matrix(self.n_lines, self.n_columns)

    @property
    def is_square_null(self):
        if not self.is_square:
            return False
        return self.is_null

    @property
    def is_identity(self):
        if not self.is_square:
            return False
        return self == Matrix.identity(self.n_lines)

    @classmethod
    def square(cls, n=1, /):
        """Makes a square matrix of dimension n (since default values are all zero, this automatically makes a square null matrix)."""
        return cls(n, n)

    def get_determinant(self):
        """Computes the determinant of the matrix. Matrix must be square."""
        if not self.is_square:
            raise TypeError("cannot compute determinant on a non-square matrix.")

        if self.n_lines == 1:
            return self.lines[0][0]

        result = 0
        for index, value in enumerate(self.lines[0]):
            new = Matrix(self.n_lines-1, self.n_columns-1)
            new.lines = [[colvalue for colindex, colvalue in enumerate(line) if colindex != index] for line in self.lines[1:]]
            result += ((-1)**index)*value*new.get_determinant()
        return result

    def is_inversible(self):
        """Returns `True` if matrix is inversible. `False` otherwise."""
        return self.is_square and bool(self.get_determinant())

    def get_inverse(self):
        """Returns the inverse of the matrix, if possible."""
        if not self.is_inversible():
            raise TypeError("matrix is not square or has determinant 0.")
        vectors = Matrix.identity(self.n_lines).lines
        inverse = Matrix.square(self.n_lines)
        for vectorindex, vector in enumerate(vectors):
            newMatrix = Matrix(self.n_lines+1, self.n_columns)
            newMatrix.lines = self.lines[:]
            for index, line in enumerate(newMatrix.lines):
                line.append(vector[index])
            m = gauss_elim(*newMatrix.lines)
            inverse.set_column(vectorindex+1, m.columns[-1])
        return inverse

    @classmethod
    def identity(cls, n=1, /):
        """Makes an indentity matrix of dimention n."""
        matrix = cls(n, n)
        for line in range(n):
            for column in range(n):
                if line == column:
                    matrix.lines[line-1][column-1] = 1
        return matrix

    def reset(self):
        """Sets all values to 0."""
        self.lines = [[0 for i in range(self.n_columns)] for j in range(self.n_lines)]
        return self

    def set_identity(self):
        """Sets matrix as identity. Matrix must be square."""
        if not self.is_square:
            raise TypeError("matrix must be square.")
        for line in range(self.n_lines):
            for column in range(self.n_columns):
                self.lines[line-1][column-1] = 1 if (line == column) else 0
        return self

    @classmethod
    def row(cls, *values):
        """Makes a row matrix with values."""
        if not values:
            raise ValueError("values must be entered.")
        matrix = cls(1, len(values))
        matrix.set_line(1, values)
        return matrix

    @classmethod
    def column(cls, *values):
        """Makes a column matrix with values."""
        if not values:
            raise ValueError("values must be entered.")
        matrix = cls(len(values), 1)
        matrix.set_column(1, values)
        return matrix

    def set_value(self, line, column, /, value):
        """Sets a value to a specific line and column."""
        if not isinstance(line, int):
            raise TypeError("line must be int.")
        if line <= 0 or line > self.n_lines:
            raise ValueError("line must be between 1 and n_lines.")
        if not isinstance(column, int):
            raise TypeError("column must be int.")
        if column <= 0 or column > self.n_columns:
            raise ValueError("column must be between 1 and n_columns.")
        self.lines[line-1][column-1] = value
        return self

    def get_value(self, line, column, /):
        """Gets a value from a specific line and column."""
        if not isinstance(line, int):
            raise TypeError("line must be int.")
        if line <= 0 or line > self.n_lines:
            raise ValueError("line must be between 1 and n_lines.")
        if not isinstance(column, int):
            raise TypeError("column must be int.")
        if column <= 0 or column > self.n_columns:
            raise ValueError("column must be between 1 and n_columns.")
        return self.lines[line-1][column-1]

    def set_line(self, line_num, /, values):
        """Sets a line to the line_num matrix. Line must be complete."""
        if not isinstance(line_num, int):
            raise TypeError("line_num must be int.")
        if line_num <= 0 or line_num > self.n_lines:
            raise ValueError("line_num must be between 1 and n_lines.")
        if not isinstance(values, (list, tuple)):
            raise TypeError("values must be a list or tuple.")
        if len(values) != self.n_columns:
            raise ValueError("not enough or too much values to set.")
        self.lines[line_num-1] = list(values)
        return self

    def get_line(self, line_num, /):
        """Gets a line from the matrix."""
        if not isinstance(line_num, int):
            raise TypeError("line_num must be int.")
        if line_num <= 0 or line_num > self.n_lines:
            raise ValueError("line_num must be between 1 and n_lines.")
        return self.lines[line_num-1]

    def set_column(self, column_num, /, values):
        """Sets a column to the column_num matrix. Column must be complete."""
        if not isinstance(column_num, int):
            raise TypeError("column_num must be int.")
        if column_num <= 0 or column_num > self.n_columns:
            raise ValueError("column_num must be between 1 and n_columns.")
        if not isinstance(values, (list, tuple)):
            raise TypeError("values must be a list or tuple.")
        if len(values) != self.n_lines:
            raise ValueError("not enough or too much values to set.")
        for index, val in enumerate(values):
            self.lines[index][column_num-1] = val
        return self

    def get_column(self, column_num, /):
        """Gets a column from the matrix."""
        if not isinstance(column_num, int):
            raise TypeError("column_num must be int.")
        if column_num <= 0 or column_num > self.n_columns:
            raise ValueError("column_num must be between 1 and n_columns.")
        return self.columns[column_num-1]

    def transpose(self):
        """Returns the transpose of the matrix."""
        m = Matrix(self.n_columns, self.n_lines)
        for i in range(len(self.lines)):
            for j in range(len(self.lines[i])):
                m.lines[j][i] = self.lines[i][j]
        return m

    def trace(self):
        """Returns the trace of the matrix. Matrix must be square."""
        if not self.is_square:
            raise TypeError("cannot compute trace on a non-square matrix.")
        s = 0
        for i in range(len(self.lines)):
            s += self.lines[i][i]
        return s

    def dot(self, other):
        """Returns dot product of two matrices. Must be both column or row."""
        if not isinstance(other, Matrix):
            raise TypeError("matrix can only dot product another matrix.")
        if self.is_row and other.is_row:
            return self.__mul__(other.transpose()).lines[0][0]
        if self.is_column and other.is_column:
            return (self.transpose()).__mul__(other).lines[0][0]
        raise TypeError("matrices cannot be multiplied by the dot product")

    def __bool__(self):
        return not self.is_null

    def __len__(self):
        return self.n_lines*self.n_columns

    def __abs__(self):
        matrix = Matrix(self.n_lines, self.n_columns)
        matrix.lines = [[abs(x) for x in line] for line in self.lines]
        return matrix

    def __neg__(self):
        return self.__mul__(-1)

    def __pos__(self):
        return self.clone()

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return False
        return self.lines == other.lines

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("matrix can only add another matrix.")
        if self.n_lines != other.n_lines or self.n_columns != other.n_columns:
            raise TypeError("matrixes must be of the same size.")
        matrix = Matrix(self.n_lines, self.n_columns)
        matrix.lines = [[self.lines[i][j]+other.lines[i][j] for j in range(self.n_columns)] for i in range(self.n_lines)]
        return matrix

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.n_columns != other.n_lines:
                raise TypeError("matrices cannot be multiplied.")
            matrix = Matrix(self.n_lines, other.n_columns)
            matrix.lines = [[sum(a*b for a,b in zip(X_row, Y_col)) for Y_col in zip(*other.lines)] for X_row in self.lines]
            return matrix
        matrix = Matrix(self.n_lines, self.n_columns)
        matrix.lines = [[other*i for i in line] for line in self.lines]
        return matrix

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        if not isinstance(other, int):
            return TypeError("matrix power can only be an integer.")

        if other <= -1:
            new = self.get_inverse()
            return new.__pow__(abs(other)) if other < -1 else new

        if not other:
            return Matrix.identity(self.n_lines)

        power = self.clone()
        for _ in range(other-1):
            power *= self

        return power

    def clone(self):
        """Returns a copy of the matrix."""
        m = Matrix(self.n_lines, self.n_columns)
        m.lines = self.lines[:]
        return m


class AugmentedMatrix(Matrix):
    """Represents an augmented matrix."""
    def __str__(self):
        M = self.lines[:]
        C = self.columns[:]
        maxspace = 1
        for line in range(len(M)):
            for col in range(len(C)):
                val = M[line][col]
                if val == int(val):
                    val = int(val)
                    M[line][col] = val
                if len(str(val)) > maxspace:
                    maxspace = len(str(val))
        maxspace += 2
        string = ""
        for index, line in enumerate(M):
            string += "("
            for number in line[:-1]:
                string += str(number) + " "*(maxspace-len(str(number)))
            last = str(line[-1])
            string += "|" + " "*(maxspace-len(last)) + last + ")"
            if index != len(M)-1:
                string += "\n"
        return string

    def __repr__(self):
        return self.__str__()

    def clone(self):
        """Returns a copy of the augmented matrix."""
        m = AugmentedMatrix(self.n_lines, self.n_columns)
        m.lines = self.lines[:]
        return m


def gauss_elim(*M):
    """Performs gaussean elimination on a list of rows."""
    A = [elem[:] for elem in M]
    r = 0

    n_rows = len(A)
    n_columns = len(A[0])
    for row in range(n_rows):
        if len(A[row]) != n_columns:
            raise TypeError("matrix must have same number of columns.") from None

        for col in range(n_columns):
            row_col = A[row][col]
            if isinstance(row_col, str):
                match = pattern.fullmatch(row_col)
                if not match:
                    raise TypeError("expected int, float or str with '/' to denote fraction.")
                groups = match.groups()
                A[row][col] = Fraction(int(groups[0]), int(groups[1]))
                continue
            if isinstance(row_col, int):
                A[row][col] = Fraction(row_col, 1)

    for j in range(n_columns-1):
        k = r
        try:
            highest_val = abs(A[k][j])
        except IndexError:
            m = AugmentedMatrix(n_rows, n_columns)
            m.lines = A
            return m

        for i in range(r+1, n_rows):
            value = abs(A[i][j])
            if value > highest_val:
                highest_val = value
                k = i

        k_col = A[k][j]
        if k_col != 0:
            for col in range(n_columns):
                A[k][col] /= k_col

            if k != r:
                A[k], A[r] = A[r], A[k]

            for i in range(n_rows):
                i_j = A[i][j]
                if i != r:
                    for col in range(n_columns):
                        A[i][col] -= (A[r][col]*i_j)

            r += 1

    m = AugmentedMatrix(n_rows, n_columns)
    m.lines = A
    return m
