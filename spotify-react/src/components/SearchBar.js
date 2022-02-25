import React from "react";

export default function SearchBar(props) {

    return (
        <div className="searchbar">
            {props.token ?
                <form onSubmit={props.predictSong}>
                    <input className={"input-text"} type="text" onChange={e => props.setSearchKey(e.target.value)}/>
                    <button type={"submit"}>Search</button>
                </form>
                :
                ""
            }
        </div>
    )
}
