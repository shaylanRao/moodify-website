import React from "react";

export default function SpotifyLogin() {
    const CLIENT_ID = "ed61ad2eb1ac48f38a5971328cec9f01"
    const REDIRECT_URI = "http://localhost:8080"
    const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
    const RESPONSE_TYPE = "token"
    const SCOPE = "playlist-modify-private user-read-recently-played"

    return (
        <div data-testid="spotify-login">
            <button>
                <a className="rounded-full spotify-login-button py-3 px-6"
                   href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}&scope=${SCOPE}`}>
                    <i className="fa fa-spotify"></i>   Login to Spotify
                </a>
            </button>
        </div>


    )
}

