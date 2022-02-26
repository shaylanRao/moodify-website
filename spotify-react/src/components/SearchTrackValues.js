import React from "react";

export default function SearchTrackValues(props) {

    return (
        <div className="">
            <br/>
            <h4>{props.predictSongName}</h4>
            <img src={props.predictSongUrl} alt="temp img" width="200" height="200"/>
            <div>anger : {props.anger}</div>
            <div>fear : {props.fear}</div>
            <div>joy : {props.joy}</div>
            <div>sadness : {props.sadness}</div>
        </div>
    )
}
