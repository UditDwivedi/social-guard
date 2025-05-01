from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)
 
def trans(a):
    con = """You are an advanced language model capable of understanding and translating multiple languages. 
    Your task is to translate the provided text into English. Do not provide context or explanations. 
    Only return the translated text, and ensure it is clear, accurate, and concise.
    just only translated text
    The text to translate is as follows:
    """ + str(a)

    completion = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct-v0.3",
    messages=[{"role":"user","content":con}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True
    )
    ss=""

    for chunk in completion:
     if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
        ss+=chunk.choices[0].delta.content
    return ss
