#!/usr/local/bin python
# -*- coding: utf-8 -*-

import tweepy
import pickle

import auth_data

msg_new = "@ham_kts\n(自動)あたらしいフォロワーさんです．\n"
msg_rmv = "@ham_kts\n(自動)りむられました\n"
auth = tweepy.OAuthHandler(auth_data.api_key, auth_data.api_secret)
auth.set_access_token(auth_data.access_token, auth_data.access_token_secret)
api = tweepy.API(auth)

try:
    f = open('follower.pickle', 'br')
    old_user_set = pickle.load(f)
    print(old_user_set)
    print("ok")

except:
    f = open('follower.pickle', 'bw')
    l = api.followers_ids(screen_name = auth_data.user_name)
    old_user_set = set(l)
    pickle.dump(old_user_set.copy(), f)

finally:
    f.close()

l = api.followers_ids(screen_name = auth_data.user_name)
now_user_set = set(l)

new_user_set = now_user_set - old_user_set
removed_user_set = old_user_set - now_user_set

new_user_list =[]
removed_user_list =[]

for u in new_user_set:
    new_user_list.append(api.get_user(u))

for u in removed_user_set:
    removed_user_list.append(api.get_user(u))

txt = msg_new
print("new")
for u in new_user_list:
    print(u.screen_name)
    txt += '@' + u.screen_name + '\n'

if len(new_user_list) > 0:
    api.update_status(txt)

txt = msg_rmv
print("remove")
for u in removed_user_list:
    print(u.screen_name)
    txt += '@' + u.screen_name + '\n'

if len(removed_user_list) > 0:
    api.update_status(txt)

f = open('follower.pickle', 'bw')
pickle.dump(now_user_set.copy(), f)
