import React from 'react';
import ReactDOM from 'react-dom'
import Navbar from "../Navbar";

import { render, cleanup } from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";
import renderer from "react-test-renderer"


it("renders without crashing", ()=> {
    const div = document.createElement("div");
    ReactDOM.render(<Navbar/>, div)
})

afterEach(cleanup);

it("renders navbar correctly", ()=>{
    const {getByTestId} = render(<Navbar />)
    expect(getByTestId("navbar")).toBeDefined()
})

it("matches snapshot", ()=>{
    const tree = renderer.create(<Navbar />).toJSON();
    expect(tree).toMatchSnapshot();
})