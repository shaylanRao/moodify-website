import React from 'react';

export default function Sidebar(props) {
    function limitName(str) {
        if (str.length > 35) {
            return (str.substring(0, 35) + "...")
        }
        return str
    }

    return (
        <div className="recently-played-sidebar w-full grow h-full shadow-md bg-white px-1 flex" data-testid="sidebar">
            {props.tracks ?
                <ul className="relative">
                    <div className="recently-played-heading text-left px-3 py-5">Recently Played</div>
                    {props.tracks.map(track => (
                        <li className="recently-played-card" title={track.track.name}>
                            <a className="flex items-center text-sm py-7 px-6 h-12 text-gray-400 text-ellipsis whitespace-nowrap rounded hover:text-gray-100 hover:bg-indigo-500 transition duration-300 ease-in-out"
                               href={track.track.external_urls.spotify} target="_blank" data-mdb-ripple="true"
                               data-mdb-ripple-color="dark" rel="noreferrer">
                                <img src={track.track.album.images[0].url} alt="Orange" className="w-10 h-10 mr-3"/>
                                <span className="text-left">{limitName(track.track.name)}
                                    <br/>- {limitName(track.track.artists[0].name)} </span>
                            </a>
                        </li>
                    ))
                    }
                </ul>
                :
                <div>No Recent Tracks </div>
            }
        </div>
    )
}
