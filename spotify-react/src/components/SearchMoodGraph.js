import {
    Chart,
    ChartSeries,
    ChartSeriesItem,
    ChartValueAxis,
    ChartValueAxisItem,
} from "@progress/kendo-react-charts";
import "hammerjs";
import {COLORS} from "../constants";
import ChartTooltip from "@progress/kendo-react-charts/dist/es/components/Tooltip";
import React from "react";

export default function SearchGraph(props) {

    const renderTooltip = ({point}) => (
        <span>
            {Math.round(point.value * 10) / 10}%
        </span>
    );


    const searchData = [
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

    return (
        <Chart pannable zoomable style={{height: 200, width: 300}} data-testid="search-graph">
            <ChartValueAxis>
                <ChartValueAxisItem title={{text: "Emotional Intensity"}} min={0}/>
            </ChartValueAxis>
            <ChartSeries>
                {searchData.map((item, idx) => (
                    <ChartSeriesItem key={idx} type="bar" spacing={0.1} color={item.color} data={item.data}/>
                ))}
            </ChartSeries>
            <ChartTooltip render={renderTooltip}/>
        </Chart>
    )
}