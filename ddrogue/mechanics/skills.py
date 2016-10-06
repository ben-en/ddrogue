from collections import namedtuple


Skill = namedtuple('Skill', ['name', 'stat', 'enc'])

SKILL_LIST = [
    Skill('acrobatics', 'dex', True),
    Skill('appraise', 'int', False),
    Skill('bluff', 'cha', False),
    Skill('climb', 'str', True),
    Skill('craft', 'int', False),
    Skill('disable-device', 'dex', False),
    Skill('diplomacy', 'cha', False),
    Skill('disguise', 'cha', False),
    Skill('escape-artist', 'dex', True),
    Skill('fly', 'dex', True),
    Skill('handle-animal', 'cha', False),
    Skill('heal', 'wis', False),
    Skill('intimidate', 'cha', False),
    Skill('knowledge', 'int', False),
    Skill('linguistics', 'int', False),
    Skill('perception', 'wis', False),
    Skill('perform', 'cha', False),
    Skill('profession', 'wis', False),
    Skill('ride', 'dex', True),
    Skill('sense-motive', 'wis', False),
    Skill('sleight-of-hand', 'dex', True),
    Skill('spellcraft', 'int', False),
    Skill('stealth', 'dex', True),
    Skill('survival', 'wis', False),
    Skill('swim', 'str', True),
    Skill('use-magic-device', 'cha', False),
]

SkillBlock = namedtuple('SkillBlock', [x.name for x in SKILL_LIST])

KNOWLEDGE_LIST = (
    'arcana dungeoneering engineering geography history local nature nobility'
    'planes religion'
).split()
