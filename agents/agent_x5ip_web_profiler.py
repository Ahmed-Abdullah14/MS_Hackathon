import requests
from collections import Counter
import re
import base64

# This code dispaly entire REAME content (without summarizing it). 
# The code for dispalying only few lines of README content is commented out at the end. 

# Extract username from GitHub URL
def extract_username_from_url(github_url):
    pattern = r"https?://github.com/([a-zA-Z0-9_-]+)"
    match = re.match(pattern, github_url)
    return match.group(1) if match else None

# Fetch GitHub Profile and Repos
def fetch_github_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else None

def fetch_repos(username):
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
        response = requests.get(url)
        if response.status_code != 200 or not response.json():
            break
        repos.extend(response.json())
        page += 1
    return repos

def fetch_readme(username, repo_name):
    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    response = requests.get(url)
    if response.status_code == 200:
        content = response.json()
        readme_content = base64.b64decode(content['content']).decode('utf-8', errors='ignore')
        return readme_content
    return "No README available"

def summarize_profile(profile, repos):
    name = profile.get("name", profile["login"])
    bio = profile.get("bio", "No bio available.")
    location = profile.get("location", "Unknown location")
    followers = profile.get("followers", 0)
    public_repos = profile.get("public_repos", 0)

    languages = Counter()
    total_stars = sum(r["stargazers_count"] for r in repos)
    total_forks = sum(r["forks_count"] for r in repos)

    for repo in repos:
        if repo.get("language"):
            languages[repo["language"]] += 1

    summary = f"👤 Name: {name}\n"
    summary += f"📍 Location: {location}\n"
    summary += f"💬 Bio: {bio}\n"
    summary += f"📊 Public Repos: {public_repos}\n"
    summary += f"⭐ Total Stars: {total_stars}\n"
    summary += f"🍴 Total Forks: {total_forks}\n"
    summary += f"🧑‍🤝‍🧑 Followers: {followers}\n"
    summary += f"💻 Most Used Languages: {', '.join([f'{lang} ({count})' for lang, count in languages.most_common(5)])}\n\n"

    summary += "🖥️ All Languages Used:\n"
    for lang, count in languages.items():
        summary += f" - {lang}: {count} repo(s)\n"

    summary += "\n🚀 All Projects:\n"
    for repo in repos:
        readme_content = fetch_readme(profile["login"], repo["name"])
        summary += f" - {repo['name']} ({repo['stargazers_count']} ⭐)\n"
        summary += f"   📦 Description: {repo['description'] or 'No description'}\n"
        summary += f"   🔗 URL: {repo['html_url']}\n"
        summary += f"   📖 README:\n{readme_content}\n"
        summary += "\n"

    return summary

# Main function
def generate_summary_from_github_url(github_url):
    username = extract_username_from_url(github_url)
    if not username:
        return "❌ Invalid GitHub URL format."

    profile = fetch_github_profile(username)
    if not profile:
        return f"❌ GitHub user '{username}' not found."
    
    repos = fetch_repos(username)
    return summarize_profile(profile, repos)

# Execution block
if __name__ == "__main__":
    github_url = input("🔗 Enter GitHub profile URL (e.g., https://github.com/username): ").strip()
    print(generate_summary_from_github_url(github_url))



# #Code to dispaly only few lines of README content 

# # Extract username from GitHub URL
# def extract_username_from_url(github_url):
#     pattern = r"https?://github.com/([a-zA-Z0-9_-]+)"
#     match = re.match(pattern, github_url)
#     return match.group(1) if match else None

# # Fetch GitHub Profile and Repos
# def fetch_github_profile(username):
#     url = f"https://api.github.com/users/{username}"
#     response = requests.get(url)
#     return response.json() if response.status_code == 200 else None

# def fetch_repos(username):
#     repos = []
#     page = 1
#     while True:
#         url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
#         response = requests.get(url)
#         if response.status_code != 200 or not response.json():
#             break
#         repos.extend(response.json())
#         page += 1
#     return repos

# def fetch_readme(username, repo_name):
#     url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
#     response = requests.get(url)
#     if response.status_code == 200:
#         content = response.json()
#         try:
#             readme_content = base64.b64decode(content.get('content', '')).decode('utf-8', errors='ignore')
#             return readme_content
#         except Exception as e:
#             return "Error decoding README"
#     return "No README available"

# def summarize_profile(profile, repos):
#     name = profile.get("name", profile["login"])
#     bio = profile.get("bio", "No bio available.")
#     location = profile.get("location", "Unknown location")
#     followers = profile.get("followers", 0)
#     public_repos = profile.get("public_repos", 0)

#     languages = Counter()
#     total_stars = sum(r["stargazers_count"] for r in repos)
#     total_forks = sum(r["forks_count"] for r in repos)

#     for repo in repos:
#         if repo.get("language"):
#             languages[repo["language"]] += 1

#     summary = f"👤 Name: {name}\n"
#     summary += f"📍 Location: {location}\n"
#     summary += f"💬 Bio: {bio}\n"
#     summary += f"📊 Public Repos: {public_repos}\n"
#     summary += f"⭐ Total Stars: {total_stars}\n"
#     summary += f"🍴 Total Forks: {total_forks}\n"
#     summary += f"🧑‍🤝‍🧑 Followers: {followers}\n"
#     summary += f"💻 Most Used Languages: {', '.join([f'{lang} ({count})' for lang, count in languages.most_common(5)])}\n\n"

#     summary += "🖥️ All Languages Used:\n"
#     for lang, count in languages.items():
#         summary += f" - {lang}: {count} repo(s)\n"

#     summary += "\n🚀 All Projects:\n"
#     for repo in repos:
#         readme_content = fetch_readme(profile["login"], repo["name"])
#         summary += f" - {repo['name']} ({repo['stargazers_count']} ⭐)\n"
#         summary += f"   📦 Description: {repo['description'] or 'No description'}\n"
#         summary += f"   🔗 URL: {repo['html_url']}\n"
#         summary += f"   📖 README (first 300 chars):\n     {readme_content[:300]}...\n"
#         summary += "\n"

#     return summary

# # Main function
# def generate_summary_from_github_url(github_url):
#     username = extract_username_from_url(github_url)
#     if not username:
#         return "❌ Invalid GitHub URL format."

#     profile = fetch_github_profile(username)
#     if not profile:
#         return f"❌ GitHub user '{username}' not found."
    
#     repos = fetch_repos(username)
#     return summarize_profile(profile, repos)

# # Entry point
# if __name__ == "__main__":
#     github_url = input("🔗 Enter GitHub profile URL (e.g., https://github.com/username): ").strip()
#     print(generate_summary_from_github_url(github_url))