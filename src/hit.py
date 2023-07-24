class Hit:
    def __init__(self, username, damage, boss, level, kills):
        self.username = self.sanitize(username)
        self.damage = self.sanitize_number(self.sanitize(damage))
        self.boss = self.serialize_boss(self.sanitize(boss))
        self.level = self.sanitize_number(self.sanitize(level))
        self.kills = kills

    def sanitize(self, text, verbose=False):
        # Remove leading/trailing whitespace
        text = text.strip()
        # Remove commas
        text = text.replace(",", "").replace(".", "")
        if verbose:
            print(text)
        return text
    
    def sanitize_number(self, text, verbose=False):
        # Extract digits and join them
        text = "".join([char for char in text if char.isdigit()])
        if verbose:
            print(text)
        return text

    def __str__(self):
        return f"Username: {self.username}, Damage: {self.damage}, Boss: {self.boss}, Level: {self.level}, Kills: {self.kills}"

    def serialize(self):
        return {
            "username": self.username,
            "damage": self.damage,
            "boss": self.boss,
            "level": self.level,
            "kills": self.kills
        }

    def serialize_boss(self, boss):
        bosses = {
            'RVD': ["red", "velvet", "dragon", "redvelvetdragon", "redvelvet", "velvetdragon"],
            'TLA': ["living", "abyss", "the", "livingabyss", "thelivingabyss", "theliving"],
            'AOD': ["avatar", "of", "destiny", "avatarofdestiny", "avatarof" "ofdestiny"],
        }
        
        for key, values in bosses.items():
            if any(val in boss.lower() for val in values):
                return key
                
        return 'unknown'