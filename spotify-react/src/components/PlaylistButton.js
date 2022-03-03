import React from "react";

export default function PlaylistButton(props) {

    return (
        <div className="playlist-button">
            {props.token ?
                <div className={""}>
                    <h5 className={"text-2xl text-indigo-400 "}>Click to make a playlist</h5>
                    <form onSubmit={props.testingFunction}>
                        <select className={"shadow appearance-none border rounded-l-lg w-auto py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-xl"} name={"emotion"} id={"emotion-playlist"} onClick={e => props.setPlaylistEmotion(e.target.value)}>
                            <option value="Anger">anger</option>
                            <option value="Fear">fear</option>
                            <option value="Joy">joy</option>
                            <option value="Sadness">sadness</option>
                        </select>
                        <button
                            className={"shadow bg-indigo-500 border rounded-r-lg hover:bg-indigo-700 focus:shadow-outline leading-tight focus:outline-none text-white py-2 px-3 text-xl"}
                            type={"submit"}>Make
                        </button>
                    </form>
                </div>
                :
                ""
            }
        </div>
    )
}
