import React from "react";
import ReactDOM from 'react-dom'
import SearchTrackValues from '../SearchTrackValues'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<SearchTrackValues/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<SearchTrackValues/>)
    expect(getByTestId("search-track-values")).toBeDefined()
})


