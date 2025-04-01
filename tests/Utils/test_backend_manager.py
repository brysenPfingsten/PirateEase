import pytest
from PirateEase.Utils.backend_manager import BackendManager

def test_process_request_order(mocker):
    mock_order_service = mocker.patch("PirateEase.Utils.backend_manager.OrderService")
    mock_instance = mock_order_service.return_value
    mock_instance.retrieve_order.return_value = "Order Details"

    result = BackendManager.process_request("order", "order123")

    mock_order_service.assert_called_once()
    mock_instance.retrieve_order.assert_called_once_with("order123")
    assert result == "Order Details"

def test_process_request_refund(mocker):
    mock_refund_service = mocker.patch("PirateEase.Utils.backend_manager.RefundService")
    mock_instance = mock_refund_service.return_value
    mock_instance.refund_past_order.return_value = "Refund Processed"

    result = BackendManager.process_request("refund", "refund456")

    mock_refund_service.assert_called_once()
    mock_instance.refund_past_order.assert_called_once_with("refund456")
    assert result == "Refund Processed"

def test_process_request_inventory(mocker):
    mock_inventory_service = mocker.patch("PirateEase.Utils.backend_manager.InventoryService")
    mock_instance = mock_inventory_service.return_value
    mock_instance.check_availability.return_value = "In Stock"

    result = BackendManager.process_request("inventory", "item789")

    mock_inventory_service.assert_called_once()
    mock_instance.check_availability.assert_called_once_with("item789")
    assert result == "In Stock"

def test_process_request_agent(mocker):
    mock_agent_service = mocker.patch("PirateEase.Utils.backend_manager.LiveAgentService")
    mock_instance = mock_agent_service.return_value
    mock_instance.get_available_agent.return_value = "Agent Connected"

    result = BackendManager.process_request("agent")

    mock_agent_service.assert_called_once()
    mock_instance.get_available_agent.assert_called_once()
    assert result == "Agent Connected"

def test_process_request_exit(mocker):
    mock_exit_service = mocker.patch("PirateEase.Utils.backend_manager.ExitService")
    mock_instance = mock_exit_service.return_value
    mock_instance.get_exit_response.return_value = "Goodbye"

    result = BackendManager.process_request("exit")

    mock_exit_service.assert_called_once()
    mock_instance.get_exit_response.assert_called_once()
    assert result == "Goodbye"

def test_process_request_invalid_type():
    result = BackendManager.process_request("invalid_type", "data")
    assert result is None

def test_backend_manager_is_singleton():
    assert BackendManager() is BackendManager()