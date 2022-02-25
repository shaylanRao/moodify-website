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


function App() {
    const [token, setToken] = useState("")
    const [searchKey, setSearchKey] = useState("")
    const [recentTracks, setRecentTracks] = useState([])
    const [angerData, setAngerData] = useState([])
    const [fearData, setFearData] = useState([])
    const [joyData, setJoyData] = useState([])
    const [sadnessData, setSadnessData] = useState([])


    // const getToken = () => {
    //     let urlParams = new URLSearchParams(window.location.hash.replace("#","?"));
    //     let token = urlParams.get('access_token');
    // }

    const [testData, setTestData] = useState([])

    // useEffect(() => {
    //     fetch("/time").then(
    //         res => res.json()
    //     ).then(
    //         testData => {
    //             setTestData(testData["test var"])
    //             console.log(testData)
    //         }
    //     )
    // }, []);


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

    const searchRecentTracks = async (e) => {
        e.preventDefault()
        const {data} = await axios.get("https://api.spotify.com/v1/me/player/recently-played", {
            headers: {
                Authorization: `Bearer ${token}`
            },
            // If search request, then use below, atm just a get recently played
            // params: {
            //     q: searchKey,
            //     type: "artist"
            //}
        })
        // console.log(data.items[0].track.album.images[0].url)
        console.log(data.items[0].track)
        setRecentTracks(data.items)
    }

    // const loadRecentTracks = async (e) => {
    //     e.preventDefault()
    //     const {data} = await axios.get("https://api.spotify.com/v1/me/player/recently-played", {
    //         headers: {
    //             Authorization: `Bearer ${token}`
    //         },
    //     })
    //     console.log(data.items[0].track)
    //     setRecentTracks(data.items)
    // }

    useEffect(() => {
            async function fetchAPI() {
                if (token) {
                    const {data} = await axios.get("https://api.spotify.com/v1/me/player/recently-played", {
                        headers: {
                            Authorization: `Bearer ${token}`
                        },
                    })
                    console.log(data.items[0].track)
                    setRecentTracks(data.items)

                    //TODO replace /time with /getPredictions

                    fetch("/getPredictions").then(
                        res => res.json()
                    ).then(
                        pyData => {
                            setAngerData(pyData["anger"][0])
                            setFearData(pyData["fear"][0])
                            setJoyData(pyData["joy"][0])
                            setSadnessData(pyData["sadness"][0])
                            console.log(angerData)
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


    return (
        <div className="App">
            {token ?
                <Navbar logout={logout}/> :
                ""}
            <div className="grid grid-flow-col-dense gap-1 flex">
                {token ?
                    <div>
                        <div className="bg-blue-100">
                            {/*Renders recently played tracks in sidebar when search is pressed (tracks has loaded)*/}
                            {renderRecentCards()}
                        </div>
                    </div>
                    :
                    ""
                }

                <div className="main-page col-span-12 flex h-full w-full">
                    {token ?
                        <div>
                            <br/>
                            <SearchBar token={token} searchRecentTracks={searchRecentTracks}
                                       setSearchKey={setSearchKey}/>
                            <div>
                                <br/>
                                <Line anger={angerData} fear={fearData} joy={joyData} sadness={sadnessData}/>
                            </div>
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

                    <div>{testData}</div>
                </div>
            </div>
        </div>
    )
}

export default App;