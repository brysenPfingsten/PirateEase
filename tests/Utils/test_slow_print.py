from unittest.mock import patch, call
from PirateEase.Utils.slow_print import slow_print


def test_slow_print_output():
    test_string = "Hello"

    with patch('builtins.print') as mock_print:
        with patch('time.sleep'):
            slow_print(test_string)

    # Verify each character was printed individually
    char_calls = [call(c, end='', flush=True) for c in test_string]
    mock_print.assert_has_calls(char_calls)

    # Verify final newline
    mock_print.assert_called_with()


def test_slow_print_delay():
    test_string = "Test"
    test_delay = 0.05

    with patch('builtins.print'):
        with patch('time.sleep') as mock_sleep:
            slow_print(test_string, test_delay)

    # Verify correct number of sleep calls
    assert mock_sleep.call_count == len(test_string)

    # Verify each sleep used the correct delay
    for call_args in mock_sleep.call_args_list:
        assert call_args == call(test_delay)


def test_slow_print_empty_string():
    with patch('builtins.print') as mock_print:
        with patch('time.sleep'):
            slow_print("")

    # Should only print the final newline
    mock_print.assert_called_once_with()


def test_slow_print_custom_delay():
    test_string = "ABC"
    custom_delay = 0.1

    with patch('builtins.print'):
        with patch('time.sleep') as mock_sleep:
            slow_print(test_string, custom_delay)

    # Verify correct number of sleep calls with custom delay
    assert mock_sleep.call_count == len(test_string)
    for call_args in mock_sleep.call_args_list:
        assert call_args == call(custom_delay)


def test_slow_print_special_characters():
    test_string = "a\nb\tc"

    with patch('builtins.print') as mock_print:
        with patch('time.sleep'):
            slow_print(test_string)

    # Verify each character was printed, including special chars
    char_calls = [call(c, end='', flush=True) for c in test_string]
    mock_print.assert_has_calls(char_calls)
    mock_print.assert_called_with()