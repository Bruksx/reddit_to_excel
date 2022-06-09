from bot import dataBot, reddit, api, root
import time

testbot = dataBot(reddit, "makinghiphop", api)

def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end  = time.time() - start
        print(f"took {end} seconds")
    return wrapper

class Fetch:
    def __init__(self):
        self.all_subs = dataBot.get_list_of_subreddits()
        self.sub_groups = [
            "community resources",
            "hiphop",
            "large subreddits",
            "music creation",
            "music discussion",
            "music general",
            "music sharing",
            ]
    def get_subreddits_in_subgroup(self, subgroup):
        with open(root + f"/text/subgroups/{subgroup}.txt", "r") as f:
            subgroups = f.readlines()
            return [i[:-1] for i in subgroups]

    def to_string(self, collection):
        string = ""
        try:
            for i in collection:
                string += f" {str(i)}, "
            return string.strip()
        except TypeError:
            return None

    def all_data(self, sub):
        testbot = dataBot(reddit, sub, api)
        data = {
            "name": testbot.subreddit,
            "all_mods": self.to_string(testbot.get_list_of_mods()),
            "amount of subscribers": testbot.get_number_of_members(),
            "text submission": testbot.submission_type()["text"],
            "non text submission": testbot.submission_type()["non_text"],
            "number of mods": testbot.num_of_mods(),
            "list of mods": self.to_string(testbot.get_list_of_mods()),
            "number of moderator posts": testbot.num_of_moderator_posts(),
            "moderator to subscribers ratio": testbot.ratio_of_mod_to_subscribers(),
            "average comment score": testbot.average_comment_score(),
            "number of post": testbot.num_of_post(),
            "total comments": testbot.total_comments(),
            "average comment per post": testbot.average_comment_per_post(),
            "list of flairs": self.to_string(testbot.list_of_flairs()),
            "number of automod post": testbot.num_of_automod_post(),
            "list of automod flair": self.to_string(testbot.list_of_automod_flair())
        }
        return data
    
    def all_sub_data(self):
        for i in dataBot.get_list_of_subreddits():
            time.sleep(60)
            yield self.all_data(i)

