import pytest
from patient_access_utils.token_maker import token_maker

def test_token_maker():
	jwt_token = token_maker()
	assert jwt_token is not None
