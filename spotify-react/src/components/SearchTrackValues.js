import React from "react";
import SearchGraph from "./SearchMoodGraph";

export default function SearchTrackValues(props) {

    return (
        <div data-testid="search-track-values">
            <br/>
            <h4 className="text-left px-4 font-medium text-gray-400">{props.predictSongName} - {props.predictSongArtist}</h4>
            <div className="flex">
                <div>
                    <img src={props.predictSongUrl} alt="temp img" width="200" height="200"/>
                </div>
                <div>
                    <SearchGraph anger={props.anger}
                                 fear={props.fear}
                                 joy={props.joy}
                                 sadness={props.sadness}/>
                </div>
            </div>
        </div>
    )
}
