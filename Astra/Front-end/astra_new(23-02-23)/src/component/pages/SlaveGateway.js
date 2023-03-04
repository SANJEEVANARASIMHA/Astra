import React, { Component, Fragment } from "react";
import axios from "axios";
import "./Styling.css";
import $ from "jquery";
import { showMessage } from "./common";
import { masterGateway, slaveGateway } from "../../urls/apis";

class SlaveGateway extends Component {

  constructor(props) {
    super(props);
    this.state = {
      message: "",
      error: false,
      success: false,
    }
  }

  componentDidMount() {
    axios({
      method: "GET",
      url: masterGateway,
    })
      .then((response) => {
        console.log("Floor Response=====>", response);
        if (response.status === 201 || response.status === 200) {
          this.fdata = response.data;
          if (this.fdata.length !== 0) {
            for (let i = 0; i < this.fdata.length; i++) {
              $("#mastergatewayid").append(
                "<option>" + this.fdata[i].gatewayid + "</option>"
              );
            }
          } else {
            showMessage(this, false, true, false, "Please Register Master Gateway ID");
          }
        } else {
          showMessage(this, false, true, false, "Unable To Get Master Gateway ID");
        }
      })
      .catch((error) => {
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has Timed Out. Please Login Again");
        } else if (error.response.status === 404) {
          showMessage(this, false, true, false, "Please Register Master Gateway ID");
        } else {
          showMessage(this, false, true, false, "Request Failed with status code (" + error.response.status + ")");
        }
      });
  }

  show = () => {
    $("#slaveid").val("");
    $("input[type='text']").val("");
    document.getElementById("slave-del-form").style.display =
      $("#slave-del-form").css("display") === "block" ? "none" : "block";
  };

  hide = () => {
    showMessage(this, false, false, false, "")
  };

  registerSlave = (e) => {
    e.preventDefault();
    this.hide();
    $("#slave-del-form").css("display", "none");
    let slave = $("#slaveid").val();
    if (slave.length === 0) {
      showMessage(this, true, true, false, "Please Enter Gateway ID")
    } else if (slave.match("^5a-c2-15-0a-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
      showMessage(this, true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-0a-00-00");
    } else {
      let gateway = $("#mastergatewayid").val();
      axios({
        method: "POST",
        url: slaveGateway,
        data: { master: gateway, macaddress: slave },
      })
        .then((response) => {
          if (response.status === 200 || response.status === 201) {
            showMessage(this, true, false, true, "Slave Gateway Registered Successfully")
            $("#slaveid").val("");
          } else {
            showMessage(this, true, true, false, "Unable to Registered Slave Gateway")
          }
        })
        .catch((error) => {
          console.log(error.response);
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text(
              "User Session has Timed Out. Please Login Again"
            );
          } else {
            showMessage(this, true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  unregisterSlave = (e) => {
    this.hide();
    e.preventDefault();
    let id = $("#slaveid-del").val();
    if (id.length === 0) {
      showMessage(this, true, true, false, "Please Enter Gateway ID");
    } else if (id.match("^5a-c2-15-0a-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
      showMessage(this, true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-0a-00-00");
    } else {
      axios({
        method: "DELETE",
        url: slaveGateway,
        data: { macaddress: id },
      })
        .then((response) => {
          if (response.status === 200 || response.status === 201) {
            $("#slaveid-del").val("");
            showMessage(this, true, false, true, "Slave Gateway ID Deleted Successfully");
            this.show();
          } else {
            showMessage(this, true, true, false, "Unable To Delete Slave Gateway");
          }
        })
        .catch((error) => {
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text(
              "User Session has Timed Out. Please Login Again."
            );
          } else if (error.response.status === 400) {
            showMessage(this, true, true, false, "Bad Request");
          } else {
            showMessage(this, true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  componentWillUnmount() {
    clearTimeout(this.messageTimeout);
  }

  sessionTimeout = () => {
    $("#displayModal").css("display", "none");
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLoginError();
  };

  render() {
    const { message, success, error } = this.state;
    return (
      <Fragment>
        <span className="sub-heading">Slave Gateway Registration</span>
        <br />
        <img
          src="../images/Tiles/Underline.png"
          alt=""
          style={{
            width: "56px",
            height: "3px",
            marginTop: "2px",
            position: "absolute",
          }}
        />
        <br></br>
        <div>
          {error && (
            <div style={{ color: "red", marginBottom: "20px" }}>
              <strong>{message}</strong>
            </div>
          )}

          {success && (
            <div style={{ color: "green", marginBottom: "20px" }}>
              <strong>{message}</strong>
            </div>
          )}
        </div>
        <form id="slave-reg-form">
          <div className="input-group">
            <span className="label">Master Gateway ID :</span>
            <select id="mastergatewayid" onChange={() => this.hide()}></select>
          </div>
          <div className="input-group">
            <span className="label">Gateway ID :</span>
            <input
              type="text"
              name="slaveid"
              id="slaveid"
              required="required"
              placeholder="5a-c2-15-00-00-00"
              onChange={this.hide}
            />
          </div>
        </form>
        <div style={{ display: "flex", margin: "15px", marginLeft: "153px" }}>
          <input
            style={{ background: '#eb6565' }}
            type="button"
            onClick={() => {
              this.show();
              this.hide();
            }}
            value="Remove Gateway"
            className="btn success-btn"
          />
          <input style={{ marginLeft: "40px", }}
            type="submit"
            onClick={this.registerSlave}
            value="Register Gateway"
            className="btn success-btn"
          />

        </div>
        <form
          id="slave-del-form"
          className="fading"
          style={{ display: "none" }}
        >
          <div className="input-group">
            <span className="label">Gateway ID :</span>
            <input
              type="text"
              name="slaveid-del"
              id="slaveid-del"
              required="required"
              onClick={this.hide}
              placeholder="5a-c2-15-00-00-00"
            />
          </div>
          <div className="input-group" style={{ margin: "15px", marginLeft: "253px" }}>
            <input style={{ background: '#eb6565' }}
              type="submit"
              value="Remove Gateway"
              onClick={this.unregisterSlave}
              className="btn success-btn"
            />
          </div>
        </form>
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

export default SlaveGateway;
