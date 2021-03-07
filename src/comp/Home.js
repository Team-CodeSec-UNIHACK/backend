import React, { Component } from 'react'
import Navbar from './Navbar'
import "../styles/home.css"
import QRCode from "react-qr-code";
import { FaQuestionCircle } from 'react-icons/fa';
import axios from "axios";

export default class Home extends Component {
    state={
        qrKey: "koffmaster64"
    }
    componentDidMount() {
       this.scan()
    }
    scan =()=>{
        if(localStorage.getItem("token")){
            axios.get("https://koff-backend.ratemycourse.review/scan")
            .then(res => {
                console.log(res.data.empty);
                if(res.data.empty){
                    setTimeout(function() { //Start the timer
                        this.scan() //After 1 second, set render to true
                    }.bind(this), 3000)
                }else{
                    this.props.history.push("/cert/"+res.data.token);
                }
                
              })
        }else{
            this.props.history.push("/login")
        }
    }
    render() {
        return (
            <div>
                <Navbar />
                <div className="container">
                    <div className="qrcode">
                        <QRCode value={this.state.qrKey} className="qrimage" size={400} />
                    </div>
                    <div className="instructions">
                        <div>
                            <div className="question">
                             <FaQuestionCircle size="3em" />
                            </div>
                            <p className="inst">Ask the person to scan this QR Code.</p>
                            <p className="inst">Wait for the certificate to load. if status is striked, then malicious activity detected</p>
                            <p className="inst">Cross check info with the person's ID and make a decision with the result.</p>
                        </div>
                       
                    </div>
                </div>
            </div>
        )
    }
}
