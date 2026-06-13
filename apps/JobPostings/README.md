# Job Postings App:

Fetch posting from multiple job boards

Here is the flow:
- For each job posting in job boards:
- Extract details (Job Title, Location, JD, Experience)
- Compare Job Details with user required preference with the help of llm
- If there is a match, put this jobPosting in jobQueue


ResumeGeneration:
- Must pick the job from jobQueue
- And prepare resume for this posting and present this job to user with resume
