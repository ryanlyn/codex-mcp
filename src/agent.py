import os

os.environ["ANONYMIZED_TELEMETRY"] = "false"

from browser_use import Agent, AgentHistoryList, BrowserSession
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from .browser import BrowserConnection


def get_default_llm():
    llm = ChatOpenAI(model="gpt-4.1")
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
        agent = Agent(browser_session=browser_session, llm=self.llm, task=prompt, use_vision=True)
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

    async def do(self, prompt: str) -> str:
        instruction = f"""
        {self.navigate_to(self.BASE_URL)}.
        {prompt}
        === Creating tasks ===
        The main codex input field is what you should use to create new tasks.
        Tasks are created by typing in the input field and pressing the 'Code' button.
        The task is created when the task is visible in the list of recent codex tasks.
        There is one button in the footer of the main input field called that includes 'code environments'.
        That button can be used to select the environment to use for the task.
        There is also another button in main input footer with 'branch'.
        That button is used to search for branches for the tasks to start from.
        If no branch is specified, use 'main' as the branch.

        === Creating or updating environments ===
        There are a few buttons in the header of the main codex page.
        The environments button opens the environments setting page where you can create or update environments.
        When creating a new environment, use the repository name as the environment name.
        When updating an environment, do not change the repository or the environment name.
        Press the 'Save' button to finalise the create or update.
        Do not in any circumstances delete an environment.
        """
        result = await self.execute_instruction(prompt=instruction)
        return result

    def navigate_to(self, url: str) -> str:
        return f"Navigate to {url} if you are not already there"
