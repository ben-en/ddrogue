from collections import namedtuple

from .bab import HIGH_BAB
from .saves import GOOD_SAVE, BAD_SAVE, compile_saves
from .feats import FEAT_LIST


BaseClass = namedtuple('BaseClass', [
    'hd',           # hit dice rolled for HP each level
    'bab',          # base attack bonus for the class
    'saves',        # saves to be used for a given level (under dev)
    'skills',       # list of class skills
    'knowledges',   # list of knowledges if character has knowledge skill
    'sp',           # skill points gained per level
    'gold',         # initial gold
    'equipment',    # initial equipment, if any
    'features',     # features gained at each level
    'desc'          # description of the class
])


# TODO define pick

fighter_feats = [feat for feat in FEAT_LIST if 'fighter' in feat.tags]


def fighter_feat(character, npc=False):
    """ pick a feat from the list of fighter feats """
    character.features.update(pick(fighter_feats, npc=npc))
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
        character.acp_bonuse -= 1
    except AttributeError:
        character.acp_bonuse = -1


fighter_weapon_groups = {
    'monk': []  # Shuriken and so forth
}


def weapon_training(character, npc=False):
    """ pick a group of weapons to specialize in """
    # TODO finish this, its supposed to add one bonus to each previously
    # selected. eg, at level 10, first group would be +2, second group would be
    # +1
    character.features += pick(fighter_weapon_groups, npc)


fighter_abilities = [
    {'level_up': [fighter_feat]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'level_up': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'level_up': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'level_up': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {'level_up': [armor_training]},
    {'level_up': [fighter_feat]},
    {'level_up': [weapon_training]},
    {'level_up': [fighter_feat], 'passive': [bravery]},
    {},  # TODO armor mastery
    {'level_up': [fighter_feat]},  # TODO weapon mastery
]

Fighter = BaseClass(
    '1d10',
    HIGH_BAB,
    compile_saves(GOOD_SAVE, BAD_SAVE, BAD_SAVE),
    ('climb craft handle animal intimidate knowledge profession ride survival'
     'swim').split(),
    'dungeoneering engineering'.split(),
    2,  # implies intelligence + 2 skill progression
    '5d6',
    [],
    fighter_abilities,
    'Fighter character class description'
)
