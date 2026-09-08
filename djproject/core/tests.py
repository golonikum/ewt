# coding=utf-8
from django.test import TestCase
from core.config import get_csv_from_words, get_words_from_csv, process_sentences
from core.models import Word, SpeechPart, Sentence, Group
from django.http import HttpResponse
from django.contrib.auth.models import User
from datetime import datetime


# Django only creates the test database for cases that declare they need one,
# and initial_data.json is no longer auto-loaded, so the speech parts these
# tests look up have to be requested explicitly.
class get_csv_from_words_TestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.default_sp = SpeechPart.objects.all()[0]
        self.user = User.objects.create(username='User', password='12345')
    
    def tearDown(self):
        self.user.delete()

    def test_success_simple(self):
        self.words = list()
        for i in range(2):
            self.words.append(Word.objects.create(created=datetime.now(), user=self.user, signature='word'+str(i), translation='tr of word'+str(i), speech_part=self.default_sp, transcription='tran of word'+str(i)))
        response = get_csv_from_words(HttpResponse(), self.words)
        reader = response.content.decode('utf-8').split('\r\n')
        for i, line in enumerate(reader):
            if i == 0:
                self.assertEqual(line, "signature;translation;speech part;transcription;synonyms;sentences;groups")
            elif i - 1 < len(self.words):
                self.assertEqual(line, "%s;%s;%s;%s;;;" % (self.words[i-1].signature, self.words[i-1].translation, self.words[i-1].speech_part, self.words[i-1].transcription))

    def test_success_sentence_without_translation(self):
        self.words = [Word.objects.create(created=datetime.now(), user=self.user, signature='word', translation='tr of word', speech_part=self.default_sp, transcription='tran of word')]
        sentence = Sentence.objects.create(created=datetime.now(), user=self.user, body='sentence')
        self.words[0].sentences.add(sentence)
        response = get_csv_from_words(HttpResponse(), self.words)
        reader = response.content.decode('utf-8').split('\r\n')
        for i, line in enumerate(reader):
            if i > 0 and i < len(self.words):
                self.assertEqual(line, "%s;%s;%s;%s;;sentence;" % (self.words[i].signature, self.words[i].translation, self.words[i].speech_part, self.words[i].transcription))

    def test_success_2_sentences(self):
        self.words = [Word.objects.create(created=datetime.now(), user=self.user, signature='word', translation='tr of word', speech_part=self.default_sp, transcription='tran of word')]
        sentence1 = Sentence.objects.create(created=datetime.now(), user=self.user, body='sentence1', translation='tr of sentence1')
        sentence2 = Sentence.objects.create(created=datetime.now(), user=self.user, body='sentence2', translation='tr of sentence2')
        self.words[0].sentences.add(sentence1)
        self.words[0].sentences.add(sentence2)
        response = get_csv_from_words(HttpResponse(), self.words)
        reader = response.content.decode('utf-8').split('\r\n')
        for i, line in enumerate(reader):
            if i > 0 and i < len(self.words):
                self.assertEqual(line, "%s;%s;%s;%s;;sentence1[tr of sentence1], sentence2[tr of sentence2];" % (self.words[i].signature, self.words[i].translation, self.words[i].speech_part, self.words[i].transcription))

    def test_success_unicode(self):
        self.words = [Word.objects.create(created=datetime.now(), user=self.user, signature='word', translation=u'перевод', speech_part=self.default_sp, transcription=u'\x0296\x105\x089')]
        response = get_csv_from_words(HttpResponse(), self.words)
        reader = response.content.decode('utf-8').split('\r\n')
        for i, line in enumerate(reader):
            if i > 0 and i < len(self.words):
                self.assertEqual(line, "%s;%s;%s;%s;;;" % (self.words[i].signature, self.words[i].translation, self.words[i].speech_part, self.words[i].transcription))

class get_words_from_csv_TestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.default_sp = SpeechPart.objects.all()[0]
        self.user = User.objects.create(username='User', password='12345')
        self.user2 = User.objects.create(username='User2', password='123')
        self.header = "signature;translation;speech part;transcription;synonyms;sentences;groups\r\n"
        self.csv_data = list()
    
    def tearDown(self):
        self.user.delete()
        self.user2.delete()

    def test_failed_header_is_not_correct(self):
        self.csv_data.append("self.header;self.header;self.header;self.header\r\n")
        self.csv_data.append("word;слово;verb;no;;;\r\n")
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)

    def test_failed_incorrect_data_num_of_entities(self):
        self.csv_data.append(self.header)
        self.csv_data.append("слово;verb;no;;;\r\n")
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)

    def test_failed_data_null(self):
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)
       
    def test_failed_incorrect_data_empty(self):
        self.csv_data.append(self.header)
        self.csv_data.append(";слово;verb;no;;;\r\n")
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)

        self.csv_data.pop(-1)
        self.csv_data.append("word;;verb;no;;;\r\n")
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)

    def test_failed_incorrect_data(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word2;слово1;verb;no;;;\r\n")
        self.csv_data.append("word3;слово2;verb;no;;;\r\n")
        self.csv_data.append(";слово;verb;no;;;\r\n")
        self.assertRaises(ValueError, get_words_from_csv, self.csv_data, self.user)
        self.assertEqual(0, len(Word.objects.all()))

    def test_success_some_users(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verb;no;;;\r\n")        
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.csv_data.pop(-1)
        self.csv_data.append("word;слово 2;verb;now;;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user2)

        self.assertEqual(1, len(Word.objects.filter(user=self.user)))
        self.assertEqual(1, len(Word.objects.filter(user=self.user2)))

    def test_success_some_users_with_the_same_words(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verb;no;;;\r\n")        
        self.csv_data.append("word1;слово1;verb;no;;;\r\n")
                
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.words = get_words_from_csv(self.csv_data, self.user2)

        self.assertEqual(2, len(Word.objects.filter(user=self.user)))
        self.assertEqual(2, len(Word.objects.filter(user=self.user2)))

    def test_success_end_empty_space(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verb;no;;;\r\n")
        self.csv_data.append("\r\n")       
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.assertEqual(1, len(self.words))
        self.assertEqual(1, len(Word.objects.all()))

    def test_success_word_already_exist(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verb;no;;;\r\n")
        
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.assertEqual(1, len(Word.objects.all()))
        
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.assertEqual(2, len(Word.objects.all()))

    def test_success_not_existent_speech_part(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verd;no;;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(1, len(self.words))
        self.assertEqual(1, len(Word.objects.all()))
        self.assertEqual(self.default_sp.name, self.words[0].speech_part.name)

    def test_success_similar_speech_part(self):
        sp = SpeechPart.objects.filter(name__contains='verb')[0]
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;verb;no;;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(1, len(Word.objects.all()))
        self.assertEqual(sp.name, self.words[0].speech_part.name)

    def test_success_simple(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;" + self.default_sp.name + ";no;;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(1, len(self.words))
        self.assertEqual(1, len(Word.objects.all()))
        self.assertEqual('word', self.words[0].signature)
        self.assertEqual('слово', self.words[0].translation)
        self.assertEqual(self.default_sp.name, self.words[0].speech_part.name)
        self.assertEqual('no', self.words[0].transcription)
        
    def test_success_1_synonym(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;word2;;\r\n")
        self.csv_data.append("word2;слово2;noun;no;word1;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(2, len(self.words))
        self.assertEqual('word2', self.words[0].synonyms.all()[0].signature)
        self.assertEqual('word1', self.words[1].synonyms.all()[0].signature)
        
    def test_success_synonyms(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;word3;;\r\n")
        self.csv_data.append("word2;слово2;noun;no;word3;;\r\n")
        self.csv_data.append("word3;слово3;noun;no;word1, word2;;\r\n")        
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(3, len(Word.objects.all()))
        self.assertEqual(3, len(self.words))
        self.assertEqual('word3', self.words[0].synonyms.all()[0].signature)
        self.assertEqual('word3', self.words[1].synonyms.all()[0].signature)
        self.assertTrue('word1' in [self.words[2].synonyms.all()[0].signature, self.words[2].synonyms.all()[1].signature])
        self.assertTrue('word2' in [self.words[2].synonyms.all()[0].signature, self.words[2].synonyms.all()[1].signature])

    def test_success_synonyms_speech_part(self):
        sp = SpeechPart.objects.filter(name__contains='verb')[0]
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;;;\r\n")
        self.csv_data.append("word3;слово3;verb;no;word1;;\r\n")
        self.csv_data.append("word1;слово2;verb;no;word3;;\r\n")
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(3, len(Word.objects.all()))
        self.assertEqual(3, len(self.words))
        self.assertEqual(0, len(self.words[0].synonyms.all()))
        self.assertEqual('word1', self.words[1].synonyms.all()[0].signature)
        self.assertEqual(sp.name, self.words[1].synonyms.all()[0].speech_part.name)
        self.assertEqual('word3', self.words[2].synonyms.all()[0].signature)

    def test_success_groups(self):
        gr1 = Group.objects.create(created=datetime.now(), name='group1', user=self.user)
        gr2 = Group.objects.create(created=datetime.now(), name='group2', user=self.user)
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;;;group1\r\n")
        self.csv_data.append("word2;слово2;noun;no;;;group2, group1\r\n")        
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(2, len(Word.objects.all()))
        self.assertEqual(2, len(Group.objects.all()))
        self.assertEqual(2, len(self.words))
        self.assertEqual(gr1.name, self.words[0].groups.all()[0].name)
        self.assertTrue(gr1.name in [self.words[1].groups.all()[0].name, self.words[1].groups.all()[1].name])
        self.assertTrue(gr2.name in [self.words[1].groups.all()[0].name, self.words[1].groups.all()[1].name])

    def test_success_group_not_exist(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;;;not exist group\r\n")       
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(1, len(Word.objects.all()))
        self.assertEqual(1, len(Group.objects.all()))
        self.assertEqual(1, len(self.words))
        self.assertEqual('not exist group', self.words[0].groups.all()[0].name)

    def test_success_group_empty_space(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word1;слово1;noun;no;;;        \r\n")       
        self.words = get_words_from_csv(self.csv_data, self.user)

        self.assertEqual(1, len(Word.objects.all()))
        self.assertEqual(0, len(Group.objects.all()))

    def test_success_sentence_empty_space(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;noun;no;;       ;\r\n")       
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.assertEqual(0, len(Sentence.objects.all()))
        self.assertEqual(1, len(Word.objects.all()))

    def test_success_sentence_incorrect(self):
        self.csv_data.append(self.header)
        self.csv_data.append("word;слово;noun;no;;dfsdfsdf[;\r\n")       
        self.words = get_words_from_csv(self.csv_data, self.user)
        self.assertEqual(0, len(Sentence.objects.all()))
        self.assertEqual(1, len(Word.objects.all()))
        
class process_sentences_TestCase(TestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.default_sp = SpeechPart.objects.all()[0]
        self.user = User.objects.create(username='User2', password='12345')
        self.csv_data = list()
        self.word = Word.objects.create(created=datetime.now(),
                                   user=self.user,
                                   signature='word', 
                                   translation='translation',
                                   speech_part=self.default_sp)
    
    def tearDown(self):
        self.user.delete()

    def test_success_body_absent(self):
        self.word.temp = dict({'sentences': '[translation of sentence]'})
        self.assertEqual(0, len(Sentence.objects.all()))

    def test_success_simple(self):
        self.word.temp = dict({'sentences': 'Sentence 1.[Translation of sentence 1...] | Se nte nce no 2. | Sent3[tr_of_s3]'})
        process_sentences(self.word)

        self.assertEqual(3, len(Sentence.objects.all()))
        self.assertEqual('Translation of sentence 1...', Sentence.objects.get(body='Sentence 1.').translation)
        self.assertEqual('Sent3', Sentence.objects.get(translation='tr_of_s3').body)
        self.assertEqual(None, Sentence.objects.get(body='Se nte nce no 2.').translation)

    def test_success_many_sentences(self):
        s1 = Sentence.objects.create(created=datetime.now(), body='sentence 1', user=self.user, translation='translation 1')
        s2 = Sentence.objects.create(created=datetime.now(), body='sentence 2', user=self.user)
        self.word.temp = dict({'sentences': 'sentence 1 | sentence 3[translation 3] | sentence 2[kkk]'})
        process_sentences(self.word)

        self.assertEqual(3, len(Sentence.objects.all()))
        self.assertTrue(s1 in self.word.sentences.all())
        self.assertTrue(s2 in self.word.sentences.all())
        self.assertEqual('translation 3', Sentence.objects.get(body='sentence 3').translation)
