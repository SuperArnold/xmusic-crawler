#!/usr/bin/env python

import os
import configparser
import logging

from database.connection import Connection
from database.artistrepo import ArtistRepo

from provider.musicvideoinfo.spotifyprovider import SpotifyProvider

if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read("config.cfg")

    logging.basicConfig(
        filename = config["LOGGING"]["file"],
        level = config["LOGGING"]["level"],
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    db = Connection(config["DATABASE"]["username"],
            config["DATABASE"]["password"],
            config["DATABASE"]["host"],
            config["DATABASE"]["port"],
            config["DATABASE"]["database"])
    
    artist_repo = ArtistRepo(db.getSession())

    """
    Fetching the information of the artist name from data provider.
    """
    musicVideoInfoProvider = SpotifyProvider()
    
    target = "Ed Sheeran"
    artists = musicVideoInfoProvider.getArtistsByName(target)
    # We got two artist here, but the first artist is more accurate than other.
    # It's the tuple in the list of the artists, the first attribute is artist id 
    # that given by provider, and the second attribute is the entity object of 
    # Artist.
    artist_id = artists[0][0]
    artist = artists[0][1]
    artist.albums = []

    # It's the tuple in the list of albums, the first attribute is the album id
    # that given by provider, and the second attribute is the entity object of 
    # Album.
    albums = musicVideoInfoProvider.getAlbumsByArtistId(artist_id)
    for (album_id, album) in albums:
        tracks = musicVideoInfoProvider.getTracksByAlbumId(album_id)
        album.tracks = tracks
        artist.albums.append(album)
   
    logging.info("Fetching(" + target + ") done.")
    logging.debug(artist)

    """
    Insert the fetching result into xmusic-db.
    """
    logging.info("Store the fetching result(" + target + ") into database.")
    artist_repo.save(artist)

    """
    Fetching the information of the artist name from xmusic-db.
    """
    artists = artist_repo.getArtistsByName(target)
    logging.info("Artist(" + target + ") information in the database.")
    logging.debug(artists)

