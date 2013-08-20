import math
from operator import mul
import functools
#max terms in partial sum is length of list
#each partial sum can be expanded to some point... 1234 is only 4-term that can be expanded to full
#so, keep track of last term in each p-sum
#also, need to keep track of number of partial sums, so keep track of last term of the first n-1 p-sum
def checkNibs(val,suits):
	hnd = list(val[0:4])
	for i in range(hnd.count(10)):
		ind = hnd.index(10)
		hnd.remove(10)
		if suits[ind] == suits[4]:
			return 1
	return 0


def checkFlush(suits):
	pts = 0
	if suits[0] == suits[1] and suits[0] == suits[2] and suits[0] == suits[3]:
		pts+=4
		if suits[3] == suits[4]:
			pts +=1
	return pts

def checkFifteens(val):
	numValH = []
	numValL = []
	n15 = 0
	pSum = []
	ind = []
	numP = 0
	for v in val:
		if v < 7:
			numValL.append(v+1)
		elif v < 9:
			numValH.append(v+1)
		else:
			numValH.append(10)
	if len(numValL) < 1:
		return 0
	pSum = list(numValL)
	ind = list(range(len(numValL)))
	n = len(pSum)
	for j in range(2,n+1): #run through lengths of partial Sums
		m = len(pSum)
		newP = len(ind)-1
		for sumInd in range(numP,m): #run through partial Sums
			for index in range(ind[sumInd]+1,len(numValL)): #run through terms to add to this partial sum
				ppSum = pSum[sumInd]
				pSum.append(ppSum+numValL[index])
				ind.append(index)
		numP = newP
	fifteens = pSum.count(15)
	for card in numValH:
		fifteens+=pSum.count(15-card)
	return 2*fifteens
		
		
	

def checkMults(val):
	unVal = []
	for v in val:
		if v not in unVal:
			unVal.append(v)
	pts = 0
	for v in unVal:
		mult = val.count(v)
		if mult > 1:
			com = math.factorial(mult)/(math.factorial(2)*math.factorial(mult-2))
			pts += 2*com
	return pts


def checkRuns(val):
	unVal = []
	for v in val:
		if v not in unVal:
			unVal.append(v)
	unVal.sort()
	seq = [unVal.pop(0)]
	mult = [val.count(seq[0])]
	for v in unVal:
		if v == seq[len(seq)-1]+1:
			seq.append(v)
			mult.append(val.count(v))
		else:
			if len(seq) > 2:
				break
			seq = [v]
			mult = [val.count(v)]
	if len(seq) > 2:
		return len(seq) * functools.reduce(mul,mult,1)
	else: 
		return 0
	
	#found run, now need to find multiplicity of it

def handEval(hand):
	# hand stored as cards, 0-51. take mod(4) to get suit 1-S, 2-H, 3-D, 4-C. Divide by 4 to get value
	pts = 0
	val = []
	suits = []
	for card in hand:
		val.append(math.floor(card/4))
		suits.append(math.fmod(card,4)+1)
	pts += checkRuns(val)
	#print(pts)
	pts += checkMults(val)
	#print(pts)
	pts += checkFifteens(val)
	#print(pts)
	pts += checkFlush(suits)
	pts += checkNibs(val,suits)
	return pts

def start():
	ask = ['first','second','third','fourth','fifth','sixth']
	hand = []
	vals = {'a':0, '2':1, '3': 2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'t':9,'j':10,'q':11,'k':12}
	revVals = {0: 'a', 1:'2', 2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'10',10:'j',11:'q',12:'k'}
	revSuit = {1:'s',2:'h',3:'d',4:'c'}
	suit = {'s':1,'h':2,'d':3,'c':4}
	strHand = []
	print('Welcome to the Cribbage hand analyzer!')
	print('Please enter your hand in the form value_suit, i.e. jh for jack of hearts. Lowercase only, t for 10s!')
	for i in range(6):
		nott = True
		while nott:
			x = input('What is the ' + ask[i] + ' card in your hand? ')
			nott = True
			if x[0] not in vals or x[1] not in suit:
				print("Invalid card, uppercase only")
				continue
			cc = 4*vals[x[0]]+suit[x[1]]-1
			if cc in hand:
				print("That card's already in your hand!")
				continue
			else:
				if x[0] == 't':
					x = '10' + x[1]
				strHand.append(x)
				hand.append(cc)
				nott = False
	deck = set(range(52))-set(hand)
	disc = []
	possHands = []
	for i in range(len(hand)):
		for j in range(i+1,len(hand)):
			inds = set(range(6))-set([i,j])
			hnd = [hand[k] for k in inds]
			disc.append([i,j])
			possHands.append(hnd)
	pPts = [0]*15
	totalMax = [0,0,0]
	eachMax = []
	for i in range(15):
		eachMax.append([0,0])	
	for start in deck:
		for i in range(len(possHands)):
			hnd = list(possHands[i])
			hnd.append(start)
			pts = handEval(hnd)
			if pts >= totalMax[0]:
				totalMax[0] = pts
				totalMax[1] = start
				totalMax[2] = i
			if eachMax[i][0] <= pts:
				eachMax[i][0] = pts
				eachMax[i][1] = start
			pPts[i] += pts/46
	maxPts = max(pPts)
	ii = pPts.index(maxPts)
	avg = sum(pPts)/15
	print('The total average value for this hand is: %.2f' %avg)
	discard = disc[ii]
	discc = disc[totalMax[2]]
	maxStartVal = math.floor(totalMax[1]/4)
	maxStartSuit = math.fmod(totalMax[1],4)+1
	maxStart = revVals[maxStartVal]+revSuit[maxStartSuit]
	startVal = math.floor(eachMax[ii][1]/4)
	startSuit = math.fmod(eachMax[ii][1],4)+1
	start = revVals[startVal]+revSuit[startSuit]
	print('Your hand is', strHand[0], strHand[1], strHand[2], strHand[3], strHand[4], strHand[5])
	print('The maximum average value is: %.2f, achieved when you discard ' %maxPts,strHand[disc[ii][0]], 'and ', strHand[disc[ii][1]])
	print('The maximum hand you can achieve with this is: %.2f ' %eachMax[ii][0], 'when the starter is: ',start)
	if eachMax[ii][0] == totalMax[0]:
		print('This is the maximum value hand for any discard')
	else:
		print('The maximum value hand is: %.2f, achieved when you discard ' %totalMax[0], strHand[discc[0]], 'and ', strHand[discc[1]], ' and starter is ', maxStart)
	print('Hope this helps, please keep in mind the crib is not considered in these calculations!')
		
start()
