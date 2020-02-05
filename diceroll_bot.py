"""A bot to roll Vampire dice in Discord."""
import discord
import random
from datetime import datetime
from envreader import Env


def log(message):
    """Log a message in console."""
    print("%s - %s" % (datetime.now(), message))


def get_options():
    """Return the available options for dicerollbot."""
    return "Use:\n" + \
           "\t* /v <dice amount> - Roll with difficulty 6\n" + \
           "\t* /v <dice amount> <difficulty>"


def vampire_roll(params):
    """Make a Vampire roll given an amount of dice and difficulty."""
    try:
        amount = int(params[0])
        diff = int(params[1]) - 1
    except ValueError:
        return get_options()

    if (amount > 10):
        return 'Too many dice!'
    if (amount < 1):
        return 'Too few dice!'
    if (diff < 1):
        return 'Too easy!'
    if (diff > 9):
        return 'Too hard!'

    rolls = [random.randrange(0, 10) for x in range(amount)]
    rolls.sort()
    log('Rolled ' + ', '.join([str(roll+1) for roll in rolls]))

    failures = list(filter(lambda i: i == 0, rolls))
    nothing = list(filter(lambda i: i > 0 and i < diff, rolls))
    successes = list(filter(lambda i: i >= diff, rolls))

    if (len(failures) > len(successes)):
        remove_starting_point = 0
        amount_str = "Failure"
    else:
        remove_starting_point = len(successes) - len(failures)
        amount_str = str(remove_starting_point) + " successes"

    formatted_rolls = \
        ['**%d**' % (i+1) for i in failures] + \
        ['_%d_' % (i+1) for i in nothing] + \
        [str(i+1) for i in successes[:remove_starting_point]] + \
        ['~~%d~~' % (i+1) for i in successes[remove_starting_point:]]

    return '(%s) = %s' % (
        ', '.join(formatted_rolls),
        amount_str
    )


ENVIRONMENT = Env()

if __name__ == '__main__':
    client = discord.Client()

    @client.event
    async def on_ready():
        """Routine to run when bot is ready."""
        random.seed((datetime.now() - datetime(1970, 1, 1)).total_seconds())
        log('The bot is up and running')

    @client.event
    async def on_message(message):
        """Routine to run when receiving message."""
        if (message.content.startswith('/v')):
            log('Received message: ' + message.content)
            params = message.content.split(' ')

            response = get_options()
            if (len(params) == 2):
                response = vampire_roll([params[1], 6])
            if (len(params) == 3):
                response = vampire_roll(params[1:])
            await message.channel.send(response)

            if (response.endswith('Failure')):
                await message.channel.send('(╯°□°）╯︵ ┻━┻')

            log("Message answered")

    client.run(ENVIRONMENT.get('TOKEN'))
