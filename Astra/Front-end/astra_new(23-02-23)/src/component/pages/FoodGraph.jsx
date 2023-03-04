import React, { Component } from 'react'
import ApexCharts from 'react-apexcharts';
import $ from "jquery";
import axios from "axios";
import { DataLoading, showMessage } from './common';
import { foodreport } from "../../urls/apis";

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

export default class FoodGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            series: [],
            categories: [],
            loading: true,
            error: false,
            message: "",
            macID: "",
            graphWidth: "",
        };

    }
    componentDidMount = async () => {
        await this.macIdChange();
    }

    macIdChange = async () => {
        $("#foodwatage_error").text("");
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
                        this.wastageData("macid")
                    } else {
                        $("#macidCotent").css("display", "none");
                        $(".summarycard").css("margin-top", "40px");
                        $(".boxes").css("margin-top", "40px");
                        $("#timing").text("00:00:00");
                        showMessage(this, false, true, false, "MAC ID Data Not Found");
                        this.setState({ wastage: 0, price: 0, people: 0 });
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
                    $("#timing").text("00:00:00");
                    showMessage(this, false, true, false, "MAC ID Data Not Found");
                }
            })
    }

    wastageData = (filter) => {
        this.setState({ series: [], categories: [], loading: true })
        let key = "", id = "";
        if (filter === "macid") {
            $("#weight_filter").val("weekly");
            key = "weekly";
        } else {
            key = $("#weight_filter").val();
        }
        id = $("#macid").val();
        axios({ method: "GET", url: "/api/report/graph?key=" + key + "&tagid=" + id })
            .then((response) => {
                if (response.status === 200 || response.status === 201) {
                    let data = response.data;
                    console.log("wastageData=====>", response);
                    let val = [], cat = [], graphWidth = "", length = data.length;
                    this.timeout = setTimeout(() => {
                        if (length !== 0) {
                            if (length <= 10) {
                                graphWidth = (length * 4).toString() + "%";
                            } else if (length >= 11 && length <= 15) {
                                graphWidth = "50%";
                            } else if (length >= 16 && length <= 20) {
                                graphWidth = "70%";
                            } else if (length >= 21 && length <= 25) {
                                graphWidth = "80%";
                            } else if (length >= 26 && length <= 31) {
                                graphWidth = "90%";
                            }
                            for (let i = 0; i < data.length; i++) {
                                let reading = data[i].reading === null ? 0 : data[i].reading
                                cat.push(data[i].date);
                                val.push(parseFloat(reading).toFixed(2));
                            }
                            this.setState({
                                series: val, categories: cat,
                                graphWidth: graphWidth, loading: false
                            });

                        } else {
                            this.setState({ series: [], categories: [], loading: false })
                            showMessage(this, false, true, false, "Data Not Found");
                        }
                    }, 2000)

                }
            })
            .catch((error) => {
                console.log("=========>", error);
                if (error.response.status === 403) {
                    $("#displayModal").css("display", "block");
                    $("#content").text("User Session has Timed Out. Please Login Again");
                } else if (error.response.status === 404) {
                    this.setState({ series: [], categories: [] })
                    showMessage(this, false, true, false, "Data Not Found");
                } else if (error.response.status === 400) {
                    this.setState({ series: [], categories: [] })
                    showMessage(this, false, true, false, "Bad Request");
                }
                this.setState({ loading: false })
            })
    }


    componentWillUnmount() {
        clearInterval(this.interval);
        clearTimeout(this.messageTimeout);
    }

    sessionTimeout = () => {
        this.props.parentCallback()
    };
    render() {
        const { series, categories, graphWidth, loading, error, message } = this.state;
        return (
            <>
                <div style={{ marginTop: '10px' }}>
                    <select style={{ marginTop: "10px", marginLeft: '20px', marginRight: '20px' }}
                        name="macid"
                        id="macid"
                        onChange={() => {
                            this.wastageData("macid");
                        }}>
                    </select>
                    <select id="weight_filter" onChange={() => {
                        this.wastageData("weight_filter");
                    }}>
                        <option value="weekly">Weekly</option>
                        <option value="monthly">Monthly</option>
                    </select>
                </div>

                {error && (
                    <div
                        className="error-msg"
                        style={{ color: "red", marginTop: "40px" }}>
                        <strong>{message}</strong>
                    </div>
                )}
                <div style={{ marginTop: "10px" }}>
                    {
                        categories.length !== 0 ?
                            (<ApexCharts
                                options={{
                                    chart: {
                                        type: 'bar',
                                        height: 350,
                                        stacked: true,
                                        toolbar: {
                                            show: true
                                        },
                                        zoom: {
                                            enabled: true
                                        }
                                    },
                                    plotOptions: {
                                        bar: {
                                            columnWidth: graphWidth,
                                            horizontal: false,
                                            borderRadius: 10
                                        },
                                    },
                                    xaxis: {
                                        labels: {
                                            show: true,
                                        },
                                        type: 'category',
                                        categories: categories,
                                    },
                                    yaxis: {
                                        decimalsInFloat: 0,
                                        labels: {
                                            formatter: function (value) {
                                                if (value <= 5)
                                                    return parseFloat(value).toFixed(1).toString() + "(kg)";
                                                else
                                                    return parseInt(value).toString() + "(kg)";
                                            }
                                        },
                                    },
                                    tooltip: {
                                        y: {
                                            formatter: function (value, { series }) {
                                                return value + "(kg)"
                                            }
                                        }
                                    },
                                    legend: {
                                        position: 'top',
                                        offsetY: 0
                                    },
                                    dataLabels: {
                                        enabled: true,
                                        style: {
                                            fontSize: "11px",
                                        }
                                    }
                                }}

                                series={[{
                                    name: 'wastage',
                                    data: series,
                                }]}
                                type="bar" height={350} />) : (<p />)
                    }
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
            </>
        )
    }
}