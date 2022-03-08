import React, {useState} from "react";
import ReactDOM from 'react-dom'
import SearchBar from '../SearchBar'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import userEvent from "@testing-library/user-event";

it("renders without crashing", () => {
    const div = document.createElement("div");
    ReactDOM.render(<SearchBar/>, div)
})

afterEach(cleanup);

it("renders empty recent tracks correctly", () => {
    const {getByTestId} = render(<SearchBar/>)
    expect(getByTestId("search-bar")).toBeDefined()
})


// it("choosing option", () => {
//     let setSearchKey = ""
//     const {getByTestId} = render(<SearchBar token={"testing token"} setSearchKey={setSearchKey}/>)
//     expect(getByTestId).toHaveValue("Drake")
//     // userEvent.type(getByTestId("search-input"), "Drake");
//     //
//     // expect(getByTestId("search-input")).toHaveValue("Drake");
//
// })
