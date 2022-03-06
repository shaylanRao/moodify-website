import './App.css';
import '@progress/kendo-theme-material/dist/all.css'
import 'hammerjs'

import {useEffect, useState} from "react";
import axios from "axios";
import Sidebar from "./components/RecentSongArtist";
import SpotifyLogin from "./components/SpotifyLogin";
import Navbar from "./components/Navbar";
import Line from "./components/MoodGraph";
import SearchTrackValues from "./components/SearchTrackValues";
import SearchBar from "./components/SearchBar";
import TopSongCard from "./components/TopSong";
import PlaylistButton from "./components/PlaylistButton";
import TwitterLogin from "./components/TwitterLogin";


function App() {
    const [spotifyToken, setSpotifyToken] = useState("")
    const [twitterToken, setTwitterToken] = useState("")

    const [searchKey, setSearchKey] = useState("")
    const [recentTracks, setRecentTracks] = useState([])
    const [playlistEmotion, setPlaylistEmotion] = useState("")

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
    const [predictSongArtist, setPredictSongArtist] = useState("")


    useEffect(() => {
        const hash = window.location.hash
        let token = window.localStorage.getItem("spotify_token")

        // getToken()

        if (!token && hash) {
            token = hash.substring(1).split("&").find(elem => elem.startsWith("access_token")).split("=")[1]

            window.location.hash = ""
            window.localStorage.setItem("spotify_token", token)
        }

        setSpotifyToken(token)

    }, [])


    const logout = () => {
        setSpotifyToken("")
        setTwitterToken("")
        window.localStorage.removeItem("spotify_token")
    }

    const predictThisSong = async (e) => {
        e.preventDefault()
        const {data} = await axios.get("https://api.spotify.com/v1/search", {
            headers: {
                Authorization: `Bearer ${spotifyToken}`
            },
            // If search request, then use below, atm just a get recently played
            params: {
                q: searchKey,
                type: "track"
            }
        })

        setPredictSongName(data.tracks.items[0].name)
        setPredictSongArtist(data.tracks.items[0].artists[0].name)
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
                setSearchTrackAnger(pyData["anger"][0])
                setSearchTrackFear(pyData["fear"][0])
                setSearchTrackJoy(pyData["joy"][0])
                setSearchTrackSadness(pyData["sadness"][0])
            }
        )
    }

    const updatePlaylist = async (e) => {
        e.preventDefault()
        //get playlist id
        await getPlaylistId()

        //add new data to playlist
    }

    const getPlaylistId = async () => {
        const {data} = await axios.get("https://api.spotify.com/v1/me/playlists?limit=10", {
            headers: {
                Authorization: `Bearer ${spotifyToken}`
            },
        })
        const playlists = (data.items)
        const reqPlaylist = playlists.filter(playlist => playlist.name === `Moodify ${playlistEmotion}`);

        //Both paths lead to the same add tracks function without having sync problems
        if (reqPlaylist.length === 0) {
            (createPlaylist())
            //Need delay for search to be updated, otherwise would run twice as search misses new made playlist
            //recursion does not work as return time is not waited for and returns undefined
        } else {
            // setUpdatePlaylistId(reqPlaylist[0].id)
            let val;
            getTopTenTracks(reqPlaylist[0].id).then(r => val)
        }
    }


    const createPlaylist = () => {
        fetch(`https://api.spotify.com/v1/me/playlists`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${spotifyToken}`
            },
            body: JSON.stringify({
                name: `Moodify ${playlistEmotion}`,
                description: "New playlist description",
                public: false
            })
        }).then(response => response.json()).then(jsonResponse => {
            let val;
            getTopTenTracks(jsonResponse.id).then(r => val)
        });
    }

    const getTopTenTracks = async (playlistId) => {
        console.log("+ music function")
        console.log(playlistId)
        console.log(playlistEmotion)
        let moodData

        switch (playlistEmotion) {
            case "Anger":
                moodData = angerData
                break;
            case "Fear":
                moodData = fearData
                break;
            case "Joy":
                moodData = joyData
                break;
            default:
                moodData = sadnessData
        }

        const tempRecPlayed = recentTracks.slice().reverse()
        const tempMoodDataSort = moodData.slice().reverse()
        const tempMoodData = moodData.slice()

        const TopTenVals = tempMoodDataSort.sort(function (a, b) {
            return a - b;
        }).slice(-10).reverse();

        //Need this for not indexing song with same value (avoids duplicates)
        const topTenIdx = TopTenVals.map(function (val) {
            let idx = (tempMoodData).indexOf(val)
            tempMoodData[idx] = -1
            return idx
        });


        const topTenTracks = topTenIdx.map(idx => tempRecPlayed[idx])
        const topTenIds = topTenTracks.map(track => track.track.id)

        const {data} = await axios.get(`https://api.spotify.com/v1/playlists/${playlistId}/tracks`, {
            headers: {
                Authorization: `Bearer ${spotifyToken}`
            },
        })

        const trackObjects = (data.items).map(item => item)
        if (trackObjects.length === 0) {
            console.log("add")
            await addTracksToPlaylist(topTenIds, playlistId)
        } else {
            const trackIdsInPlaylist = trackObjects.map(item => item.track.id)
            const tracksToAdd = topTenIds.filter(item => !trackIdsInPlaylist.includes(item))
            console.log("add")
            if (tracksToAdd.length !== 0) {
                await addTracksToPlaylist(tracksToAdd, playlistId)
            } else {
                alert("All tracks are already in this playlist")
            }
        }
    }

    const addTracksToPlaylist = async (addTrackIds, playlistId) => {

        //TODO make a post call to add tracks to playlist

        let urlStr = ""
        addTrackIds.map(track => urlStr += "spotify:track:" + track.toString() + ",")
        urlStr = urlStr.slice(0, -1)

        await fetch(`https://api.spotify.com/v1/playlists/${playlistId}/tracks?uris=${urlStr}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "Authorization": `Bearer ${spotifyToken}`
            },
        })
        console.log("added")
    }


    useEffect(() => {
            async function fetchAPI() {
                if (spotifyToken) {
                    const {data} = await axios.get("https://api.spotify.com/v1/me/player/recently-played?limit=50", {
                        headers: {
                            Authorization: `Bearer ${spotifyToken}`
                        },
                    })
                    setRecentTracks(data.items)

                    fetch("/getPredictions").then(
                        res => res.json()
                    ).then(
                        pyData => {
                            setAngerData(pyData["anger"][0])
                            setFearData(pyData["fear"][0])
                            setJoyData(pyData["joy"][0])
                            setSadnessData(pyData["sadness"][0])
                            setMadePred(true)
                        }
                    )
                }
            }

            fetchAPI()

        }

        ,
        [spotifyToken]
    )

    const renderRecentCards = () => {
        return <Sidebar tracks={recentTracks}/>
    }

    const renderSearchValues = () => {
        return (<SearchTrackValues predictSongName={predictSongName}
                                   predictSongArtist={predictSongArtist}
                                   predictSongUrl={predictSongUrl}
                                   anger={searchTrackAnger}
                                   fear={searchTrackFear}
                                   joy={searchTrackJoy}
                                   sadness={searchTrackSadness}/>)
    }

    const renderTopTrack = (moodData, type) => {
        //Need to do this as reverse changes the original variable
        const tempRecPlayed = recentTracks.slice().reverse()
        const tempMoodData = moodData.slice()
        console.log(tempMoodData)
        // tempArr.slice().reverse()

        const maxEmotion = Math.max(...tempMoodData)
        const indexMaxEmotion = (moodData).indexOf(maxEmotion)
        const topTrack = (tempRecPlayed)[indexMaxEmotion]

        if (indexMaxEmotion === -1) {
            return <div>Loading...</div>
        } else {
            return (
                <TopSongCard maxEmotion={maxEmotion} topTrack={topTrack} emotion={type}/>
            )
        }
    }

    return (
        <div className="App">
            {spotifyToken ?
                <Navbar logout={logout}/> :
                ""}
            <div className="grid grid-flow-col-dense gap-1 flex">
                {spotifyToken ?
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
                    {spotifyToken ?
                        <div className={""}>
                            <div className={"justify-center"}>
                                <br/>
                                <Line anger={angerData} fear={fearData} joy={joyData} sadness={sadnessData}
                                      recentTracks={recentTracks.map(track => (track.track.name))}/>
                            </div>

                            <br/>
                            {madePred ?
                                <div className={"k-p-lg text-base py-5"}>
                                    <div className={"flex justify-center"}>
                                        <div className={"k-p-lg w-2/6"}>
                                            {renderTopTrack(joyData, "joy")}
                                        </div>
                                        <div className={"k-p-lg w-2/6"}>
                                            {renderTopTrack(sadnessData, "sadness")}
                                        </div>
                                        <div className={"k-p-lg w-2/6"}>
                                            {renderTopTrack(angerData, "anger")}
                                        </div>
                                    </div>

                                    <div className={"flex justify-around py-10"}>
                                        <div className={"k-p-lg rounded-lg shadow-lg border border-blue_purple w-3/6"}>
                                            <SearchBar token={spotifyToken} predictSong={predictThisSong}
                                                       setSearchKey={setSearchKey}/>
                                            {searchTrackAnger.length !== 0 ?
                                                renderSearchValues()
                                                :
                                                ""
                                            }
                                        </div>

                                        <div className={"flex justify-center py-5"}>
                                            <div
                                                className={"k-p-lg rounded-lg shadow-lg border border-blue_purple w-auto"}>
                                                <PlaylistButton token={spotifyToken} testingFunction={updatePlaylist}
                                                                setPlaylistEmotion={setPlaylistEmotion}/>
                                            </div>
                                        </div>
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
                                    className="font-medium leading-tight text-6xl mt-0 mb-2 text-blue_purple row-span-1">
                                    Moodify
                                    {twitterToken}
                                </div>
                                <br/>
                                <div className="">
                                    {!spotifyToken ? <SpotifyLogin/> : ""}
                                    <br/>
                                    {!twitterToken ? <TwitterLogin setTwitterToken={setTwitterToken}/> : ""}

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