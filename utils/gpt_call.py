from openai import AzureOpenAI, OpenAI
import os


def AskChatGPT(input_template, model, api_key, temperature=0, top_p=1):
    os.environ['OPENAI_API_KEY'] = api_key
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_template,
            }
        ],
        model=model,
        temperature=temperature,
        top_p=top_p,
        stop=None
    )
    return response


def AskGPTAzure(input_template, api_key, azure_endpoint, api_version, model, temperature=0, top_p=1):
    client = AzureOpenAI(api_key=api_key,
                       azure_endpoint=azure_endpoint,
                      api_version=api_version)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": input_template,
            }
        ],
        temperature=temperature,
        top_p=top_p,
        stop=None)

    return response