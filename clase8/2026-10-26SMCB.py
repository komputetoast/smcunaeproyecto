import heapq
from typing import List


class Solution:
	def findKthLargest(self, nums: List[int], k: int) -> int:
		# Mantiene los k valores más grandes en un montículo mínimo; la raíz es la respuesta.
		largest = nums[:k]
		heapq.heapify(largest)

		for num in nums[k:]:
			if num > largest[0]:
				heapq.heapreplace(largest, num)

		return largest[0]


if __name__ == "__main__":
	print(Solution().findKthLargest([3, 2, 1, 5, 6, 4], 2))
