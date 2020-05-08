import React, { Component } from "react"
import "./Mobile.css"
// import GetDiv from "./GetDiv"
const IP_ADDRESS_PG = "ws://192.168.0.120:"
const PORT = 7681
const URL = IP_ADDRESS_PG + PORT
var qaLogsButton = 1
var getExperimentsButton = 0
class Mobile extends Component {
  constructor(props) {
    super(props)
    this.state = {
      ws: null,
      flag: true,
      logs: ""
    }
  }

  componentDidMount() {
    this.connect()
  }
  timeout = 250

  connect = () => {
    var ws = new WebSocket(URL)
    let that = this // cache the this
    var connectInterval
    ws.onopen = () => {
      console.log("connected websocket main component")

      this.setState({ ws: ws })
      this.setState({ flag: true })

      ws.send('{"command":"qaLogs"}')
      that.timeout = 250 // reset timer to 250 on open of websocket connection
      clearTimeout(connectInterval) // clear Interval on on open of websocket connection
    }

    ws.onclose = (e) => {
      console.log(
        `Socket is closed. Reconnect will be attempted in ${Math.min(
          10000 / 1000,
          (that.timeout + that.timeout) / 1000
        )} second.`,
        e.reason
      )

      that.timeout = that.timeout + that.timeout //increment retry interval
      connectInterval = setTimeout(this.check, Math.min(10000, that.timeout)) //call check function after timeout
    }

    ws.onerror = (err) => {
      console.error("Socket encountered error: ", err.message, "Closing socket")

      ws.close()
    }

    ws.onmessage = (evt) => {
      console.log("on message")
      if (qaLogsButton !== 0) {
        var log = JSON.parse(evt.data)
        var name_list = ""
        var elementType = []
        // var zindexChoice = document.getElementById("zindex").checked
        var zindexChoice = 0
        var filterZIndex = this.getFullScreenElementZIndex(log)
        var FTUE_Z_ORDER = 75
        var output = document.getElementById("output")

        for (var i = 0; i < log.length; i++) {
          if (log[i]["zindex"] < FTUE_Z_ORDER && zindexChoice) {
            continue
          }
          if (log[i]["zindex"] >= FTUE_Z_ORDER && !zindexChoice) {
            continue
          }

          if (log[i]["elementType"] !== "ScrollView") {
            output.innerHTML +=
              '<div id="element" onclick="this.clicked" class="elements" onmouseover="this.showcontent" onmouseout="this.hidecontent" value="' +
              JSON.stringify(log[i]).replace(/\"/g, "'") +
              '" data_type="' +
              log[i]["elementType"] +
              '" name="' +
              log[i]["name"] +
              '" style="z-index:0;position: absolute;border:solid grey 1px;width:' +
              log[i]["boundbox"]["width"] +
              "px; height:" +
              log[i]["boundbox"]["height"] +
              "px;left:" +
              log[i]["boundbox"]["x"] +
              "px;top:" +
              log[i]["boundbox"]["y"] +
              'px;"></div>'
          }
          if (!elementType.includes(log[i]["elementType"])) {
            elementType.push(log[i]["elementType"])
          }
        }
        var elementTypeButtons = ""
        for (var k = 0; k < elementType.length; k++) {
          elementTypeButtons +=
            "<input type='checkbox' onclick='elementTypeFilter(this);'name='elementTypeButtons' value='" +
            elementType[k] +
            "'checked>" +
            elementType[k] +
            "<br>"
        }
        elementTypeButtons = "<div>" + elementTypeButtons + "</div>"
        output.innerHTML =
          "<div id='screen' style='float:left;margin-left:auto;zoom:0.3;position:relative;width:720px;height:1364px;background:black;opacity:0.7'>" +
          output.innerHTML +
          "</div>" +
          "<div id='idname' style='height:150px;width:600px;float:left'></div>" +
          elementTypeButtons
        //addMessage( evt.data );
        qaLogsButton = 0
      } else if (getExperimentsButton !== 0) {
        var exp = JSON.parse(evt.data)["arr"]
        var exp_ui = ""
        for (var i = 0; i < exp.length; i++) {
          exp_ui +=
            "<select onchange='updateExperiment(this)' id='" +
            exp[i]["expName"] +
            "'>"
          var exp_var_ui = ""
          for (k = 0; k < exp[i]["variant"].length; k++) {
            var exp_name = exp[i]["variant"][k]["name"]
            if (exp[i]["chosenVariant"] === exp_name) {
              exp_var_ui +=
                "<option value='" +
                exp[i]["variant"][k]["name"] +
                "'selected>" +
                exp[i]["expName"] +
                "-" +
                exp[i]["variant"][k]["name"] +
                "</option>"
            } else {
              exp_var_ui +=
                "<option value='" +
                exp[i]["variant"][k]["name"] +
                "'>" +
                exp[i]["expName"] +
                "-" +
                exp[i]["variant"][k]["name"] +
                "</option>"
            }
          }
          exp_ui += exp_var_ui
          exp_ui += "</select></div>"
        }
        document.getElementById("exp").innerHTML = exp_ui
        getExperimentsButton = 0
      } else {
        this.addMessage(evt.data)
      }
      console.log("*&*&*&*&*&*&*&")
      console.log(evt.data)
    }
  }

  addMessage = (msg) => {
    var output = document.getElementById("output")
    console.log(msg)
    output.innerHTML += msg + "<br/>"
  }

  getFullScreenElementZIndex = (log) => {
    console.log("get Full screen ElementZindex is called")
    for (var i = 0; i < log.length; i++) {
      if (log[i]["boundbox"]["height"] >= 1920) {
        return log[i]["zindex"]
      }
    }
  }

  showcontent = () => {
    console.log("showContent is called")
    // console.log(c)
    // console.log(c)
    // c.style.background = "lightgrey"
    // c.style.border = "dotted 1px Blue"
    // //c.style.zIndex = -2;
    // var contentpretty = this.syntaxHighlight(
    //   c.getAttribute("value").replace("/'/g", '"')
    // )
    // document.getElementById("idname").innerHTML = contentpretty
    // console.log(contentpretty)
  }

  hidecontent = (c) => {
    console.log("hidecontent is called")
    console.log(c)
    // c.style.background = null
    // c.style.border = "solid 1px grey"
    // //c.style.zIndex = -1;
    // document.getElementById("idname").innerHTML = ""
  }

  syntaxHighlight = (json) => {
    console.log("syntaxHighlight is called")
    json = json
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
    return json.replace(
      /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g,
      function (match) {
        var cls = "number"
        if (/^"/.test(match)) {
          if (/:$/.test(match)) {
            cls = "key"
          } else {
            cls = "string"
          }
        } else if (/true|false/.test(match)) {
          cls = "boolean"
        } else if (/null/.test(match)) {
          cls = "null"
        }
        return '<span class="' + cls + '">' + match + "</span>"
      }
    )
  }

  check = () => {
    const { ws } = this.state.ws
    if (!ws || ws.readyState === WebSocket.CLOSED) this.connect() //check if websocket instance is closed, if so call `connect` function.
  }

  getFullScreenElementZIndex = (log) => {
    for (var i = 0; i < log.length; i++) {
      if (log[i]["boundbox"]["height"] >= 1920) {
        return log[i]["zindex"]
      }
    }
  }

  qaLogs = (event) => {
    console.log("Yrs")
    console.log(this.state.flag)
    if (this.state.flag) {
      this.ws.send('{"command":"qaLogs"}')
      console.log("&&&&&&")
    }
    event.preventDefault()
  }

  click = (ele) => {
    console.log(ele.getAttribute("name"))
  }

  clicked = (ele) => {
    console.log("clicked")
    // TODO add the path to tap sprite
  }

  get_magic_logs() {
    // TODO add the path to call the magic logs
    console.log("magic Logs")
  }

  elementTypeFilter = (et) => {
    console.log(et.checked)
    var value = et.getAttribute("value")
    var alldiv = document.getElementsByClassName("elements")

    for (var a = 0; a < alldiv.length; a++) {
      if (et.checked) {
        if (alldiv[a].getAttribute("data_type") === value) {
          alldiv[a].style.display = "block"
        }
      } else {
        if (alldiv[a].getAttribute("data_type") === value) {
          alldiv[a].style.display = "none"
        }
      }
    }
  }

  render() {
    // const {data} = this.state.log
    // const nameList = data.map(item=>{
    //   return(
    //     <div id = "element" onClick={this.clicked} className="elemnts" onMouseOver={this.showcontent}
    //     onMouseOut = {this.hidecontent} value

    //     >

    //     </div>
    //   )
    // })

    return (
      <div>
        {/* <form onSubmit={this.qaLogs}>
          <button type="submit" onSubmit={this.qaLogs}>
            click
          </button>
        </form> */}

        <div id="output" style={{ marginTop: "15%", float: "left" }}></div>
      </div>
    )
  }
}

export default Mobile
