import os

os.environ["ANONYMIZED_TELEMETRY"] = "false"

from browser_use import Agent, AgentHistoryList, BrowserSession
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .browser import BrowserConnection


def get_default_llm():
    llm = ChatOpenAI(model="gpt-4o")
    return llm


class BrowserAgent:
    browser_connection: BrowserConnection
    llm: BaseChatModel
    verbose: bool
    # reuse a single browser session for all agents
    browser_session: BrowserSession | None = None

    def __init__(
        self,
        browser_connection: BrowserConnection,
        llm: BaseChatModel | None = None,
        verbose: bool = False,
    ):
        self.browser_connection = browser_connection
        self.llm = llm or get_default_llm()
        self.verbose = verbose

    async def execute_instruction(self, prompt: str) -> str:
        browser_session = self.get_browser_session()
        agent = Agent(browser_session=browser_session, llm=self.llm, task=prompt)
        history: AgentHistoryList = await agent.run()
        final_result = str(history.final_result()) if hasattr(history, "final_result") else str(history)
        return final_result

    def get_browser_session(self) -> BrowserSession:
        if self.browser_session:
            return self.browser_session

        self.browser_session = BrowserSession(
            cdp_url=self.browser_connection.base_url,
            headless=False,
            keep_alive=True,
        )
        return self.browser_session


class CodexAgent(BrowserAgent):
    BASE_URL = "https://chatgpt.com/codex"
    ENVIRONMENT_URL = f"{BASE_URL}/settings/environments"

    def __init__(
        self,
        browser_connection: BrowserConnection,
        llm: BaseChatModel | None = None,
        verbose: bool = False,
    ):
        super().__init__(browser_connection, llm, verbose)

    async def wait_until_logged_in(self):
        instruction = f"""
        {self.navigate_to(self.BASE_URL)}.
        Wait until the user is logged in to the website.
        The task is completed when the user is logged in and the list of recent codex tasks is visible.
        """

        result = await self.execute_instruction(prompt=instruction)
        return result

    def navigate_to(self, url: str) -> str:
        return f"Navigate to {url} if you are not already there"
