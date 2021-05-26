import json, jwt, pem, boto3, time, traceback

region_name = "us-east-1"
commonwell_secrets = "ecdr-dev-commonwell-secrets"
commonwell_creds = "commonwell-creds"

def get_secret(secret_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name)

    try:
        resp = client.get_secret_value(
            SecretId=secret_name)
        return resp['SecretString']
    except:
        return "Failed to get secrets. Error: " + traceback.format_exc()

def token_maker():
    # Get commonwell secrets
    secret_str = get_secret(commonwell_secrets)
    secret = json.loads(secret_str)
    
    # Declare "nbf" (not before) & "exp" (expiration time)
    # The duration between the “exp” and the “nbf” claims cannot be more than eight (8) hours.
    current_time = int(time.time()) 
    expiration_time = current_time + 8 * 60 * 60

    # Construct payload
    payload = {
        "iss": "self",
        "aud": "urn:commonwellalliance.org",
        "nbf": current_time,
        "exp": expiration_time,
        "urn:oasis:names:tc:xacml:2.0:subject:role": secret['subject_role_code'],
        "urn:oasis:names:tc:xspa:1.0:subject:subject-id": secret['subject_name'],
        "urn:oasis:names:tc:xspa:1.0:subject:organization": secret['ecdr_organization_name'],
        "urn:oasis:names:tc:xspa:1.0:subject:organization-id": secret['ecdr_organization_id'],
        "urn:oasis:names:tc:xspa:1.0:subject:purposeofuse": secret['purpose_of_use_code']}

    # Get private key
    creds_str = get_secret(commonwell_creds)
    creds = json.loads(creds_str)
    private_key_str = creds['private_key']
    delimiter_begin = "-----BEGIN RSA PRIVATE KEY-----"
    delimiter_end = "-----END RSA PRIVATE KEY-----"
    key_body = private_key_str.replace(delimiter_begin, "").replace(delimiter_end, "").replace(" ", "\n")
    private_key = delimiter_begin + key_body +  delimiter_end
    
    # Encode a token with RS256
    token = jwt.encode(payload, private_key, algorithm="RS256")
    return token