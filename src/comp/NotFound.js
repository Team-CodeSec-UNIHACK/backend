import React, { Component } from 'react'
import { Link } from 'react-router-dom'
import Navbar from './Navbar'
import "../styles/nfound.css"
export default class NotFound extends Component {
    render() {
        return (
            <div>
                <Navbar />
                <div className="err">
                    <div>
                    <h1><i>Oops!! Wrong URL</i></h1>
                    <Link to="/" className="hyplink">
                        Go Home
                    </Link>
                    </div>
                    {/* <img src="https://media.giphy.com/media/8L0Pky6C83SzkzU55a/source.gif" width="300" height="300"/> */}
                </div>

            </div>
        )
    }
}
