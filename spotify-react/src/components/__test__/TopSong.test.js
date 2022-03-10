import React from "react";
import ReactDOM from 'react-dom'
import TopSongCard from '../TopSong'
import {trackObject} from './TrackObject'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import renderer from "react-test-renderer";

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<TopSongCard/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<TopSongCard/>)
    expect(getByTestId("top-song-card")).toBeDefined()
})

it("matches empty snapshot", () => {
    const tree = renderer.create(<TopSongCard/>).toJSON();
    expect(tree).toMatchSnapshot();
})

it("matches joy snapshot", () => {
    const tree = renderer.create(<TopSongCard topTrack={trackObject} emotion={"joy"} maxEmotion={45}/>).toJSON();
    expect(tree).toMatchSnapshot();
})

it("matches sadness snapshot", () => {
    const tree = renderer.create(<TopSongCard topTrack={trackObject} emotion={"sadness"} maxEmotion={45}/>).toJSON();
    expect(tree).toMatchSnapshot();
})

it("matches anger snapshot", () => {
    const tree = renderer.create(<TopSongCard topTrack={trackObject} emotion={"anger"} maxEmotion={45}/>).toJSON();
    expect(tree).toMatchSnapshot();
})
