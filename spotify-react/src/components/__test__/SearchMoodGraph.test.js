import React from "react";
import ReactDOM from 'react-dom'

import {cleanup, getByTestId, render} from '@testing-library/react';
import "@testing-library/jest-dom/extend-expect";

//TODO import error, not working for testing 'import outside a module fr ChartToolTip'
// import SearchGraph from '../SearchMoodGraph'
// it("renders without crashing", () => {
//     const div = document.createElement("div");
//     ReactDOM.render(<SearchGraph/>, div)
// })
//
// afterEach(cleanup);
//
// it("renders empty recent tracks correctly", () => {
//     const {getByTestId} = render(<SearchGraph/>)
//     expect(getByTestId("search-graph")).toBeDefined()
// })


