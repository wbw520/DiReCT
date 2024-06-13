from openai import AzureOpenAI, OpenAI
import os


def AskChatGPT(input_template, temperature, model_engine, api_key):
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
        model=model_engine,
        temperature=temperature,
        top_p=1,
        stop=None
    )
    return response


def AskGPTCompany(input_template, temperature, api_key):
    # #gpt3.5
    # client_gpt=AzureOpenAI(api_key=api_key,
    #                    azure_endpoint = "https://cog-42bbrearckery.openai.azure.com/",
    #                   api_version="2023-05-15")
    #
    # response = client_gpt.chat.completions.create(
    #     model="chat",  # for gpt3.5 use chat, gpt4 use gpt4 as model
    #     messages=[
    #             {
    #                 "role": "user",
    #                 "content": input_template,
    #             }
    #         ],
    #     temperature=temperature,
    #     top_p=1,
    #     stop=None)


    #gpt4
    client_gpt4 = AzureOpenAI(api_key=api_key,
                       azure_endpoint = "https://wbw520520.openai.azure.com/",
                      api_version="2024-02-15-preview")

    response = client_gpt4.chat.completions.create(
        model="gpt-4-32k",
        messages=[
            {
                "role": "user",
                "content": input_template,
            }
        ],
        temperature=temperature,
        top_p=1,
        stop=None)

    return response

#
# tempp = "Please tell me the name of apple's current CEO."
#
# # res = AskGPTCompany(tempp, temperature=0)
# res = AskChatGPT(tempp, temperature=0, model_engine="gpt-4")
# print(res.choices[0].message.content)