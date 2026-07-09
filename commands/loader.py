from commands import balance,daily,shop

def load_commands(tree):
    balance.register(tree)
    daily.register(tree)
    shop.register(tree)
    print('Commands Loaded')
