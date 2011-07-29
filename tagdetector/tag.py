
class TagPart:

    def __init__(self, name, part):
        self.name = name
        self.part = part

    def __str__(self):
        return self.name + "(" + str(self.part) + ")"

    def __eq__(self, other):
        return self.name == other.name and self.part == other.v

    def __ne__(self, other):
        return self.name != other.name or self.part != other.part

    def __le__(self, other):
        return self.part <= other.part

    def __ge__(self, other):
        return self.part >= other.part

    def __lt__(self, other):
        return self.part < other.part

    def __gt__(self, other):
        return self.part < other.part


class TagWord:

    def __init__(self, word, count, part = 0):
        self.word = word
        self.count = count
        self.part = part

    def __str__(self):
        return self.word + "(" + str(self.count) + ", " + str(self.part) + ")"

    def __eq__(self, other):
        return self.word == other.word and self.count == other.count
    
    def __ne__(self, other):
        return self.word != other.word or self.count != other.count

    def __le__(self, other):
        return self.count <= other.count

    def __ge__(self, other):
        return self.count >= other.count

    def __lt__(self, other):
        return self.count < other.count

    def __gt__(self, other):
        return self.count < other.count