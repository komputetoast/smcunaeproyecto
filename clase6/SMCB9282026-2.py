class Solution:
    def flatten(self, root):
        if root is None:
            return

        self.flatten(root.left)
        self.flatten(root.right)

        left = root.left
        right = root.right

        root.left = None
        root.right = left

        current = root

        while current.right is not None:
            current = current.right

        current.right = right
