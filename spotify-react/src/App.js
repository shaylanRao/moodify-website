import './App.css';
import '@progress/kendo-theme-material/dist/all.css'
import 'hammerjs'

import {useEffect, useState} from "react";
import axios from "axios";
import Sidebar from "./components/RecentSongArtist";
import SearchBar from "./components/SearchBar";
import Login from "./components/SpotifyLogin";
import Navbar from "./components/Navbar";
import Line from "./components/MoodGraph";
import SearchTrackValues from "./components/SearchTrackValues";


function App() {
    const [token, setToken] = useState("")
    const [searchKey, setSearchKey] = useState("")
    const [recentTracks, setRecentTracks] = useState([])
    const [recentTracksLabels, setRecentTracksLabels] = useState([])

    const [angerData, setAngerData] = useState([])
    const [fearData, setFearData] = useState([])
    const [joyData, setJoyData] = useState([])
    const [sadnessData, setSadnessData] = useState([])

    const [searchTrackAnger, setSearchTrackAnger] = useState([])
    const [searchTrackFear, setSearchTrackFear] = useState([])
    const [searchTrackJoy, setSearchTrackJoy] = useState([])
    const [searchTrackSadness, setSearchTrackSadness] = useState([])

    const [madePred, setMadePred] = useState(false)

    const [predictSongUrl, setPredictSongUrl] = useState("")
    const [predictSongName, setPredictSongName] = useState("")


    useEffect(() => {
        const hash = window.location.hash
        let token = window.localStorage.getItem("token")

        // getToken()

        if (!token && hash) {
            token = hash.substring(1).split("&").find(elem => elem.startsWith("access_token")).split("=")[1]

            window.location.hash = ""
            window.localStorage.setItem("token", token)
        }

        setToken(token)

    }, [])

    const logout = () => {
        setToken("")
        window.localStorage.removeItem("token")
    }

    const predictThisSong = async (e) => {
        e.preventDefault()
        const {data} = await axios.get("https://api.spotify.com/v1/search", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            // If search request, then use below, atm just a get recently played
            params: {
                q: searchKey,
                type: "track"
            }
        })
        // console.log(data.items[0].track.album.images[0].url)

        setPredictSongName(data.tracks.items[0].name)
        setPredictSongUrl(data.tracks.items[0].album.images[0].url)

        fetch(`/postPredictSong`, {
            'method': 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({trackid: data.tracks.items[0].id})
        })
            .then(response => response.json())
            .catch(error => console.log(error))

        fetch("/getPredictSong", {'method': 'GET'}).then(
            res => res.json()
        ).then(
            pyData => {
                console.log("SINGLE PRED")
                console.log(pyData["anger"][0])
                setSearchTrackAnger(pyData["anger"][0])
                setSearchTrackFear(pyData["fear"][0])
                setSearchTrackJoy(pyData["joy"][0])
                setSearchTrackSadness(pyData["sadness"][0])
            }
        )
    }


    useEffect(() => {
            async function fetchAPI() {
                if (token) {
                    const {data} = await axios.get("https://api.spotify.com/v1/me/player/recently-played", {
                        headers: {
                            Authorization: `Bearer ${token}`
                        },
                    })
                    setRecentTracks(data.items)

                    //TODO replace /time with /getPredictions

                    fetch("/getPredictions").then(
                        res => res.json()
                    ).then(
                        pyData => {
                            setMadePred(true)
                            setAngerData(pyData["anger"][0])
                            setFearData(pyData["fear"][0])
                            setJoyData(pyData["joy"][0])
                            setSadnessData(pyData["sadness"][0])
                            setRecentTracksLabels(pyData["recent_track_list"][0])
                            renderRecentCards()
                        }
                    )
                }
            }

            fetchAPI()

        }

        ,
        [token]
    )

    const renderRecentCards = () => {
        return <Sidebar tracks={recentTracks}/>
    }

    const renderSearchValues = () => {
        return (<SearchTrackValues predictSongName={predictSongName}
                                   predictSongUrl={predictSongUrl}
                                   anger={searchTrackAnger}
                                   fear={searchTrackFear}
                                   joy={searchTrackJoy}
                                   sadness={searchTrackSadness}/>)
    }

    // class APIService {
    //     // Insert an article
    //     static
    //
    // }


    return (
        <div className="App">
            {token ?
                <Navbar logout={logout}/> :
                ""}
            <div className="grid grid-flow-col-dense gap-1 flex">
                {token ?
                    <div>
                        <div className="bg-dark_blue">
                            {/*Renders recently played tracks in sidebar when search is pressed (tracks has loaded)*/}
                            {renderRecentCards()}
                        </div>
                    </div>
                    :
                    ""
                }

                <div className="main-page col-span-12 flex h-full w-full bg-background">
                    {token ?
                        <div>
                            <div className={""}>
                                <br/>
                                <Line anger={angerData} fear={fearData} joy={joyData} sadness={sadnessData}
                                      recentTracks={recentTracksLabels}/>
                            </div>

                            <br/>
                            {madePred ?
                                <div className={"k-p-lg text-base"}>
                                    <div className={"k-p-lg border border-blue_purple w-3/6"}>
                                        <SearchBar token={token} predictSong={predictThisSong}
                                                   setSearchKey={setSearchKey}/>
                                        {searchTrackAnger.length !== 0 ?
                                            renderSearchValues()
                                            :
                                            ""
                                        }
                                    </div>
                                </div>
                                :
                                ""
                            }
                        </div>

                        :


                        <div className="moodify-title flex flex-row min-h-screen justify-center items-center">
                            <div>
                                <div
                                    className="font-medium leading-tight text-5xl mt-0 mb-2 text-indigo-500 row-span-1">
                                    Spotify React
                                    {/*TODO make grid to separate title to login*/}
                                </div>
                                <br/>
                                <br/>
                                <div className="">
                                    <Login/>
                                </div>
                            </div>
                        </div>
                    }
                </div>
            </div>
        </div>
    )
}

export default App;