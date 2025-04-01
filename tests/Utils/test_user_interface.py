import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from PirateEase.Utils.user_interface import UserInterface

@pytest.fixture
def mock_dependencies():
    """Fixture to mock all external dependencies"""
    with patch('PirateEase.Utils.user_interface.ResponseFactory') as mock_factory, \
            patch('PirateEase.Utils.user_interface.slow_print'), \
            patch('PirateEase.Utils.user_interface.SessionManager') as mock_session_manager, \
            patch('builtins.input'):
        # Configure mock ResponseFactory
        mock_factory.get_response.side_effect = lambda x: {
            'order_id': 'Please enter your order ID: ',
            'invalid_order_id': 'Invalid order ID!',
            'product': 'Which product are you looking for? ',
            'refund_reason': 'Why are you requesting a refund? '
        }.get(x, '')

        # Create a mock session instance
        mock_session_instance = MagicMock()
        mock_session_manager.return_value = mock_session_instance

        # Patch the class-level session attribute directly
        with patch.object(UserInterface, 'session', new_callable=PropertyMock) as mock_session_prop:
            mock_session_prop.return_value = mock_session_instance
            yield mock_factory, mock_session_instance


def test_get_order_id_valid(mock_dependencies):
    """Test get_order_id with valid numeric input"""
    mock_factory, mock_session = mock_dependencies

    # Configure input to return valid order ID
    with patch('builtins.input', return_value='12345'):
        result = UserInterface.get_order_id('order_id')

    # Verify result
    assert result == '12345'

    # Verify session history
    calls = mock_session.append_history.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0].startswith('PirateEase: Please enter your order ID:')
    assert calls[1][0][0] == 'User: 12345'


def test_get_order_id_invalid_then_valid(mock_dependencies):
    mock_factory, mock_session = mock_dependencies

    # Configure input to first return invalid then valid order ID
    with patch('builtins.input', side_effect=['invalid', '54321']):
        result = UserInterface.get_order_id('order_id')

    # Verify result
    assert result == '54321'

    # Verify session history
    calls = mock_session.append_history.call_args_list
    assert len(calls) == 5  # prompt + invalid input + error + prompt + valid input
    assert calls[0][0][0].startswith('PirateEase: Please enter your order ID:')
    assert calls[1][0][0] == 'User: invalid'
    assert calls[2][0][0] == 'Invalid order ID!'
    assert calls[3][0][0] == 'PirateEase: Please enter your order ID: '
    assert calls[4][0][0] == 'User: 54321'


def test_get_item_name(mock_dependencies):
    """Test get_item_name with normal input"""
    mock_factory, mock_session = mock_dependencies

    test_item = 'Golden Compass'
    with patch('builtins.input', return_value=test_item):
        result = UserInterface.get_item_name()

    assert result == test_item

    # Verify session history
    calls = mock_session.append_history.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0] == 'PirateEase: Which product are you looking for? '
    assert calls[1][0][0] == f'User: {test_item}'


def test_get_refund_reason(mock_dependencies):
    """Test get_refund_reason with normal input"""
    mock_factory, mock_session = mock_dependencies

    test_reason = 'Item arrived damaged'
    with patch('builtins.input', return_value=test_reason):
        result = UserInterface.get_refund_reason()

    assert result == test_reason

    # Verify session history
    calls = mock_session.append_history.call_args_list
    assert len(calls) == 2
    assert calls[0][0][0] == 'PirateEase: Why are you requesting a refund? '
    assert calls[1][0][0] == f'User: {test_reason}'


def test_empty_input_handling(mock_dependencies):
    """Test handling of empty/whitespace input"""
    mock_factory, mock_session = mock_dependencies

    # Test empty input for item name
    with patch('builtins.input', return_value='  '):
        result = UserInterface.get_item_name()

    assert result == ''  # .strip() removes whitespace

    # Verify empty input was recorded
    calls = mock_session.append_history.call_args_list
    assert calls[1][0][0] == 'User: '