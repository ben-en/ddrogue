from collections import namedtuple

from ..ui import menu
from .bab import LOW_BAB, HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves
from .feats import FEAT_LIST
from .skills import KNOWLEDGE_LIST
from .weapons import simple_proficiency, fighter_proficiency


BaseClass = namedtuple('BaseClass', [
    's',             # class as a string
    'hd',            # hit dice rolled for HP each level
    'bab',           # base attack bonus for the class
    'saves',         # saves to be used for a given level (under dev)
    'skills',        # list of class skills
    'knowledges',    # list of knowledges if character has knowledge skill
    'sp',            # skill points gained per level
    'gold',          # initial gold
    'equipment',     # initial equipment, if any
    'proficiency',  # weapons the class is proficient with
    'features',      # features gained at each level
    'spells',        # spells available per spell level (different than char)
    'alignment',     # alignments that are allowed to pick this class
    'desc'           # description of the class
])


fighter_feats = [feat for feat in FEAT_LIST if 'fighter' in feat.tags]


def fighter_feat(character, npc=False):
    """ pick a feat from the list of fighter feats """
    character.features.update(menu(fighter_feats, npc=npc))
    return None


def bravery(character, npc=False):
    """ increase the character's save against fear """
    try:
        character.fear_bonus += 1
    except AttributeError:
        character.fear_bonus = 1


def armor_training(character, npc=False):
    """ reduce the arcmor check penalty for armor for each level of this """
    try:
        character.acp_bonus -= 1
    except AttributeError:
        character.acp_bonus = -1


fighter_weapon_groups = {
    'monk': []  # Shuriken and so forth
}


def weapon_training(character, npc=False):
    """ pick a group of weapons to specialize in """
    # TODO finish this, its supposed to add one bonus to each previously
    # selected. eg, at level 10, first group would be +2, second group would be
    # +1
    character.features += menu(fighter_weapon_groups)


fighter_abilities = [
    {'level_up': [fighter_feat]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'passive': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'passive': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'passive': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'passive': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {},  # TODO armor mastery
    {'level_up': [fighter_feat]},  # TODO weapon mastery
]

Fighter = BaseClass(
    'Fighter',
    '1d10',
    HIGH_BAB,
    compile_saves(GOOD_SAVE, BAD_SAVE, BAD_SAVE),
    ('climb craft handle animal intimidate knowledge profession ride survival'
     'swim').split(),
    'dungeoneering engineering'.split(),
    2,  # implies intelligence + 2 skill progression
    '5d6',
    [],
    fighter_proficiency,
    fighter_abilities,
    None,  # no spells
    None,  # any alignment can be a fighter
    'Fighter character class description'
)


def arcane_bond():
    """ wizards get a familiar or a special object """
    return {}


def familiar():
    """ Return an additional character to the party """
    return {}


def school():
    """ select a wizard school """
    return {}


def cantrips():
    """  wizards can memorize x 0 lvl spells and cast them unlimited times """
    return {}


def wizard_feat():
    """ wizards get a free feat that is tagged wizard """
    return {}


def scribe_scroll():
    """ wizards get scribe scroll feat for free at first level """
    return {}


wizard_abilities = [
    {'level_up': [arcane_bond, school, cantrips, scribe_scroll]},
    {},
    {},
    {},
    {'level_up': [wizard_feat]},
    {},
    {},
    {},
    {},
    {'level_up': [wizard_feat]},
    {},
    {},
    {},
    {},
    {'level_up': [wizard_feat]},
    {},
    {},
    {},
    {},
    {'level_up': [wizard_feat]},
]


Wizard = BaseClass(
    'Wizard',
    '1d6',
    LOW_BAB,
    compile_saves(BAD_SAVE, BAD_SAVE, GOOD_SAVE),
    'appraise craft fly knowledge linguistics profession spellcraft'.split(),
    KNOWLEDGE_LIST,
    2,  # implies intelligence + 2 skill progression
    '2d6',
    ['spellbook', 'spell components'],
    simple_proficiency,
    wizard_abilities,
    [[0 for i in range(10)] for x in range(20)],
    None,  # any alignment can be a wizard
    'Wizard character class description'
)


CLASS_LIST = [Fighter, Wizard]
