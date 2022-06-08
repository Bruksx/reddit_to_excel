import praw
from psaw import PushshiftAPI
import json
import datetime
import time
from prawcore.exceptions import Redirect

root = "C:/Users/Owner/Documents/projects/python/scrapper"

with open("var.json", "r") as f:
    var = json.loads(f.read())

now = time.time()
yesterday = now - 86400

reddit = praw.Reddit(
    client_id= var["id"],
    client_secret= var["secret"],
    password= var["password"],
    user_agent= "paceful agent f",
    username= var["username"],
)

api = PushshiftAPI(reddit)

class dataBot:
    def __init__(self, reddit, subreddit, api):
        self.reddit = reddit
        self.api = api
        self.subreddit = subreddit

    @staticmethod
    def get_list_of_subreddits():
        with open(root + "/text/subs.txt") as f:
            subs = f.readlines()
        li = [i[2:-1] for i in subs]
        return li
    
    @staticmethod
    def get_or_return_none(func):
        def wrap(*args, **kwargs):
            try:
                return func(*args,**kwargs)
            except Redirect:
                return None
        return wrap

    def get_all_mods(self):
        all_subs = self.get_list_of_subreddits()
        li = []
        try:
            for i in all_subs:
                bot = dataBot(reddit, i, api)
                li += bot.get_list_of_mods()
        except TypeError:
            pass
        return li

    def mod_occurence(self):
        all_mods = self.get_all_mods()
        data = {}
        for i in all_mods:
            data[str(i)] = all_mods.count(i)
        return data

    def test(self):
        sub = self.reddit.submission("uv7vhx").comments
        total = 0
        count = 0
        for i in sub:
            try:
                total += i.score
                count += 1
            except AttributeError:
                total += 0
                count += 0
        
        print(round(total/count, 2))
    
    @get_or_return_none
    def get_new_submissions(self):
        d  = datetime.date.today()
        #print(datetime.datetime(d.year, d.month, d.day).timestamp())
        #print(d.year, d.month, d.day)
        start_epoch=int(datetime.datetime(d.year, d.month, d.day).timestamp())
        data = list(self.api.search_submissions(after=start_epoch,
                subreddit= self.subreddit,
                filter=['url','author', 'title', 'subreddit'],
                limit=None))
        return data
    
    @get_or_return_none
    def get_new_submissions(self):
        new = self.reddit.subreddit(self.subreddit).new(limit = 500)
        result = []
        for i in new:
            if i.created_utc > yesterday:
                result.append(i)
        return result
    
    @get_or_return_none
    def get_number_of_members(self):
        return self.reddit.subreddit(self.subreddit).subscribers

    @get_or_return_none
    def submission_type(self):
        all_subs = self.get_new_submissions()
        text = 0
        non_text = 0
        for i in all_subs:
            if self.reddit.submission(i).is_self:
                text += 1
            else:
                non_text += 1
        return {
            "text": text,
            "non_text": non_text}
    
    def test_ratio(self, sub):
        ratio = sub.upvote_ratio
        net_upvotes = sub.score
        up_votes = net_upvotes
        down_votes = 0
        condition = True
        while condition:
            total = up_votes + down_votes
            if round(up_votes/total, 2) == ratio:
                condition = False
            print(round(up_votes/total, 2), ratio, total, up_votes, down_votes)
            up_votes += 1
            down_votes += 1
    
    def num_of_mods(self):
        mod_list = [i for i in self.reddit.subreddit(self.subreddit).moderator()]
        return len(mod_list)
    
    def list_of_mods(self):
        mod_list = [str(i) for i in self.reddit.subreddit(self.subreddit).moderator()]
        return (mod_list)

    def num_of_moderator_posts(self):
        mod_list = [i for i in self.reddit.subreddit(self.subreddit).moderator()]
        count = 0
        for i in self.get_new_submissions():
            if i.author in mod_list:
                count += 1
        return count
    
    @get_or_return_none
    def ratio_of_mod_to_subscribers(self):
        return round(self.num_of_mods() / self.get_number_of_members())
    
    @get_or_return_none
    def average_comment_score(self):
        all_posts = self.get_new_submissions()
        total = 0
        try:
            for post in all_posts:
                for comment in post.comments:
                    try:
                        total += comment.score
                    except AttributeError:
                        total += 0
            return round(total/len(all_posts), 2)
        except ZeroDivisionError:
            return None

    @get_or_return_none
    def get_list_of_mods(self):
        mod_list = [str(i) for i in self.reddit.subreddit(self.subreddit).moderator()]
        return mod_list
    
    def num_of_post(self):
        return len(self.get_new_submissions())
    
    def total_comments(self):
        total = 0
        for post in self.get_new_submissions():
            total += post.num_comments
        return total
    
    def average_comment_per_post(self):
        try:
            data = round(self.total_comments() /self.num_of_post())
            return data
        except ZeroDivisionError:
            return None
    
    def list_of_flairs(self):
        all_posts = self.get_new_submissions()
        list = set()
        for post in all_posts:
            if post.link_flair_text:
                list.add(post.link_flair_text)
        return list
        
    def num_of_automod_post(self):
        all_posts = self.get_new_submissions()
        count = 0
        try:
            for post in all_posts:
                if post.author.name == "AutoModerator":
                    count += 1
        except AttributeError:
            pass

        return count

    @get_or_return_none    
    def list_of_automod_flair(self):
        all_posts = self.get_new_submissions()
        list = []
        for post in all_posts:
            try:
                if str(post.author.name) == "AutoModerator":
                    list.append(post.link_flair_text)
            except AttributeError:
                pass
        return list

testbot = dataBot(reddit, "makinghiphop", api)
"""
start = time.time()
testbot.get_new()
print(time.time() - start)
start = time.time()
testbot.get_new_submissions()
print(time.time() - start)"""