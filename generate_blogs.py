import requests
import json
import re

# I use this script to generate the blogs and then i manually commit and push them.

f = open("token.txt", "r")
bot_token = f.read().replace('\n', '')
f.close()
f = open("sid.txt", "r")
server_id = f.read().replace('\n', '')
f.close()
url_base = f"https://discord.com/api/v10/"

class Image:
    def __init__(self, url):
        self.url = str(url)

    def ToHTML(self):
        html = f"<img src=\"{self.url}\">"
        return html
    
class Text:
    def __init__(self, string):
        self.string = string

    def ToHTML(self):

        html = self.string

        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        html = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', html)
        html = re.sub(r'__([^_]+)__', r'<u>\1</u>', html)
        html = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', html)
        html = html.replace('\n', '<br>')
        html += "<br>"

        return html

class Post:
    def __init__(self, contents, title):
        self.contents = contents
        self.title = title

    def ToHTML(self):
        return f"<h1>{self.title}</h1>" + "".join([string.ToHTML() for string in self.contents])

headers = {
    "Authorization": f"Bot {bot_token}"
}

resp = requests.get(f"{url_base}guilds/{server_id}/channels", headers=headers)

channel_list = []

if resp.status_code == 200:
    channels = resp.json()
    for channel in channels:
        channel_list.append([channel['id'], channel['name']])
else:
    print('err')

posts = []

for id in channel_list:
    resp = requests.get(f"{url_base}channels/{id[0]}/messages", headers=headers)
    title_prettier = str(id[1])
    title_prettier = title_prettier.replace('-', ' ')
    title_prettier = title_prettier.capitalize()
    if resp.status_code == 200:
        post_contents = []
        content = resp.json()
        for msg in content:
            #print(msg)
            if msg['attachments'] != []:
                for at in msg['attachments']:
                    post_contents.append(Image(at['url']))
            if msg['content'] != '':
                post_contents.append(Text(msg['content']))
            #print('\n')
        post_contents.reverse()
        posts.append(Post(post_contents, title_prettier))


for i in posts:
    title_ugly = str(i.title)
    title_ugly = title_ugly.lower().replace(' ', '+')
    f = open(f"blogs/{title_ugly}.html", "w")
    f.write(f"<!DOCTYPE html><html lang=\"en\"><head><title>{i.title}</title><link rel=\"stylesheet\" href=\"../style.css\"></head><body><div class=\"container MainView\"><span>")
    f.write(i.ToHTML())
    f.write("</span></div></body></html>")
    f.flush()
    f.close()


