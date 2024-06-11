from sick_tag_loc_connector.api import RestClient
from sick_tag_loc_connector.api.feed import Feed
from sick_tag_loc_connector.api.tag import Tag



api_key = "17254faec6a60f58458308763"
url = "http://192.168.225.2:8080/sensmapserver/api/"

rest_client = RestClient(url, api_key)

feed = Feed.get(rest_client, "1")
print(feed.description)