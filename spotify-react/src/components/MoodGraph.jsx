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
import ChartTooltip from "@progress/kendo-react-charts/dist/es/components/Tooltip";
import ChartArea from "@progress/kendo-react-charts/dist/es/components/ChartArea";


//For song list, replace [1,2,3] with songlist
// const categories = Array.from([1,2,3].keys());

// const categories = Array.from(props.anger.keys());


export default function Line(props) {

    const renderTooltip = ({point}) => (
        <span>
            {point.category}: {Math.round(point.value * 10) / 10}%
        </span>
    );

    // const trackNames = props.recentTracks.map(track => (
    //     track.track.name
    // ))


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
        console.log("Graphing")
        return (
            <Chart pannable zoomable style={{height: 350}}>
                <ChartArea background="white" margin={20} border={{color: "#7466F0", width: 3}}/>
                <ChartTitle color = "black" text="Recent Predicted Mood"/>
                <ChartLegend position="top" orientation="horizontal"/>
                <ChartValueAxis>
                    <ChartValueAxisItem title={{text: "Emotional Intensity"}} min={0} max={100}/>
                </ChartValueAxis>
                <ChartCategoryAxis>
                    <ChartCategoryAxisItem visible={false} categories={(props.recentTracks)}/>
                </ChartCategoryAxis>
                <ChartSeries>
                    {
                        //TODO change to loading icon
                        pythonData.map((item, idx) => (
                            <ChartSeriesItem
                                key={idx}
                                type="line"
                                data={item.data}
                                name={item.name}
                                color={item.color}
                            />
                        ))
                    }
                </ChartSeries>
                <ChartTooltip render={renderTooltip}/>
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
