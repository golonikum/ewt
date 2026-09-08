from django import template
import re

register = template.Library()

@register.filter
def highlight(value, word):
	return str(value).replace(word, '<span class="hl">%s</span>' % word)

def build_word_regexp(word):
	w = str(word.signature)

	# all
	w = '(%s|%s)%s' % (w[0].upper(), w[0], w[1:])

	if word.speech_part.name in ('phrase','verb'):

		# phrase, verb
		if w.find('(C|c)atch') != -1:
			w = w.replace("(C|c)atch", '(C|c)a(tch|ught)')
		if w.find('(C|c)reep') != -1:
			w = w.replace("(C|c)reep", '(C|c)re(ep|pt)')
		if w.find('(B|b)end') != -1:
			w = w.replace("(B|b)end", '(B|b)en(d|t)')
		if w.find('(B|b)low') != -1:
			w = w.replace("(B|b)low", '(B|b)l(ow|ew|own)')
		if w.find('(B|b)ring') != -1:
			w = w.replace("(B|b)ring", '(B|b)r(ing|ought)(| me)')
		if w.find('(B|b)reak') != -1:
			w = w.replace("(B|b)reak", '(B|b)r(eak|oke|oken)')
		if w.find('(D|d)rive') != -1:
			w = w.replace("(D|d)rive", '(D|d)r(ive|ove|iven|iving)')
		if w.find('(F|f)ly') != -1:
			w = w.replace("(F|f)ly", '(F|f)l(y|ew|own)')
		if w.find('(F|f)all') != -1:
			w = w.replace("(F|f)all", '(F|f)(all|ell|allen)')
		if w.find('(G|g)ive') != -1:
			w = w.replace("(G|g)ive", '(G|g)(ive|ave|iven|iving)')
		if w.find('(G|g)o') != -1:
			w = w.replace("(G|g)o", '((G|g)o(|ne)|(W|w)ent)')
		if w.find('(H|h)ave') != -1:
			w = w.replace("(H|h)ave", '(H|h)a(ve|d|ving)')
		if w.find('(R|r)ing') != -1:
			w = w.replace("(R|r)ing", '(R|r)(i|a|u)ng')
		if w.find('(K|k)eep') != -1:
			w = w.replace("(K|k)eep", '(K|k)e(ep|pt)')
		if w.find('(L|l)ose') != -1:
			w = w.replace("(L|l)ose", '(L|l)o(se|st)')
		if w.find('(M|m)ake') != -1:
			w = w.replace("(M|m)ake", '(M|m)a(k|d)e')
		if w.find('(S|s)ee') != -1:
			w = w.replace("(S|s)ee", '(S|s)(ee|aw|een)')
		if w.find('(S|s)hoot') != -1:
			w = w.replace("(S|s)hoot", '(S|s)ho(ot|t)')
		if w.find('(S|s)hake') != -1:
			w = w.replace("(S|s)hake", '(S|s)h(ake|ook|aken|aking)')
		if w.find('(S|s)mite') != -1:
			w = w.replace("(S|s)mite", '(S|s)m(ite|ote|itten)')
		if w.find('(S|s)pring') != -1:
			w = w.replace("(S|s)pring", '(S|s)pr(ing|ang|ung)')
		if w.find('(S|s)tand') != -1:
			w = w.replace("(S|s)tand", '(S|s)t(and|ood)')
		if w.find('(S|s)teal') != -1:
			w = w.replace("(S|s)teal", '(S|s)t(eal|olen|ole)')
		if w.find('(S|s)tride') != -1:
			w = w.replace("(S|s)tride", '(S|s)tr(ide|ode|idden|iding)')
		if w.find('(S|s)trike') != -1:
			w = w.replace("(S|s)trike", '(S|s)tr(ike|uck|iking)')
		if w.find('(S|s)tick') != -1:
			w = w.replace("(S|s)tick", '(S|s)t(i|u)ck')
		if w.find('(S|s)well') != -1:
			w = w.replace("(S|s)well", '(S|s)w(ell|elled|ollen)')
		if w.find('(T|t)ell') != -1:
			w = w.replace("(T|t)ell", '(T|t)(ell|old)')
		if w.find('(T|t)ake') != -1:
			w = w.replace("(T|t)ake", '(T|t)(ake|ook|aken|aking)')
		if w.find('(T|t)read') != -1:
			w = w.replace("(T|t)read", '(T|t)r(ea|o)d')
		if w.find('(W|w)ind') != -1:
			w = w.replace("(W|w)ind", '(W|w)(i|ou)nd')

		# phrase, verb
		if re.search(r'e$', w):
			w = re.sub(r'e$', r'(e|ing)', w)

		# phrase, verb
		if re.search(r'y$', w):
			w = re.sub(r'y$', r'(y|ied|ies)', w)

		# phrase
		if word.speech_part.name == 'phrase':

			if w.find('(B|b)e ') != -1:
				w = w.replace('(B|b)e', "(be|am|'m|is|'s|are|'re|was|were|been)")

			if w.find('(N|n)ot have ') != -1:
				w = w.replace('(N|n)ot have', "(d(o|id)(|es)n't have|ha(ve|s|d)n't(| got))")

			if w.find('oneself') != -1:
				w = w.replace('oneself', '((my|your|him|her|it)self|(your|our)selves)')
			if w.find("smb.'s") != -1:
				w = w.replace("smb.'s", "(my|your|his|her|their|our|.+'s)")
			if w.find("one's") != -1:
				w = w.replace("one's", '(my|your|his|her|their|our)')
			if re.search(r'smb.$', w):
				w = w[:-5]
			if w.find("smb.") != -1:
				w = w.replace("smb.", r'(me|you|him|her|them|us|[^\.\?!]+)')
			if re.search(r'smth.$', w):
				w = w.replace('smth.', '')
			if w.find('smth.') != -1:
				w = w.replace('smth.', '.+')

			if w.find(' ') != -1:
				w = w.replace("e ", '(e|ing) ')
				w = w.replace(' ', '(|(|p|n|g|m|v|t)ing|d|(|p|n|g|m|v|t)ed|s) ')

	elif word.speech_part.name == 'noun':
		# noun
		if re.search(r'y$', w):
			w = re.sub(r'y$', r'(y|ies|ied)', w)
		if w.find('-') != -1:
			w = w.replace('-', '(s|)-')

	elif word.speech_part.name == 'adverb':
		# adverb
		if w.find("one's") != -1:
			w = w.replace("one's", '(my|your|his|her|their|our)')
	
	return w

@register.filter
def highlight_words(value, words, with_title=False):
	s = str(value)
	for word in words:
		w = build_word_regexp(word)
		if with_title:
			s = re.sub(r'(' + w + r')', r'<span class="hl" title="%s">\1</span>' % word.translation, s)
		else:
			s = re.sub(r'(' + w + r')', r'<span class="hl">\1</span>', s)
	return s

@register.filter
def hide_word(value, word):
	s = str(value)
	w = build_word_regexp(word)
	s = re.sub(r'(' + w + r')', r'_____', s)
	return s
	
@register.filter
def highlight_words_with_title(value, words):
	return highlight_words(value, words, True)

@register.filter
def get_success(value):
	return len(value.filter(is_passed=True))

@register.filter
def get_failed(value):
	return len(value.filter(is_passed=False))

@register.filter
def check_even(value):
	return (value % 2) == 0
