# Job Scraper Application

## Overview:
This web scraping application, built with Python and Django, is designed to scrape job listings from **JobVision**, a popular job portal website. The application fetches the first 10 job listings, including the company name, job position, and job link. This project is an example of how web scraping and automation can be implemented using Python tools and frameworks.

### Key Features:
- **Job Scraping**: The app scrapes the first 10 job listings (this can be customized in `crawler.py`).
- **Search Functionality**: A search bar allows users to search job listings by company name or job title.
- **Job Listing Details**: Clicking on a button redirects users to the individual job page with full details.
- **Back to Home**: Clicking the "Back to Home" button redirects users to the main job listings page.
- **Automatic Updates**: Job listings are automatically updated every midnight using **Celery** to ensure fresh data.
- **Image Storage**: All images related to the app are stored in the **APP PICTURE** folder.
- **User-friendly Interface**: Simple and intuitive UI to browse and search job listings easily.

### Technologies Used:
- **Selenium**: Used for web scraping and automating browser interactions.
- **BeautifulSoup**: Used for parsing HTML and extracting job listing data.
- **Celery**: For scheduling automatic job scraping at midnight.
- **Django**: Web framework used for building the application and serving it as a web app.

### Customization:
- Ensure the necessary configurations and directories are set up on your system for the app to function correctly. Specifically, you need to configure the `crawler.py` file for scraping the correct job listings and adjust settings like the scraping interval.

### Running the Application:
To run the application, follow these steps:

1. Clone the repository or download the application files.
2. Install the required dependencies by running:
   `pip install -r requirements.txt`

3. To start the application, run:
   `python run.py`
   

### Requirements:
The required dependencies are listed in the `requirements.txt` file. Ensure to install all the necessary packages by running the command mentioned above.



### WITHOUT A DOUBT, TOOLS LIKE CHATGPT AND OTHERS HAVE BEEN USED IN THE DEVELOPMENT OF THIS APP.

