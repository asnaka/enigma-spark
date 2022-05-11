from random import randint

def rollFlat(type, character):
	roll = randint(1,20)
	match type:
		case 'acro | Flat':
			return f'{roll} + {character.acroMod} = {roll + character.acroMod}'
		case 'anim | Flat':
			return f'{roll} + {character.animMod} = {roll + character.animMod}'
		case 'arca | Flat':
			return f'{roll} + {character.arcaMod} = {roll + character.arcaMod}'
		case 'athl | Flat':
			return f'{roll} + {character.athlMod} = {roll + character.athlMod}'
		case 'dece | Flat':
			return f'{roll} + {character.deceMod} = {roll + character.deceMod}'
		case 'hist | Flat':
			return f'{roll} + {character.histMod} = {roll + character.histMod}'
		case 'insi | Flat':
			return f'{roll} + {character.insiMod} = {roll + character.insiMod}'
		case 'inti | Flat':
			return f'{roll} + {character.intiMod} = {roll + character.intiMod}'
		case 'inve | Flat':
			return f'{roll} + {character.inveMod} = {roll + character.inveMod}'
		case 'medi | Flat':
			return f'{roll} + {character.mediMod} = {roll + character.mediMod}'
		case 'natu | Flat':
			return f'{roll} + {character.natuMod} = {roll + character.natuMod}'
		case 'perc | Flat':
			return f'{roll} + {character.percMod} = {roll + character.percMod}'
		case 'perf | Flat':
			return f'{roll} + {character.perfMod} = {roll + character.perfMod}'
		case 'pers | Flat':
			return f'{roll} + {character.persMod} = {roll + character.persMod}'
		case 'reli | Flat':
			return f'{roll} + {character.reliMod} = {roll + character.reliMod}'
		case 'slei | Flat':
			return f'{roll} + {character.sleiMod} = {roll + character.sleiMod}'
		case 'stea | Flat':
			return f'{roll} + {character.steaMod} = {roll + character.steaMod}'
		case 'surv | Flat':
			return f'{roll} + {character.survMod} = {roll + character.survMod}'

def rollAdv(type, character):
	roll = randint(1,20)
	roll2 = randint(1,20)
	higher = roll if roll > roll2 else roll2
	lower = roll if roll < roll2 else roll2
	match type:
		case 'acro | Advantage':
			return f'{lower}, {higher} + {character.acroMod} = {higher + character.acroMod}'
		case 'anim | Advantage':
			return f'{lower}, {higher} + {character.animMod} = {higher + character.animMod}'
		case 'arca | Advantage':
			return f'{lower}, {higher} + {character.arcaMod} = {higher + character.arcaMod}'
		case 'athl | Advantage':
			return f'{lower}, {higher} + {character.athlMod} = {higher + character.athlMod}'
		case 'dece | Advantage':
			return f'{lower}, {higher} + {character.deceMod} = {higher + character.deceMod}'
		case 'hist | Advantage':
			return f'{lower}, {higher} + {character.histMod} = {higher + character.histMod}'
		case 'insi | Advantage':
			return f'{lower}, {higher} + {character.insiMod} = {higher + character.insiMod}'
		case 'inti | Advantage':
			return f'{lower}, {higher} + {character.intiMod} = {higher + character.intiMod}'
		case 'inve | Advantage':
			return f'{lower}, {higher} + {character.inveMod} = {higher + character.inveMod}'
		case 'medi | Advantage':
			return f'{lower}, {higher} + {character.mediMod} = {higher + character.mediMod}'
		case 'natu | Advantage':
			return f'{lower}, {higher} + {character.natuMod} = {higher + character.natuMod}'
		case 'perc | Advantage':
			return f'{lower}, {higher} + {character.percMod} = {higher + character.percMod}'
		case 'perf | Advantage':
			return f'{lower}, {higher} + {character.perfMod} = {higher + character.perfMod}'
		case 'pers | Advantage':
			return f'{lower}, {higher} + {character.persMod} = {higher + character.persMod}'
		case 'reli | Advantage':
			return f'{lower}, {higher} + {character.reliMod} = {higher + character.reliMod}'
		case 'slei | Advantage':
			return f'{lower}, {higher} + {character.sleiMod} = {higher + character.sleiMod}'
		case 'stea | Advantage':
			return f'{lower}, {higher} + {character.steaMod} = {higher + character.steaMod}'
		case 'surv | Advantage':
			return f'{lower}, {higher} + {character.survMod} = {higher + character.survMod}'

def rollDis(type, character):
	roll = randint(1,20)
	roll2 = randint(1,20)
	higher = roll if roll > roll2 else roll2
	lower = roll if roll < roll2 else roll2
	match type:
		case 'acro | Disadvantage':
			return f'{higher}, {lower} + {character.acroMod} = {lower + character.acroMod}'
		case 'anim | Disadvantage':
			return f'{higher}, {lower} + {character.animMod} = {lower + character.animMod}'
		case 'arca | Disadvantage':
			return f'{higher}, {lower} + {character.arcaMod} = {lower + character.arcaMod}'
		case 'athl | Disadvantage':
			return f'{higher}, {lower} + {character.athlMod} = {lower + character.athlMod}'
		case 'dece | Disadvantage':
			return f'{higher}, {lower} + {character.deceMod} = {lower + character.deceMod}'
		case 'hist | Disadvantage':
			return f'{higher}, {lower} + {character.histMod} = {lower + character.histMod}'
		case 'insi | Disadvantage':
			return f'{higher}, {lower} + {character.insiMod} = {lower + character.insiMod}'
		case 'inti | Disadvantage':
			return f'{higher}, {lower} + {character.intiMod} = {lower + character.intiMod}'
		case 'inve | Disadvantage':
			return f'{higher}, {lower} + {character.inveMod} = {lower + character.inveMod}'
		case 'medi | Disadvantage':
			return f'{higher}, {lower} + {character.mediMod} = {lower + character.mediMod}'
		case 'natu | Disadvantage':
			return f'{higher}, {lower} + {character.natuMod} = {lower + character.natuMod}'
		case 'perc | Disadvantage':
			return f'{higher}, {lower} + {character.percMod} = {lower + character.percMod}'
		case 'perf | Disadvantage':
			return f'{higher}, {lower} + {character.perfMod} = {lower + character.perfMod}'
		case 'pers | Disadvantage':
			return f'{higher}, {lower} + {character.persMod} = {lower + character.persMod}'
		case 'reli | Disadvantage':
			return f'{higher}, {lower} + {character.reliMod} = {lower + character.reliMod}'
		case 'slei | Disadvantage':
			return f'{higher}, {lower} + {character.sleiMod} = {lower + character.sleiMod}'
		case 'stea | Disadvantage':
			return f'{higher}, {lower} + {character.steaMod} = {lower + character.steaMod}'
		case 'surv | Disadvantage':
			return f'{higher}, {lower} + {character.survMod} = {lower + character.survMod}'