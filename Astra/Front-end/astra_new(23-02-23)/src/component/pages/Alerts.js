import React, { Component } from "react";
import { linkClicked } from "../navbar/Navbar";
import axios from "axios";
import $ from "jquery";
import "./Styling.css";
import moment from "moment";
import { alertData } from "../../urls/apis";
import { getPagination, TableDetails, DataLoading, showMessage } from './common'
const Underline = {
  width: "75px",
  height: "9px",
  position: "absolute",
};

class Alerts extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      error: false,
      message: ""
    };
  }
  componentDidMount() {
    linkClicked(5);
    this.getAlertData("first");
    this.interval = setInterval(() => {
      this.getAlertData("repeat");
    }, 15 * 1000);
  }
  componentWillUnmount() {
    clearInterval(this.interval);
    clearTimeout(this.messageTimeout);
  }

  getAlertData = (callStatus) => {
    this.setState({ error: false, message: "" });
    if (callStatus === "first") {
      this.setState({ loading: true });
    } else {
      this.setState({ loading: false });
    }
    let alertTypeId = $("#type").val();
    axios({
      method: "POST", url: alertData,
      data: { value: alertTypeId }
    })
      .then((response) => {
        $(".pagination").hide();
        $("#rangeDropdown").hide();
        $("#table_det tbody").empty();
        $("#table_det thead").empty();
        let data = response.data;
        if (response.status === 200 || response.status === 201) {
          console.log("Alerts Response====>", response);
          if (data.length !== 0) {
            $("#table_det thead").append(
              "<tr>" +
              "<th>SNO</th>" +
              "<th>MAC ID</th>" +
              "<th>EMPLOYEE NAME</th>" +
              // "<th>ALERT TYPE</th>" +
              "<th>START TIME</th>" +
              "<th>END TIME</th>" +
              "<th>DURATION</th>" +
              "</tr>"
            );
            let i = 0;
            let sno = 1;
            for (i = 0; i < data.length; i++) {
              var alert = "";
              let start_time = data[i].timestamp.substring(0, 19).replace("T", " ");
              let end_time = data[i].lastseen.substring(0, 19).replace("T", " ");

              const startTime = moment(start_time);
              const endTime = moment(end_time);
              const dura = moment.duration(endTime.diff(startTime));
              const seconds = dura.asSeconds();
              var hoursLeft = Math.floor(seconds / 3600);
              var min = Math.floor((seconds - hoursLeft * 3600) / 60);
              var secondsLeft = seconds - hoursLeft * 3600 - min * 60;
              secondsLeft = Math.round(secondsLeft * 100) / 100;
              let duration = hoursLeft < 10 ? "0" + hoursLeft : hoursLeft;
              duration += ":" + (min < 10 ? "0" + min : min);
              duration += ":" + (secondsLeft < 10 ? "0" + secondsLeft : secondsLeft);
              if (data[i].value === 1) alert = "Panic Button";
              else if (data[i].value === 3) alert = "Free Fall";
              else if (data[i].value === 4) alert = "No activity";
              else if (data[i].value === 5) alert = "Low Battery";
              $("#table_det tbody").append(
                "<tr>" +
                "<td>" + (sno) + "</td>" +
                "<td>" + data[i].asset.tagid + "</td>" +
                "<td>" + data[i].asset.name + "</td>" +
                // "<td>" + alert + "</td>" +
                "<td>" + start_time + "</td>" +
                "<td>" + end_time + "</td>" +
                "<td>" + duration + "</td>" +
                "</tr>"
              );
              sno += 1;
            }
            if (data.length > 25) {
              $(".pagination").show();
              $("#rangeDropdown").show();
              getPagination(this, "#table_det");
            }
            this.setState({ loading: false });
            showMessage(this, false, false, false, "");
          }
          else {
            this.setState({ loading: false });
            showMessage(this, false, true, false, "No Alert Data Found");
          }
        }
      })
      .catch((error) => {
        this.setState({ loading: false });
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has Timed Out. Please Login Again");
        } else if (error.response.status === 404) {
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          $("#table_det tbody").empty();
          $("#table_det thead").empty();
          showMessage(this, false, true, false, "No Alert Data Found");
        } else {
          showMessage(this, false, true, false, "Request Failed");
        }
      });
  };

  sessionTimeout = () => {
    $("#displayModal").css("display", "none");
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLogin(0);
  };

  render() {
    const { loading, error, message } = this.state;
    return (
      <>
        <div className="panel"
          style={{
            height: loading === true ? "600px" : "auto",
            overflow: loading === true ? "hidden" : "none",
          }}>
          <span className="main-heading">ALERTS</span>
          <br />
          <img alt="" src="../images/Tiles/Underline.png" style={Underline} />
          <div className="container fading" style={{ marginTop: "50px" }}>
            <div className="row">
              {/* Select list for tag type */}
              <div className="input-group">
                <span className="label">Event Type : </span>
                <select name="type" id="type" onChange={() => this.getAlertData("first")}>
                  <option value="1">Panic Button</option>
                  <option value="3">Free Fall</option>
                  <option value="4">No Activity</option>
                  <option value="5">Low Battery</option>
                </select>
              </div>
            </div>

            <br></br>
            {error && (
              <div
                className="error-msg"
                style={{ color: "red" }}>
                <strong>{message}</strong>
              </div>
            )}

            <TableDetails />

            {loading === true && (
              <div
                style={{
                  top: "0%",
                  left: "0%",
                }} className="frame">
                <DataLoading />
              </div>
            )}

          </div>
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
      </>
    );
  }
}

export default Alerts;
