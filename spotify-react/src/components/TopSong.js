import React from "react";

export default function TopSongCard(props) {

    return (
        <div>
            <div className="flex items-center">
                {props.emotion === "joy" ?
                    <div className="rounded-lg shadow-lg border border-joy">
                        <div className={"flex justify-center p-6"}>
                            <img className="rounded-lg w-auto" src={props.topTrack.track.album.images[0].url}
                                 width={250}
                                 alt=""/>
                        </div>

                        <div className="w-auto">
                            <h5 className="text-joy text-4xl font-medium mb-2">{Math.round(props.maxEmotion * 10) / 10}%</h5>
                            <p className="text-gray-200 text-base mb-4">
                                The <span className="text-joy">happiest</span> song recently has been, <br/> <span
                                className={"text-white font-bold italic"}> {props.topTrack.track.name} </span>
                                <br/>
                                {props.topTrack.played_at}
                            </p>
                        </div>
                    </div>
                    :
                    props.emotion === "sadness" ?
                        <div className="rounded-lg shadow-lg border border-sadness">
                            <div className={"flex justify-center p-6"}>
                                <img className="rounded-lg w-auto"
                                     src={props.topTrack.track.album.images[0].url}
                                     width={250}
                                     alt=""/>
                            </div>

                            <div className="w-auto">
                                <h5 className="text-sadness text-4xl font-medium mb-2">{Math.round(props.maxEmotion * 10) / 10}%</h5>
                                <p className="text-gray-200 text-base mb-4">
                                    The <span className="text-sadness">saddest</span> song recently has been, <br/>
                                    <span className={"text-white font-bold italic"}> {props.topTrack.track.name} </span>
                                </p>
                            </div>
                        </div>

                        :
                        <div className="rounded-lg shadow-lg border border-anger">
                            <div className={"flex justify-center p-6"}>
                                <img className="rounded-lg w-auto"
                                     src={props.topTrack.track.album.images[0].url}
                                     width={250}
                                     alt=""/>
                            </div>

                            <div className="w-auto">
                                <h5 className="text-anger text-4xl font-medium mb-2">{Math.round(props.maxEmotion * 10) / 10}%</h5>
                                <p className="text-gray-200 text-base mb-4">
                                    The <span className="text-anger">angriest</span> song recently has been, <br/>
                                    <span className={"text-white font-bold italic"}> {props.topTrack.track.name} </span>
                                </p>
                            </div>
                        </div>

                }


            </div>
        </div>
    )
}
