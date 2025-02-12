from celery import shared_task
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import Job
from celery.schedules import crontab

# Defining the Celery task for scraping jobs
@shared_task
def scrape_jobs():
    # URL to scrape job data from
    url = 'https://jobvision.ir/jobs/keyword/python%20developer'

    # Path to the Chrome driver (update the path as per your system)
    driver_path = r"C:\chromedriver-win64\chromedriver.exe"
    
    # Create Chrome options for headless browsing (no UI)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Set up the Chrome driver service
    service = Service(driver_path)

    # Launch the Chrome browser with the options and service
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the specified URL
    driver.get(url)
    
    # Get the page source (HTML) after it loads
    page_source = driver.page_source
    
    # Parse the page using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all the job cards on the page by their class
    job_cards = soup.find_all('job-card', {'class': 'col-12 row cursor px-0 ng-star-inserted'})

    # Initialize lists to store the job data
    company_name_list = []
    titles_list = []
    link_list = []

    # Loop through each job card to extract the relevant data
    for card in job_cards:
        # Find all the job post links
        all_links = card.find_all('a', {'class': 'col-12 row align-items-start rounded pt-3 px-0 mb-3 mb-md-2 position-relative bg-white mobile-job-card shadow-sm pb-3'})
        link_list.extend([link.get('href') for link in all_links if link.get('href')])
        
        # Find all the job titles
        all_titles = card.find_all('div', {'class': 'job-card-title w-100 font-weight-bolder text-black px-0 pl-4 line-height-24'})
        titles_list.extend([title.get_text(strip=True) for title in all_titles])
        
        # Find all the company names
        all_company_name = card.find_all('a', {'class': 'text-black line-height-24 pointer-events-none'})
        company_name_list.extend([name.get_text(strip=True) for name in all_company_name])

    # Combine the job titles, company names, and links into tuples, and slice the data to get specific entries (19 to 29)
    zipped_data = list(zip(titles_list, company_name_list, link_list))[0:10]

    # Loop through the zipped data to check if the job already exists in the database, if not, create a new job entry
    jobs = []
    for title, name, link in zipped_data:
        if not Job.objects.filter(title=title, company_name=name).exists():
            Job.objects.create(
                title=title,
                company_name=name,
                link='https://jobvision.ir' + link  # Add the base URL to the job link to have a compelete link
            )
    
    # Retrieve all job entries from the database
    jobs = Job.objects.all()

    # Print a message when the scraping is complete
    print('Job scraping completed')
