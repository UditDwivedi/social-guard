from openai import OpenAI

client = OpenAI(
  base_url = "https://integrate.api.nvidia.com/v1",
  api_key = "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"
)
 
def sumup(a):
    con="summarize\n"+str(a)

    completion = client.chat.completions.create(
    model="mistralai/mistral-7b-instruct-v0.3",
    messages=[{"role":"user","content":con}],
    temperature=0.2,
    top_p=0.7,
    max_tokens=1024,
    stream=True
    )
    s=""

    for chunk in completion:
     if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
        s+=chunk.choices[0].delta.content
    return s
