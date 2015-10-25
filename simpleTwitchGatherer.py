import thread, time, datetime, csv
import requests, json
session = requests.Session()
global totalBadRequests
totalBadRequests = 0

def input_thread(L):
	raw_input()
	L.append(None)

def do_rec():
	global totalBadRequests
	L = []
	thread.start_new_thread(input_thread, (L,))
	bad_requests = 0
	good_requests = 0
	while len(L) == 0 and bad_requests <= tolerance:
		time.sleep(sleeptime)
		
		r = session.get("https://api.twitch.tv/kraken/streams/" + streamer)
		
		if r.status_code != requests.codes.ok:
			print "!!!! Request Failed !!!! \a"
			totalBadRequests += 1
			bad_requests += 1
			good_requests = 0
		else:
			good_requests += 1
			if(good_requests >= 5):
				bad_requests = 0
				good_requests = 0

			jsonObject = r.json()

			if jsonObject is None or jsonObject['stream'] is None: 
				print "!!!! Stream is offline !!!!"
				break

			num_viewers = jsonObject['stream']['viewers']
			num_followers = jsonObject['stream']['channel']['followers']
			num_views = jsonObject['stream']['channel']['views']
			currTime = datetime.datetime.time(datetime.datetime.now())
			str_game = jsonObject['stream']['game']
			if str_game is None:
				str_game = "No Game"

			print "Health Check: ", num_viewers, num_followers, num_views, datetime.datetime.time(datetime.datetime.now())

			currRowToWrite = [num_viewers, num_followers, num_views, currTime, str_game.encode('utf8')]
			wr.writerow(currRowToWrite)

streamer = raw_input("Please enter the streamer: ")
sleeptime = float(raw_input("Please input sleep time: "))
tolerance = raw_input("Please input bad request tolerance: ")
filename = streamer + "_" + str(datetime.datetime.now().time()).replace(":", "_").replace(".", "_") + ".csv"
resultFile = open(filename, "a")
wr = csv.writer(resultFile, delimiter=",")
rowToWrite = ["Viewers","Followers","Views","Timestamp","Game"]
wr.writerow(rowToWrite)

print "<Press \"Enter\" to stop>"
do_rec()

print "Closing csv and session"
session.close()
resultFile.close()

print "Total Bad Requests: ", totalBadRequests