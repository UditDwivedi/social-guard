# from openai import OpenAI

# client = OpenAI(
#   base_url = "https://integrate.api.nvidia.com/v1",
#   api_key = "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"
# )

# def validator(transcribed_text,user_content):

#     a=prompt = (
#         "You are an AI tasked with analyzing and evaluating content alignment. Below are summaries of a YouTube video transcription and a news article on a similar topic. "
#         "Your tasks are:\n"
#         "1. Compare the two summaries and identify key similarities, differences, and discrepancies.\n"
#         "2. Assess the overall accuracy of the YouTube video summary based on the news article summary.\n"
#         "3. You can Your understand also .\n"
#         "4. Provide your evaluation as one of the following:\n"
#         "   - **Green**: The YouTube video summary aligns well with the news article summary.\n"
#         "   - **Yellow**: The YouTube video summary is misses some key points or includes minor discrepancies.\n"
#         "   - **Red**: The YouTube video summary contains major inaccuracies or contradictions with the news article summary.\n"
#         "Only respond with Green, Blue, or Red, without any explanation..\n\n"
#         "Here are the inputs:\n\n"
#         f"YouTube Video Summary:\n\"{str(transcribed_text)}\"\n\n"
#         f"News Article Summary:\n\"{str(user_content)}\""
#     )
#     completion = client.chat.completions.create(
#         model="meta/llama3-70b-instruct",
#         messages=[{"role":"user","content":a}],
#         temperature=0.5,
#         top_p=1,
#         max_tokens=1024,
#         stream=True
#     )
#     stt=""
#     for chunk in completion:
#         if chunk.choices[0].delta.content is not None:
            
#             print(chunk.choices[0].delta.content, end="")
#             stt+=chunk.choices[0].delta.content

#     return stt

from module import genai

identifier_prompt = '''
You are an Verifier tasked with analyzing and evaluating content alignment. Below are summaries of a YouTube video transcription and a news article on a similar topic. 
#         Your tasks are:
#         0. If the Video summary is about common general fact (not a social, political, religous, etc event or saying), evalute the video summary only with your knowledge and majorly ignore the news summary.
#         1. Compare the two summaries and identify key similarities, differences, and discrepancies.
#         2. Assess the overall accuracy of the YouTube video summary based on the news article summary.
#         3. You can Your understand also .
#         4. Provide your evaluation as one of the following:
#            - **Green**: The YouTube video summary aligns well with the news article summary or actual facts.
#            - **Yellow**: The YouTube video summary is misses some key points or includes minor discrepancies.
#            - **Red**: The YouTube video summary contains major inaccuracies or contradictions with the news article summary or actual facts.
#         Only respond with Green, Blue, or Red, without any explanation..
#         Here are the inputs:
'''

def validator(video_summary:str, news_summary) -> str:
    print("Validating")
    print()
    response = genai.ask(f"{identifier_prompt}\nVideo Summary:{video_summary}\nNews Summary:{news_summary}")

    return response

# if __name__ == "__main__":
#     print(genai.ask(f"{summarizer_prompt}{test_content}"))