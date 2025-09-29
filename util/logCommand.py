from datetime import datetime, timezone

def logCommand(ctx):
    print(f'{datetime.now(timezone.utc)} UTC | Command !{ctx.command} invoked by {ctx.author} in Guild: {ctx.guild}, Channel: {ctx.channel}')