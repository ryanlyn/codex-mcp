from browser_use import Agent, BrowserSession
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def get_default_llm():
    llm = ChatOpenAI(model="gpt-4o")
    return llm


class CodexAgent:
    browser_session: BrowserSession
    llm: BaseChatModel
    verbose: bool

    def __init__(self, browser_session: BrowserSession, llm: BaseChatModel | None = None, verbose: bool = False):
        self.browser_session = browser_session
        self.llm = llm or get_default_llm()
        self.verbose = verbose

    async def execute_instruction(self, prompt: str) -> str:
        agent = Agent(
            llm=self.llm,
            browser_session=self.browser_session,
            verbose=self.verbose,
        )
        result = await agent.run(prompt)
        return result
