import React from "react";

export default function Logout(props) {
    return (
        <div>
            <button className="h-10 px-5 text-red-100 transition-colors duration-150 bg-red-700 rounded-lg focus:shadow-outline hover:bg-red-800" onClick={props.logout}>Logout</button>
        </div>
    )
}

