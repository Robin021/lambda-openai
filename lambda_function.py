from openai import OpenAI
import json
import datetime
import boto3
from botocore.exceptions import ClientError



def get_openai_api():

    secret_name = "chatgpt-personal-openai"
    region_name = "us-west-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret_string = get_secret_value_response['SecretString']
    # Parse the JSON string to get the secret value
    secret_dict = json.loads(secret_string)
    secret_key = secret_dict['chatgpt-personal-openai']

    return secret_key

# openai.api_key = get_openai_api()
def lambda_handler(event, context):
    '''Provide an event that contains the following keys:
      - prompt: text of an open ai prompt
    '''
    prompt = event['prompt']
        # Diagnose API Key accessibility
    api_key = get_openai_api() # First element of the list is the API key
    print("sssss" + api_key)
    if not api_key:
            raise ValueError("OpenAI API key not found in environment variables.")
    client = OpenAI(api_key=api_key)
    # Create chat 
    messages = [{"role": "user", "content": prompt}]
    completion = client.chat.completions.create(model="gpt-4o",messages=messages ,max_tokens=250)
    response = completion.choices[0].message.content

    return {
        "statusCode": 200,
        "body": json.dumps({"response": response})}
    # print("call time: {}, event: {}".format(datetime.datetime.now(),event))
    # response = openai.Completion.create(model="text-davinci-003", prompt=event['prompt'], temperature=0.6)
    # return (response.choices[0].text)
