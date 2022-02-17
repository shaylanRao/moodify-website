import './App.css';
import { useEffect, useState } from "react";
import axios from "axios";
import Login from './components/spotifyLogin'
import SearchBar from './components/searchBar';
import ArtistCards from './components/ArtistCards';


function App() {
    const [token, setToken] = useState("")
    const [searchKey, setSearchKey] = useState("")
    const [tracks, setTracks] = useState([])

    // const getToken = () => {
    //     let urlParams = new URLSearchParams(window.location.hash.replace("#","?"));
    //     let token = urlParams.get('access_token');
    // }

    const [testData, setTestData] = useState({})

    useEffect(() => {
        fetch("/time").then(
            res => res.json()
        ).then(
            testData => {
                setTestData(testData)
                console.log(testData)
            }
        )
    }, []);

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
        const { data } = await axios.get("https://api.spotify.com/v1/me/player/recently-played", {
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
        setTracks(data.items)
    }

    const renderRecentAlbums = () => {
        return tracks.map(track => (
            <div key={track.track.id}>
                {track.track.id ? <img width={"50%"} src={track.track.album.images[0].url} alt="" /> : <div>No Image</div>}
                {track.name}
            </div>
        ))
    }

    const renderRecentArtists = () => {
        return tracks.map(track => (
            <div key={track.track.id}>
                {track.track.id ? <img width={"50%"} src={track.track.artists[0].uri} alt="" /> : <div>No Image</div>}
                {track.name}
            </div>
        ))
    }

    return (
        <div className="App relative">
            <div className="App-header">
                <header class = "fixed top-0 left-0 right-0">            
                    <h1 class="font-medium leading-tight text-5xl mt-0 mb-2 text-blue-600">Spotify React</h1>
                </header>

                <ArtistCards />

                <SearchBar token={token} searchRecentTracks={searchRecentTracks} setSearchKey={setSearchKey} />

                {/* Login and logout function */}
                <Login token={token} logout={logout} />

                {renderRecentArtists()}

            </div>
        </div>

    );
}

export default App;