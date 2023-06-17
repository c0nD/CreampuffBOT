class Hit:
    def __init__(self, username, damage, boss, level):
        self.username = self.sanitize(username)
        self.damage = self.sanitize_number(self.sanitize(damage))
        self.boss = self.serialize_boss(self.sanitize(boss))
        self.level = self.sanitize_number(self.sanitize(level))

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
        return f"Username: {self.username}, Damage: {self.damage}, Boss: {self.boss}, Level: {self.level}"

    def serialize(self):
        return {
            "username": self.username,
            "damage": self.damage,
            "boss": self.boss,
            "level": self.level
        }

    def serialize_boss(self, boss):
        bosses = {
            'dragon': ["red", "velvet", "dragon"],
            'abyss': ["living", "abyss"],
            'avatar': ["avatar", "of", "destiny"]
        }
        
        for key, values in bosses.items():
            if any(val in boss.lower() for val in values):
                return key
                
        return 'unknown'
