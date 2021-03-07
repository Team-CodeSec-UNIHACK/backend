import React, { Component } from 'react'
import Navbar from './Navbar'
import axios from "axios"

export default class Login extends Component {
    state ={
        password: ""
    }
    onChange = (event) =>{
        this.setState({[event.target.name]: event.target.value})
    }
    onSubmit = (e) => {
        e.preventDefault();
        axios.post("https://koff-backend.ratemycourse.review/let-me-in", {"password": this.state.password})
        .then(res => {
            localStorage.setItem('token', res.data.access)
            this.props.history.push("/");
          })
    }
    render() {
        return (
            <div>
                <Navbar />
                <div className="log">
                    <input 
                     className="pass"
                     name="password"
                     type="password"
                     placeholder="Enter master password"
                     value={this.state.password}
                     onChange={this.onChange} />
                    <button className="butt" onClick={this.onSubmit}>Submit</button>
                </div>
                
            </div>
        )
    }
}
