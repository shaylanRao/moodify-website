import React from "react";
import ReactDOM from 'react-dom'
import PlaylistButton from '../PlaylistButton'

import {cleanup, render, fireEvent, getByTestId, getAllByTestId} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import renderer from "react-test-renderer";


it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<PlaylistButton/>, div)
})

afterEach(cleanup);

it("renders playlist-button correctly", () => {
    const {getByTestId} = render(<PlaylistButton/>)
    expect(getByTestId("playlist-button")).toBeDefined()
})

it("matches snapshot", () =>{
    const tree = renderer.create(<PlaylistButton token={"testing token"}/>).toJSON();
    expect(tree).toMatchSnapshot();
})

it("choosing option", () =>{
    const {getByTestId, getAllByTestId} = render(<PlaylistButton token={"testing token"}/>)
    fireEvent.change(getByTestId('select-menu'), {target: { value: "Anger"}})
    let options = getAllByTestId('option')
    expect(options[0].selected).toBeTruthy()
    expect(options[1].selected).toBeFalsy()
    expect(options[2].selected).toBeFalsy()
    expect(options[3].selected).toBeFalsy()
})

