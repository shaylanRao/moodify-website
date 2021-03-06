import React from "react";
import ReactDOM from 'react-dom'
import SearchBar from '../SearchBar'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<SearchBar/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<SearchBar/>)
    expect(getByTestId("search-bar")).toBeDefined()
})


