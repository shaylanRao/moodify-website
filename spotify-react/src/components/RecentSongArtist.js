import React from 'react';
import {Heading2, Heading4} from "@material-tailwind/react";

const list = [
    {
        id: 'a',
        firstname: 'Robin',
        lastname: 'Wieruch',
        year: 1988,
    },
    {
        id: 'b',
        firstname: 'Dave',
        lastname: 'Davidds',
        year: 1990,
    },
];

const List = (props) => (
    <div className="recently-played-sidebar w-full grow h-full shadow-md bg-white px-1 flex">
        <ul className="relative">
            <div className="recently-played-heading text-left">Recently Played</div>
            <br/>
            {props.tracks.map(track => (
                <li className="recently-played-card" key={track.track.id}>
                    <a className="flex items-center text-sm py-7 px-6 h-12 text-gray-400 text-ellipsis whitespace-nowrap rounded hover:text-gray-100 hover:bg-indigo-500 transition duration-300 ease-in-out"
                       href={track.track.external_urls.spotify} target="_blank" data-mdb-ripple="true" data-mdb-ripple-color="dark">
                        <img src={track.track.album.images[0].url} alt="Orange" className="w-10 h-10 mr-3"/>
                        <span className="text-left">{track.track.name} <br/>- {track.track.artists[0].name} </span>
                    </a>
                </li>
            ))
            }
        </ul>
    </div>
);

export default List;