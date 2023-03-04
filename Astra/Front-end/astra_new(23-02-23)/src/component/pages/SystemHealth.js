import React, { Component, Fragment } from "react";
import axios from "axios";
import $ from "jquery";
import "./Styling.css";
import { getPagination, TableDetails, DataLoading, showMessage } from './common'
import {
   employeeRegistration,
   masterGateway,
   signalRepeator,
   slaveGateway,
   tempertureSensor,
   irqSensor
} from "../../urls/apis";

const Underline = {
   width: "75px",
   height: "9px",
   position: "absolute",
};

axios.defaults.xsrfHeaderName = "x-csrftoken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

class SystemHealth extends Component {
   constructor() {
      super();
      this.state = {
         message: "",
         error: false,
         loading: false,
      };
   }
   componentDidMount() {
      this.getTableDetails("first");
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
      if ($("#healthtype").val() === "Master") {
         axios({ method: "GET", url: masterGateway })
            .then((response) => {
               const data = response.data;
               console.log("Master Response====>", data);
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (data.length !== 0 && response.status === 200) {
                  $("#table_det thead").append(
                     "<tr>" +
                     "<th>SNO</th>" +
                     "<th>MASTER ID</th>" +
                     "<th>FLOOR NAME</th>" +
                     "<th>LAST SEEN</th>" +
                     " <th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     if ((new Date() - new Date(data[i].lastseen)) <= (2 * 60 * 1000)) {
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].gatewayid + "</td>" +
                        "<td>" + data[i].floor.name + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  showMessage(this, false, true, false, "Master Data Not Found");
                  this.setState({ loading: false });
               }
            })
            .catch((error) => {
               console.log("ERROR====>", error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "Master Data Not Found");
               }
            })
      }
      else if ($("#healthtype").val() === "Slave") {
         axios({ method: "GET", url: slaveGateway })
            .then((response) => {
               const data = response.data;
               console.log('=====>slave', data);
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (data.length !== 0 && response.status === 200) {
                  $("#table_det thead").append(
                     "<tr>" +
                     "<th>SNO</th>" +
                     "<th>SLAVE ID</th>" +
                     "<th>MASTER ID</th>" +
                     "<th>FLOOR NAME</th>" +
                     "<th>LAST SEEN</th>" +
                     " <th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     if ((new Date() - new Date(data[i].lastseen)) <= (2 * 60 * 1000)) {
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].gatewayid + "</td>" +
                        "<td>" + data[i].master.gatewayid + "</td>" +
                        "<td>" + data[i].master.floor.name + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  showMessage(this, false, true, false, "Slave Data Not Found");
                  this.setState({ loading: false });
               }
            })
            .catch((error) => {
               console.log('Health Slave Gate Error====', error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "Slave Data Not Found");
               }
            })
      }
      else if ($("#healthtype").val() === 'Assets') {
         axios({ method: "GET", url: employeeRegistration + "?key=all" })
            .then((response) => {
               const data = response.data;
               console.log('=====>', response);
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (data.length !== 0 && response.status === 200) {
                  $("#table_det thead").append(
                     "<tr>" +
                     "<th>SNO</th>" +
                     "<th>ASSET NAME</th>" +
                     "<th>ASSET ID</th>" +
                     "<th>EMAIL ID</th>" +
                     "<th>BATTERY STATUS(%)</th>" +
                     " <th>IN-TIME</th>" +
                     "<th>LAST SEEN</th>" +
                     " <th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     if ((new Date() - new Date(data[i].lastseen)) <= (2 * 60 * 1000)) {
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].name + "</td>" +
                        "<td>" + data[i].tagid + "</td>" +
                        "<td>" + data[i].email + "</td>" +
                        "<td>" + data[i].battery + "</td>" +
                        "<td>" + data[i].intime.replace("T", " ").substring(0, 19) + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  this.setState({ loading: false });
                  showMessage(this, false, true, false, "Asset Data Not Found");
               }
            })
            .catch((error) => {
               console.log('Health asset tag gate Error====', error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "Asset Data Not Found");
               }
            })
      }
      else if ($("#healthtype").val() === 'Temperature/Humidity') {
         axios({ method: "GET", url: tempertureSensor })
            .then((response) => {
               const data = response.data;
               console.log('=====>', response);
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (data.length !== 0 && response.status === 200) {
                  $("#table_det thead").append(
                     "<tr>" +
                     "<th>SNO</th>" +
                     "<th>MAC ID </th>" +
                     "<th>TEMPERATURE </th>" +
                     "<th>HUMIDITY</th>" +
                     "<th>BATTERY STATUS(%)</th>" +
                     "<th>LAST SEEN</th>" +
                     " <th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     let mil = new Date() - new Date(data[i].lastseen.replace("T", " ").substr(0, 19));
                     if (mil <= (86400 * 1000)) { // Within 24hrs will display green
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].macid + "</td>" +
                        "<td>" + parseInt(data[i].temperature) + "</td>" +
                        "<td>" + parseInt(data[i].humidity) + "</td>" +
                        "<td>" + data[i].battery + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  this.setState({ loading: false });
                  showMessage(this, false, true, false, "Temperature/Humidity Data Not Found");
               }
            })
            .catch((error) => {
               console.log('Health Sensors Tag Gate Error====', error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "Temperature/Humidity Data Not Found");
               }
            })
      }
      else if ($("#healthtype").val() === 'IAQ') {
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
                     "<th>BATTERY</th>" +
                     "<th>LAST SEEN</th>" +
                     "<th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     if ((new Date() - new Date(data[i].lastseen)) <= (2 * 60 * 1000)) {
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].macid + "</td>" +
                        "<td>" + data[i].battery + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  this.setState({  loading: false });
                  showMessage(this, false, true, false, "IAQ Data Not Found");
               }
            })
            .catch((error) => {
               console.log('Health IAQ Error====', error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "IAQ Data Not Found");
               }
            })
      }
      else if ($("#healthtype").val() === 'SignalRepeaters') {
         axios({ method: "GET", url: signalRepeator })
            .then((response) => {
               const data = response.data;
               console.log('=====>', response);
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (data.length !== 0 && response.status === 200) {
                  $("#table_det thead").append(
                     "<tr>" +
                     "<th>SNO</th>" +
                     "<th>MAC ID </th>" +
                     "<th>LAST SEEN</th>" +
                     "<th>STATUS</th>" +
                     "</tr>"
                  );
                  for (let i = 0; i < data.length; i++) {
                     let status = 'red';
                     if ((new Date() - new Date(data[i].lastseen)) <= (2 * 60 * 1000)) {
                        status = "green";
                     }
                     $("#table_det tbody").append(
                        "<tr class=row_" + (i + 1) + ">" +
                        "<td>" + (i + 1) + "</td>" +
                        "<td>" + data[i].macid + "</td>" +
                        "<td>" + data[i].lastseen.replace("T", " ").substr(0, 19) + "</td>" +
                        "<td><div class='circle' style='margin:auto;background-color:" +
                        status +
                        ";'></div></td> " +
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
                  this.setState({ loading: false });
                  showMessage(this, false, true, false, "Signal Repeater Data Not Found");
               }
            })
            .catch((error) => {
               console.log('Health signalRepeater Gate Error====', error);
               this.setState({ loading: false });
               $(".pagination").hide();
               $("#rangeDropdown").hide();
               $("#table_det tbody").empty();
               $("#table_det thead").empty();
               if (error.response.status === 403) {
                  $("#displayModal").css("display", "block");
                  $("#content").text("User Session has timed out. Please Login again.");
               } else if (error.response.status === 404) {
                  showMessage(this, false, true, false, "Signal Repeater Data Not Found");
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
      const { loading, error, message } = this.state;
      return (
         <Fragment>
            <div className="panel"
               style={{
                  height: loading === true ? "600px" : "auto",
                  overflow: loading === true ? "hidden" : "none",
               }}>
               <span className="main-heading">SYSTEM HEALTH</span>
               <br />
               <img alt="" src="../images/Tiles/Underline.png" style={Underline} />
               <div style={{ marginBottom: '30px' }}>
                  <div className="inputdiv" style={{ marginTop: "20px" }}>
                     <span className="label">Health:</span>
                     <select
                        name="healthtype"
                        id="healthtype"
                        required="required"
                        onChange={() => {
                           clearInterval(this.interval)
                           this.componentDidMount()
                        }}>
                        <option value="Master">Master</option>
                        <option value="Slave">Slave</option>
                        <option value="Assets">Assets</option>
                        <option value="Temperature/Humidity">Temperature/Humidity Sensor</option>
                        <option value="IAQ">IAQ Sensor</option>
                        <option value="SignalRepeaters">Signal Repeaters</option>
                     </select>
                  </div>
               </div>
               {error && (
                  <div
                     className="error-msg"
                     style={{ color: "red", marginTop: "20px" }}>
                     <strong>{message}</strong>
                  </div>
               )}
               <TableDetails />
            </div>
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

            {loading === true && (
               <div
                  style={{
                     top: "0%",
                     left: "0%",
                  }} className="frame">
                  <DataLoading />
               </div>
            )}
         </Fragment>
      );
   }
}

export default SystemHealth;
