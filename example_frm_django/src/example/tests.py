import pytest
from src.example.models import Example

@pytest.mark.django_db
def test_check_db():
    Example.objects.create(name="123")

