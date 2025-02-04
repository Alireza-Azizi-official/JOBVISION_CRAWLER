from django.shortcuts import render
from .crawler import scrape_jobs  
from .models import Job  

# Define the view function to display the list of jobs
def job_list(request):
    # Call the scrape_jobs function to scrape job data from the website
    scrape_jobs()  
    
    # Retrieve all the job entries from the database
    jobs = Job.objects.all()
    
    # Get the search query from the GET request, if provided
    search_query = request.GET.get('search', '').lower()

    # If there's a search query, filter the jobs based on title or company name
    if search_query:
        jobs = jobs.filter(
            title__icontains=search_query  # Filter jobs which title contains the search query
        ) | jobs.filter(
            company_name__icontains=search_query  # Filter jobs which company name contains the search query
        )

    # Render the job list page, passing the jobs and search query to the template
    return render(request, 'jobs/job_list.html', {'jobs': jobs, 'search_query': search_query})
