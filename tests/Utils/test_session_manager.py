import pytest

from PirateEase.Utils.session_manager import SessionManager
from PirateEase.Utils.singleton import Singleton

@pytest.fixture
def session():
    Singleton.reset()
    return SessionManager()

def test_singleton_behavior():
    """Test that only one instance exists"""
    instance1 = SessionManager()
    instance2 = SessionManager()

    assert instance1 is instance2
    assert id(instance1) == id(instance2)


def test_initial_state(session):
    assert session.state == {}
    assert session.history == []


def test_state_management(session):
    # Test setting and getting values
    session.set("user_id", "123")
    assert session.get("user_id") == "123"
    assert "user_id" in session

    # Test default value
    assert session.get("nonexistent", "default") == "default"
    assert "nonexistent" not in session


def test_history_management(session):
    session.append_history("Hello")
    session.append_history("How can I help?")

    assert session.history == ["Hello", "How can I help?"]


def test_multiple_operations(session):
    # Set some state
    session.set("order_id", "ORD123")
    session.set("customer", "John Doe")

    # Add to history
    session.append_history("Order placed")
    session.append_history("Payment processed")

    # Verify state
    assert session.get("order_id") == "ORD123"
    assert session.get("customer") == "John Doe"
    assert "order_id" in session

    # Verify history
    assert len(session.history) == 2
    assert "Order placed" in session.history
    assert "Payment processed" in session.history


def test_edge_cases(session):
    # Test empty string
    session.set("empty", "")
    assert session.get("empty") == ""

    # Test None value
    session.set("none", None)
    assert session.get("none") is None

    # Test empty history append
    session.append_history("")
    assert session.history[-1] == ""


def test_reinitialization(session):
    session1 = session
    session1.set("test", "value")
    session1.append_history("message")

    session2 = SessionManager()

    # Verify state and history persist
    assert session2.get("test") == "value"
    assert session2.history == ["message"]