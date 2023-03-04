import React, { Component } from 'react'
import axios from 'axios'
import 'animate.css';
import $ from "jquery";
import { DataLoading, showMessage } from './common';
import { foodreport } from "../../urls/apis";

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;


export default class FoodSummary extends Component {
    constructor() {
        super();
        this.state = {
            loading: true,
            error: false,
            message: "",
            wastage: 0,
            price: 0,
            people: 0,
            battery: 0,
            macID: "",
        };
    }
    componentDidMount = async () => {
        this.timeout = setTimeout(async () => {
            await this.macIdChange();
        }, 1500);
    }

    macIdChange = async () => {
        showMessage(this, false, false, false, "");
        await axios({ method: "GET", url: foodreport })
            .then((response) => {
                let data = response.data;
                console.log('MACID Response-----------', response)
                if (response.status === 200) {
                    if (data.length !== 0) {
                        this.macID = data;
                        $("#macidCotent").css("display", "block");
                        for (let i = 0; i < data.length; i++) {
                            $("#macid").append("<option value=" + data[i].id + ">" + data[i].tagid + "</option>")
                        }
                        this.wastage();
                        this.interval = setInterval(() => {
                            this.wastage();
                        }, 2000);
                    } else {
                        $("#macidCotent").css("display", "none");
                        $(".summarycard").css("margin-top", "40px");
                        $(".boxes").css("margin-top", "40px");
                        $("#timing").text("00:00:00");
                        showMessage(this, false, true, false, "MAC ID Data Not Found");
                        this.setState({ wastage: 0, price: 0, people: 0, loading: false });
                    }
                }
            })
            .catch((error) => {
                console.log("error===>", error);
                $("#macidCotent").css("display", "none");
                $(".summarycard").css("margin-top", "40px");
                $(".boxes").css("margin-top", "40px");
                this.setState({ wastage: 0, price: 0, people: 0 })
                if (error.response.status === 403) {
                    $("#displayModal").css("display", "block");
                    $("#content").text("User Session has Timed Out. Please Login Again");
                } else if (error.response.status === 404) {
                    showMessage(this, false, true, false, "MAC ID Data Not Found");
                    $("#timing").text("00:00:00");
                }
            })
    }

    wastage = () => {
        let id = $("#macid").val();
        axios({ method: "POST", url: '/api/sensor/report', data: { tagid: parseInt(id) } })
            .then((response) => {
                console.log('wastage response-------', response)
                let data = response.data;
                if (response.status === 200) {
                    let waste = data.currentDiff.toFixed(2);
                    let cost = (waste * 80).toFixed(0);
                    let people = (cost / 50).toFixed(0);
                    let battery_status = data.battery;
                    let time = data.timestamp.substring(0, 19).replace("T", " ")
                    $("#timing").text(time)
                    this.setState({
                        wastage: waste, price: cost,
                        people: people, battery: battery_status,
                        loading: false,
                    })
                }
                else {
                    showMessage(this, false, true, false, "Data Not Found");
                    this.setState({ wastage: 0, price: 0, people: 0, loading: false })
                }
            })
            .catch((error) => {
                console.log("error===>", error)
                this.setState({ wastage: 0, price: 0, people: 0, loading: false })
                if (error.response.status === 403) {
                    $("#displayModal").css("display", "block");
                    $("#content").text("User Session has Timed Out. Please Login Again");
                } else if (error.response.status === 404) {
                    showMessage(this, false, true, false, "Data Not Found");
                }
            })
    }
    sessionTimeout = () => {
        this.props.parentCallback()
    };

    componentWillUnmount() {
        clearInterval(this.interval);
        clearTimeout(this.messageTimeout);
    }
    render() {
        const { wastage, price, people, loading, error, message } = this.state;
        return (
            <div>
                {error && (
                    <div
                        className="error-msg"
                        style={{ color: "red", }}>
                        <strong>{message}</strong>
                    </div>
                )}
                <div style={{ display: 'flex' }}>
                    <div className='summarycard'>
                        <div>
                            <span style={{
                                marginTop: '15px',
                                display: 'inline-block', color: '#717171',
                                fontSize: '18px',
                                float: "right", marginRight: '20px'
                            }}>Last Updated : &nbsp;
                                <span id="timing" style={{
                                    color: '#0073B6',
                                    display: 'inline-block',
                                    fontSize: '18px'
                                }}></span>
                            </span>
                            <select style={{ marginTop: "10px", marginLeft: '20px' }}
                                name="type"
                                id="macid"
                                onChange={() => {
                                    this.wastage();
                                }}>
                            </select>
                        </div>
                        <br />
                        <div className='subdiv2' style={{ marginTop: '5px' }}>
                            <p style={{ marginTop: '6px' }}> Food wastage for today is
                                <div className='textfield'>
                                    <span className="animate__animated animate__heartBeat animate__infinite" id='values'>{wastage}</span>
                                </div> kg
                            </p>

                            <p>
                                Cost of food waste for
                                <div className='textfield'>
                                    <span className="animate__animated animate__pulse animate__infinite"
                                        id='values'>{wastage}
                                    </span>
                                </div> kg is Rs
                                <span style={{ fontSize: '30px', fontFamily: "ui-serif" }}>(₹)</span>
                                <div className='textfield'>
                                    <span className="animate__animated animate__pulse animate__infinite"
                                        id='values'>{price}
                                    </span>
                                </div>
                            </p>

                            <p>
                                This is enough to feed
                                <div className='textfield'>
                                    <span className="animate__animated animate__pulse animate__infinite"
                                        id='values'>{people}
                                    </span>
                                </div> people for a day
                            </p>
                            <img alt='' src='/images/weightscale/dustbin.png'
                                style={{
                                    float: 'right', marginTop: '-40px',
                                    width: '160px', marginRight: '5px'
                                }} />
                        </div>
                    </div>

                    <div className="boxes" style={{ marginTop: '10px', marginLeft: '40px' }}>
                        <div className='weightcard'>
                            <img alt='' src='/images/weightscale/icon1.png'
                                className='foodIcons'
                                style={{ paddingTop: '10px' }} /><br />
                            <span className='spantxtclr'>Food waste costs our </span><br />
                            <span className='spantxtclr'> economy $36.6 billion</span><br />
                            <span className='spantxtclr'> a year.</span><br />
                        </div>
                        <div className="weightcard">
                            <img alt='' src='/images/weightscale/icon3.png'
                                className='foodIcons'
                                style={{ paddingTop: '10px' }} /><br />
                            <span className='spantxtclr' style={{ fontWeight: 600 }}>15% </span><br />
                            <span className='spantxtclr'> of India is</span><br />
                            <span className='spantxtclr'> Undernourished </span><br />
                        </div>

                        <div className="weightcard" style={{ marginBottom: "0px" }}>
                            <img alt='' src='/images/weightscale/icon5.png'
                                className='foodIcons'
                                style={{ paddingTop: '0px', width: "60px" }} /><br />
                            <span className='spantxtclr' style={{ fontWeight: 600 }}>$1 trillion </span><br />
                            <span className='spantxtclr'> value of food waste</span><br />
                            <span className='spantxtclr'> happen globally in a year </span><br />
                        </div>
                    </div>

                    <div className="boxes" style={{ marginTop: '10px', marginLeft: '40px' }}>
                        <div className="weightcard">
                            <img alt='' src='/images/weightscale/icon2.png'
                                className='foodIcons'
                                style={{ paddingTop: '15px' }} /><br />
                            <span className='spantxtclr' style={{ fontWeight: 600 }}>20 million</span><br />
                            <span className='spantxtclr'> Indians</span><br />
                            <span className='spantxtclr'> Starve to sleep </span><br />
                        </div>

                        <div className="weightcard">
                            <img alt='' src='/images/weightscale/icon4.png'
                                className='foodIcons'
                                style={{ paddingTop: '10px', width: "65px" }} /><br />
                            <span className='spantxtclr' style={{ fontWeight: 600 }}>20%</span><br />
                            <span className='spantxtclr'>of childern in</span><br />
                            <span className='spantxtclr'>India are Underweight</span><br />
                        </div>

                        <div className="weightcard" style={{ marginBottom: "0px" }}>
                            <img alt='' src='/images/weightscale/icon6.png'
                                className='foodIcons'
                                style={{ paddingTop: '5px', width: "55px" }} /><br />
                            <span className='spantxtclr' style={{ fontWeight: 600 }}>25% </span><br />
                            <span className='spantxtclr'>of the world’s fresh</span><br />
                            <span className='spantxtclr'>water supply is wasted</span><br />
                        </div>
                    </div>
                </div>

                {loading === true && (
                    <div
                        style={{
                            top: "0%",
                            left: "0%",
                        }} className="frame">
                        <DataLoading />
                    </div>
                )}


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
