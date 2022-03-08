import React from "react";
import ReactDOM from 'react-dom'
import Sidebar from '../RecentSongArtist'
import {TestArray} from './RecentTracksArray'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import renderer from "react-test-renderer";


it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<Sidebar/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<Sidebar/>)
    expect(getByTestId("sidebar")).toBeDefined()
})

it("renders recent tracks correctly", () => {
    const {getByTestId} = render(<Sidebar tracks={TestArray} />)
    expect(getByTestId("sidebar")).toBeDefined()
})

it("matches snapshot", () => {
    const tree = renderer.create(<Sidebar tracks={TestArray}/>).toJSON();
    expect(tree).toMatchSnapshot();
})

it("matches empty snapshot", () => {
    const tree = renderer.create(<Sidebar />).toJSON();
    expect(tree).toMatchSnapshot();
})

