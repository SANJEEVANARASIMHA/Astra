/* eslint-disable jsx-a11y/alt-text */
import React, { Component } from 'react'
import 'animate.css';
import $ from "jquery";
import axios from 'axios'
import FoodSummary from './FoodSummary';
import FoodGraph from './FoodGraph';


const Underline = {
    width: "85px",
    height: "9px",
    position: "absolute",
};

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;


export default class Foodwaste extends Component {
    optionList = [false, false];
    constructor() {
        super();
        this.state = {
            flag: false,
        };
    }

    componentDidMount() {
        this.setState({ flag: true })
        this.optionList[0] = true;
        $("#opt0").css({ "background": "#00629B", "color": "white" });

    }
    btnOption = (e) => {
        $(".myDIV").parent().find('button').removeClass("active");
        this.setState({ flag: true });
        this.optionList = [false, false];
        this.optionList[e.target.id - 1] = true;
        $("#" + e.target.id).addClass("active");
    }

    sessionTimeout = () => {
        $("#displayModal").css("display", "none");
        sessionStorage.setItem("isLoggedIn", 0);
        this.props.handleLogin(0);
    };
    render() {
        return (
            <div className="panel">
                <span className="main-heading">FOOD WASTAGE</span>
                <br />
                <img alt="" src="../images/Tiles/Underline.png" style={Underline} />
                <div className="input-group"
                    style={{ marginTop: "20px", marginLeft: "30px" }}>
                    <div className="myDIV" >
                        <button id="1" onClick={this.btnOption} className="fancy-button active">Summary</button>
                        <button id="2" onClick={this.btnOption} className="fancy-button">History</button>
                    </div>
                </div>

                <div style={{ width: '99%', padding: '5px', marginTop: '0px', height: '67vh' }} >
                    {this.optionList[0] && (<FoodSummary parentCallback={this.sessionTimeout} />)}
                    {this.optionList[1] && (<FoodGraph parentCallback={this.sessionTimeout} />)}
                </div>
                <div id="displayModal" className="modal">
                    <div className="modal-content">
                        <p id="content" style={{ textAlign: "center" }}></p>
                        <button
                            id="ok"
                            className="btn-center btn success-btn"
                            onClick={this.sessionTimeout}
                        >
                            OK
                        </button>
                    </div>
                </div>
            </div>

        )
    }
}



