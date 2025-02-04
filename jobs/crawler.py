from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
from .models import Job


def scrape_jobs():
    # Define the URL to scrape job data from
    url = 'https://jobvision.ir/jobs/keyword/python%20developer'

    # Set the path for the Chrome driver
    driver_path = r"C:\chromedriver-win64\chromedriver.exe"
    
    # Create Chrome options to run the browser in headless mode (no UI)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    
    # Set up the Chrome driver service
    service = Service(driver_path)

    # Launch the Chrome browser with the specified options
    driver = webdriver.Chrome(service=service, options=options)
    
    # Open the URL in the browser
    driver.get(url)
    
    # Get the page source (HTML) after it loads
    page_source = driver.page_source
    
    # Use BeautifulSoup to parse the page source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all job cards on the page using the appropriate HTML class
    job_cards = soup.find_all('job-card', {'class': 'col-12 row cursor px-0 ng-star-inserted'})

    # Lists to store the scraped data
    company_name_list = []
    titles_list = []
    link_list = []

    # Loop through each job card and extract the relevant data
    for card in job_cards:
        # Find all the links for job posts
        all_links = card.find_all('a', {'class': 'col-12 row align-items-start rounded pt-3 px-0 mb-3 mb-md-2 position-relative bg-white mobile-job-card shadow-sm pb-3'})
        link_list.extend([link.get('href') for link in all_links if link.get('href')])
        
        # Find all the job titles
        all_titles = card.find_all('div', {'class': 'job-card-title w-100 font-weight-bolder text-black px-0 pl-4 line-height-24'})
        titles_list.extend([title.get_text(strip=True) for title in all_titles])
        
        # Find all the company names
        all_company_name = card.find_all('a', {'class': 'text-black line-height-24 pointer-events-none'})
        company_name_list.extend([name.get_text(strip=True) for name in all_company_name])

    # Combine the job titles, company names, and links into tuples, slice the data to get specific entries (19 to 29) you can change it to get all the cards
    zipped_data = list(zip(titles_list, company_name_list, link_list))[19:29]

    jobs = []
    # For each job entry, check if it already exists in the database, if not, create a new job entry
    for title, name, link in zipped_data:
        if not Job.objects.filter(title=title, company_name=name).exists():
            Job.objects.create(
                title=title,
                company_name=name,
                link='https://jobvision.ir' + link  # Append the base URL to the link to make a compelete link
            )
    
    # Retrieve all job entries from the database
    jobs = Job.objects.all()
    
    # Return the list of jobs
    return jobs
