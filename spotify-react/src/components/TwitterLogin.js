import React from "react";

export default function TwitterLogin(props) {

    return (
        <div>
            <form>
                <button type={"submit"}>
                    <a className="rounded-full twitter-login-button py-3 px-6" href={""}>
                        <i className="fa fa-twitter"></i> Login to Twitter
                    </a>
                </button>
            </form>
        </div>


    )
}

