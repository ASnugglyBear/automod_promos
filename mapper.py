#! /usr/bin/python3

import pystache # https://github.com/defunkt/pystache, install directions with pip3 recommended
import csv


template = """
#
# These are generated with a program. Move them out of the generated section if you edit them by hand 
#

#
#  START GENERATED SECTION
# 
{{#promotion}}
__
# Cross promotion to {{{subreddit}}}
comment: 'Cross Promotion: In addition to talking about {{{title}}} here, readers of this post can check out {{{subreddit}}}'
type: submission
title+body: [{{{list_of_keywords}}}]
{{/promotion}}


#
#  END GENERATED SECTION
# 

"""

def promotion_info(subreddit_link,keywords):
  cleaned_subreddit_name = subreddit_link.strip()
  cleaned_subreddit_name = cleaned_subreddit_name[cleaned_subreddit_name.find("/"):]
  return {
      'subreddit':cleaned_subreddit_name,
      'title':'{{match}}',
      'list_of_keywords':keywords
      }

def promotions_for_game(subreddit_link, game_string):
  games = ", ".join(["'"+game+"'" for game in game_string.split(",")])
  return promotion_info(subreddit_link,games)


with open("GamesMappedToSubreddits.csv","r") as csvfile:
  map_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
  promotions = [promotions_for_game(row[0],row[1]) for row in map_reader]
  print(template)
  print(promotions)
  rendered = pystache.Renderer().render(template,{"promotion":promotions})
 # print(rendered)
  open("output.yaml","w+").write(rendered)



