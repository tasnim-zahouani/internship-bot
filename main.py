import os
import feedparser
import requests
from google import genai

# The new SDK automatically detects the GEMINI_API_KEY environment variable!
DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK"]

def fetch_recent_jobs():
    feed_url = "https://weworkremotely.com/categories/remote-programming-jobs.rss" 
    feed = feedparser.parse(feed_url)
    
    print(f"Found {len(feed.entries)} jobs in the RSS feed.")
    jobs = []
    for entry in feed.entries[:15]: 
        jobs.append(f"Title: {entry.title}\nLink: {entry.link}\nDescription: {entry.description}\n---")
    return "\n".join(jobs)

def filter_jobs_with_gemini(job_data):
    # Initialize the new Gemini client
    client = genai.Client()
    
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
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def send_to_discord(message):
    if len(message) > 1900:
        message = message[:1900] + "\n\n...(truncated for Discord length limit)"
        
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)

    print(f"Discord API Response Code: {response.status_code}")
    if response.status_code != 204:
        print(f"Discord Error Details: {response.text}")

if __name__ == "__main__":
    print("Starting internship search...")
    raw_jobs = fetch_recent_jobs()
    
    if raw_jobs:
        print("Filtering with Gemini...")
        curated_list = filter_jobs_with_gemini(raw_jobs)
        
        print("Sending message to Discord...")
        send_to_discord(f"🌅 **Good morning! Here is your 8 AM Internship Report:**\n\n{curated_list}")
        print("Done!")
    else:
        print("No jobs found in the feed to process.")