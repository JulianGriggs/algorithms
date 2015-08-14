"""
	Binary Search Tree data structure implemented:
	--------------------------------
	The Binary Search Tree represents an ordered symbol table of generic
	key-value pairs.  Keys must be comparable.  Does not permit duplicate keys.
	When assocating a value with a key already present in the BST, the previous
	value is replaced by the new one.  This implementation is for an unbalanced
	BST.
	
	It supports the following primary operations:
	Method        Description
	-----------------------------------------
	size          Return size of BST
	get           Retrieve value for key in BST 
	put           Add key-value pair to BST
	contains      Check if key is in BST
	is_empty      Check if BST is empty
	min_key       Get the minimum key in BST
	max_key       Get the maximum key in BST
	floor_key     Get the biggest key that is less than or equal to key
	ceiling_key   Get the smallest key that is greater than or equal to key
	rank          Get get the number of keys less than key
	select_key    Get the key with a given rank
	delete_min    Delete the key-value pair with minimum key from BST
	delete_max    Delete the key-value pair with maximum key from BST
	delete        Delete key-value pair with given key from BST
	keys          Get all keys in BST in ascending order

	Method       Worst Case     Balanced Tree
	-----------------------------------------
	size         O(1)           O(1)
	get          O(N)           O(lg N)
	put          O(N)           O(lg N)
	contains     O(N)           O(lg N)
	is_empty     O(1)           O(1)
	min_key      O(N)           O(lg N)
	max_key      O(N)           O(lg N)
	floor_key    O(N)           O(lg N)
	ceiling_key  O(N)           O(lg N)
	rank         O(N)           O(lg N)
	select_key   O(N)           O(lg N)
	delete_min   O(N)           O(lg N)
	delete_max   O(N)           O(lg N)
	delete       O(N)           O(lg N)
	keys         O(N)           O(N)
	
	Adapted from: http://algs4.cs.princeton.edu/32bst
"""
class Node:

	def __init__(self, key=None, val=None, size_of_subtree=1):
		self.key = key
		self.val = val
		self.size_of_subtree = size_of_subtree
		self.left = None
		self.right = None

class BinarySearchTree:

	def __init__(self):
		self.root = None


	def _size(self, node):
		if node == None: 
			return 0
		else:
			return node.size_of_subtree

	def size(self):
		'''
		Return the number of nodes in the BST
		'''
		return self._size(self.root)

	def is_empty(self):
		return self.size() == 0

	def _get(self, key, node):
		if node == None: 
			return None

		if key < node.key:
			return self._get(key, node.left)
		elif key > node.key:
			return self._get(key, node.right)
		else:
			return node.val

	def get(self, key):
		'''
		Return the value paired with 'key'
		'''
		return self._get(key, self.root)

	def contains(self, key):
		return self.get(key) != None

	def _put(self, key, val, node):

		# If we hit the end of a branch, create a new node
		if node == None: 
			return Node(key, val)

		# Follow left branch
		if key < node.key:
			node.left = self._put(key, val, node.left)
		# Follow right branch
		elif key > node.key:
			node.right = self._put(key, val, node.right)
		# Overwrite value
		else:
			node.val = val

		node.size_of_subtree = self._size(node.left) + self._size(node.right)+1
		return node

	def put(self, key, val):
		'''
		Add a new key-value pair.
		'''
		self.root = self._put(key, val, self.root)

	def _min_node(self):
		'''
		Return the node with the minimum key in the BST
		'''
		min_node = self.root
		# Return none if empty BST
		if min_node == None: return None

		while min_node.left != None:
			min_node = min_node.left

		return min_node

	def min_key(self):
		'''
		Return the minimum key in the BST
		'''
		min_node = self._min_node()
		if min_node == None: 
			return None
		else:
			return min_node.key

	def _max_node(self):
		'''
		Return the node with the maximum key in the BST
		'''
		max_node = self.root
		# Return none if empty BST
		if max_node == None: return None

		while max_node.right != None:
			max_node = max_node.right

		return max_node

	def max_key(self):
		'''
		Return the maximum key in the BST
		'''
		max_node = self._max_node()
		if max_node == None: 
			return None
		else:
			return max_node.key

	def _floor_node(self, key, node):
		'''
		Returns the node with the biggest key that is less than or equal to the
		given value 'key'
		'''
		if node == None: return None

		if key < node.key:
			# Floor must be in left subtree
			return self._floor_node(key, node.left)

		elif key > node.key:
			# Floor is either in right subtree or is this node
			attempt_in_right = self._floor_node(key, node.right)
			if attempt_in_right == None:
				return node
			else:
				return attempt_in_right

		else: 
			# Keys are equal so floor is node with this key
			return node

	def floor_key(self, key):
		''' 
		Returns the biggest key that is less than or equal to the given value 
		'key'
		'''
		floor_node = self._floor_node(key, self.root)
		if floor_node == None:
			return None
		else:
			return floor_node.key

	def _ceiling_node(self, key, node):
		'''
		Returns the node with the smallest key that is greater than or equal to
		the given value 'key'
		'''
		if node == None:
			return None

		if key < node.key:
			# Ceiling is either in left subtree or is this node
			attempt_in_left = self._ceiling_node(key, node.left)
			if attempt_in_left == None:
				return node
			else:
				return attempt_in_left
		elif key > node.key:
			# Ceiling must be in right subtree
			return self._ceiling_node(key, node.right)
		else:
			# Keys are equal so ceiling is node with this key
			return node

	def ceiling_key(self, key):
		''' 
		Returns the smallest key that is greater than or equal to the given 
		value 'key'
		'''
		ceiling_node = self._ceiling_node(key, self.root)
		if ceiling_node == None:
			return None
		else: 
			return ceiling_node.key

	def _select_node(self, rank, node):
		'''
		Return the node with rank equal to 'rank'
		'''
		if node == None:
			return None

		left_size = self._size(node.left)
		if left_size < rank:
			return self._select_node(rank - left_size - 1, node.right)
		elif left_size > rank:
			return self._select_node(rank, node.left)
		else:
			return node

	def select_key(self, rank):
		'''
		Return the key with rank equal to 'rank'
		'''
		select_node = self._select_node(rank, self.root)
		if select_node == None: 
			return None
		else:
			return select_node.key

	def _rank(self, key, node):
		if node == None: return None

		if key < node.key:
			return self._rank(key, node.left)
		elif key > node.key:
			return self._size(node.left) + self._rank(key, node.right) + 1

		else:
			return self._size(node.left)

	def rank(self, key):
		'''
		Return the number of keys less than a given 'key'.
		'''
		return self._rank(key, self.root)

	def _delete(self, key, node):
		if node == None:
			return None
		if key < node.key:
			node.left = self._delete(key, node.left)
		elif key > node.key:
			node.right = self._delete(key, node.right)

		else:
			if node.right == None: 
				return node.left
			elif node.left == None:
				return node.right
			else:
				old_node = node
				node = self._ceiling_node(key, node.right)
				node.right = self._delete_min(old_node.right)
				node.left = old_node.left
		node.size_of_subtree = self._size(node.left) + self._size(node.right)+1
		return node

	def delete(self, key):
		'''
		Remove the node with key equal to 'key'
		'''
		self.root = self._delete(key, self.root)

	def _delete_min(self, node):
		if node.left == None:
			return node.right

		node.left = self._delete_min(node.left)
		node.size_of_subtree = self._size(node.left) + self._size(node.right)+1
		return node

	def delete_min(self):
		'''
		Remove the key-value pair with the smallest key.
		'''
		self.root = self._delete_min(self.root)

	def _delete_max(self, node):
		if node.right == None:
			return node.left

		node.right = self._delete_max(node.right)
		node.size_of_subtree = self._size(node.left) + self._size(node.right)+1
		return node

	def delete_max(self):
		'''
		Remove the key-value pair with the largest key.
		'''
		self.root = self._delete_max(self.root)

	def _keys(self, node, keys):

		if node == None:
			return keys

		if node.left != None:
			keys = self._keys(node.left, keys)

		keys.append(node.key)

		if node.right != None:
			keys = self._keys(node.right, keys)

		return keys

	def keys(self):
		'''
		Return all of the keys in the BST in aschending order
		'''
		keys = []
		return self._keys(self.root, keys)
