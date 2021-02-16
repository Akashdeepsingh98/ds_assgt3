from math import ceil
b = 3


class InternalNode:
    def __init__(self):
        self.data = []

    def insert(self, ele):

        if len(self.data) < b*2-1:

            if isinstance(self.data[0], LeafNode):
                iinsert = 0
                while iinsert+1<len(self.data) and self.data[iinsert+1]<=ele:
                    iinsert += 2
                
                if len(self.data[iinsert].data)==b:

                    pass
                else:
                    pass

            else:
                pass

        else:
            
            if isinstance(self.data[0], LeafNode):
                pass
            
            else:
                pass
        pass


class LeafNode:
    def __init__(self):
        self.data = []
        self.data.append(None)
        self.parent = None

    def __repr__(self):
        return str(self.data)

    def insert(self, ele):
        present = self.elepresent(ele)
        if present == -1:
            if len(self.data) < b:

                self.data.insert(0, [ele, 1])
                self.data[:-1] = sorted(self.data[:-1], key=lambda x: x[0])

            else:
                # get a new leafnode and adjust stuff appropriately
                if self.parent==None:
                    il = ceil((b-1)/2)
                    self.data[-1] = LeafNode()
                    for i in range(il, len(self.data)-1):
                        self.data[-1].data.insert(0, self.data[i])
                    newdata = []
                    for i in range(il):
                        newdata.append(self.data[i])
                    newdata.append(self.data[-1])
                    self.data = newdata
                    self.data[:-1] = sorted(self.data[:-1], key=lambda x: x[0])

                    newInode = InternalNode()
                    newInode.data.append(self)
                    newInode.data.append(self.data[-1].data[0][0])
                    newInode.data.append(self.data[-1])
                    self.parent = newInode

                    return newInode
                else:
                    pass

        else:
            self.data[present][1] += 1
        return self

    def elepresent(self, ele):
        for i in range(len(self.data)-1):
            if self.data[i][0] == ele:
                return i
        return -1


class BPlusTree:
    def __init__(self):
        self.root = LeafNode()

    def insert(self, ele):
        self.root = self.root.insert(ele)
        print(self.root.data)
        pass


mytree = BPlusTree()
mytree.insert(6)
mytree.insert(16)
mytree.insert(26)
