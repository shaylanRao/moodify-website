import React from "react";
import Logout from "./navbar-components/logout";

export default function Navbar() {
    return (<nav className="container flex justify-around py-3 mx-auto rounded dark:bg-gray-800">
            <div>
                <h3 className="text-2xl font-medium text-blue-500">MOODIFY</h3>
            </div>
            <div className="space-x-8">

                <a href="" className="text-lg font-semibold whitespace-nowrap text-white"><Logout/></a>
            </div>
        </nav>
    )
}