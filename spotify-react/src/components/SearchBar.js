import React from "react";

export default function SearchBar(props) {

    return (
        <div className="searchbar" data-testid="search-bar">
            {props.token ?
                <div className={"p"}>
                    <h5 className={"text-2xl text-indigo-400 pt-2 pb-5"}>Enter a song to get predicted mood</h5>
                    <form onSubmit={props.predictSong} data-testid={"search-form"}>
                        <input
                            className="shadow appearance-none border rounded-l-lg w-auto py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline text-xl"
                            type="text" placeholder="Search Track"
                            onChange={e => props.setSearchKey(e.target.value)} data-testid={"search-input"}/>
                        <button
                            className={"shadow bg-indigo-500 border rounded-r-lg hover:bg-indigo-700 focus:shadow-outline leading-tight focus:outline-none text-white py-2 px-3 text-xl"}
                            type={"submit"}>Search
                        </button>
                    </form>
                </div>
                :
                ""
            }
        </div>
    )
}
