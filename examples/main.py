from patient_access_utils.token_maker import token_maker
	
if __name__ == "__main__":
	jwt_token = token_maker()
	print("jwt_token: ", jwt_token)