import json
from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
from pprint import pprint

class StanfordNLP:
    def __init__(self):
        self.server = ServerProxy(JsonRpc20(),
                                  TransportTcpIp(addr=("127.0.0.1", 8080)))

    def parse(self, text):
        return json.loads(self.server.parse(text))

nlp = StanfordNLP()
# user_input = "My son usually gets up at six every morning"
while(1):
	user_input = raw_input(">>> Input: ")
	result = nlp.parse(user_input)

	count = 0
	flag = 1
	start = []
	end = []
	for i, item in enumerate(result['sentences'][0]['words']):
		if flag == 1:
			x = ['last', 'this', 'next', 'every']
			if item[1]['PartOfSpeech'] == 'IN':
				start.append(count)
				flag = 0
			elif item[1]['Lemma'] in x:
				start.append(count)
				flag = 0
		elif flag == 0:
			if item[1]['PartOfSpeech'] == 'CD':
				end.append(count)
				flag = 1
			elif item[1]['PartOfSpeech'] == 'NNP' and result['sentences'][0]['words'][i+1][1]['PartOfSpeech'] != 'NN':
				end.append(count)
				flag = 1
			elif item[1]['PartOfSpeech'] == 'NNP' and result['sentences'][0]['words'][i+1][1]['PartOfSpeech'] != 'NNS':
				end.append(count)
				flag = 1
			elif item[1]['PartOfSpeech'] == 'NN' or  item[1]['PartOfSpeech'] == 'NNS' :
				end.append(count)
				flag = 1
		count = count + 1

	# print start
	# print end
	print "-----"
	# print "Input : ", user_input
	for i in range(0,len(start)):
		time =  result['sentences'][0]['text'].split(' ')[start[i]:end[i]+1]
		time_type = result['sentences'][0]['text'].split(' ')[end[i]]
		if nlp.parse(time_type)['sentences'][0]['words'][0][1]['NamedEntityTag'] in ['NUMBER', 'DATE', 'TIME']:
			print ' '.join(time)
	print "-----"


# Input: I usually get up at 5:00 in the early morning every Sunday morning in summer at school
#-----
# at 5:00
# in the early morning
# on Sunday
# in summer
#------
