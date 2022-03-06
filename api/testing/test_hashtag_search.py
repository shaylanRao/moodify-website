import unittest

from twitter_data.hashtag_search import get_trackid_from_urls, get_user_s_tweets, clean_text


class TestHashtagSearch(unittest.TestCase):

    # testing with example data from twitter API
    def test_get_trackid_from_urls(self):
        normal_data = get_trackid_from_urls([{'url': 'https://t.co/P2L96QqKA7',
                                              'expanded_url': 'https://open.spotify.com/track/1pU5SijPp89lNrZHJL0166?si=srFVAl5PStyJ5nAzk1d7NA&utm_source=copy-link',
                                              'display_url': 'open.spotify.com/track/1pU5SijP…', 'indices': [35, 58]}])
        self.assertEqual(normal_data, "1pU5SijPp89lNrZHJL0166")

        normal_data = get_trackid_from_urls([{'url': 'https://t.co/xl5j9G9xSh',
                                              'expanded_url': 'https://open.spotify.com/track/2JoJrsEV15OzbijS47lids?si=D48kLuwmTvqzdqhPC50_Eg&utm_source=copy-link',
                                              'display_url': 'open.spotify.com/track/2JoJrsEV…', 'indices': [33, 56]}])
        self.assertEqual(normal_data, "2JoJrsEV15OzbijS47lids")

        # Missing the index of the required url
        erroneous_data = get_trackid_from_urls([{'url': 'https://t.co/xl5j9G9xSh',
                                                 'display_url': 'open.spotify.com/track/2JoJrsEV…',
                                                 'indices': [33, 56]}])
        self.assertIsNotNone(erroneous_data)
        self.assertEqual(erroneous_data, "")

        # Input has extra character
        boundary_data = get_trackid_from_urls([{'url': 'https://t.co/xl5j9G9xSh',
                                                'expanded_url': 'https://open.spotify.com/tracks/2JoJrsEV15OzbijS47lids?si=D48kLuwmTvqzdqhPC50_Eg&utm_source=copy-link',
                                                'display_url': 'open.spotify.com/track/2JoJrsEV…',
                                                'indices': [33, 56]}])
        self.assertEqual(boundary_data, "")

    # Returns a tweepy.cursor.ItemIterator object
    def test_get_user_s_tweets(self):
        normal_data = get_user_s_tweets("kwangyajail")
        self.assertIsNotNone(normal_data)

    def test_clean_text(self):
        normal_data = "This is a valid message"
        self.assertEqual(clean_text(normal_data), normal_data)

        # Standard normal entry with no cleaning needed
        normal_data = "This is still a valid entry\nEven though\n\nIt has new lines"
        self.assertEqual(clean_text(normal_data), "This is still a valid entry Even though  It has new lines")

        # Remove invalid characters
        normal_data = "Wow he said  get skepta  tell him to bring his skirt and blouse  🤣😂😂 Hahahahaha 🔥🔥🔥🔥 \n Listen now! \n FƎRИO - Microchip Riddim #FOREVERGOLDEN \n #Microchip "
        accepted_response = "Wow he said  get skepta  tell him to bring his skirt and blouse   Hahahahaha    Listen now!   FRO - Microchip Riddim #FOREVERGOLDEN   #Microchip "
        self.assertEqual(clean_text(normal_data), accepted_response)

        # Remove links
        normal_data = "Just up in #Spotify - one thing about a #pandemic, it will make you 'Lonely' - https://open.spotify.com/track/3cY9zQxblxRSH7B6kVWEFU\n@spotifyplaylsts\n@spotify\n@SpotifyPlaying\n #music #funk #love #house #covidlife #Radio #listenlive @SpotifyPlaylist\n#NowPlaying #VOTE"
        accepted_response = "Just up in #Spotify - one thing about a #pandemic, it will make you 'Lonely' -  @spotifyplaylsts @spotify @SpotifyPlaying  #music #funk #love #house #covidlife #Radio #listenlive @SpotifyPlaylist #NowPlaying #VOTE"
        self.assertEqual(clean_text(normal_data), accepted_response)

        # passing a nonstring
        erroneous_data = self
        self.assertIsNotNone(clean_text(erroneous_data))
        self.assertEqual(clean_text(erroneous_data), "")

    def test_name(self):
        pass


if __name__ == '__main__':
    unittest.main()

# Use below to run code in terminal
# python -m unittest test_sentiment_analyser.py
