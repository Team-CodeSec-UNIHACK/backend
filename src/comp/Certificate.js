import React, { Component } from 'react'
import Navbar from './Navbar'
import "../styles/cert.css";
import { FaTimes } from 'react-icons/fa';
import axios from "axios";
const Web3 = require('web3');

const url = "https://rinkeby.infura.io/v3/c1f318b7993a428e8c47d5167175465c";
const web3 = new Web3(new Web3.providers.HttpProvider(url));



export default class Certificate extends Component {
    state = {
        home:{},
        history:[],
        score: 0,
        blockID:"",
        misConduct: false,
    }
    close = () =>{
        axios.get("https://koff-backend.ratemycourse.review/pop-it");
        this.props.history.push("/");
    }
    componentDidMount(){
        const token = this.props.match.params.id
        if(localStorage.getItem("token")){
            axios.get("https://koff-backend.ratemycourse.review/home/"+token)
            .then(rem => {
                console.log(rem.data);
                this.setState({home:rem.data});
                axios.get("https://koff-backend.ratemycourse.review/history/"+token)
                .then(res => {
                
                    let success_tests = 0;
                    for (let i = 0; i < res.data.length; i++) {
                        if(res.data[i].result){
                            success_tests = success_tests + 1
                        }
                        let ourData = "0x" + rem.data.uuid + "::" + (res.data[i].result? "NOT-ILL": "ILL")
                        const tx = web3.eth.getTransaction(res.data[i].blockID);
                        tx.then(ti =>{
                            const lata = decodeURIComponent(ti.input.replace(/\s+/g, '').replace(/[0-9a-f]{2}/g, '%$&'));
        
                            if (ourData === lata){
                                res.data[i]["verified"]= true
                            }else{
                                res.data[i]["verified"]= false
                            }
                        })
                    }
                    this.setState({history:res.data, score: ((success_tests/res.data.length)*100), blockID: res.data[0].blockID});
                })
            })
    
            
        }else{
            this.props.history.push("/login")
        }
    }
    truncate = (str) => {
        console.log(this.state);
        return str.length > 10 ? str.substring(0, 25) + "..." : str;
    }
    formatDate = (undate) =>{
        let date = new Date(undate);
        return date.toLocaleString('default')
    }
    verifyBlock =  (valid, message) =>{
        console.log(valid);
        return valid ? <strike>{message}</strike> : message
        
    }
    render() {
        return (
            
            <div>
               
                <Navbar />
                <div className="container2">
                <FaTimes size="2em" color="white" className="times" onClick={this.close}/>
                    <div className="bot">
                        <div className="no-padder">
                            <div className="padder2">
                            <p className="black">Last block:</p>
                            <p className="white">
                                <a href={"https://rinkeby.etherscan.io/tx/"+this.state.blockID}
                                    className="stylist" target="_blank" rel="noreferrer" >
                                    {this.truncate(this.state.blockID)}
                                </a>
                                
                            </p>
                            </div>
                            
                            <div className="container3">
                                <div className="padder2" >
                                    <p className="black">Last 5 tests:</p>
                                    { this.state.history.map((test, index) => 
                                        
                                        test.result ? 
                                        <a href={"https://rinkeby.etherscan.io/tx/"+test.blockID} 
                                        className="stylist" target="_blank" rel="noreferrer" key={index}>
                                            <div className="mini-card-suc" >{ test.blockID }</div>
                                        </a>:
                                         <a href={"https://rinkeby.etherscan.io/tx/"+test.blockID}
                                         className="stylist" target="_blank" rel="noreferrer" key={index}>
                                            <div className="mini-card-fail" >{ this.verifyBlock(test.blockID, "failure")}</div>
                                        </a>
                                    )}
                                </div>
                                <div className="padder2">
                                    <p><span className="black">Uuid: </span><span className="white">{this.state.home.uuid}</span></p>
                                    <p><span className="black">Age: </span><span className="white">{this.state.home.age}</span></p>
                                    <p><span className="black">Country: </span><span className="white">{this.state.home.country}</span></p>
                                    <p className="black">Last test was at: </p>
                                    <p className="white">{this.formatDate(this.state.home.last_test_timestamp)}</p>                                    
                                </div>
                            </div>
                        </div>
                        <div className="right">
                            <div className="circle">
                                <p>{this.state.score}</p>
                            </div>
                            <span className="label1">
                            <h1 >Safety Score</h1>
                            {this.state.misConduct &&
                                <p style={{fontSize:"15px", textAlign:"center", color:"red"}} className="mini-card-mis">Data misconduct detected</p>
                            }
                            </span>
                           
                        </div>
                    </div>
                </div>
          
            </div>
            
        )
    }
}
