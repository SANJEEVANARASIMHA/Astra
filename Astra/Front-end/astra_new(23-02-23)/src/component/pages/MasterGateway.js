import React, { Component, Fragment } from "react";
import axios from "axios";
import "./Styling.css";
import $ from "jquery";
import { showMessage } from "./common";
import { masterGateway, floorMap } from "../../urls/apis";

class MasterGateway extends Component {
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
      url: floorMap,
    })
      .then((response) => {
        console.log("Floor Response=====>", response);
        if (response.status === 201 || response.status === 200) {
          this.fdata = response.data;
          if (this.fdata.length !== 0) {
            for (let i = 0; i < this.fdata.length; i++) {
              $("#fname").append("<option value=" +this.fdata[i].id +">" +this.fdata[i].name +"</option>");
            }
          } else {
            showMessage(this, false, true, false, "Please Upload Floormap");
          }
        } else {
          showMessage(this, false, true, false, "Unable to Fetch Floor Names");
        }
      })
      .catch((error) => {
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has Timed Out. Please Login Again.");
        } else if (error.response.status === 400) {
          showMessage(this, false, true, false, "Bad Request");
        } else {
          showMessage(this, false, true, false, "Request Failed with status code (" + error.response.status + ").");
        }
      });
  }

  /** Displays Delete master gateway form on clicking Delete Gateway Button */
  show = () => {
    document.getElementById("gatewayid").value = "";
    $("input[type='text']").val("");
    document.getElementById("gateway-del-form").style.display =
      document.getElementById("gateway-del-form").style.display === "block"
        ? "none"
        : "block";
  };

  /** Hides all error and success messages displayed on all button clicks */
  hide = () => {
    showMessage(this, false, false, false, "")
  };

  /** Reigster the master gateway for particular floor */
  registerGateway = (e) => {
    e.preventDefault();
    this.hide();
    $("#gateway-del-form").css("display", "none");
    let id = document.getElementById("gatewayid").value;
    if (id.length === 0) {
      showMessage(this, true, true, false, "Please Enter Gateway ID");
    }else if (id.match("^5a-c2-15-08-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
      showMessage(this, true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-08-00-00");
    } else {
      let floorid = $("fname").val();
      axios({
        method: "POST",
        url: masterGateway,
        data: { macaddress: id, id: floorid },
      })
        .then((response) => {
          if (response.status === 201 || response.status === 200) {
            $("#gatewayid").val("");
            showMessage(this, true, false, true, "Master Gateway Registered Successfully");
          } else {
            showMessage(this, true, true, false, response.data.message);
          }
        })
        .catch((error) => {
          console.log(error.response);
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text(
              "User Session has Timed Out. Please Login Again."
            );
          } else if (error.response.status === 400) {
            showMessage(this, true, true, false, "Master Gateway ID Already Exist");
          } else {
            showMessage(this, true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  /** Remove master gateway for particular floor along with all slaves under it */
  unregisterGateway = (e) => {
    e.preventDefault();
    this.hide();
    let id = document.getElementById("gateway").value;
    if (id.length === 0) {
      showMessage(this, true, true, false, "Please Enter Gateway ID");
    } else if (id.match("^5a-c2-15-08-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
      showMessage(this, true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-08-00-00");
    } else {
      axios({
        method: "DELETE",
        url: masterGateway,
        data: { macaddress: id },
      })
        .then((response) => {
          if (response.status === 201 || response.status === 200) {
            $("#gateway").val("");
            showMessage(this, true, false, true, "Gateway ID Deleted Successfully");
            this.show();
          } else {
            showMessage(this, true, true, false, response.data.message);
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

  /** Terminate the session on forbidden (403) error */
  sessionTimeout = () => {
    document.getElementById("displayModal").style.display = "none";
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLoginError();
  };

  render() {
    const { message, success, error } = this.state;
    return (
      <Fragment>
        <span className="sub-heading">Master Gateway Registration</span>
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
        {/* Elements for displaying error messages */}
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
        {/* Form to register master gateway */}
        <form id="gateway-reg-form">
          {/* Select list for Floor names */}
          <div className="input-group">
            <span className="label">Floor Name :</span>
            <select name="type" id="fname" onChange={() => this.hide()}></select>
          </div>
          {/* Input field for Gateway ID */}
          <div className="input-group">
            <span className="label">Gateway ID :</span>
            <input
              type="text"
              name="gatewayid"
              id="gatewayid"
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
            onClick={this.registerGateway}
            value="Register Gateway"
            className="btn success-btn"
          />
        </div>
        <form
          id="gateway-del-form"
          className="fading"
          style={{ display: "none" }}
        >
          {/* Input Field for Tag MAC ID */}
          <div className="input-group">
            <span className="label">Gateway MAC ID :</span>
            <input
              type="text"
              name="gateway"
              id="gateway"
              required="required"
              onClick={this.hide}
              placeholder="5a-c2-15-00-00-00"
            />
          </div>
          {/* Elements for displaying error messages */}
          <div className="input-group" style={{ margin: "15px", marginLeft: "260px" }}>
            <input
              style={{ background: '#eb6565' }}
              type="submit"
              value="Remove Gateway"
              onClick={this.unregisterGateway}
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

export default MasterGateway;
