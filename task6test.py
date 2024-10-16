import pytest
from task6 import Stack

def test_push():
    stack = Stack()
    stack.push(10)
    assert stack.peek() == 10

def test_pop():
    stack = Stack()
    stack.push(10)
    stack.push(20)
    assert stack.pop() == 20
    assert stack.peek() == 10

def test_peek():
    stack = Stack()
    stack.push(30)
    assert stack.peek() == 30 

def test_is_empty():
    stack = Stack()
    assert stack.is_empty()
    stack.push(10)
    assert not stack.is_empty()

def test_pop_empty_stack():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_peek_empty_stack():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()
