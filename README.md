## The Internship bot 

This simple bot, An automated job-hunting pipeline that fetches job offers via Google Alerts RSS feeds, filters them using the Gemini AI API based on specific criteria, and sends a curated daily summary to a Discord channel using GitHub Actions.

Tech Stack: Python, Google Gemini API, GitHub Actions (CI/CD / Cron Jobs), Discord Webhooks.

It will send you a message as soon as it can!


### Visual proof on how it should work
<img width="802" height="366" alt="image" src="https://github.com/user-attachments/assets/a8f4c516-3656-4b14-b056-941a67afe53e" />

## Set-up Guide
1. Discord Webhook

Have a (private) Discord server ready.
In Server Settings, navigate to Integrations > Webhooks. Click on New Webhook and copy the URL.

2. GitHub Secrets (Environment Variables)

Go to your GitHub repository. Click on Settings > Secrets and variables > Actions.
Create a New Repository Secret for your webhook. Name it: DISCORD_WEBHOOK.

Retrieve your Gemini API key and create a second secret. Name it: GEMINI_API_KEY

3. Configure your RSS Feeds

In the code, open main.py and modify the feed_urls = [...] block with your own RSS links from Google Alerts.

*Note: When creating your Google Alert, ensure you select 'All results' instead of 'Only the best results' to prevent feed errors.*

4. Run it locally

python main.py

To check if the automated CI/CD pipeline is working, go to the Actions tab in your GitHub repository!


✣
