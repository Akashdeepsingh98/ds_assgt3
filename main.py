from math import ceil
GLOBAL_ORDER = 3


class Node:
    def __init__(self):
        self.keys = []
        self.values = []  # this could be count of keys or pointer to child nodes
        self.isLeaf: bool = False
        self.parent: Node = None
        self.nextLeaf: Node = None

    def __repr__(self) -> str:
        return 'keys: {}, values: {}.'.format(str(self.keys), str(self.values))

    def __str__(self) -> str:
        return 'keys: {}, values: {}.'.format(str(self.keys), str(self.values))

    def leafInsert(self, ele: int):
        if (self.keys == None) or len(self.keys) == 0:
            self.keys = [ele]
            self.values = [1]
        else:
            i = 0
            while i < len(self.keys):
                if ele == self.keys[i]:
                    self.values[i] += 1
                    i = len(self.keys) + 1
                elif ele < self.keys[i]:
                    self.keys = self.keys[:i] + [ele] + self.keys[i:]
                    self.values = self.values[:i] + [1] + self.values[i:]
                    i = len(self.keys) + 1
                elif i == len(self.keys) - 1:
                    self.keys.append(ele)
                    self.values.append(1)
                    i = len(self.keys) + 1
                i += 1


class BPTree:
    def __init__(self):
        self.root = Node()
        self.root.isLeaf = True
        self.mn = None
        self.mx = None

    def commonInsert(self, ele):
        if (self.mn == None) or ele < self.mn:
            self.mn = ele
        if (self.mx == None) or ele > self.mx:
            self.mx = ele
        leaf = self.getLeaf(ele)
        leaf.leafInsert(ele)

        if len(leaf.keys) == GLOBAL_ORDER:
            mid = ceil((GLOBAL_ORDER - 1) / 2)
            newLeaf = Node()
            newLeaf.isLeaf = True
            newLeaf.parent = leaf.parent
            newLeaf.keys = leaf.keys[mid:]
            newLeaf.values = leaf.values[mid:]
            newLeaf.nextLeaf = leaf.nextLeaf
            leaf.keys = leaf.keys[:mid]
            leaf.values = leaf.values[:mid]
            leaf.nextLeaf = newLeaf
            # print(newLeaf)
            # print(leaf)
            self.intInsert(leaf, newLeaf, newLeaf.keys[0])

    def range(self, low, high):
        if high < self.mn or low > self.mx:
            return 0

        if low < self.mn:
            low = self.mn
        if high > self.mx:
            high = self.mx

        leaf1 = self.getLeaf(low)
        leaf2 = self.getLeaf(high)

        li, hi = None, None

        # work on li and hi

        while li < len(leaf1.keys) and leaf1.keys[li] < low:
            li += 1

        while hi < len(leaf2.keys) and leaf2.keys[hi] < high:
            hi += 1

        if hi < len(leaf2.keys) and leaf2.keys[hi] != high:
            hi -= 1
        elif hi >= len(leaf2.keys):
            hi = -1

        curLeaf = leaf1
        total = len(leaf1.keys) - li
        # print(total)
        curLeaf = leaf1.nextLeaf
        while curLeaf != leaf2:
            total += len(curLeaf.keys)
            curLeaf = curLeaf.nextLeaf
        # print(total)
        total += hi + 1
        # print(total)
        return total

    def intInsert(self, leftLeaf: Node, rightLeaf: Node, key: int):
        if self.root == leftLeaf:
            rootNode = Node()
            rootNode.keys = [key]
            rootNode.values = [leftLeaf, rightLeaf]
            self.root = rootNode
            leftLeaf.parent = rightLeaf.parent = self.root

        else:
            parNode = leftLeaf.parent
            for i in range(len(parNode.values)):
                if parNode.values[i] == leftLeaf:
                    parNode.keys = parNode.keys[:i] + \
                        [key] + parNode.keys[i:]
                    parNode.values = parNode.values[:i+1] + \
                        [rightLeaf] + parNode.values[i+1:]

                    if len(parNode.keys) == GLOBAL_ORDER:
                        newparent = Node()
                        newparent.parent = parNode.parent
                        mid = ceil((GLOBAL_ORDER-1)/2)
                        newparent.keys = parNode.keys[mid+1:]
                        newparent.values = parNode.values[mid+1:]
                        midkey = parNode.keys[mid]
                        parNode.keys = parNode.keys[:mid]
                        parNode.values = parNode.values[:mid+1]
                        for child in parNode.values:
                            child.parent = parNode
                        for child in newparent.values:
                            child.parent = newparent
                        self.intInsert(parNode, newparent, midkey)

    def getLeaf(self, ele: int) -> Node:
        curNode = self.root
        while not curNode.isLeaf:
            # print(curNode)
            i = 0
            while i < len(curNode.keys):
                if ele < curNode.keys[i]:
                    curNode = curNode.values[i]
                    i = len(curNode.keys) + 1
                elif ele == curNode.keys[i]:
                    curNode = curNode.values[i + 1]
                    i = len(curNode.keys) + 1
                elif i == len(curNode.keys) - 1:
                    # print(i)
                    # print(len(curNode.values))
                    curNode = curNode.values[i + 1]
                    i = len(curNode.keys) + 1
                i += 1
        return curNode

    def count(self, ele):
        leaf = self.getLeaf(ele)
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == ele:
                return leaf.values[i]
        return 0

    def find(self, ele):
        leaf = self.getLeaf(ele)
        for i in range(len(leaf.keys)):
            if leaf.keys[i] == ele:
                return True
        return False

    def printTree(self):
        print(self.root)


mytree = BPTree()
mytree.commonInsert(5)
mytree.commonInsert(15)
mytree.commonInsert(25)
mytree.commonInsert(35)
mytree.commonInsert(45)
mytree.commonInsert(5)
mytree.commonInsert(35)
mytree.commonInsert(45)
mytree.commonInsert(45)
mytree.printTree()

# print(mytree.count(5))
# print(mytree.count(15))
# print(mytree.count(25))
# print(mytree.count(35))
# print(mytree.count(45))
# print(mytree.count(55))
# print(mytree.count(-5))

print(mytree.range(24, 34))
