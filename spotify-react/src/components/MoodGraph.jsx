import {
    Chart,
    ChartCategoryAxis,
    ChartCategoryAxisItem,
    ChartLegend,
    ChartSeries,
    ChartSeriesItem,
    ChartTitle,
    ChartValueAxis,
    ChartValueAxisItem,
} from "@progress/kendo-react-charts";

import * as React from "react";
import {Loader} from "@progress/kendo-react-indicators";
import {COLORS} from "../constants";


//For song list, replace [1,2,3] with songlist
// const categories = Array.from([1,2,3].keys());

// const categories = Array.from(props.anger.keys());


export default function Line(props) {

    const pythonData = [
        {
            name: "Anger",
            data: props.anger,
            color: COLORS.anger,
        },
        {
            name: "Fear",
            data: props.fear,
            color: COLORS.fear,
        },
        {
            name: "Joy",
            data: props.joy,
            color: COLORS.joy,
        },
        {
            name: "Sadness",
            data: props.sadness,
            color: COLORS.sadness,
        },
    ];


    if (props.anger.length > 1) {
        console.log("TRUE")
        console.log(props.anger)
        return (
            <Chart pannable zoomable style={{height: 350, color: "red"}}>
                <ChartTitle text="Application status - last 3 months"/>
                <ChartLegend position="top" orientation="horizontal"/>
                <ChartValueAxis>
                    <ChartValueAxisItem title={{text: "Job Positions"}} min={0} max={1}/>
                </ChartValueAxis>
                <ChartCategoryAxis>
                    <ChartCategoryAxisItem categories={Array.from(props.anger.keys())}/>
                </ChartCategoryAxis>
                <ChartSeries>
                    {
                        //TODO change to loading icon
                        pythonData.map((item, idx) => (
                            <ChartSeriesItem
                                key={idx}
                                type="line"
                                tooltip={{visible: true}}
                                data={item.data}
                                name={item.name}
                                color={item.color}
                            />
                        ))
                    }
                </ChartSeries>
            </Chart>
        )
    } else {
        return (
            <div>
                <Loader size="large" type={"infinite-spinner"}/>
            </div>
        );
    }

};
