import React, { Component, Fragment } from "react";
import axios from "axios";
import $ from "jquery";
import "./Styling.css";
import {
  employeeRegistration,
  irqSensor,
  signalRepeator,
  tempertureSensor,
} from "../../urls/apis";
import { getPagination, TableDetails, DataLoading, showMessage } from './common'

// Styling property for Underline Image
const Underline = {
  width: "75px",
  height: "9px",
  position: "absolute",
};

class Assets extends Component {
  constructor() {
    super();
    this.state = {
      loading: false,
      error: false,
      message: ''
    };
  }

  /** Method is called on Component Load */
  componentDidMount() {
    this.getTableDetails("first");
    $("#rangeDropdown").css("margin-top", "-5%");
    this.interval = setInterval(() => {
      this.getTableDetails("repeat");
    }, 15 * 1000);
  }

  componentWillUnmount() {
    clearInterval(this.interval);
    clearTimeout(this.messageTimeout);
  }

  getTableDetails = (callStatus) => {
    showMessage(this, false, false, false, "");
    if (callStatus === "first") {
      this.setState({ loading: true });
    } else {
      this.setState({ loading: false });
    }
    if ($("#tagtype").val() === "temperature") {
      axios({ method: "GET", url: tempertureSensor })
        .then((response) => {
          const data = response.data;
          console.log("temp/humid Response====>", response);
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          $("#table_det tbody").empty();
          $("#table_det thead").empty();
          if (response.status === 200 || response.status === 201) {
            if (data.length !== 0) {
              this.setState({ loading: false });
              $("#table_det thead").append(
                "<tr>" +
                "<th>SNO</th>" +
                "<th>MAC ID</th>" +
                "<th>TEMPERATURE</th>" +
                "<th>HUMIDITY</th>" +
                "<th>BATTERY</th>" +
                "<th>LAST SEEN</th>" +
                "</tr>"
              );
              for (let i = 0; i < data.length; i++) {
                $("#table_det tbody").append(
                  "<tr>" +
                  "<td>" + (i + 1) + "</td>" +
                  "<td>" + data[i].macid + "</td>" +
                  "<td>" + data[i].temperature + "</td>" +
                  "<td>" + data[i].humidity + "</td>" +
                  "<td>" + data[i].battery + "</td>" +
                  "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                  "</tr>"
                )
              }
              this.setState({ loading: false });
            }
          } else {
            showMessage(this, false, true, false, "Temperature/Humidity Data Not Found");
            this.setState({ loading: false });
          }
          if (data.length > 25) {
            $(".pagination").show();
            $("#rangeDropdown").show();
            getPagination(this, "#table_det");
          }
        })
        .catch((error) => {
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          console.log("ERROR====>", error);
          this.setState({ loading: false });
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text("User Session has timed out. Please Login again.");
          } else if (error.response.status === 404) {
            showMessage(this, false, true, false, "Temperature/Humidity Data Not Found");
            $("#table_det thead").empty();
            $("#table_det tbody").empty();
          }
        })
    }

    else if ($("#tagtype").val() === "iaq") {
      axios({ method: "GET", url: irqSensor })
        .then((response) => {
          const data = response.data;
          console.log('=====>iaq', data);
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          $("#table_det tbody").empty();
          $("#table_det thead").empty();
          if (data.length !== 0 && response.status === 200) {
            $("#table_det thead").append(
              "<tr>" +
              "<th>SNO</th>" +
              "<th>MAC ID</th>" +
              "<th>SENSOR TYPE</th>" +
              "<th>BATTERY</th>" +
              "<th>LAST SEEN</th>" +
              "</tr>"
            );
            for (let i = 0; i < data.length; i++) {
              $("#table_det tbody").append(
                "<tr class=row_" + (i + 1) + ">" +
                "<td>" + (i + 1) + "</td>" +
                "<td>" + data[i].macid + "</td>" +
                "<td>IAQ Sensors</td>" +
                "<td>" + data[i].battery + "</td>" +
                "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                "</tr>"
              )
            }
            if (data.length > 25) {
              $(".pagination").show();
              $("#rangeDropdown").show();
              getPagination(this, "#table_det");
            }
            this.setState({ loading: false });
          } else {
            showMessage(this, false, true, false, "IAQ Data Not Found");
            this.setState({ loading: false });
          }
        })
        .catch((error) => {
          //  console.log(' Error====', error);
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          this.setState({ loading: false });
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text("User Session has timed out. Please Login again.");
          } else if (error.response.status === 404) {
            showMessage(this, false, true, false, "IAQ Data Not Found");
            $("#table_det thead").empty();
            $("#table_det tbody").empty();
          }
        })
    } else if ($("#tagtype").val() === 'signal') {
      axios({ method: "GET", url: signalRepeator })
        .then((response) => {
          const data = response.data;
          console.log('signal=====>', response);
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          $("#table_det tbody").empty();
          $("#table_det thead").empty();
          if (data.length !== 0 && response.status === 200) {
            $("#table_det thead").append(
              "<tr>" +
              "<th>SNO</th>" +
              "<th>MAC ID</th>" +
              "<th>LAST SEEN</th>" +
              "</tr>"
            );
            for (let i = 0; i < data.length; i++) {
              $("#table_det tbody").append(
                "<tr class=row_" + (i + 1) + ">" +
                "<td>" + (i + 1) + "</td>" +
                "<td>" + data[i].macid + "</td>" +
                "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                "</tr>"
              )
            }
          } else {
            showMessage(this, false, true, false, "Signal Repeater Data Not Found");
            this.setState({ loading: false });
          }
          if (data.length > 25) {
            $(".pagination").show();
            $("#rangeDropdown").show();
            getPagination(this, "#table_det");
          }
          this.setState({ loading: false });
        })
        .catch((error) => {
          //  console.log('Health asset tag gate Error====', error);
          this.setState({ loading: false });
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text("User Session has timed out. Please Login again.");
          } else if (error.response.status === 404) {
            showMessage(this, false, true, false, "Signal Repeater Data Not Found");
            $("#table_det thead").empty();
            $("#table_det tbody").empty();
          }
        })
    }
    else if ($("#tagtype").val() === 'employee') {
      axios({ method: "GET", url: employeeRegistration + "?key=all", })
        .then((response) => {
          const data = response.data;
          console.log('employee=====>', response);
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          $("#table_det tbody").empty();
          $("#table_det thead").empty();
          if (data.length !== 0 && response.status === 200) {
            $("#table_det thead").append(
              "<tr>" +
              "<th>SNO</th>" +
              "<th>MAC ID </th>" +
              "<th>EMPLOYEE NAME</th>" +
              "<th>EMPLOYEE ID</th>" +
              "<th>EMAIL ID</th>" +
              " <th>IN-TIME</th>" +
              "</tr>"
            );
            for (let i = 0; i < data.length; i++) {
              $("#table_det tbody").append(
                "<tr><td>" +
                (i + 1) +
                "</td><td>" +
                data[i].tagid +
                "</td><td>" +
                data[i].name +
                "</td><td>" +
                data[i].empid +
                "</td><td>" +
                data[i].email +
                "</td><td>" +
                data[i].intime.substring(0, 19).replace("T", " ") +
                "</td></tr>"
              )
            }
          } else {
            showMessage(this, false, true, false, "Employee Data Not Found");
            this.setState({ loading: false });
          }
          if (data.length > 25) {
            $(".pagination").show();
            $("#rangeDropdown").show();
            getPagination(this, "#table_det");
          }
          this.setState({ loading: false });
        })
        .catch((error) => {
          console.log('Health Sensors Tag Gate Error====', error);
          this.setState({ loading: false });
          $(".pagination").hide();
          $("#rangeDropdown").hide();
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text("User Session has timed out. Please Login again.");
          } else if (error.response.status === 404) {
            showMessage(this, false, true, false, "Employee Data Not Found");
            $("#table_det thead").empty();
            $("#table_det tbody").empty();
          }
        })
    }
  };

  sessionTimeout = () => {
    $("#displayModal").css("display", "none");
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLogin(0);
  };

  render() {
    const { error, message, loading } = this.state;
    return (
      <Fragment>
        <div className="panel"
          style={{
            height: loading === true ? "600px" : "auto",
            overflow: loading === true ? "hidden" : "none",
          }}>
          <span className="main-heading">ALL ASSETS</span>
          <br />
          <img alt="" src="../images/Tiles/Underline.png" style={Underline} />

          <div className="container fading" style={{ marginTop: "20px" }}>
            <div className="row">
              <div className="input-group">
                <span className="label">Tag Type : </span>
                <select
                  name="tagtype"
                  id="tagtype"
                  onChange={() => this.getTableDetails("first")}>
                  <option value="temperature">
                    Temperature/Humidity Sensor
                  </option>
                  <option value="iaq">IAQ Sensor</option>
                  <option value="signal">Signal Repeater</option>
                  <option value="employee">Employee</option>
                </select>
              </div>
            </div>
            <hr />
            {error && (
              <div
                className="error-msg"
                style={{ color: "red", marginTop: "20px" }}>
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
        {/* Display modal to display error messages */}
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
      </Fragment>
    );
  }
}

export default Assets;
