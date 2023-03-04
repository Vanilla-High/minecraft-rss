import os
import xml.etree.ElementTree as ET
from requests import get
import time
from discord_webhook import DiscordWebhook, DiscordEmbed
import shutil


def main():
    rss = mc_rss_to_list()
    with open("last-edited.txt") as log:
        previous_epoch = float(log.read())
        newest_epoch = previous_epoch
    post_types = [
        "A Minecraft Java Snapshot",
        "A Minecraft Java Pre-Release",
        "A Minecraft Java Release Candidate",
        "A Minecraft Java Release",
    ]

    update_log = False
    mc_url_pre = "https://www.minecraft.net"
    web_hook_pfp = "https://uovh.net/mc-rss-images/favicon-96x96.webp"
    for item in rss:
        publish_epoch = time_convert(item['pubDate'])
        if publish_epoch > newest_epoch:
            newest_epoch = publish_epoch
        if previous_epoch >= publish_epoch:
            print("No (more) updated posts")
            break
        update_log = False

        if item["description"] not in post_types:
            print("Post not related to minecraft updates.")
        else:
            image_file_name = item['imageURL'].split('/')[6]
            download_image(f"{mc_url_pre}/{item['imageURL']}", image_file_name)
            webhook = DiscordWebhook(
                url=os.environ['test_webhook_url'],
                username=item['primaryTag'],
                avatar_url=web_hook_pfp
            )
            print(web_hook_pfp)
            embed = DiscordEmbed(title=item['title'], description=item['description'])
            embed.set_url(item['link'])
            embed.set_image(f"{mc_url_pre}/{item['imageURL']}")
            print(f"{mc_url_pre}/{item['imageURL']}")
            embed.set_footer(text=item['pubDate'])
            webhook.add_embed(embed)
            webhook.execute()

    if update_log:
        with open("last-edited.txt", "w") as log:
            log.write(str(newest_epoch))


def time_convert(datetime):
    pub_date = datetime.split()
    p_weekday = pub_date[0][:-1]
    p_day = pub_date[1]
    p_mon = pub_date[2]
    p_year = pub_date[3]
    p_time = pub_date[4]
    p_date_form = time.strptime(f"{p_weekday} {p_mon} {p_day} {p_time} {p_year}")
    p_epoch = time.mktime(p_date_form)
    return p_epoch


def mc_rss_to_list():
    rss_url = "https://www.minecraft.net/en-us/feeds/community-content/rss"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36"
    }
    req = get(url=rss_url, headers=headers)
    root = ET.fromstring(req.content)
    rss_list = []
    for item in root.iter('item'):
        rss_item = {
            item[0].tag : item[0].text,
            item[1].tag : item[1].text,
            item[2].tag : item[2].text,
            item[3].tag : item[3].text,
            item[4].tag : item[4].text,
            item[5].tag : item[5].text,
        }
        rss_list.append(rss_item)
    return rss_list

def download_image(url, file_name):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/107.0.0.0 Safari/537.36"
    }
    res = get(url, stream = True, headers=headers)
    if res.status_code == 200:
        with open(images/file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ',file_name)
    else:
        print('Image Couldn\'t be retrieved')

if __name__ == "__main__":
    main()
    # 1677423600.0
