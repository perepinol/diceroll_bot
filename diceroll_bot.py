"""A bot to roll Vampire dice in Discord."""
import os
import discord
import random
from datetime import datetime


def log(message):
    """Log a message in console."""
    print("%s - %s" % (datetime.now(), message), flush=True)


def get_options():
    """Return the available options for dicerollbot."""
    return "Use:\n" + \
           "\t* /r XdY: Roll X dice with Y sides" + \
           "\t* /v <dice amount> - VtM roll with difficulty 6\n" + \
           "\t* /v <dice amount> <difficulty> - VtM roll"


def roll(amount, faces):
    rolls = [random.randrange(1, faces + 1) for _ in range(amount)]
    rolls.sort()
    log('Rolled ' + ', '.join([str(roll) for roll in rolls]))
    return rolls


def standard_roll(param):
    """
    Make a normal dice roll (XdY where X is the amount of dice and Y is the number of sides).

    params[0] = X
    params[1] = Y
    """
    amount, sides = None, None
    try:
        roll_params = list(map(lambda x: int(x), param.split('d')))
        if len(roll_params) == 2:
            amount, sides = roll_params
    except ValueError:
        return [get_options()]
    if amount < 1:
        return ['Not enough dice!']
    if amount > 100:
        return ['Too many dice!']
    if sides < 1:
        return ['Not enough sides!']
    if sides > 100:
        return ['Too many sides!']
    rolls = map(lambda x: str(x), roll(amount, sides))
    return ['%s: (%s)' % (param, ', '.join(rolls))]



def vampire_roll(params):
    """
    Make a Vampire roll given an amount of dice and difficulty.

    params[0] = amount of dice [1, 10]
    params[1] = difficulty [2, 10]    
    """
    try:
        amount = params.pop(0)
        diff = params.pop(0)
    except ValueError:
        return [get_options()]

    if amount > 10:
        return ['Too many dice!']
    if amount < 1:
        return ['Not enough dice!']
    if diff < 2:
        return ['Too easy!']
    if diff > 10:
        return ['Too hard!']

    rolls = roll(amount, 10)

    failures = list(filter(lambda i: i == 1, rolls))
    nothing = list(filter(lambda i: 1 < i < diff, rolls))
    successes = list(filter(lambda i: i >= diff, rolls))

    net_successes = max(0, len(successes) - len(failures))

    formatted_rolls = \
        ['**%d**' % i for i in failures] + \
        ['_%d_' % i for i in nothing] + \
        ['%d' % i for i in successes[:net_successes]] + \
        ['~~%d~~' % i for i in successes[net_successes:]]

    failure = len(failures) > 0 and len(successes) == 0
    result = '(%s) = %s' % (
        ', '.join(formatted_rolls),
        'Failure' if failure else '%d successes' % net_successes
    )
    return [result] + (['(╯°□°）╯︵ ┻━┻'] if failure else [])


if __name__ == '__main__':
    token = os.getenv('TOKEN')
    if not token:
        log('No TOKEN in environment variables')
        exit(1)
    client = discord.Client()

    @client.event
    async def on_ready():
        """Routine to run when bot is ready."""
        random.seed((datetime.now() - datetime(1970, 1, 1)).total_seconds())
        log('The bot is up and running')

    @client.event
    async def on_message(message):
        """Routine to run when receiving message."""
        if not message.content.startswith('/'):
            return
        params = message.content.split(' ')
        if not len(params):
            return

        log('Received message: ' + message.content)
        command = params.pop(0)

        responses = [get_options()]
        if command == '/d':
            if len(params) == 1:
                responses = standard_roll(params.pop(0))
        elif command == '/v':
            try:
                params = list(map(lambda x: int(x), params))
                if len(params) == 1:
                    responses = vampire_roll(params + [6])
                if len(params) == 2:
                    responses = vampire_roll(params)
            except ValueError:
                pass

        for response in responses:
            await message.channel.send(response)

        log("Message answered")

    client.run(token)
