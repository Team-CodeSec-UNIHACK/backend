import React, { Component } from 'react'
import "../styles/nav.css"
import { ShakeRotate  } from 'reshake';
export default class Navbar extends Component {
    render() {
        return (
            <ul className="nav">
                <li><a href="/">
                    <ShakeRotate>
                        koff
                    </ShakeRotate >
                    </a>
                </li>
            </ul>
        )
    }
}
