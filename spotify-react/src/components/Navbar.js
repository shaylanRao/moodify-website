import React from "react";
import Logout from "./navbar-components/Logout";

export default function Navbar(props) {
    return (<nav className="container flex justify-around py-3 mx-auto rounded dark:bg-gray-800">
            <div>
                <h3 className="text-2xl font-medium text-blue-500">MOODIFY</h3>
            </div>
            <div className="space-x-8">

                <a href="" className="text-lg font-semibold whitespace-nowrap text-white"><Logout logout={props.logout}/></a>
            </div>
        </nav>
    )
}