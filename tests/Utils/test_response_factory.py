import pytest
from PirateEase.Utils.response_factory import ResponseFactory

responses: dict[str, list[str]] = ResponseFactory.responses

@pytest.mark.parametrize("category", responses.keys())
def test_valid_category(category):
    for _ in range(20):
        response: str = ResponseFactory.get_response(category)
        assert response in responses[category]

def test_invalid_category():
    with pytest.raises(KeyError):
        ResponseFactory.get_response("non_existent_category")

