import React, { Component } from 'react';
import axios from "axios";
import $ from "jquery";
import "./Styling.css";
import "./Pulse.css";
import { linkClicked } from "../navbar/Navbar";
import moment from "moment";
import { employeeTracking } from "../../urls/apis";
import { DataLoading, showMessage } from './common';

const Underline = {
    width: "75px",
    height: "9px",
    position: "absolute",
    zIndex: "-1",
};

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

export default class EmployeeTrackingHistory extends Component {
    fWidth = 0;
    fHeight = 0;
    value = 0;
    floorData = [];
    constructor() {
        super();
        this.state = {
            message: "",
            error: false,
            loading: false,
            currentDateTime: moment(new Date()).format("YYYY-MM-DDTHH:mm"),
        }
    }

    componentDidMount = async () => {
        linkClicked(2);
        this.floor = await this.getFloormap();
        if (this.floor.floorData.length !== 0) {
            this.floorData = this.floor.floorData;
            $("#floorBlock").css("display", "block");
            this.plotFloorMap();
        } else {
            this.setState({ loading: false });
            showMessage(this, false, true, false, this.floor.message);
        }
    }

    getFloormap = async () => {
        var floor = { error: false, message: "", floorData: [] };
        await axios({
            method: "GET",
            url: "/api/uploadmap",
            headers: {
                "content-type": "multipart/form-data",
            },
        })
            .then((response) => {
                console.log("=======>", response);
                let data = response.data;
                if (data.length !== 0 && response.status === 200) {
                    $("#floorBlock").css("display", "block");
                    $("#fname").append(
                        "<option value=" + 1 + ">" + data[1].name + "</option>"
                    );
                    for (let i = 0; i < data.length; i++) {
                        if (i !== 1) {
                            $("#fname").append(
                                "<option value=" + i + ">" + data[i].name + "</option>"
                            );
                        }
                    }
                    floor.floorData = response.data;
                } else {
                    floor = { error: true, message: "Please Upload Floormap.", floorData: [] }
                }
            })
            .catch((error) => {
                if (error.response.status === 403) {
                    $("#displayModal").css("display", "block");
                    $("#content").text("User Session has timed out. Please Login again");
                } else if (error.response.status === 400) {
                    floor = { error: true, message: "Bad Request!", floorData: [] }
                    this.setState({ error: true, message: 'Bad Request!' });
                } else if (error.response.status === 404) {
                    floor = { error: true, message: "Please Upload Floormap.", floorData: [] }
                }
            });
        return floor;
    }

    componentWillUnmount() {
        clearInterval(this.interval);
        clearTimeout(this.timeout);
        clearInterval(this.empInterval);
        clearTimeout(this.messageTimeout);
    }

    plotFloorMap = () => {
        this.setState({ loading: false });
        clearInterval(this.empInterval);
        $("#track-error").text("");
        let floorID = $("#fname").val();
        this.fimage = this.floorData[floorID];
        this.fWidth = this.fimage.width;
        this.fHeight = this.fimage.height;
        $("#tempimg").attr("src", this.fimage.image);
        $("#tempimg").attr("style", "width:auto;height:auto;");
        $("#temp .empls").remove();
        $("input[type=text]").val("");
        $("input[type=datetime-local]").val("");
        clearInterval(this.interval);
    };

    plotAssets = () => {
        let fname = $("#fname").val();
        axios({
            method: "GET",
            url: employeeTracking + this.floorData[fname].id,
        })
            .then((response) => {
                console.log("plotAssets response========>", response);
                if (response.status === 200) {
                    let data = response.data;
                    if (data.length !== 0) {
                        this.count = 0;
                        this.pilotingEmpHistory(data[this.count]);
                        this.empInterval = setInterval(() => {
                            this.count += 1;
                            $(".history-circle").removeClass();
                            if (this.count < data.length)
                                this.pilotingEmpHistory(data[this.count]);
                            else
                                clearInterval(this.empInterval);
                        }, 1200);
                    } else {
                        showMessage(this, false, true, false, "No Data Found in Between Date and Time");
                    }
                } else {
                    showMessage(this, false, true, false, "Unable To Get Tags Data");
                }
            })
            .catch((error) => {
                console.log("error=====>", error);
                if (error.response.status === 403) {
                    $("#displayModal").css("display", "block");
                    $("#content").text("User Session has timed out. Please Login again");
                } else if (error.response.status === 404) {
                    showMessage(this, false, true, false, "No Data Found in Between Date and Time");
                } else {
                    showMessage(this, false, true, false, "Request Failed with status code (" + error.response.status + ")");
                }
            });
    };

    pilotingEmpHistory = (data) => {
        let wpx = document.getElementById("temp").clientWidth / this.fWidth;
        let hpx = document.getElementById("temp").clientHeight / this.fHeight;
        let empDiv = document.createElement("div");
        $(empDiv).attr("class", "empls");
        $(empDiv).attr(
            "style",
            "position:absolute;" +
            "left:" +
            (wpx * parseFloat(data.x)).toFixed(2) +
            "px; top:" +
            (hpx * parseFloat(data.y)).toFixed(2) +
            "px;"
        );
        let pulse = document.createElement("div");
        $(pulse).attr("class", "history_circle");
        $(pulse).attr(
            "title",
            "X : " +
            (parseFloat(data.x)).toFixed(2) +
            "\nY : " +
            (parseFloat(data.y)).toFixed(2)
        );
        $(empDiv).append(pulse);
        $("#temp").append(empDiv);
    }

    search = () => {
        clearInterval(this.empInterval);
        $("#temp .empls").remove();
        let floorID = $("#fname").val();
        let tagid = $("#tagid").val();
        let floorid = this.floorData[floorID].id;
        let start = $("#start_time").val();
        let end = $("#end_time").val();
        if (tagid.length !== 0 && (floorid.toString()).length !== 0 &&
            start.length !== 0 && end.length !== 0) {
            if (!tagid.match("([A-Za-z0-9]{2}[-]){5}([A-Za-z0-9]){2}")) {
                showMessage(this, true, true, false, "Invalid Tag ID Entered");
            } else {
                showMessage(this, false, false, false, "");
                let datas = {
                    tagid: tagid,
                    floor: this.floorData[floorID].id,
                    start: start.replace("T", " ") + ":00",
                    end: end.replace("T", " ") + ":00",
                }
                console.log("=======>", datas);
                axios({ method: "POST", url: "/api/employee/history", data: datas })
                    .then((response) => {
                        console.log("plotAssets response========>", response);
                        if (response.status === 200) {
                            let data = response.data;
                            if (data.length !== 0) {
                                this.count = 0;
                                this.pilotingEmpHistory(data[this.count]);
                                this.empInterval = setInterval(() => {
                                    this.count += 1;
                                    $(".history-circle").removeClass();
                                    if (this.count < data.length)
                                        this.pilotingEmpHistory(data[this.count]);
                                    else
                                        clearInterval(this.empInterval);
                                }, 1000);
                            } else {
                                showMessage(this, false, true, false, "No Data Found in Between Date and Time");
                            }
                        } else {
                            showMessage(this, false, true, false, "Unable To Get Tags Data");
                        }
                    })
                    .catch((error) => {
                        console.log("error=====>", error);
                        if (error.response.status === 403) {
                            $("#displayModal").css("display", "block");
                            $("#content").text("User Session has timed out. Please Login again");
                        } else if (error.response.status === 404) {
                            $("#track-error").text("No Data Found in Between Date and Time ");
                        } else if (error.response.status === 400) {
                            $("#track-error").text("Tag MacID not exist");
                        } else {
                            $("#track-error").text(
                                "Request Failed with status code (" + error.response.status + ")."
                            );
                        }
                    });
            }
        } else {
            showMessage(this, true, true, false, "Required All Fields");
        }
    }

    sessionTimeout = () => {
        $("#displayModal").css("display", "none");
        sessionStorage.setItem("isLoggedIn", 0);
        this.props.handleLogin(0);
    };
    render() {
        const { loading, message, error } = this.state;
        return (
            <div className="panel"
                style={{
                    overflow: loading === true ? "hidden" : "visible",
                    height: loading === true ? "500px" : "auto",
                }}>
                <span className="main-heading">TRACKING HISTORY</span>
                <br />
                <img alt="" src="../images/Tiles/Underline.png" style={Underline} />
                <div className="container fading" style={{ marginTop: "50px" }}>
                    {error && (
                        <div style={{ color: "red", marginBottom: "20px" }}>
                            <strong>{message}</strong>
                        </div>
                    )}
                    <div className="row" style={{ display: "flex", marginRight: "30px" }}>
                        <div className="input-group">
                            <span className="label">Floor Name : </span>
                            <select
                                name="type"
                                id="fname"
                                onChange={() => {
                                    this.plotFloorMap();
                                }}
                            ></select>
                        </div>

                        <div className="input-group" style={{ marginLeft: "50px" }}>
                            <span className="label">Tag MAC ID : </span>
                            <input
                                type="text"
                                id="tagid"
                                placeholder="5a-c2-15-00-00-00"
                                required="required"
                                onClick={() => $("#track-error").text("")}
                            />
                        </div>
                    </div>

                    <div className="row" style={{ display: "flex", marginRight: "30px" }}>
                        <div className="input-group">
                            <span className="label">From : </span>
                            <input
                                type="datetime-local"
                                name="start_time"
                                id="start_time"
                                max={this.state.currentDateTime}
                                required="required" />
                        </div>

                        <div className="input-group" style={{ marginLeft: "50px" }}>
                            <span className="label">To : </span>
                            <input
                                type="datetime-local"
                                name="end_time"
                                id="end_time"
                                max={this.state.currentDateTime}
                                required="required"
                            />
                        </div>

                        <div className="input-group" style={{ marginLeft: "50px" }}>
                            <div className="btn success-btn"
                                onClick={() => this.search()}>Search
                            </div>
                        </div>
                    </div>

                    <div id="floorBlock" style={{ display: "none", marginTop: "30px" }}>
                        <div
                            id="temp"
                            style={{
                                display: "block",
                                position: "relative",
                                width: "fit-content",
                            }}>
                            <img id="tempimg" alt=""></img>
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
                {/* Display modal to display error messages */}
                <div id="displayModal" className="modal">
                    <div className="modal-content">
                        <p id="content" style={{ textAlign: "center" }}></p>
                        <button
                            id="ok"
                            className="btn-center btn success-btn"
                            onClick={this.sessionTimeout}>
                            OK
                        </button>
                    </div>
                </div>
            </div>
        );
    }
}
