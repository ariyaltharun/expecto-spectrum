import os

from urllib import parse as urllib_parse
from playwright.sync_api import sync_playwright
import time
from apps.JobPostings.services.AIJobMatching.AIJobMatching import AIJobMatching
from utils.logger import getLogger

logger = getLogger(__name__)


class LinkedIn:
    def __init__(self):
        # TODO: This is just for testing, later we can move this to a config file or database
        self.last_x_hrs = 3
        self.search_keyword = "Software Developer"
        # self.companies = ["Amazon", "Google", "Microsoft"]
        self.companies = ["Amazon"]
        self.company_id_mapping = {
            "Amazon": "1586",
            "Cisco": "1063",
            "Meta": "10667",
            "Oracle": "1028",
            "Visa": "2190",
            "Wells Fargo": "1235",
            "Barclays": "1426",
            "Apple": "162479",
            "Nvidia": "3608",
            "Qualcomm": "2017",
            "AMD": "1497",
            "arm": "4472",
            "Google": "1441",
            "HPE": "1025",
            "Nutanix": "735085",
            "Amazon Web Services": "2382910",
            "Microsoft": "1035",
            "Adobe": "1480",
            "NetApp": "2105",
            "Rubrik": "4840301",
            "ServiceNow": "29352",
            "Dell Technologies": "15088102",
            "VMware": "2988",
            "MasterCard": "3015",
            "Goldman Sachs": "1382",
            "JPMorgan Chase": "1068",
            "PhonePe": "10479149",
            "Razorpay": "",
            "American Express": "",
            "Intuit": "",
            "Stripe": "",
            "Paypal": "",
            "Paytm": "",
            "Morgan Stanley": "",
        }
        self.ai_job_matching = AIJobMatching()

    def filterJobPostings(self):
        # Get browser page and login to LinkedIn
        self.page = self.getBrowserPage()
        self.login()
        # Process company wise job postings
        for company in self.companies:
            company_id = self.company_id_mapping[company]
            job_url = self._createJobUrl(company_id)
            logger.info(f"Processing job postings for {company} with URL: {job_url}")
            import json
            data = self.processJobPostings(job_url)
            # Save the fetched data to a json file
            with open(f"{company}_job_postings.json", "w") as f:
                json.dump(data, f, indent=4)

    def getBrowserPage(self):
        logger.info("Setting up browser page using Playwright.")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_navigation_timeout(120000)
        return page

    def login(self):
        logger.info("Logging in to LinkedIn.")
        # Go to linkedin.com and login
        self.page.goto("https://www.linkedin.com/login/")
        logger.info("Waiting for login page to load.")
        time.sleep(30)
        # Enter Creds
        logger.info("Filling in login credentials.")
        email_or_phone = self.page.locator("input[type='email']")
        password = self.page.locator("input[type='password']")
        linkedin_email = os.getenv("LINKEDIN_EMAILID")
        linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        email_or_phone.fill(linkedin_email)
        password.fill(linkedin_password)
        # Click on sign in button
        logger.info("Clicking on sign in button.")
        sign_in = self.page.locator("button[aria-label='Sign in']")
        sign_in.click()
        logger.info("Attempting to log in.")
        time.sleep(10)

    def processJobPostings(self, job_url):
        # Go to the job url and fetch the job postings
        self.page.goto(job_url, timeout=120000, wait_until="domcontentloaded")
        time.sleep(5)

        jobListID = "ul >> nth=6"
        jobDivID = "div[data-job-id]"
        postingData = []
        while True:
            # Code to fetch job postings from the page and process them with llm
            # jobList = await page.locator("div[data-job-id]").all()
            # postingList = self.page.locator(jobListID).locator("li").all() # TODO: This is not the right way, please change
            # print(f"Found {len(postingList)} job postings.")
            # for posting in postingList:
            for jobIndex in range(100):
                # Click on posting to open the job details
                if not self._isJobPostingVisible(self.page, jobIndex, jobListID, jobDivID):
                    logger.info(f"Job at index {jobIndex} is not visible. Scrolling the page a little and waiting for 10 seconds.........")
                    self.page.mouse.wheel(0, 300)
                    time.sleep(5)
                    if not self._isJobPostingVisible(self.page, jobIndex, jobListID, jobDivID):
                        logger.info(f"Job at index {jobIndex} is still not visible after scrolling. Breaking the loop.")
                        break
                posting = self.page.locator(jobListID).locator(jobDivID).nth(jobIndex)
                posting.click()
                logger.info(f"Clicking on job at index {jobIndex}")
                time.sleep(10)
                # Fetch Job Details
                job_details = self._extractJobDetails(self.page)
                logger.info(f"Fetched details for job at index {jobIndex}: {job_details['title']}")
                # Append the fetched data to postingData list
                job_match_details = self.ai_job_matching.getMatchDetails(job_details=str(job_details))
                if job_match_details["is_match"]:
                    job_details["reason_for_match"] = job_match_details["reason_for_match"]
                    postingData.append(job_details)
                    logger.info(f"Job Matched hurray!!!: {str(job_details)}")
                else:
                    logger.info(f"Job did not match with user preferences: {str(job_details)}")
            # Click on Next button in pagination section
            # If no next button in pagination section, break the while loop
            if not self._navigateToNextPage(self.page):
                break
            logger.info("Navigated to the next page of job postings. Waiting for 10 seconds.........")
            time.sleep(10)
        return postingData

    def _createJobUrl(self, company_id):
        base_url = "https://www.linkedin.com/jobs/search/?"
        urlParams = {
            "keywords": self.search_keyword, # Search keyword
            "f_C": company_id, # Companies
            # "geoId": "90009633", # Geo ID
            # "distance": "25", # Distance
            "f_TPR": f"r{self.last_x_hrs * 3600}", # Time posted range (last X hours)
        }
        encode_url_params = urllib_parse.urlencode(urlParams, quote_via=urllib_parse.quote)
        full_url = base_url + encode_url_params
        return full_url

    def _isJobPostingVisible(self, browser_page, jobIndex, jobListID="ul >> nth=6", jobDivID="div[data-job-id]"):
        is_job_posting_visible = browser_page.locator(jobListID).locator(jobDivID).nth(jobIndex).is_visible()
        return is_job_posting_visible

    def _extractJobDetails(self, browser_page):
        # Fetch job title, location, description and other details from the posting
        ## Fetch job title
        jobTitleID = ".job-details-jobs-unified-top-card__job-title a"
        jobTitle = browser_page.locator(jobTitleID).inner_text()
        ## Fetch job location
        jobLocationID = ".job-details-jobs-unified-top-card__tertiary-description-container"
        jobLocation = browser_page.locator(jobLocationID).inner_text()
        jobLocation = jobLocation.split("·")[0].strip()
        ## Fetch job description
        jobDescriptionID = "#job-details"
        jobDescription = browser_page.locator(jobDescriptionID).inner_text()
        return {
            "title": jobTitle,
            "location": jobLocation,
            "description": jobDescription
        }

    def _navigateToNextPage(self, browser_page):
        # Check if there is a next page in pagination section
        nextButtonID = "button[aria-label='View next page']"
        nextButton = browser_page.locator(nextButtonID)
        if len(nextButton.all()) > 0 and nextButton.is_enabled():
            nextButton.click()
            return True
        return False
