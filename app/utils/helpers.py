

def is_cli_user_agent(user_agent):
    '''
    Check if the user agent is a CLI tool
    '''
    cli_agents = ['curl', 'wget', 'httpie', 'python-requests', 'aria2', 'libwww-perl']
    if not user_agent:
        return False
    return any(agent in user_agent.lower() for agent in cli_agents)
