import discord
from discord.ext import commands
from github import Github

DISCORD_TOKEN = "YOUR_DC_TOKEN"

GITHUB_TOKEN = "YOUR_GITHUB_TOKEN"

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

github = Github(GITHUB_TOKEN)

@bot.event
async def on_ready():
    print("Bot is ready!")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if 'github.com/' in message.content:
        repo_name = "owner/repo"
        commit_sha = "12345"
        repo = github.get_repo(repo_name)
        commit = repo.get_commit(commit_sha)
        bot.dispatch('github_commit', repo, commit)

    await bot.process_commands(message)

@bot.command()
async def issues(ctx, repo_name):
    repo = github.get_repo(repo_name)
    issues = repo.get_issues(state="open")
    response = f"Open issues in {repo.full_name}:\n"
    if issues.totalCount == 0:
        response += "No open issues!"
    else:
        for issue in issues:
            response += f"- {issue.number} ({issue.title})\n"
    
    await ctx.send(response)

@bot.event
async def on_github_commit(repo, commit):
    print(f'New commit in {repo.full_name}: {commit.sha}')

@bot.command()
async def commits(ctx, repo_name):
    repo = github.get_repo(repo_name)
    commits = repo.get_commits()
    response = f"Commits in {repo.full_name}:\n"
    if commits.totalCount == 0:
        response += "No commits!"
    else:
        for commit in commits:
            response += f"- {commit.sha} ({commit.commit.message})\n"
    
    await ctx.send(response)

@bot.command()
async def pr(ctx, repo_name):
    repo = github.get_repo(repo_name)
    pull_requests = repo.get_pulls(state="open")
    response = f"Open pull requests in {repo.full_name}:\n"
    if pull_requests.totalCount == 0:
        response += "No open pull requests!"
    else:
        for pull_request in pull_requests:
            response += f"- {pull_request.number} ({pull_request.title})\n"
    
    await ctx.send(response)


bot.run(DISCORD_TOKEN)
