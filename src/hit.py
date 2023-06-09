class Hit:
    def __init__(self, username, damage, boss):
        self.username = self.sanitize(username)
        self.damage = self.sanitize(damage)
        self.boss = self.serialize_boss(self.sanitize(boss))

    def sanitize(self, text):
        # Remove leading/trailing whitespace
        text = text.strip()
        # Remove commas
        text = text.replace(",", "")
        return text

    def __str__(self):
        return f"Username: {self.username}, Damage: {self.damage}, Boss: {self.boss}"

    def serialize(self):
        return {
            "username": self.username,
            "damage": self.damage,
            "boss": self.boss,
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
