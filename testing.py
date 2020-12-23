data = {
    "channel_id": "781315923503611944",
    "data": {
        "id": "791160278858858566",
        "name": "sendmessage",
        "options": [{"name": "message", "value": "test"}],
    },
    "guild_id": "576970476715507729",
    "id": "791166634118348841",
    "member": {
        "deaf": False,
        "is_pending": False,
        "joined_at": "2019-05-12T18:36:16.878000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "2147483647",
        "premium_since": None,
        "roles": [
            "577200590803697676",
            "577200612618403875",
            "681590545952407637",
            "715808753273929728",
            "741507081403629659",
        ],
        "user": {
            "avatar": "565a9285876372cd84eb723979992a56",
            "discriminator": "3333",
            "id": "356139270446120960",
            "public_flags": 768,
            "username": "exo",
        },
    },
    "token": "aW50ZXJhY3Rpb246NzkxMTY2NjM0MTE4MzQ4ODQxOmtVdWJiVVoyVDA3emwxYnZMVUVvWkowNE9wT1NRakZnUnV1ZjM1YUN0bHA5cE9hUVdvZWl1bWJwT3FFRmlpYlA2RXhpWEJKNUJnb2t4ZDhOeGRqanpTTkhyYjRZMWpqcktQOFRLTFhDelg5eGJZeGhPcnpaOFo0bTQ1WVlVTEEy",
    "type": 2,
    "version": 1,
}

from dispike.models.incoming import IncomingDiscordInteraction


IncomingDiscordInteraction(**data)
