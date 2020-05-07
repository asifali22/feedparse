import feedparser
import time
import json
import os


def get_news_feed_from_url(url: str) -> feedparser.FeedParserDict:
    """
    Returns raw news feed from the provided url. The function doesn't raise any exception
    with a wrong url. The exception is encoded as part of response or returned dictionary.
    :param url: RSS Url to load feed from
    :return: raw feed
    """
    feed = feedparser.parse(url)
    return feed


def get_latest_feed(feed: feedparser.FeedParserDict, latest_published_time: float) -> (list, float):

    """
    :param feed: Loaded feed
    :param latest_published_time: time in epochs to compare and get latest feed
    :return: list of feeds which are newer than specified time
    """

    latest_feed = []
    next_latest_time = latest_published_time
    if feed:
        for entry in feed.entries:
            if time.mktime(entry.published_parsed) > latest_published_time:
                latest_feed.append(entry)
                if time.mktime(entry.published_parsed) > next_latest_time:
                    next_latest_time = time.mktime(entry.published_parsed)
    else:
        return [], next_latest_time
    return latest_feed, next_latest_time


def get_feed_as_csv_strings(feeds: feedparser.FeedParserDict) -> list:
    pass


def get_formatted_json_feeds(feeds: list) -> json:

    """
    Picks required fields from the feeds if present and return json formatted string.
    :param feeds: Feeds to be parsed.
    :return: json formatted feed string
    """

    json_feeds = []

    for feed in feeds:
        current_feed = {}

        if "title" in feed:
            current_feed["title"] = feed["title"]

        if "links" in feed:
            link_list = []
            for link in feed["links"]:
                if "href" in link:
                    current_link = dict()
                    current_link["link"] = link["href"]
                    link_list.append(current_link)

            if link_list:
                current_feed["links"] = link_list

        if "summary" in feed:
            current_feed["summary"] = feed["summary"]

        if "published" in feed:
            current_feed["published"] = feed["published"]

        if "published_parsed" in feed:
            current_feed["published_parsed"] = feed["published_parsed"]

        json_feeds.append(current_feed)

    return json.dumps(json_feeds)


def get_last_time(filename: str) -> float:

    """
    Parses last time used to fetch data from rss feed. Returns None if the time is invalid.
    :param filename: Filename which stores the time.
    :return: time in float (epochs)
    """

    current_time = time.time()

    if os.path.isfile(filename):
        fp = open(filename, 'r')
        t = fp.read()
        fp.close()
        try:
            t = float(t)
            return t
        except ValueError as e:
            print("Invalid time in {}".format(filename))
            return None
    else:
        fp = open(filename, 'w')
        fp.write(str(current_time))
        fp.close()
        return current_time


def create_new_json_feed_file(filename, formatted_feed) -> None:

    """
    Creates a new json feed file and writes to the specified file.
    :param filename: output file
    :param formatted_feed: feeds to be written
    :return: None
    """

    fp = open(filename, 'w')
    fp.write(formatted_feed)
    fp.close()


def update_last_time_file(filename, last_time) -> None:

    """
    Updates or overwrites the data of the file holding last time of fetch
    with the updated value received.
    :param filename: Time file
    :param last_time: new time to be written
    :return: None
    """

    fp = open(filename, 'w')
    fp.write(str(last_time))
    fp.close()


if __name__ == "__main__":

    latest_time_recorded = None

    rss_url = "https://www.indiatoday.in/rss/home"
    last_time_file = "lasttime.time"
    latest_published_time = get_last_time(last_time_file)
    json_output_file = "newsfeed.{}.json"

    if latest_published_time:
        news_feed = get_news_feed_from_url(rss_url)
        latest_feed, latest_time_recorded = get_latest_feed(news_feed, latest_published_time)
        json_formatted_feed = get_formatted_json_feeds(latest_feed)
        create_new_json_feed_file(json_output_file.format(int(latest_published_time)), json_formatted_feed)
        update_last_time_file(last_time_file, latest_time_recorded)
    else:
        print("Make sure time file has correct epoch time.")
