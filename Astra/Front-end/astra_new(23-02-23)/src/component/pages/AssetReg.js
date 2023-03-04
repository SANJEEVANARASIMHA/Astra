import React, { Component, Fragment } from "react";
import axios from "axios";
import "./Styling.css";
import $ from "jquery";
import { showMessage } from "./common";
import {
  employeeRegistration,
  empBulkReg,
  floorMap,
  irqSensor,
  signalRepeator,
  tempertureSensor,
} from "../../urls/apis";
import * as XLSX from "xlsx";

class AssetReg extends Component {

  constructor(props) {
    super(props);
    this.state = {
      message: "",
      error: false,
      success: false,
    }
  }

  componentDidMount = () => {
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
              $("#fname").append(
                "<option value=" +
                this.fdata[i].id +
                ">" +
                this.fdata[i].name +
                "</option>"
              );
              $("#fname1").append(
                "<option value=" +
                this.fdata[i].id +
                ">" +
                this.fdata[i].name +
                "</option>"
              );
            }
          } else {
            showMessage(this,false, true, false, "Please Upload Floormap");
          }
        } else {
          showMessage(this,false, true, false, "Unable to Fetch Floor Names");
        }
      })
      .catch((error) => {
        if (error.response.status === 403) {
          $("#displayModal").css("display", "block");
          $("#content").text("User Session has Timed Out. Please Login Again.");
        } else if (error.response.status === 400) {
          showMessage(this,false, true, false, "Bad Request");
        } else {
          showMessage(this,false, true, false, "Request Failed with status code (" + error.response.status + ").");
        }
      });
  };

  displayTrackingForm = () => {
    let type = $("#type").val();
    this.setState({ type: type });
    if (type === "Temperature/Humidity Sensor") {
      $("#temp_form").css("display", "block");
      $("#bulk_reg").css("display", "none");
    } else $("#temp_form").css("display", "none");

    if (type === "IAQ Sensor") {
      $("#iaq_form").css("display", "block");
      $("#bulk_reg").css("display", "none");
    } else $("#iaq_form").css("display", "none");

    if (type === "Signal Repeater") {
      $("#bulk_reg").css("display", "none");
    }

    if (type === "Employee") {
      $("#emp_form").css("display", "block");
      $("#bulk_reg").css("display", "block");
    } else {
      $("#emp_form").css("display", "none");
    }
  };

  show = () => {
    $("input[type=text]").val("");
    $("input[type=email]").val("");
    $("#bulk_form").css("display", "none");

    document.getElementById("delete-form").style.display =
      $("#delete-form").css("display") === "none" ? "block" : "none";
    window.scrollTo(0, document.body.scrollHeight);
  };

  hide = () => {
    showMessage(this,false, false, false, "")
  };

  register = (e) => {
    e.preventDefault();
    this.hide();
    $("#delete-form").css("display", "none");
    let data = {};
    if ($("#type").val() === "Temperature/Humidity Sensor") {
      data = {
        macaddress: $("#tagid").val(),
        x1: $("#x").val(),
        y1: $("#y").val(),
        x2: $("#x1").val(),
        y2: $("#y1").val(),
        id: $("#fname").val(),
      };
      if (
        data.x1 !== "" &&
        data.y1 !== "" &&
        data.x2 !== "" &&
        data.y2 !== "" &&
        data.id !== ""
      ) {
        if ($("#tagid").val().match("^5a-c2-15-03-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
          showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-03-00-00");
        } else {
          axios({
            method: "POST",
            url: tempertureSensor,
            data: data,
          })
            .then((response) => {
              console.log("======>", response);
              if (response.status === 201) {
                showMessage(this,true, false, true, "Temperature/Humidity Sensor Registered Successfully");
              } else {
                showMessage(this,true, true, false, response.data.message);
              }
            })
            .catch((error) => {
              if (error.response.status === 403) {
                $("#displayModal").css("display", "block");
                $("#content").text(
                  "User Session has Timed Out. Please Login Again."
                );
              } else if (error.response.status === 400) {
                showMessage(this,true, true, false, "Tag ID Already Exist");
              } else {
                showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
              }
            });
        }
      } else {
        showMessage(this,true, true, false, "Please Provide All Information");
      }
    } else if ($("#type").val() === "IAQ Sensor") {
      data = {
        macaddress: $("#tagid").val(),
        x: $("#xval").val(),
        y: $("#yval").val(),
        id: $("#fname1").val(),
      };
      if (data.x !== "" && data.y !== "" && data.id !== "" && data.macaddress !== "") {
        if ($("#tagid").val().match("^5a-c2-15-04-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
          showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-04-00-00");
        } else {
          axios({
            method: "POST",
            url: irqSensor,
            data: data,
          })
            .then((response) => {
              console.log("======>", response);
              if (response.status === 201) {
                showMessage(this,true, false, true, "IAQ Sensor Registered Successfully");
              } else {
                showMessage(this,true, true, false, response.data.message);
              }
            })
            .catch((error) => {
              console.log(error);
              if (error.response.status === 403) {
                $("#displayModal").css("display", "block");
                $("#content").text(
                  "User Session has Timed Out. Please Login again."
                );
              } else if (error.response.status === 400) {
                showMessage(this,true, true, false, "Tag ID Already Registered");
              } else {
                showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
              }
            });
        }
      } else {
        showMessage(this,true, true, false, "Please Provide All Information");
      }
    } else if ($("#type").val() === "Employee") {
      data = {
        tagid: $("#tagid").val(),
        name: $("#emp_name").val(),
        role: $("#emp_role").val(),
        email: $("#emp_email").val(),
        empid: $("#emp_id").val(),
        phone: $("#emp_phoneNo").val(),
      };
      console.log("Employee========>", data);
      if (
        data.tagid.length !== 0 &&
        data.name.length !== 0 &&
        data.role.length !== 0 &&
        data.email.length !== 0 &&
        data.empid.length !== 0 &&
        data.phone.length !== 0
      ) {
        if ($("#tagid").val().match("^5a-c2-15-01-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
          showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-01-00-00");
        } else {
          axios({
            method: "POST",
            url: employeeRegistration,
            data: data,
          })
            .then((response) => {
              console.log("------->", response);
              if (response.status === 201 || response.status === 200) {
                showMessage(this,true, false, true, "Employee Tag Registered Successfully");
              } else {
                showMessage(this,true, true, false, response.data.message);
              }
            })
            .catch((error) => {
              if (error.response.status === 403) {
                $("#displayModal").css("display", "block");
                $("#content").text(
                  "User Session has timed out. Please Login again."
                );
              } else if (error.response.status === 400) {
                showMessage(this,true, true, false, "Employee Tag ID Already Exist");
              } else {
                showMessage(this,true, true, false, "Request Failed with status code(" + error.response.status + ")");
              }
            });
        }
      } else {
        showMessage(this,true, true, false, "Please Provide All Information");
      }
    } else {
      data = {
        macaddress: $("#tagid").val(),
      };
      if (data.macaddress.length !== 0) {
        if ($("#tagid").val().match("^5a-c2-15-06-[a-x0-9]{2}-[a-x0-9]{2}") === null) {
          showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-06-00-00");
        } else {
          axios({
            method: "POST",
            url: signalRepeator,
            data: data,
          })
            .then((response) => {
              if (response.status === 201 || response.status === 200) {
                console.log("======>", response);
                showMessage(this,true, false, true, "Signal Repeater Registered Successfully");
              } else {
                showMessage(this,true, true, false, response.data.message);
              }
            })
            .catch((error) => {
              if (error.response.status === 403) {
                $("#displayModal").css("display", "block");
                $("#content").text(
                  "User Session has Timed Out. Please Login Again."
                );
              } else if (error.response.status === 400) {
                showMessage(this,true, true, false, "Signal Repeater Already Exist");
              } else {
                showMessage(this,true, true, false, "Request Failed with status code(" + error.response.status + ")");
              }
            });
        }
      } else {
        showMessage(this,true, true, false, "Please Provide All Information");
      }
    }

    $("input[type=text]").val("");
    $("input[type=email]").val("");
    $("input[type=number]").val("");
  };

  unregister = (e) => {
    this.hide();
    e.preventDefault();
    let id = $("#macid").val();

    if ($("#tagtype").val() === "Temperature/Humidity Sensor") {
      if (id.length === 0)
        showMessage(this,true, true, false, "Please Enter MAC ID");
      else if (id.match("^5a-c2-15-03-[a-x0-9]{2}-[a-x0-9]{2}") === null)
        showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-03-00-00");
      else {
        axios({
          method: "DELETE",
          url: tempertureSensor,
          data: { macaddress: id },
        })
          .then((response) => {
            if (response.status === 200) {
              $("#delete-form").css("display", "none");
              showMessage(this,true, false, true, "Temperature/Humidity Sensor Deleted Successfully");
            } else {
              showMessage(this,true, true, false, response.data.message);
            }
          })
          .catch((error) => {
            if (error.response.status === 403) {
              $("#displayModal").css("display", "block");
              $("#content").text(
                "User Session has Timed Out. Please Login Again"
              );
            } else {
              showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
            }
          });
      }
    } else if ($("#tagtype").val() === "IAQ Sensor") {
      if (id.length === 0)
        showMessage(this,true, true, false, "Please Enter MAC ID");
      else if (id.match("^5a-c2-15-04-[a-x0-9]{2}-[a-x0-9]{2}") === null)
        showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-04-00-00");
      else {
        axios({
          method: "DELETE",
          url: irqSensor,
          data: { macaddress: id },
        })
          .then((response) => {
            if (response.status === 200) {
              $("#delete-form").css("display", "none");
              showMessage(this,true, false, true, "IAQ Sensor Deleted Successfully");
            } else {
              showMessage(this,true, true, false, response.data.message);
            }
          })
          .catch((error) => {
            if (error.response.status === 403) {
              $("#displayModal").css("display", "block");
              $("#content").text(
                "User Session has Timed Out. Please Login Again"
              );
            } else {
              showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
            }
          });
      }
    } else if ($("#tagtype").val() === "Signal Repeater") {
      if (id.length === 0)
        showMessage(this,true, true, false, "Please Enter MAC ID");
      else if (id.match("^5a-c2-15-06-[a-x0-9]{2}-[a-x0-9]{2}") === null)
        showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-06-00-00");
      else {
        axios({
          method: "DELETE",
          url: signalRepeator,
          data: { macaddress: id },
        })
          .then((response) => {
            if (response.status === 200) {
              $("#delete-form").css("display", "none");
              showMessage(this,true, false, true, "Signal Repeater Sensor Deleted Successfully");
            } else {
              showMessage(this,true, true, false, response.data.message);
            }
          })
          .catch((error) => {
            if (error.response.status === 403) {
              $("#displayModal").css("display", "block");
              $("#content").text(
                "User Session has Timed Out. Please Login Again."
              );
            } else {
              showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
            }
          });
      }
    } else if ($("#tagtype").val() === "Employee") {
      if (id.length === 0)
        showMessage(this,true, true, false, "Please Enter MAC ID");
      else if (id.match("^5a-c2-15-01-[a-x0-9]{2}-[a-x0-9]{2}") === null)
        showMessage(this,true, true, false, "Invalid ID Entered. Please Follow The Pattern 5a-c2-15-01-00-00");
      else {
        axios({
          method: "DELETE",
          url: employeeRegistration,
          data: { tagid: id },
        })
          .then((response) => {
            if (response.status === 200) {
              $("#delete-form").css("display", "none");
              showMessage(this,true, false, true, "Employee Tag Deleted Successfully");
            } else {
              showMessage(this,true, true, false, response.data.message);
            }
          })
          .catch((error) => {
            if (error.response.status === 403) {
              $("#displayModal").css("display", "block");
              $("#content").text(
                "User Session has Timed Out. Please Login Again."
              );
            } else {
              showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
            }
          });
      }
    }
    $("input[type=text]").val("");
    $("input[type=email]").val("");
  };

  excelToJson(reader) {
    var fileData = reader.result;
    var wb = XLSX.read(fileData, { type: "binary" });
    var data = {};
    var data1 = [];
    wb.SheetNames.forEach(function (sheetName) {
      var rowObj = XLSX.utils.sheet_to_row_object_array(wb.Sheets[sheetName]);
      var rowString = JSON.stringify(rowObj);
      data[sheetName] = rowString;
      data1 = rowObj;
    });
    this.setState({ excelData: data1 });
  }

  loadFileXLSX(event) {
    var input = event.target;
    var reader = new FileReader();
    reader.onload = this.excelToJson.bind(this, reader);
    reader.readAsBinaryString(input.files[0]);
  }

  bulkRegister = (e) => {
    e.preventDefault();
    $("#bulk_file").val("");
    console.log("bulkRegister=======>", this.state.excelData);
    if (this.state.excelData === undefined || this.state.excelData === null) {
      showMessage(this,true, true, false, "No File Found");
    } else if (this.state.excelData.length > 0) {
      axios({
        method: "POST",
        url: empBulkReg,
        data: this.state.excelData,
      })
        .then((res) => {
          console.log("RESPONSE======>", res);
          if (res.status === 200 || res.status === 201) {
            $("#bulk_file").val("");
            showMessage(this,true, false, true, "Bulk Registered Successfully");
          } else if (res.status === 208) {
            showMessage(this,true, true, false, res.data.error);
          } else {
            showMessage(this,true, true, false, "Unable to Register");
          }
        })
        .catch((error) => {
          console.log("ERROR=====>", error.response.data.message);
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text(
              "User Session has Timed Out. Please Login Again."
            );
          } else if (error.response.status === 406) {
            showMessage(this,true, true, false, error.response.data.message);
          } else {
            showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  bulkUpdate = (e) => {
    e.preventDefault();
    $("#bulk_file").val("");
    console.log("bulkUpdate==========>", this.state.excelData);
    if (this.state.excelData === undefined || this.state.excelData === null) {
      showMessage(this,true, true, false, "No File Found");
    } else if (this.state.excelData.length > 0) {
      axios({
        method: "PATCH",
        url: empBulkReg,
        data: this.state.excelData,
      })
        .then((res) => {
          if (res.status === 200 || res.status === 201) {
            console.log("RESPONSE======>", res);
            $("#bulk_file").val("");
            showMessage(this,true, false, true, "Bulk Update Successfully");
          } else if (res.status === 208) {
            showMessage(this,true, true, false, res.data.error);
          } else {
            showMessage(this,true, true, false, "Unable to Update");
          }
        })
        .catch((error) => {
          console.log("ERROR=====>", error);
          if (error.response.status === 403) {
            $("#displayModal").css("display", "block");
            $("#content").text(
              "User Session has Timed Out. Please Login Again."
            );
          } else {
            showMessage(this,true, true, false, "Request Failed with status code (" + error.response.status + ")");
          }
        });
    }
  };

  sessionTimeout = () => {
    $("#displayModal").css("display", "none");
    sessionStorage.setItem("isLoggedIn", 0);
    this.props.handleLoginError();
  };

  componentWillUnmount() {
    clearTimeout(this.messageTimeout);
  }

  render() {
    const { message, success, error } = this.state;
    return (
      <Fragment>
        <span className="sub-heading">Asset Registration</span>
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
        <form id="reg-form">
          <div className="input-group">
            <span className="label">Tag MAC ID :</span>
            <input
              type="text"
              id="tagid"
              required="required"
              onClick={this.hide}
              placeholder="5a-c2-15-00-00-00"
            />
          </div>
          <div className="input-group">
            <span className="label">Tag Type :</span>
            <select
              id="type"
              onChange={() => {
                this.displayTrackingForm();
                this.hide();
              }}
            >
              <option>Temperature/Humidity Sensor</option>
              <option>IAQ Sensor</option>
              <option>Signal Repeater</option>
              <option>Employee</option>
            </select>
          </div>
          <div id="temp_form" className="fading" style={{ display: "block" }}>
            <div className="input-group">
              <span className="label">Floor Name : </span>
              <select name="type" id="fname"
                onChange={() => showMessage(this,false, false, false, "")}></select>
            </div>
            <div className="input-group">
              <span className="label">X Co-ordinate : </span>
              <input type="number" id="x" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Y Co-ordinate : </span>
              <input type="number" id="y" required="required" />
            </div>
            <div className="input-group">
              <span className="label">X1 Co-ordinate : </span>
              <input type="number" id="x1" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Y1 Co-ordinate : </span>
              <input type="number" id="y1" required="required" />
            </div>
          </div>
          <div id="iaq_form" className="fading" style={{ display: "none" }}>
            <div className="input-group">
              <span className="label">Floor Name : </span>
              <select name="type" id="fname1"></select>
            </div>
            <div className="input-group">
              <span className="label">X Co-ordinate : </span>
              <input type="number" id="xval" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Y Co-ordinate : </span>
              <input type="number" id="yval" required="required" />
            </div>
          </div>

          <div id="emp_form" className="fading" style={{ display: "none" }}>
            <div className="input-group">
              <span className="label">Name : </span>
              <input type="text" id="emp_name" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Role : </span>
              <input type="text" id="emp_role" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Employee ID : </span>
              <input type="text" id="emp_id" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Email : </span>
              <input type="text" id="emp_email" required="required" />
            </div>
            <div className="input-group">
              <span className="label">Phone.No : </span>
              <input type="text" id="emp_phoneNo" required="required" />
            </div>
          </div>

          {/* Button for searching tag */}
          <div style={{ display: "flex", margin: "15px", marginLeft: "153px" }}>
            <input
              style={{ marginLeft: "40px", background: '#eb6565' }}
              type="button"
              onClick={() => {
                this.show();
                this.hide();
              }}
              value="Remove Tag"
              className="btn success-btn"
            />
            <input style={{ marginLeft: "40px" }}
              type="submit"
              onClick={this.register}
              value="Register Tag"
              className="btn success-btn"
            />

            <input
              id="bulk_reg"
              style={{ marginLeft: "20px", display: "none" }}
              type="button"
              onClick={() => {
                $("#delete-form").css("display", "none");
                $("#bulk_form").css(
                  "display",
                  $("#bulk_form").css("display") === "block" ? "none" : "block"
                );
                window.scrollTo(0, document.body.scrollHeight);
              }}
              value="Bulk Register"
              className="btn success-btn"
            />
          </div>
        </form>

        <form id="bulk_form" className="fading" style={{ display: "none" }}>
          <div className="input-group">
            <span className="label">Employee Bulk Upload :</span>
            <input
              type="file"
              accept=".csv,.xlsx,.xls"
              required="required"
              onChange={this.loadFileXLSX.bind(this)}
              name="bulk_file"
              id="bulk_file"
            />
          </div>
          <div style={{ display: "flex", margin: "15px", marginLeft: "193px" }}>
            <div className="input-group">
              <input
                type="submit"
                value="Bulk Update"
                onClick={this.bulkUpdate}
                className="btn update-btn"
              />
              <input
                style={{ marginLeft: "20px" }}
                type="submit"
                value="Bulk Register"
                onClick={this.bulkRegister}
                className="btn success-btn"
              />
            </div>
          </div>
        </form>

        <form id="delete-form" className="fading"
          style={{ display: "none" }}>
          <div className="input-group">
            <span className="label">Tag Type :</span>
            <select
              id="tagtype"
              onChange={() => {
                this.displayTrackingForm();
                this.hide();
              }}
            >
              <option>Temperature/Humidity Sensor</option>
              <option>IAQ Sensor</option>
              <option>Signal Repeater</option>
              <option>Employee</option>
            </select>
          </div>

          {/* Input Field for Tag MAC ID */}
          <div className="input-group">
            <span className="label">Tag MAC ID :</span>
            <input
              type="text"
              name="macid"
              id="macid"
              required="required"
              onClick={this.hide}
              placeholder="5a-c2-15-00-00-00"
            />
          </div>

          <div className="input-group" style={{ margin: "15px", marginLeft: "260px" }}>
            <input
              type="submit"
              value="Remove Tag"
              onClick={this.unregister}
              className="btn warning-btn"
            />
          </div>
        </form>

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

export default AssetReg;
