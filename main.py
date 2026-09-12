import google.generativeai as genai
import feedparser
import requests
import os

# 1. Setup API Keys
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

def fetch_recent_jobs():
    # Example using an RSS feed (e.g., from Upwork, StackOverflow, or a custom Indeed RSS)
    # Replace with your actual data source
    feed_url = "YOUR_JOB_BOARD_RSS_URL" 
    feed = feedparser.parse(feed_url)
    
    jobs = []
    for entry in feed.entries[:15]: # Grab the latest 15 jobs
        jobs.append(f"Title: {entry.title}\nLink: {entry.link}\nDescription: {entry.description}\n---")
    return "\n".join(jobs)

def filter_jobs_with_gemini(job_data):
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = f"""
    You are an expert technical recruiter. Review the following job listings.
    I am looking for a CS internship with these strict criteria:
    - Must be a Software Engineering or Data Science role.
    - Must use Python, Java, or C++.
    - Must be located in France or London or Dublin or Europe.
    
    Filter out any jobs that do not match. 
    Return a concise summary of only the matching jobs in this format:
    [Job Title] - [Company] - [Link]
    Brief reason for match: ...
    
    If none match, reply with "No matching internships today."
    
    Job Listings:
    {job_data}
    """
    
    response = model.generate_content(prompt)
    return response.text

def send_to_discord(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

if __name__ == "__main__":
    raw_jobs = fetch_recent_jobs()
    if raw_jobs:
        curated_list = filter_jobs_with_gemini(raw_jobs)
        send_to_discord(f"🌅 **Good morning! Here is your 8 AM Internship Report:**\n\n{curated_list}")