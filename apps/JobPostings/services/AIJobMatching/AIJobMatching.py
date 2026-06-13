import random
from ai.llm import LLM
from typing import Dict


class AIJobMatching:
    def __init__(self):
        self.prefix_path = "apps/JobPostings/services/AIJobMatching/"
        self.user_job_pref = self._getFileContent(path="user_job_preference.txt")
        self.system_prompt = self._getFileContent(path="system_prompt.txt")
        self.prompt_template = self._getFileContent(path="ai-job-matching-prompt-template.txt")
        self.llm = LLM(system_prompt=self.system_prompt)

    def getMatchDetails(self, job_details) -> Dict[str, str]:
        """
            Use llm to process job_details with User required job
        """
        prompt = self.prompt_template
        prompt = prompt.replace("<user-job-preference>", self.user_job_pref)
        prompt = prompt.replace("<job-details>", job_details)
        llm_response = self.llm.query(prompt=prompt)
        llm_response = eval(llm_response)
        return llm_response

    def _getFileContent(self, path):
        with open(self.prefix_path + path, mode='r') as f:
            content = f.read()
        return content

