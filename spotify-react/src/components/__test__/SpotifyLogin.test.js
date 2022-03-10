import React from "react";
import ReactDOM from 'react-dom'
import SpotifyLogin from '../SpotifyLogin'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import renderer from "react-test-renderer";

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<SpotifyLogin/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<SpotifyLogin/>)
    expect(getByTestId("spotify-login")).toBeDefined()
})

it("matches snapshot", () => {
    const tree = renderer.create(<SpotifyLogin/>).toJSON();
    expect(tree).toMatchSnapshot();
})


