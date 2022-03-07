import React from "react";

export default function TwitterLogin(props) {

    return (
        <div>
            <form>
                <button type={"submit"}>
                    {/* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
                    <a className="rounded-full twitter-login-button py-3 px-6">
                        <i className="fa fa-twitter"></i> Login to Twitter
                    </a>
                </button>
            </form>
        </div>


    )
}

