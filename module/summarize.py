from module import genai
# import genai

summarizer_prompt = '''
You are Video summarizer which focuses on the important details in less than 200 words. 
You need to get 2-4 tags about the content which it targets.
Your response needs to follow the format:
space,planets,size<EndOfTags>Among the solar planets in space, Jupiter is the largest.
Text to Summarize:
'''

test_content1 = '''
If you want to understand what is pollution, what is the polutant, what is water pollution, what is air pollution, what is a land pollution, then definitely watch this video till the end. Pollution means that any of us we full material comes in our environment and it causes damage to the environment, then it is called pollution and it is called polutant that we are full material when it is mixed with full, material water, then it is called water pollution when it is a water pollution with a water pollution when it is mixed with full, material water. When he is mixed with Ham Full, Material Land, it is called Land Pollution, then these were some things about the pollution thank you so much, focus four watching this video til de and end.'''

test_content2 = '''
the other space was around Computing resources so how much Compu resources um you know AI requires if you're kind of going to go and do that you know uh sort of AI infrastructures a service you know sort of thing yourself uh we've seen uh various articles from you know Microsoft um uh looking at you using uh small modular reactors nuclear reactors smrs uh for future hyperscale data centers um advertising for things like power managers or nuclear power managers um kind of job address going up I think I'll cover some of this in the um class state of play as well so I'll maybe try to include some uh links to that uh their ignite event last year they announced their Maya accelerator accelerators same thing really with Google and Amazon with q and bedro and and various other things
'''
def summarize(content:str) -> list[str]:
    print("summarizing")
    print()
    response = genai.ask(f"{summarizer_prompt}{content}")

    return response.split('<EndOfTags>')

if __name__ == "__main__":
    print(genai.ask(f"{summarizer_prompt}{test_content2}"))
