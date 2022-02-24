import React from "react";

const ArtistCards = () => {
    return (
        <div className="p-4 max-w-md bg-white rounded-lg border shadow-md sm:p-8 dark:bg-gray-800 dark:border-gray-700">
            <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold leading-none text-gray-900 dark:text-white">Recent Artists</h3>
            </div>
            <div className="flow-root">
                <ul role="list" className="divide-y divide-gray-200 dark:divide-gray-700">
                    <li className="py-3 sm:py-4">
                        <div className="flex items-center space-x-4">
                            <div className="flex-shrink-0">
                                <img className="w-8 h-8 rounded-full" src="https://upload.wikimedia.org/wikipedia/commons/2/24/Circle-icons-image.svg" alt="Neil image"/>
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="text-sm font-medium text-gray-900 truncate dark:text-white">
                                    Neil Sims
                                </p>
                            </div>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    )

}

export default ArtistCards