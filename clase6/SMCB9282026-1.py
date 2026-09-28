class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        new_node = Node(value)

        if self.root is None:
            self.root = new_node
            return

        current = self.root

        while True:
            if value < current.value:
                if current.left is None:
                    current.left = new_node
                    return
                current = current.left

            elif value > current.value:
                if current.right is None:
                    current.right = new_node
                    return
                current = current.right

            else:
                return  # No insertar duplicados

    def search(self, value):
        current = self.root

        while current is not None:
            if value == current.value:
                return True
            elif value < current.value:
                current = current.left
            else:
                current = current.right

        return False

    def inorder(self, node):
        if node is not None:
            self.inorder(node.left)
            print(node.value, end=" ")
            self.inorder(node.right)


# Ejemplo de uso
tree = BinarySearchTree()

tree.insert(50)
tree.insert(30)
tree.insert(70)
tree.insert(20)
tree.insert(40)
tree.insert(60)
tree.insert(80)

print("Recorrido in-order:")
tree.inorder(tree.root)

print("\n¿Existe 40?", tree.search(40))
print("¿Existe 90?", tree.search(90))
