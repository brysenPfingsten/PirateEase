import pytest
from PirateEase.Utils.singleton import Singleton


def test_singleton_creates_only_one_instance():
    class TestClassA(Singleton):
        pass

    class TestClassB(Singleton):
        pass

    instance_a1 = TestClassA()
    instance_a2 = TestClassA()
    instance_b1 = TestClassB()
    instance_b2 = TestClassB()

    # Same class returns same instance
    assert instance_a1 is instance_a2
    assert id(instance_a1) == id(instance_a2)

    # Different classes have different instances
    assert instance_a1 is not instance_b1
    assert id(instance_a1) != id(instance_b1)

    # But same behavior within each class
    assert instance_b1 is instance_b2
    assert id(instance_b1) == id(instance_b2)


def test_reset_method():
    class TestClass(Singleton):
        pass

    # Create and verify singleton
    instance1 = TestClass()
    assert instance1 is TestClass()

    # Reset and verify new instance
    Singleton.reset()
    instance2 = TestClass()
    assert instance2 is not instance1
    assert instance2 is TestClass()


def test_initialization_flag():
    class TestClass(Singleton):
        def __init__(self):
            if self._initialized:
                return
            self.value = 42
            self._initialized = True

    instance1 = TestClass()
    assert hasattr(instance1, 'value')
    assert instance1.value == 42

    # Second instance should not reinitialize
    instance2 = TestClass()
    assert instance2.value == 42
    assert instance1 is instance2


def test_multiple_subclasses():
    class ClassA(Singleton):
        pass

    class ClassB(Singleton):
        pass

    a1 = ClassA()
    a2 = ClassA()
    b1 = ClassB()
    b2 = ClassB()

    assert a1 is a2
    assert b1 is b2
    assert a1 is not b1
    assert ClassA._instances[ClassA] is a1
    assert ClassB._instances[ClassB] is b1


def test_reset_affects_all_subclasses():
    class ClassA(Singleton):
        pass

    class ClassB(Singleton):
        pass

    a1 = ClassA()
    b1 = ClassB()

    Singleton.reset()

    a2 = ClassA()
    b2 = ClassB()

    assert a1 is not a2
    assert b1 is not b2
    assert a2 is ClassA()
    assert b2 is ClassB()


def test_instance_dictionary_management():
    Singleton.reset()
    assert Singleton._instances == {}

    class TestClass(Singleton):
        pass

    instance = TestClass()
    assert TestClass in Singleton._instances
    assert Singleton._instances[TestClass] is instance

    Singleton.reset()
    assert Singleton._instances == {}