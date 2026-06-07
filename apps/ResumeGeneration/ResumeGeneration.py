from ai.llm import LLM


class ResumeGeneration:
    def __init__(self):
        self.prefix_path = "apps/ResumeCreation/"
        system_prompt = self._getFileContent(path="system-prompt.txt")
        # Init llm with system prompt
        self.llm = LLM(
            system_prompt=system_prompt
        )

    def generate(self):
        prompt = self._getResumePrompt()
        self._writeContent(path="generated-resume.tex", content=prompt)
        # llm_response = self.llm.query(request)

    def _getResumePrompt(self):
        prompt_template = self._getFileContent(path="resume-prompt-template.txt")
        resume_template = self._getFileContent(path="resume-template.tex")
        user_info = self._getFileContent(path="user-info.md")
        print("generating resume...")
        # Replace replacable content in prompt_template

        prompt = prompt_template
        # replace resume template tex
        prompt = prompt.replace("<resume-template>", resume_template)
        # replace user-info
        prompt = prompt.replace("<user-info>", user_info)
        # replace job description
        prompt = prompt.replace("<job-description>", "Job Needs you to die and go to hell")
        return prompt

    def _getFileContent(self, path):
        with open(self.prefix_path + path, "r") as f:
            content = f.read()
        return content

    def _writeContent(self, path, content):
        with open(self.prefix_path + path, "w") as f:
            f.write(content)
        return None
