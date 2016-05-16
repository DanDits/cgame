import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.



def intended(line, level):
    return ("    " * level) + str(line)


keywords = ('(', ')', '=', ';')


class Element:
    def __init__(self, name):
        self.name = name

    def pretty_text(self, level):
        pass

    @staticmethod
    def parse_atoms(atoms, start_index):
        for element_class in (Block, Primitive, KeyValue):
            index, element = element_class.parse_atoms(atoms, start_index)
            if element is not None:
                return index, element
        return start_index, None


class Block(Element):
    # elements is an iterable which contains Elements, can be empty or None
    def __init__(self, elements=None):
        super().__init__("BLOCK")
        self.elements = list(elements) if elements is not None else []

    def pretty_text(self, level):
        content = ";\n".join([el.pretty_text(level + 1) for el in self.elements])
        return intended("(\n", level) + content + ("\n" if len(content) > 0 else "") + intended(")", level)

    @staticmethod
    def parse_atoms(atoms, start_index):
        if atoms[start_index] == '(':
            depth = 0
            elements = []
            index = start_index + 1
            while atoms[index] != ')':
                index, element = Element.parse_atoms(atoms, index)
                elements.append(element)
                if atoms[index] == ';':
                    index += 1
            return index + 1, Block(elements)
        return start_index, None


class Primitive(Element):
    # primitive_type is one of the following: (str, int, bool, NoneType, None)
    # primitive_value is interpreted corresponding to type, if type is None the type() of the value will be used
    def __init__(self, primitive_value, primitive_type=None):
        super().__init__("PRIMITIVE_TYPE")
        self.primitive_class = type(primitive_value) if primitive_type is None else primitive_type
        self.primitive_value = primitive_value

    def pretty_text(self, level):
        if self.primitive_class is str:
            return intended("'" + self.primitive_value + "'", level)
        elif self.primitive_class is int:
            return intended(self.primitive_value, level)
        elif self.primitive_class is bool:
            return intended("true" if self.primitive_value else "false", level)
        elif self.primitive_class is type(None):
            return intended("null", level)

    @staticmethod
    def parse_atoms(atoms, start_index):
        if (atoms[start_index] not in keywords
            and (len(atoms) < start_index + 2 or atoms[start_index + 1] != '=')):
            new_primitive = None
            if atoms[start_index] == 'null':
                new_primitive = Primitive(None)
            elif atoms[start_index] in ('true', 'false'):
                new_primitive = Primitive(atoms[start_index] == 'true')
            elif atoms[start_index][0] != "'":
                new_primitive = Primitive(int(atoms[start_index]))
            else:
                new_primitive = Primitive(atoms[start_index][1:-1])
            return start_index + 1, new_primitive
        return start_index, None


class KeyValue(Element):
    # Identifier is a string that is the keys characters
    # value is of either of class Primitive or of class Block or a type that
    # can be used to create a valid Primitive
    def __init__(self, identifier, value):
        super().__init__("KEY_VALUE")
        self.identifier = Primitive(identifier)
        if type(value) is Primitive or type(value) is Block:
            self.value = value
        else:
            self.value = Primitive(value)

    def pretty_text(self, level):
        if isinstance(self.value, Primitive):
            return self.identifier.pretty_text(level) + "=" + self.value.pretty_text(0)
        # assert value type is BLOCK
        return (self.identifier.pretty_text(level) + "=\n" +
                self.value.pretty_text(level))

    @staticmethod
    def parse_atoms(atoms, start_index):
        if (atoms[start_index] not in keywords
            and (len(atoms) >= start_index + 2 and atoms[start_index + 1] == '=')):
            identifier = atoms[start_index][1:-1]
            index = start_index + 2  # start_index + 1 is the equals keyword
            element_class = Block if atoms[index] == '(' else Primitive
            index, value = element_class.parse_atoms(atoms, index)
            return index, KeyValue(identifier, value)
        return start_index, None


def cgx_stream():
    n = int(input())
    for i in range(n):
        cgxline = input()
        for char in cgxline:
            yield char


def next_atom():
    cgx = cgx_stream()
    curr_primitive_build = None
    while True:
        curr = ' '
        while curr.isspace():
            try:
                curr = next(cgx)
            except StopIteration as e:
                if curr_primitive_build is not None:
                    yield "".join(curr_primitive_build)
                    curr_primitive_build = None
                raise e
        if curr in keywords:
            if curr_primitive_build is not None:
                yield "".join(curr_primitive_build)
                curr_primitive_build = None
            # keyword
            yield curr
        elif curr == "'":
            # string primitive / identifier
            string = [curr]
            curr = ''
            while curr != "'":
                curr = next(cgx)
                string.append(curr)
            yield "".join(string)
        else:
            # other primitive, end it when a keyword or whitespace appears
            if curr_primitive_build is None:
                curr_primitive_build = []
            curr_primitive_build.append(curr)


# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
root = KeyValue("users",
                Block([Block([KeyValue("id", 10), KeyValue("name", "S. Karamazov"),
                              KeyValue("roles", Block([Primitive("visitor"), Primitive("moderator")])),
                              Primitive(None)]),
                       Block([KeyValue("id", 11), KeyValue("name", "P; Biales")]), Primitive(True)]))

atoms = [atom for atom in next_atom()]
_, root = Element.parse_atoms(atoms, 0)
print(atoms, file=sys.stderr)
print(root.pretty_text(0))
