"""Platform names and icons used for ease of html code generation"""    

def platforms(request):
    return {'platforms': [{'type':'PC', 'names': ['Battle.net', 'DRM-Free', 'Epic Games Store', 'GOG', 'Itch.io', 'Origin', 'PC', 'Steam', 'Ubisoft Connect']},
            {'type': 'Consoles', 'names': ['Nintendo Switch', 'Playstation 4', 'Playstation 5', 'Xbox 360', 'Xbox One', 'Xbox Series X|S', 'Other Console']},
            {'type': 'Mobile', 'names': ['Android', 'iOS']},
            {'type': 'Other Platforms', 'names': ['VR']}
    ]}

def platform_icons(request):
    return {'platform_icons': [('PC', 'windows'), ('Steam', 'steam-symbol'), ('Itch.io', 'itch-io'), ('Battle.net', 'battle-net'), ('Playstation', 'playstation'), ('Xbox', 'xbox'), ('Android', 'google-play'), ('iOS', 'apple')]}

