import React from "react";

export default function SearchBar(props) {

    return (
        <div>
        {props.token ?
            <form onSubmit={props.searchRecentTracks}>
                <input type="text" onChange={e => props.setSearchKey(e.target.value)} />
                <button type={"submit"}>Search</button>
            </form>

            : <h2 >Please login</h2>
        }
        </div>
    )
}
