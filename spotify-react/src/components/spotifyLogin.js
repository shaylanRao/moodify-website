import React from "react";

export default function Login(props) {
    const CLIENT_ID = "ed61ad2eb1ac48f38a5971328cec9f01"
    const REDIRECT_URI = "http://localhost:8080"
    const AUTH_ENDPOINT = "https://accounts.spotify.com/authorize"
    const RESPONSE_TYPE = "token"

    return (
        <div>
            {!props.token ?
                <a href={`${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}`}>Login
                    to Spotify</a>
                : <button onClick={props.logout}>Logout</button>}
        </div>


    )
}

