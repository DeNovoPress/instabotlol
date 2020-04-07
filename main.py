import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from instapy import InstaPy

## Start a simple HTTP Server

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):	
  #Handler for the GET requests
  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()
    # Send the html message
    self.wfile.write("ok")
    return
  
server = HTTPServer(('', 8080), myHandler)
print 'Started httpserver on port 8080'
	
#Wait forever for incoming htto requests
server.serve_forever()


## Instapy Documentation: https://github.com/timgrossmann/InstaPy/blob/master/DOCUMENTATION.md

session = InstaPy(username=os.environ.get('USER'), password=os.environ.get('PASS'), headless_browser=True)
session.login()

session.set_simulation(enabled=os.environ.get('SIMULATION'))

## Set quota limits to keep Instagram from banning you because it thinks you're a bot

session.set_quota_supervisor(enabled=True, sleep_after=["likes", "comments_d", "follows", "unfollows", "server_calls_h"], sleepyhead=True, stochastic_flow=True, notify_me=False,
peak_likes_hourly=51, peak_likes_daily=385, peak_comments_hourly=12, peak_comments_daily=82, peak_follows_hourly=18, peak_follows_daily=411, peak_unfollows_hourly=35,
peak_unfollows_daily=402, peak_server_calls_hourly=None, peak_server_calls_daily=4200)

## Like the images matching either of these tags and not some others
session.like_by_tags(["novels", "books", "authors", "writers" "reading"], amount=5)
session.set_dont_like(["mein kampf", "nsfw"])

## Auto-follow half of the time
session.set_do_follow(True, percentage=50)

## Auto-Commenting - Disabled by default
session.set_do_comment(False, percentage=50)
session.set_comments(["Nice!", "Sweet!", "Beautiful :heart_eyes:"])

## Additional filters
session.set_skip_users(skip_private=True, private_percentage=100, skip_no_profile_pic=True, no_profile_pic_percentage=100,
 skip_business=False, skip_non_business=False, business_percentage=100, skip_business_categories=[], dont_skip_business_categories=[])

## Dont waste time following people with over 8.5k followers
session.set_relationship_bounds(enabled=True, max_followers=8500)

session.end()
