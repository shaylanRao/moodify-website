import React from "react";
import Logout from "./navbar-components/Logout";

export default function Navbar(props) {
    return (<nav className="container flex py-3 p-20 justify-between rounded dark:bg-gray-800" data-testid="navbar">
            <div className={""}>
                <h3 className="text-4xl font-medium text-blue_purple">MOODIFY</h3>
            </div>
            <div className="space-x-3">

                {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
                <a className="text-lg font-semibold whitespace-nowrap text-white"><Logout logout={props.logout}/></a>
            </div>
        </nav>
    )
}