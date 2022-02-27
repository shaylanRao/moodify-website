import React from "react";
import SearchGraph from "./SearchMoodGraph";

export default function SearchTrackValues(props) {

    return (
        <div className="">
            <br/>
            <h4>{props.predictSongName}</h4>
            <img src={props.predictSongUrl} alt="temp img" width="200" height="200"/>
            <SearchGraph anger={props.anger}
                         fear={props.fear}
                         joy={props.joy}
                         sadness={props.sadness}/>
        </div>
    )
}
