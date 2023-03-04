/* eslint-disable no-useless-concat */
import React, { Component } from "react";
import { linkClicked } from "../navbar/Navbar";
import axios from "axios";
import $ from "jquery";
import "./Styling.css";
import "./Pulse.css";
import {
  zoneConfiguration,
  empDailyData,
  empWeeklyData,
  empMonthlyData,
  employeeTracking
} from "../../urls/apis";
import ApexCharts from 'react-apexcharts';
import { DataLoading, chartOption, showMessage } from './common';

const graphBtn = {
  padding: "8px 10px",
  border: "none",
  marginLeft: "15px",
  borderRadius: "4px",
  fontSize: "16px",
  cursor: "pointer",
  color: "Black",
  fontWeight: "bold",
  boxShadow: "3px 3px 5px 3px rgba(0, 0, 0, 0.25)",
};

const Underline = {
  width: "75px",
  height: "9px",
  position: "absolute",
  zIndex: "-1",
};

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

class Tracking extends Component {
  fWidth = 0;
  fHeight = 0;
  value = 0;
  floorData = [];
  constructor() {
    super();
    this.state = {
      chartOpts: {},
      message: "",
      zoneName: "",
      error: false,
      loading: true,
      series: [],
      chartColor: [],
      trackData: [],
    }
  }

  componentDidMount = async () => {
    linkClicked(1);
    this.chart_Option(["#352cf2"]);
    $(".serverOpt3").hide();
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

  componentWillUnmount() {
    clearInterval(this.interval);
    clearInterval(this.empInterval);
    clearTimeout(this.empTimeOut);
    clearTimeout(this.timeout);
    clearTimeout(this.messageTimeout);
  }

  chart_Option = async (graphColor) => {
    this.setState({ chartColor: graphColor });
    let value = await chartOption(graphColor, "yyyy-MM-dd HH:mm");
    this.setState({ chartOpts: value });
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

  plotFloorMap = () => {
    showMessage(this, false, false, false, "");
    $("#zonesdet").empty();
    let floorID = $("#fname").val();
    this.fimage = this.floorData[floorID];
    this.fWidth = this.fimage.width;
    this.fHeight = this.fimage.height;
    $("#tempimg").attr("src", this.fimage.image);
    $("#tempimg").attr("style", "width:auto;height:auto;");
    $("#lastupdated").css("display", "none");
    $("#tempChart").remove();
    $("#temp .sensors").remove();
    $("#graph_opt").css("display", "none");
    $("input[type=text]").val("");
    $("#total").text("0");
    this.timeout = setTimeout(() => {
      this.getZones();
      this.plotAssets();
    }, 1 * 1000);
    clearInterval(this.interval);
    this.interval = setInterval(() => {
      this.plotAssets()
    }, 5 * 1000);
  };

  getZones = () => {
    let floorID = $("#fname").val();
    this.wp = document.getElementById("temp").clientWidth;
    this.hp = document.getElementById("temp").clientHeight;
    axios({
      method: "GET",
      url: zoneConfiguration + "?floorid=" + this.floorData[floorID].id,
    })
      .then((response) => {
        console.log("getZones Response=====>", response);
        if (response.status === 200) {
          this.zones = response.data;
          $("#temp .sensors").remove();
          let wpx = this.wp / this.fWidth;
          let hpx = this.hp / this.fHeight;
          if (response.data.length !== 0) {
            $(".zonesdet").show();
            $("#zonesdet").append("<option value=''>--Select Zones--</option>");
            let data = response.data;
            $("#tempimg").attr(
              "style",
              "width:" + this.wp + "px;" + "height:" + this.hp + "px;"
            );
            for (let i = 0; i < data.length; i++) {
              $("#zonesdet").append("<option value=" + i + ">" + data[i].zonename + "</option>");
              let xaxis = 0, yaxis = 0;
              xaxis = parseInt(wpx * parseFloat(data[i].x1));
              yaxis = parseInt(hpx * parseFloat(data[i].y1));
              let width = Math.ceil((data[i].x2 - data[i].x1) * wpx);
              let height = Math.ceil((data[i].y2 - data[i].y1) * hpx);
              let childDiv1 = document.createElement("div");
              $(childDiv1).attr("id", data[i].zonename);
              $(childDiv1).attr("class", "sensors");
              $(childDiv1).attr("title", "ZoneName: " + data[i].zonename);
              $(childDiv1).attr(
                "style",
                "border:1px solid black;background:#3fffff63;" +
                "position: absolute; cursor: pointer; left:" +
                xaxis +
                "px; top:" +
                yaxis +
                "px;" +
                "width:" +
                width +
                "px;" +
                "height:" +
                height +
                "px;"
              );
              // $(childDiv1).on("click", () => {
              //   this.setState({ zoneName: data[i].zonename })
              //   this.getGraphData(empDailyData, data[i].zonename, "opt0", "Daily");
              // });
              $("#temp").append(childDiv1);
            }
          }
        }
      })
      .catch((error) => {
        console.log("error===>", error);
        if (error.response.status === 403) {
          this.setState({ loading: false });
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has timed out. Please Login again");
        } else if (error.response.status === 404) {
          $(".zonesdet").hide();
          showMessage(this, false, true, false, "Zones Data Not Found");
        } else {
          showMessage(this, false, true, false, "Request Failed with status code (" + error.response.status + ")");
        }
      });
  };

  getZonesData = () => {
    let zoneval = $("#zonesdet").val();
    if (zoneval !== "") {
      let zonedet = this.zones[zoneval];
      let zname = zonedet.zonename.toLowerCase();
      this.setState({ zoneName: zonedet.zonename })
      if (zname.includes("server") || zname.includes("hub")) {
        $(".serverOpt3").show();
        this.getGraphData(empDailyData, zonedet.zonename, "opt0", "Daily");
      } else {
        $("#graph_opt").css("display", "block");
        $(".serverOpt3").hide();
        this.getGraphData(empDailyData, zonedet.zonename, "opt0", "Daily");
      }
    } else {
      $("#graph_opt").css("display", "none");
      showMessage(this, false, true, false, "Please Select Zones");
    }
  }

  getServerTempHumiGraph = (apiurl, zonename, btnOpt, filter) => {
    this.optionChange(btnOpt);
    this.chart_Option(["#ff1a1a", "#11610c"]);
    this.setState({ error: false, message: "", series: [], loading: true })
    $("#graph_opt").css("display", "block");
    $("#chartID").text(zonename);
    let zoneValue = $("#zonesdet").val();
    let zoneDet = this.zones[zoneValue];
    let jsonData = { x1: zoneDet.x1, y1: zoneDet.y1, x2: zoneDet.x2, y2: zoneDet.y2 }
    console.log("====%%%%%%=====>", jsonData);
    axios({
      method: "POST",
      url: apiurl,
      data: jsonData,
    })
      .then((response) => {
        if (response.status === 200) {
          let data = response.data;
          console.log("Temp/Humi graph====>", response)
          if (data.length !== 0) {
            let tempData = [], humidData = [];
            for (let i = 0; i < data.length; i++) {
              let time = data[i].timestamp;
              let date = new Date(time);
              let ms = date.getTime();
              tempData.push([ms, data[i].temperature]);
              humidData.push([ms, data[i].humidity]);
            }
            this.setState({
              series: [
                { name: 'Temperature(°C) ', data: tempData },
                { name: 'Humidity(RH) ', data: humidData }
              ]
            });
            this.setState({ loading: false });
            window.scrollTo(0, document.body.scrollHeight);
          } else {
            window.scrollTo(0, 0);
            showMessage(this, false, true, false, filter + " Graph Data Not Found");
          }
        }
      })
      .catch((error) => {
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has timed out. Please Login again");
        } else if (error.response.status === 404) {
          showMessage(this, false, true, false, filter + " Graph Data Not Found");
          window.scrollTo(0, 0);
        } else {
          showMessage(this, false, true, false, "Request Failed");
        }
      });
  }

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
            $("#lastupdated").css("display", "block");
            this.wp = document.getElementById("temp").clientWidth / this.fWidth;
            this.hp = document.getElementById("temp").clientHeight / this.fHeight;
            let update_time = data[0].timestamp.substring(0, 19).replace("T", " ");
            $("#timing").text(update_time);
            let emptrack = [];
            for (let i = 0; i < data.length; i++) {
              let timestamp =
                new Date() - new Date(data[i].timestamp.substring(0, 19).replace("T", " "));
              if (timestamp <= 2 * 60 * 1000) {
                emptrack.push(data[i])
              }
            }
            $("#total").text(emptrack.length);
            console.log("emptrack============>", emptrack);
            if (emptrack.length === 0) {
              showMessage(this, true, true, false, "No Asset Turned ON, Please Check System Health Page");
              this.setState({ trackData: [], loading: false });
            } else {
              showMessage(this, false, false, false, "");
              this.setState({ trackData: emptrack, loading: false });
            }
          } else {
            this.setState({ trackData: [], loading: false });
            showMessage(this, true, true, false, "No Asset Turned ON, Please Check System Health Page");
          }
        } else {
          this.setState({ trackData: [], loading: false });
          $("#total").text("0");
          showMessage(this, true, true, false, "Unable To Get Tags Data");
        }
      })
      .catch((error) => {
        $("#total").text("0");
        this.setState({ trackData: [], loading: false });
        console.log("error=====>", error);
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has timed out. Please Login again");
        } else if (error.response.status === 404) {
          showMessage(this, false, true, false, "No Asset Turned ON, Please Check System Health Page");
        } else {
          showMessage(this, false, true, false, "Request Failed with status code (" + error.response.status + ")");
        }
      });
  };

  optionChange = (btnId) => {
    $("#opt0").css({ background: "none", color: "#000" });
    $("#opt1").css({ background: "none", color: "#000" });
    $("#opt2").css({ background: "none", color: "#000" });
    $("#opt3").css({ background: "none", color: "#000" });
    $("#" + btnId).css({ background: "rgb(0, 98, 135)", color: "#FFF" });
  };

  getGraphData = (apiurl, zonename, btnOpt, filter) => {
    this.optionChange(btnOpt);
    this.setState({ series: [] })
    showMessage(this, false, false, false, "");
    $("#graph_opt").css("display", "block");
    $("#chartID").text(zonename);
    let floorID = $("#fname").val();
    axios({
      method: "POST",
      url: apiurl,
      data: {
        floorid: this.floorData[floorID].id,
        zonename: zonename,
      },
    })
      .then((response) => {
        if (response.status === 200) {
          let data = response.data;
          console.log("graph====>", response)
          if (data.length !== 0) {
            let count = [];
            for (let i = 0; i < data.length; i++) {
              let time = data[i].timestamp;
              let date = new Date(time);
              let ms = date.getTime();
              count.push([ms, data[i].count]);
            }
            this.setState({
              series: [
                { name: 'Employee Count ', data: count }
              ]
            });
            this.setState({ loading: false });
            window.scrollTo(0, document.body.scrollHeight);
          } else {
            window.scrollTo(0, 0);
            showMessage(this, false, true, false, filter + " Graph Data Not Found");
          }
        }
      })
      .catch((error) => {
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has timed out. Please Login again");
        } else if (error.response.status === 404) {
          window.scrollTo(0, 0);
          showMessage(this, false, true, false, filter + " Graph Data Not Found");
        } else {
          showMessage(this, false, true, false, filter + "Request Failed");
        }
      });
  };

  sessionTimeout = () => {
    $("#displayModal").css("display", "none");
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLogin(0);
  };

  search1 = () => {
    let id = $("#tagid").val();
    console.log("searchhhhh====", id);
    const macIdExists = this.state.trackData.some(data => data.tagid === id);
    showMessage(this, false, false, false, "");
    if (id.length === 0) {
      showMessage(this, false, true, false, "Please Enter Employee Tag ID");
    } else if (!id.match("([A-Za-z0-9]{2}[-]){5}([A-Za-z0-9]){2}")) {
      showMessage(this, false, true, false, "Invalid Tag ID Entered");
    } else if (id.length !== 0) {
      if (macIdExists) {
        $("#temp .empls").css("display", "none");
        $("#temp #emp_" + id).css("display", "block");

      } else {
        console.log("-----searchhhhh====", id);
        clearInterval(this.interval);
        showMessage(this, false, true, false, "Asset Not Found");
        $("#temp .empls").css("display", "none");
      }
    }
  };

  callTrackData = (dt) => {
    this.colors = "blue";
    if (dt.value === 1) {
      this.colors = "red";
    } else if (dt.value === 3) {
      this.colors = "yellow";
    } else {
      this.colors = "blue";
    }
    return (
      <div className="empls"
        id={"emp_" + dt.tagid}
        // title={"Employee Name  : " + dt.name +
        //   "\nTag ID : " + dt.tagid +
        //   "\nX : " + dt.x.toFixed(2) +
        //   "\nY : " + dt.y.toFixed(2)}
        key={dt.id}>
        <div
          className={"inner_circle_" + this.colors}
          style={{
            left: (this.wp * parseFloat(dt.x)).toFixed(2) + "px",
            top: (this.hp * parseFloat(dt.y)).toFixed(2) + "px"
          }}>
          <div className={"pulsatingcircle_" + this.colors}>
          </div>
        </div>
      </div>
    );
  };

  clearSearch = () => {
    clearInterval(this.interval);
    clearInterval(this.empInterval);
    this.setState({ trackData: [] });
    document.getElementById("empid1").value = "";
    document.getElementById("empid2").value = "";
    showMessage(this, false, false, false, "");
    $("#temp .empls").empty();
    this.plotAssets();
    this.interval = setInterval(() => { this.plotAssets() }, 5 * 1000);
  }

  search = () => {
    let empid1 = $("#empid1").val();
    let empid2 = $("#empid2").val();
    console.log(empid1, "searchhhhh====", empid2);
    showMessage(this, false, false, false, "");
    if (empid1.length === 0 || empid2.length === 0) {
      showMessage(this, false, true, false, "Please enter Employee Tag ID");
    } else if (!empid1.match("([A-Za-z0-9]{2}[-]){5}([A-Za-z0-9]){2}") ||
      !empid2.match("([A-Za-z0-9]{2}[-]){5}([A-Za-z0-9]){2}")) {
      showMessage(this, false, true, false, "Invalid Tag ID Entered");
    } else if (empid1.length !== 0 && empid2.length !== 0) {
      clearInterval(this.interval);
      showMessage(this, false, false, false, "");
      $("#temp .empls").css("display", "none");

      axios({ method: "GET", url: "/api/employee/history" })
        .then((response) => {
          console.log("plotAssets response========>", response);
          if (response.status === 200) {
            // let data = response.data;
            let data = [
              {
                "id": "0",
                "left": 114,
                "top": 227,
              },
              {
                "id": "1",
                "left": 177,
                "top": 225,
                "rotate": 107,
              },
              {
                "id": "2",
                "left": 149,
                "top": 247,
                "rotate": 147,
              },
              {
                "id": "3",
                "left": 181,
                "top": 275,
                "rotate": 92,
              },
              {
                "id": "4",
                "left": 206,
                "top": 304,
                "rotate": 179,
              },
              {
                "id": "5",
                "left": 174,
                "top": 320,
                "rotate": 270,
              },
              {
                "id": "6",
                "left": 140,
                "top": 323,
                "rotate": 272,
              },
              {
                "id": "7",
                "left": 104,
                "top": 322,
                "rotate": 279,
              },
              {
                "id": "8",
                "left": 70,
                "top": 343,
                "rotate": 178,
              },
              {
                "id": "9",
                "left": 70,
                "top": 381,
                "rotate": 147,
              },
              {
                "id": "10",
                "left": 95,
                "top": 403,
                "rotate": 100,
              },
              {
                "id": "11",
                "left": 130,
                "top": 403,
                "rotate": 85,
              },
              {
                "id": "12",
                "left": 181,
                "top": 404,
                "rotate": 77,
              },
              {
                "id": "13",
                "left": 213,
                "top": 401,
                "rotate": 71,
              },
              {
                "id": "14",
                "left": 244,
                "top": 398,
                "rotate": 87,
              },
              {
                "id": "15",
                "left": 277,
                "top": 401,
                "rotate": 87,
              },
              {
                "id": "16",
                "left": 308,
                "top": 397,
                "rotate": 87,
              },
              {
                "id": "17",
                "left": 333,
                "top": 402,
                "rotate": 143,
              },
              {
                "id": "18",
                "left": 330,
                "top": 430,
              },
            ]
            this.emptrackcount = data;
            if (data.length !== 0) {
              this.count = 2;
              this.pilotingEmpIcon(data[0], $("#empid1").val());
              this.pilotingEmpIcon(data[this.emptrackcount.length - 1], $("#empid2").val());
              this.empTimeOut = setTimeout(() => {
                this.pilotingEmpHistory(data[this.count]);
                this.empInterval = setInterval(() => {
                  this.count += 1;
                  $(".history-circle").removeClass();
                  if (this.count < data.length - 1)
                    this.pilotingEmpHistory(data[this.count]);
                  else
                    clearInterval(this.empInterval);
                }, 800);
              }, 1000)
            } else {
              showMessage(this, true, true, false, "No Data Found in Between Date and Time");
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
            showMessage(this, true, true, false, "No Data Found in Between Date and Time");
          } else if (error.response.status === 400) {
            showMessage(this, true, true, false, "Tag MacID Not Exist");
          } else {
            showMessage(this, true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  pilotingEmpHistory = (data) => {
    let empDiv = document.createElement("div");
    $(empDiv).attr("class", "empls");
    let pulse = document.createElement("div");

    $(pulse).attr("class", "fas fa-angle-double-up");
    if (this.count < this.emptrackcount.length - 1)
      $(empDiv).attr(
        "style",
        "position:absolute;" +
        "left:" + data.left +
        "px; top:" + data.top +
        "px;transform:" + "rotate(" + data.rotate + "deg);"
      );
    // $(pulse).attr(
    //   "title",
    //   "X : " + data.left+
    //   "\nY : " + data.top 
    // );
    $(empDiv).append(pulse);
    $("#temp").append(empDiv);

  }

  pilotingEmpIcon = (data, empID) => {
    let empDiv = document.createElement("div");
    $(empDiv).attr("class", "empls");
    let pulse = document.createElement("div");
    $(pulse).attr("class", "fas fa-street-view");

    $(pulse).attr("class", "fas fa-street-view");
    $(empDiv).attr(
      "style",
      "position:absolute;"
      + "left:" + data.left +
      "px; top:" + data.top + "px;"
    );

    $(pulse).attr(
      "title",
      "Emp ID : " + empID
      // + "\nX : " + data.left +
      // "\nY : " + data.top
    );
    $(empDiv).append(pulse);
    $("#temp").append(empDiv);
  }

  render() {
    const { zoneName, chartOpts, loading, series, trackData, error, message } = this.state;
    return (
      <div className="panel"
        style={{
          overflow: loading === true ? "hidden" : "visible",
          height: loading === true ? "500px" : "auto",
        }}>
        <span className="main-heading">REALTIME TRACKING</span>
        <br />
        <img alt="" src="../images/Tiles/Underline.png" style={Underline} />
        <div className="container fading" style={{ marginTop: "50px" }}>
          <div className="row" style={{ display: "flex" }}>
            <div className="input-group">
              <span className="label"
                style={{ width: "150px" }}>Floor Name :</span>
              <select
                name="type"
                id="fname"
                onChange={() => {
                  this.setState({ trackData: [], loading: true });
                  this.plotFloorMap();
                }}
              ></select>
            </div>
            <div className="input-group zonesdet">
              <span className="label"
                style={{ marginLeft: "70px", width: "150px" }}>Zones : </span>
              <select
                name="type"
                id="zonesdet"
                onChange={() => {
                  this.setState({ trackData: [], loading: true });
                  this.getZonesData();
                }}
              ></select>
            </div>
          </div>

          <div id="floorBlock" style={{ display: "none" }}>
            <div className="row">
              {/* 
              <div className="input-group">
                <span className="label">Employee-1 : </span>
                <input
                  type="text"
                  id="empid1"
                  placeholder="5a-c2-15-00-00-00"
                  required="required"
                  onClick={() => $("#track-error").text("")}
                />
              </div>
              <div className="input-group">
                <span className="label">Employee-2 : </span>
                <input
                  type="text"
                  id="empid2"
                  placeholder="5a-c2-15-00-00-00"
                  required="required"
                  onClick={() => $("#track-error").text("")}
                />
              </div>

              <div style={{ display: "flex", margin: "15px 0 0 253px" }}>
                <div className="btn success-btn"
                  style={{ background: '#eb6565', marginRight: "20px" }}
                  onClick={() => this.clearSearch()}>Clear
                </div>
                <div className="btn success-btn"
                  onClick={() => this.search()}>Search
                </div>
              </div> */}
              <span
                style={{
                  float: "right",
                  fontSize: "18px",
                  display: "none",
                  marginRight: "60px",
                }}
                className="sub-heading"
                id="lastupdated">
                Last Updated : <span id="timing">00:00:00</span>{" "}
              </span>
            </div>
            {error && (
              <div className="error-msg">
                <strong>{message}</strong>
              </div>
            )}
            <div className="row sub-heading" style={{ color: "black" }}>
              <hr></hr>
              <div style={{ display: 'flex' }}>
                <div >
                  Total Tags : &nbsp;
                  <u>
                    <span id="total"> 0 </span>
                  </u>
                </div>
              </div>
            </div>
            <div
              id="temp"
              style={{
                display: "block",
                position: "relative",
                width: "fit-content",
              }}>
              <img id="tempimg" alt=""></img>
              {trackData.length > 0 &&
                trackData.map((dt, ind) => this.callTrackData(dt))}
            </div>
            <div id="graph_opt" style={{ display: "none", marginBottom: "15px" }}>
              <hr></hr>
              <div className="sub-heading" style={{ textDecoration: "none" }}>
                Employee Occupancy : <span id="chartID"></span>
              </div>
              <br></br>
              <button
                id="opt0"
                className="heading"
                style={graphBtn}
                onClick={() => this.getGraphData(empDailyData, zoneName, "opt0", "Daily")}
              >
                Daily Log
              </button>
              <button
                id="opt1"
                className="heading"
                style={graphBtn}
                onClick={() => this.getGraphData(empWeeklyData, zoneName, "opt1", "Weekly")}
              >
                Weekly Log
              </button>
              <button
                id="opt2"
                className="heading"
                style={graphBtn}
                onClick={() => this.getGraphData(empMonthlyData, zoneName, "opt2", "Monthly")}
              >
                Monthly Log
              </button>

              <button
                id="opt3"
                className="heading serverOpt3"
                style={graphBtn}
                onClick={() => this.getServerTempHumiGraph("/api/sensor/hub", zoneName, "opt3", "Temperature and Humidity")}
              >
                Temp/Humi Log
              </button>

              {series.length > 0 ? (
                <div style={{ width: "95%" }}>
                  <div
                    id="chart-timeline">
                    <ApexCharts
                      options={chartOpts}
                      series={series}
                      type="area"
                      height={380} />
                  </div>
                </div>
              ) : null}
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

export default Tracking;
