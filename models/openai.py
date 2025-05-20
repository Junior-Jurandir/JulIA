from langchain_openai import ChatOpenAI


def model_openai(model="gpt-4o-mini", temperature=0.1):
    llm = ChatOpenAI(model=model, temperature=temperature)
    return llm
